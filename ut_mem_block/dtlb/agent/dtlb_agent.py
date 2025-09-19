from toffee.agent import Agent, driver_method, monitor_method
from toffee import Value
from ..bundle.dtlb_bundle import DTLBBundle, RequestorBundle, CSRBundle, PTWBundle, PMPBundle

def _canon_sv39_vaddr(va: int) -> int:
    """把 64 位 VA 规范化为 Sv39 canonical 形式（按 bit[38] 符号扩展）"""
    va = int(va) & ((1 << 64) - 1)
    low39 = va & ((1 << 39) - 1)
    sign  = (low39 >> 38) & 1
    upper = ((-sign) & ((1 << (64 - 39)) - 1)) << 39
    return (upper | low39) & ((1 << 64) - 1)

class DTLBAgent(Agent):
    def __init__(self, dtlb_bundle):
        super().__init__(dtlb_bundle)   
        self.bundle = dtlb_bundle
        self.requestor = dtlb_bundle.requestor
        self.ptw_resp = dtlb_bundle.ptw.resp

    @driver_method()
    async def drive_request(
        self,
        port: int,
        vaddr: int,
        cmd: int,
        *,
        hyperinst: bool = False,
        pmp_addr: int | None = None,
        hlvx: bool = False,
        kill: bool = False,
        is_prefetch: bool = False,
        no_translate: bool = False,
        check_fullva: bool = False,
        debug_robIdx_flag: int = 0,
        debug_robIdx_value: int = 0,
        debug_isFirstIssue: int = 0,
        return_on_miss: bool = False,
    ):
        """
        命中且无异常 => 返回 paddr_0 (int)
        miss / 异常 => 返回 None
        return_on_miss=True: 一旦看到 miss 就立即返回 None（便于“下一拍注入”）
        """
        if not 0 <= port < 4:
            raise ValueError("Port must be 0..N-1")

        fullva = int(vaddr) & ((1 << 64) - 1)       # 完整 64 位
        canon  = _canon_sv39_vaddr(fullva)          # Sv39 规范化（再按端口位宽截取）
        pmp    = fullva if pmp_addr is None else int(pmp_addr)


        # === 驱动 req ===
        req = self.requestor[port].req
        
        req.valid.value = 0
        req.bits_vaddr.value = canon & ((1 << 39) - 1)   # 你的接口是 50 位，这里保守取低 50 位
        req.bits_fullva.value = fullva                   # 完整 64 位
        req.bits_checkfullva.value = 1 if check_fullva else 0

        req.bits_cmd.value = int(cmd)
        req.bits_hyperinst.value = 1 if hyperinst else 0
        req.bits_hlvx.value = 1 if hlvx else 0
        req.bits_kill.value = 1 if kill else 0
        req.bits_isPrefetch.value = 1 if is_prefetch else 0
        req.bits_no_translate.value = 1 if no_translate else 0

        req.bits_pmp_addr.value = pmp & ((1 << 48) - 1)

        req.bits_debug_robIdx_flag.value = 1 if debug_robIdx_flag else 0
        req.bits_debug_robIdx_value.value = int(debug_robIdx_value) & 0xFF
        req.bits_debug_isFirstIssue.value = 1 if debug_isFirstIssue else 0
        
        while (self.requestor[port].resp.valid.value == 1):
            await self.bundle.step()
        
        req.valid.value = 1
        # print("resp_miss before request : ",self.requestor[port].resp.bits_miss.value, flush=True)
        await Value(self.requestor[port].resp.valid, 1)  # 发起
        req.valid.value = 0 
        # print("resp_miss after request  : ",self.requestor[port].resp.bits_miss.value, flush=True)
        
        
        resp = self.requestor[port].resp
        
        miss = int(resp.bits_miss.value)
        if miss == 1:
            return None

        # 汇总异常位（ld/st 都看一遍更稳）
        # print("resp_excp_0_pf_ld : ",resp.bits_excp_0_pf_ld.value, flush=True)
        # print("resp_excp_0_pf_st : ",resp.bits_excp_0_pf_st.value, flush=True)
        # print("resp_excp_0_af_ld : ",resp.bits_excp_0_af_ld.value, flush=True)
        # print("resp_excp_0_af_st : ",resp.bits_excp_0_af_st.value, flush=True)
        # print("resp_excp_0_gpf_ld: ",resp.bits_excp_0_gpf_ld.value, flush=True)
        # print("resp_excp_0_gpf_st: ",resp.bits_excp_0_gpf_st.value, flush=True)
        
        gpf = resp.bits_excp_0_gpf_ld.value == 1 or resp.bits_excp_0_gpf_st.value == 1
        pf  = resp.bits_excp_0_pf_ld.value == 1 or resp.bits_excp_0_pf_st.value == 1
        af  = resp.bits_excp_0_af_ld.value == 1 or resp.bits_excp_0_af_st.value == 1
        if gpf or pf or af:
            return -1  # 有异常
        
        return int(resp.bits_paddr_0.value)


    @driver_method()
    async def set_ptw_resp(self, vaddr, paddr, level, *,
                        # S1/S2 选择
                        valid: bool = True,
                        s2xlate: int = 0,
                        getGpa: bool = False,
                        # ---------- S1 entry ----------
                        s1_asid: int = 0,
                        s1_vmid: int = 0,
                        s1_n: bool = False,
                        s1_pbmt: int = 0,
                        # 权限位
                        s1_perm_d: bool = False, s1_perm_a: bool = True, s1_perm_g: bool = False,
                        s1_perm_u: bool = True, s1_perm_x: bool = False, s1_perm_w: bool = False, s1_perm_r: bool = True,
                        s1_v: bool = True,              # 表项有效位
                        s1_ppn_low: list[int] | None = None, # 直接给 ppn_low[8] 列表
                        s1_valididx: list[int] | None = None, # 直接给 valididx[8] 列表
                        s1_pteidx: list[int] | None = None,   # 直接给 pteidx[8] 列表
                        s1_pf: bool = False, s1_af: bool = False,
                        # ---------- S2 entry ----------
                        s2_tag: int = 0,
                        s2_vmid: int = 0,
                        s2_n: bool = False,
                        s2_pbmt: int = 0,
                        s2_ppn: int = 0,
                        s2_perm_d: bool = False, s2_perm_a: bool = True, s2_perm_g: bool = False,
                        s2_perm_u: bool = False, s2_perm_x: bool = False, s2_perm_w: bool = False, s2_perm_r: bool = True,
                        s2_level: int = 0,
                        s2_gpf: bool = False, s2_gaf: bool = False,
                    ):
        """
        依据 vaddr/paddr 自动拼好 PTWResp：addr_low/entry_tag/entry_ppn/ppn_low/valididx/pteidx 等，
        并在观测到 ptw.req[i] 匹配的当下打一拍 resp.valid。
        约定（Sv39）：
        - vpn = va>>12（27 位），addr_low = vpn[2:0]，entry_tag = vpn>>3
        - ppn = pa>>12，entry_ppn = ppn>>3，ppn_low[addr_low] = ppn[2:0]
        - 4KB 页 level=2（2MB=1，1GB=0）
        """
        # -------- 计算索引/字段 --------
        vaddr = int(vaddr) & ((1 << 64) - 1)
        paddr = int(paddr) & ((1 << 56) - 1)   # 物理位宽保守截断
        vpn = (vaddr >> 12) & ((1 << 27) - 1)  # Sv39 VPN
        ppn = (paddr >> 12)
        addr_low = vpn & 0b111                 # vpn[2:0]
        entry_tag = vpn >> 3                   # 与硬件压缩槽对齐
        if s2xlate == 0:
            entry_ppn = (ppn >> 3) & ((1 << 21) - 1)   # 高 21 位（低 3 位走 ppn_low[]）
        else:
            entry_ppn = (ppn >> 3) & ((1 << 26) - 1)
        ppn_low_val = ppn & 0b111

        # -------- （valid 暂时保持 0）--------
        self.ptw_resp.valid.value = 0
        self.ptw_resp.bits_s2xlate.value = s2xlate
        self.ptw_resp.bits_getGpa.value  = 1 if getGpa else 0

        # S1 基本字段
        self.ptw_resp.bits_s1_entry_tag.value   = entry_tag
        self.ptw_resp.bits_s1_entry_asid.value  = s1_asid
        self.ptw_resp.bits_s1_entry_vmid.value  = s1_vmid
        self.ptw_resp.bits_s1_entry_n.value     = 1 if s1_n else 0
        self.ptw_resp.bits_s1_entry_pbmt.value  = s1_pbmt

        self.ptw_resp.bits_s1_entry_perm_d.value = 1 if s1_perm_d else 0
        self.ptw_resp.bits_s1_entry_perm_a.value = 1 if s1_perm_a else 0
        self.ptw_resp.bits_s1_entry_perm_g.value = 1 if s1_perm_g else 0
        self.ptw_resp.bits_s1_entry_perm_u.value = 1 if s1_perm_u else 0
        self.ptw_resp.bits_s1_entry_perm_x.value = 1 if s1_perm_x else 0
        self.ptw_resp.bits_s1_entry_perm_w.value = 1 if s1_perm_w else 0
        self.ptw_resp.bits_s1_entry_perm_r.value = 1 if s1_perm_r else 0

        self.ptw_resp.bits_s1_entry_level.value = int(level)
        self.ptw_resp.bits_s1_entry_v.value     = 1 if s1_v else 0
        self.ptw_resp.bits_s1_entry_ppn.value   = entry_ppn
        self.ptw_resp.bits_s1_addr_low.value    = addr_low

        # 8 路列表：清零后只在 addr_low 位置写有效/索引/ppn_low
        if s1_ppn_low is None and s1_valididx is None and s1_pteidx is None:
            for i in range(8):
                self.ptw_resp.bits_s1_ppn_low[i].value  = 0
                self.ptw_resp.bits_s1_valididx[i].value = 0
                self.ptw_resp.bits_s1_pteidx[i].value   = 0
            self.ptw_resp.bits_s1_ppn_low[addr_low].value  = ppn_low_val
            self.ptw_resp.bits_s1_valididx[addr_low].value = 1
            self.ptw_resp.bits_s1_pteidx[addr_low].value   = 1
        else:
            for i in range(8):
                self.ptw_resp.bits_s1_ppn_low[i].value  = s1_ppn_low[i] & 0b111
                self.ptw_resp.bits_s1_valididx[i].value = 1 if s1_valididx[i] else 0
                self.ptw_resp.bits_s1_pteidx[i].value   = 1 if s1_pteidx[i] else 0

        self.ptw_resp.bits_s1_pf.value = 1 if s1_pf else 0
        self.ptw_resp.bits_s1_af.value = 1 if s1_af else 0

        # S2
        self.ptw_resp.bits_s2_entry_tag.value  = s2_tag
        self.ptw_resp.bits_s2_entry_vmid.value = s2_vmid
        self.ptw_resp.bits_s2_entry_n.value    = 1 if s2_n else 0
        self.ptw_resp.bits_s2_entry_pbmt.value = s2_pbmt
        self.ptw_resp.bits_s2_entry_ppn.value  = s2_ppn

        self.ptw_resp.bits_s2_entry_perm_d.value = 1 if s2_perm_d else 0
        self.ptw_resp.bits_s2_entry_perm_a.value = 1 if s2_perm_a else 0
        self.ptw_resp.bits_s2_entry_perm_g.value = 1 if s2_perm_g else 0
        self.ptw_resp.bits_s2_entry_perm_u.value = 1 if s2_perm_u else 0
        self.ptw_resp.bits_s2_entry_perm_x.value = 1 if s2_perm_x else 0
        self.ptw_resp.bits_s2_entry_perm_w.value = 1 if s2_perm_w else 0
        self.ptw_resp.bits_s2_entry_perm_r.value = 1 if s2_perm_r else 0

        self.ptw_resp.bits_s2_entry_level.value = s2_level
        self.ptw_resp.bits_s2_gpf.value         = 1 if s2_gpf else 0
        self.ptw_resp.bits_s2_gaf.value         = 1 if s2_gaf else 0

        # -------- 对拍：见到某一路 ptw.req 匹配就打一拍 resp --------
        self.ptw_resp.valid.value = 1
        await self.bundle.step()
        self.bundle.ptw.resp.valid.value = 0
    
    # @driver_method()
    # async def set_csr(self,*,
    #                 priv_mxr  = 0, priv_sum  = 0,
    #                 priv_vmxr = 0, priv_vsum = 0,
    #                 priv_virt = 0, priv_spvp = 0,
    #                 priv_imode = 0, priv_dmode = 0,

    #                 Satp_mode    = 8,  # Sv39 常见编码
    #                 Satp_asid    = 0,
    #                 Satp_ppn     = 0,
    #                 Satp_changed = 0,

    #                 Vsatp_mode    = 0,
    #                 Vsatp_asid    = 0,
    #                 Vsatp_ppn     = 0,
    #                 Vsatp_changed = 0,

    #                 HGatp_mode    = 0,
    #                 HGatp_vmid    = 0,
    #                 HGatp_ppn     = 0,
    #                 HGatp_changed = 0,):
    #     csr = self.bundle.csr
    #     csr.bits_priv_mxr.value   = priv_mxr
    #     csr.bits_priv_sum.value   = priv_sum
    #     csr.bits_priv_vmxr.value  = priv_vmxr
    #     csr.bits_priv_vsum.value  = priv_vsum
    #     csr.bits_priv_virt.value  = priv_virt
    #     csr.bits_priv_spvp.value  = priv_spvp
    #     csr.bits_priv_imode.value = priv_imode
    #     csr.bits_priv_dmode.value = priv_dmode
    #     csr.bits_Satp_mode.value    = Satp_mode
    #     csr.bits_Satp_asid.value    = Satp_asid
    #     csr.bits_Satp_ppn.value     = Satp_ppn
    #     csr.bits_Satp_changed.value = Satp_changed
    #     csr.bits_Vsatp_mode.value    = Vsatp_mode
    #     csr.bits_Vsatp_asid.value    = Vsatp_asid
    #     csr.bits_Vsatp_ppn.value     = Vsatp_ppn
    #     csr.bits_Vsatp_changed.value = Vsatp_changed
    #     csr.bits_HGatp_mode.value    = HGatp_mode
    #     csr.bits_HGatp_vmid.value    = HGatp_vmid
    #     csr.bits_HGatp_ppn.value     = HGatp_ppn
    #     csr.bits_HGatp_changed.value = HGatp_changed
    #     await self.bundle.step()
    
    @monitor_method()
    async def monitor_ptw_req(self):
        """
        监测 PTW 请求。
        """
        for port in range(4):
            req = self.bundle.ptw.req[port]
            if req.valid.value == 1:
                return {
                    "port": port,
                    "vpn": req.bits_vpn.value,
                    "tag": req.bits_vpn.value >> 3,
                    "s2xlate": req.bits_s2xlate.value,
                    "getGpa": req.bits_getGpa.value
                }
        return None
    
    @monitor_method()
    async def monitor_ptw_resp(self):
        ptw_resp = self.ptw_resp
        if ptw_resp.valid.value == 1:
            return {
                "s2xlate": ptw_resp.bits_s2xlate.value,
                "s1_asid": ptw_resp.bits_s1_entry_asid.value,
                "s1_entry_tag": ptw_resp.bits_s1_entry_tag.value,
                "s1_level": ptw_resp.bits_s1_entry_level.value,
                "s1_ppn_low[0]": ptw_resp.bits_s1_ppn_low[0].value,
                "s1_ppn_low[1]": ptw_resp.bits_s1_ppn_low[1].value,
                "s1_ppn_low[2]": ptw_resp.bits_s1_ppn_low[2].value,
                "s1_ppn_low[3]": ptw_resp.bits_s1_ppn_low[3].value,
                "s1_ppn_low[4]": ptw_resp.bits_s1_ppn_low[4].value,
                "s1_ppn_low[5]": ptw_resp.bits_s1_ppn_low[5].value,
                "s1_ppn_low[6]": ptw_resp.bits_s1_ppn_low[6].value,
                "s1_ppn_low[7]": ptw_resp.bits_s1_ppn_low[7].value,
                "s1_valididx[0]": ptw_resp.bits_s1_valididx[0].value,
                "s1_valididx[1]": ptw_resp.bits_s1_valididx[1].value,
                "s1_valididx[2]": ptw_resp.bits_s1_valididx[2].value,
                "s1_valididx[3]": ptw_resp.bits_s1_valididx[3].value,
                "s1_valididx[4]": ptw_resp.bits_s1_valididx[4].value,
                "s1_valididx[5]": ptw_resp.bits_s1_valididx[5].value,
                "s1_valididx[6]": ptw_resp.bits_s1_valididx[6].value,
                "s1_valididx[7]": ptw_resp.bits_s1_valididx[7].value,
                "s1_pteidx[0]": ptw_resp.bits_s1_pteidx[0].value,
                "s1_pteidx[1]": ptw_resp.bits_s1_pteidx[1].value,
                "s1_pteidx[2]": ptw_resp.bits_s1_pteidx[2].value,
                "s1_pteidx[3]": ptw_resp.bits_s1_pteidx[3].value,
                "s1_pteidx[4]": ptw_resp.bits_s1_pteidx[4].value,
                "s1_pteidx[5]": ptw_resp.bits_s1_pteidx[5].value,
                "s1_pteidx[6]": ptw_resp.bits_s1_pteidx[6].value,
                "s1_pteidx[7]": ptw_resp.bits_s1_pteidx[7].value
            }
        return None
    
    @monitor_method()
    async def monitor_req(self):
        """
        监测请求。
        """
        for port in range(4):
            req = self.requestor[port].req
            if req.valid.value == 1:
                return {
                    "port": port,
                    "vaddr": req.bits_vaddr.value,
                    "fullva": req.bits_fullva.value,
                    "cmd": req.bits_cmd.value,
                    "hyperinst": req.bits_hyperinst.value,
                    "hlvx": req.bits_hlvx.value,
                    "kill": req.bits_kill.value,
                    "isPrefetch": req.bits_isPrefetch.value,
                    "no_translate": req.bits_no_translate.value,
                    "pmp_addr": req.bits_pmp_addr.value
                }
        return None
    
    @monitor_method()
    async def monitor_resp(self):
        """
        监测响应。
        """
        for port in range(4):
            resp = self.requestor[port].resp
            if resp.valid.value == 1:
                return {
                    "port": port,
                    "miss": resp.bits_miss.value,
                    "paddr": resp.bits_paddr_0.value,
                    "fullva": resp.bits_fullva.value
                }
        return None
    
    
