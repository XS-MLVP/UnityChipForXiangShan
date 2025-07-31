from toffee import Agent
from ..bundle import ICacheMainPipeBundle


class ICacheMainPipeAgent(Agent):
    def __init__(self, bundle: ICacheMainPipeBundle, dut: None):
        super().__init__(bundle)
        self.bundle = bundle
        self.dut = dut
        bundle.set_all(0)

    # ==================== 基础控制API ====================
    async def flush_s0_fire(self):

        # set s0_fire
        self.bundle.io._dataArray._toIData._3._ready.value = 1
        self.bundle.io._wayLookupRead._valid.value = 1
        self.bundle.io._fetch._req._valid.value = 1
        await self.bundle.step()
        
        print( f"\nBefore setting: s0_fire is: ",self.bundle.ICacheMainPipe._s0_fire.value)

        self.bundle.io._flush.value = 1
        await self.bundle.step()

        print( f"After setting: s0_fire is: ",self.bundle.ICacheMainPipe._s0_fire.value)
    
    async def reset(self):
        """Reset state"""
        self.bundle.reset.value = 1
        await self.bundle.step(5)
        self.bundle.reset.value = 0
        await self.bundle.step(5)

    async def drive_set_flush(self, value: bool):
        """设置全局冲刷信号"""
        self.bundle.io._flush.value = int(value)
        await self.bundle.step()
        print(f"Flush signal set to {value}")

    async def drive_set_ecc_enable(self, value: bool):
        """设置ECC使能信号"""
        self.bundle.io._ecc_enable.value = int(value)
        await self.bundle.step()
        print(f"ECC enable set to {value}")

    async def drive_resp_stall(self, stall: bool = False):
        """驱动IFU响应暂停信号，用于测试反压。"""
        self.bundle.io._respStall.value = int(stall)
        await self.bundle.step()
        print(f"Response stall set to {stall}")
    # ==================== 驱动API ====================
    async def drive_data_array_ready(self, ready: bool):
        """
        驱动DataArray的ready信号，用于模拟反压。
        
        RTL逻辑：s0_can_go = io_dataArray_toIData_3_ready & io_wayLookupRead_valid & s1_ready
        当ready=False时，s0_can_go=0，阻止s0_fire，实现反压控制。
        """
        # DataArray有4个toIData接口(0-3)，只有toIData_3有ready输入信号作为反压控制点
        self.bundle.io._dataArray._toIData._3._ready.value = int(ready)
        await self.bundle.step()
        print(f"DataArray ready signal set to {ready}")
    
    async def drive_waylookup_read(self,
                                 vSetIdx_0: int = 0,
                                 vSetIdx_1: int = 0,
                                 waymask_0: int = 0,
                                 waymask_1: int = 0,
                                 ptag_0: int = 0,
                                 ptag_1: int = 0,
                                 itlb_exception_0: int = 0,
                                 itlb_exception_1: int = 0,
                                 itlb_pbmt_0: int = 0,
                                 itlb_pbmt_1: int = 0,
                                 meta_codes_0: int = 0,
                                 meta_codes_1: int = 0,
                                 gpf_gpaddr: int = 0,
                                 gpf_isForVSnonLeafPTE: int = 0) -> dict:
        """
        驱动WayLookup读取请求到S0阶段
        """
        
        result = {"send_success": False}
        
        # 设置WayLookup读取数据（不需要等待ready，因为wayLookupRead_ready = s0_fire）
        self.bundle.io._wayLookupRead._valid.value = 1
        self.bundle.io._wayLookupRead._bits._entry._vSetIdx._0.value = vSetIdx_0
        self.bundle.io._wayLookupRead._bits._entry._vSetIdx._1.value = vSetIdx_1
        self.bundle.io._wayLookupRead._bits._entry._waymask._0.value = waymask_0
        self.bundle.io._wayLookupRead._bits._entry._waymask._1.value = waymask_1
        self.bundle.io._wayLookupRead._bits._entry._ptag._0.value = ptag_0
        self.bundle.io._wayLookupRead._bits._entry._ptag._1.value = ptag_1
        self.bundle.io._wayLookupRead._bits._entry._itlb._exception._0.value = itlb_exception_0
        self.bundle.io._wayLookupRead._bits._entry._itlb._exception._1.value = itlb_exception_1
        self.bundle.io._wayLookupRead._bits._entry._itlb._pbmt._0.value = itlb_pbmt_0
        self.bundle.io._wayLookupRead._bits._entry._itlb._pbmt._1.value = itlb_pbmt_1
        self.bundle.io._wayLookupRead._bits._entry._meta_codes._0.value = meta_codes_0
        self.bundle.io._wayLookupRead._bits._entry._meta_codes._1.value = meta_codes_1
        self.bundle.io._wayLookupRead._bits._gpf._gpaddr.value = gpf_gpaddr
        self.bundle.io._wayLookupRead._bits._gpf._isForVSnonLeafPTE.value = gpf_isForVSnonLeafPTE
        await self.bundle.step()
            
        result["send_success"] = True
        result.update({
                "vSetIdx_0": self.bundle.io._wayLookupRead._bits._entry._vSetIdx._0.value,
                "vSetIdx_1": self.bundle.io._wayLookupRead._bits._entry._vSetIdx._1.value,
                "waymask_0": self.bundle.io._wayLookupRead._bits._entry._waymask._0.value,
                "waymask_1": self.bundle.io._wayLookupRead._bits._entry._waymask._1.value,
                "ptag_0": self.bundle.io._wayLookupRead._bits._entry._ptag._0.value,
                "ptag_1": self.bundle.io._wayLookupRead._bits._entry._ptag._1.value,
                "itlb_exception_0": self.bundle.io._wayLookupRead._bits._entry._itlb._exception._0.value,
                "itlb_exception_1": self.bundle.io._wayLookupRead._bits._entry._itlb._exception._1.value,
                "meta_codes_0":self.bundle.io._wayLookupRead._bits._entry._meta_codes._0.value,
                "meta_codes_1":self.bundle.io._wayLookupRead._bits._entry._meta_codes._1.value
        })
        return result
    
    async def clear_waylookup_read(self):
        """
        清除WayLookup读取请求的valid信号
        
        RTL逻辑：当io_wayLookupRead_valid=0时，s0_fire=0，流水线停止推进
        """
        self.bundle.io._wayLookupRead._valid.value = 0
        await self.bundle.step()
        print("WayLookup read request cleared")
        
    async def drive_fetch_request(self,
                                pcMemRead_addrs: list = None,
                                readValid: list = None,
                                backendException: int = 0) -> bool:
        """
        驱动FTQ取指请求
        
        RTL逻辑：
        - s0_fire = io_fetch_req_valid & s0_can_go & ~io_flush
        - io_fetch_req_ready = s0_can_go  
        - io_dataArray_toIData_X_valid = io_fetch_req_bits_readValid_X
        - s1_doubleline <= readValid_4 & startAddr[5] (跨行取指条件)
        - 当startAddr[5]=1时跨行，nextlineStart=(startAddr & ~0x3F) + 64
        - 当startAddr[5]=0时不跨行，nextlineStart=startAddr
        """
        if pcMemRead_addrs is None:
            pcMemRead_addrs = [0] * 5
        if readValid is None:
            readValid = [0] * 5
        
        # 确保数组有5个元素，不足的补0
        while len(pcMemRead_addrs) < 5:
            pcMemRead_addrs.append(0)
        while len(readValid) < 5:
            readValid.append(0)
        
        # 根据RTL逻辑自动计算nextlineStart值
        pcMemRead_nextlineStarts = []
        for i in range(5):
            addr = pcMemRead_addrs[i]
            if (addr & 0x20) != 0:  # startAddr[5] == 1，跨越64字节边界
                nextline = (addr & ~0x3F) + 64  # 下一个64字节对齐地址
            else:  # startAddr[5] == 0，同一缓存行内
                nextline = addr  # nextlineStart = startAddr
            pcMemRead_nextlineStarts.append(nextline)
        
        # RTL断言约束检查：验证pcMemRead_4地址与wayLookup vSetIdx的一致性
        wayLookup_vSetIdx_0 = self.bundle.io._wayLookupRead._bits._entry._vSetIdx._0.value
        wayLookup_vSetIdx_1 = self.bundle.io._wayLookupRead._bits._entry._vSetIdx._1.value
        
        expected_vSetIdx_0 = (pcMemRead_addrs[4] >> 6) & 0xFF  # [13:6]
        expected_vSetIdx_1 = (pcMemRead_nextlineStarts[4] >> 6) & 0xFF  # [13:6]
        
        if wayLookup_vSetIdx_0 != expected_vSetIdx_0 or wayLookup_vSetIdx_1 != expected_vSetIdx_1:
            print(f"RTL约束违反: vSetIdx不匹配，无法发起fetch请求!")
            print(f"  pcMemRead_4_startAddr[13:6] = 0x{expected_vSetIdx_0:02x}, wayLookup_vSetIdx_0 = 0x{wayLookup_vSetIdx_0:02x}")
            print(f"  pcMemRead_4_nextlineStart[13:6] = 0x{expected_vSetIdx_1:02x}, wayLookup_vSetIdx_1 = 0x{wayLookup_vSetIdx_1:02x}")
            return False
        
        # 设置fetch请求信号（ready是输出信号，不需要等待）
        print("start driving fetch request")
        for j in range(5):
            startpre = getattr(self.bundle.io._fetch._req._bits._pcMemRead, f"_{j}")
            start = getattr(startpre, "_startAddr")
            start.value = pcMemRead_addrs[j]
            
            nextpre = getattr(self.bundle.io._fetch._req._bits._pcMemRead, f"_{j}")
            next = getattr(nextpre, "_nextlineStart")
            next.value = pcMemRead_nextlineStarts[j]
            
            readValid_signal = getattr(self.bundle.io._fetch._req._bits._readValid, f"_{j}")
            readValid_signal.value = readValid[j]
        
        self.bundle.io._fetch._req._bits._backendException.value = backendException
        self.bundle.io._fetch._req._valid.value = 1
        
        await self.bundle.step()
        return True

    async def clear_fetch_request(self):
        """
        清除fetch请求的valid信号
        
        RTL逻辑：当io_fetch_req_valid=0时，s0_fire=0，流水线停止推进
        """
        self.bundle.io._fetch._req._valid.value = 0
        await self.bundle.step()
        print("Fetch request cleared")

    async def drive_pmp_response(self,
                                 instr_0: int = 0,
                                 mmio_0: int = 0,
                                 instr_1: int = 0,
                                 mmio_1: int = 0):
        """驱动PMP响应信号"""
        self.bundle.io._pmp._0._resp._instr.value = instr_0
        self.bundle.io._pmp._0._resp._mmio.value = mmio_0
        self.bundle.io._pmp._1._resp._instr.value = instr_1
        self.bundle.io._pmp._1._resp._mmio.value = mmio_1
        await self.bundle.step()

    async def drive_data_array_response(self,
                                        datas: list = None,
                                        codes: list = None) -> bool:
        """
        驱动DataArray响应数据
        
        RTL逻辑：
        - 8个64位数据块 (datas_0 到 datas_7)
        - 8个ECC校验码 (codes_0 到 codes_7)
        - 与MSHR响应进行数据选择：s1_bankMSHRHit ? mshr_data : dataArray_data
        """
        if datas is None:
            datas = [0] * 8
        if codes is None:
            codes = [0] * 8
            
        if len(datas) == 8 and len(codes) == 8:
            print("start driving data array response")
            for i in range(8):
                getattr(self.bundle.io._dataArray._fromIData._datas, f"_{i}").value = datas[i]
                getattr(self.bundle.io._dataArray._fromIData._codes, f"_{i}").value = codes[i]
            await self.bundle.step()
            print(f"DataArray response set: datas[:2]={[hex(d) for d in datas[:2]]}, codes[:2]={codes[:2]}")
            return True
        else:
            print(f"参数错误: datas长度={len(datas)}, codes长度={len(codes)}, 都需要为8")
            return False

    async def drive_mshr_response(self, 
                                  blkPaddr:int = 0,
                                  vSetIdx: int = 0,
                                  data: int = 0,
                                  corrupt: int = 0) -> bool:
        """
        发送MSHR响应，不立即清除valid信号，让它在整个测试期间保持有效
        
        RTL逻辑：
        - io_mshr_resp_valid只被读取，从未被RTL自动清除
        - s1/s2_bankMSHRHit用于数据选择: mshr_hit ? mshr_data : dataArray_data
        - blkPaddr[41:6]用于ptag匹配，vSetIdx用于地址匹配
        """
        # 直接设置MSHR响应，让valid信号保持有效以便S1/S2阶段检测
        print("start driving MSHR response")
        self.bundle.io._mshr._resp._valid.value = 1
        self.bundle.io._mshr._resp._bits._blkPaddr.value = blkPaddr
        self.bundle.io._mshr._resp._bits._vSetIdx.value = vSetIdx
        self.bundle.io._mshr._resp._bits._data.value = data
        self.bundle.io._mshr._resp._bits._corrupt.value = corrupt
        await self.bundle.step()
        print(f"MSHR response set: blkPaddr=0x{blkPaddr:x}, vSetIdx=0x{vSetIdx:x}, corrupt={corrupt}")
        return True
    # ==================== 监控API ====================
    
    async def monitor_dataarray_toIData(self) -> dict:
        """
        监控S1阶段DataArray访问情况
        """
        return {
            "toIData_0_valid": self.bundle.io._dataArray._toIData._0._valid.value,
            "toIData_0_vSetIdx_0": self.bundle.io._dataArray._toIData._0._bits._vSetIdx._0.value,
            "toIData_0_vSetIdx_1": self.bundle.io._dataArray._toIData._0._bits._vSetIdx._1.value,
            "toIData_0_waymask_0_0": self.bundle.io._dataArray._toIData._0._bits._waymask._0._0.value,
            "toIData_0_waymask_0_1": self.bundle.io._dataArray._toIData._0._bits._waymask._0._1.value,
            "toIData_0_waymask_0_2": self.bundle.io._dataArray._toIData._0._bits._waymask._0._2.value,
            "toIData_0_waymask_0_3": self.bundle.io._dataArray._toIData._0._bits._waymask._0._3.value,
            "toIData_0_waymask_1_0": self.bundle.io._dataArray._toIData._0._bits._waymask._1._0.value,
            "toIData_0_waymask_1_1": self.bundle.io._dataArray._toIData._0._bits._waymask._1._1.value,
            "toIData_0_waymask_1_2": self.bundle.io._dataArray._toIData._0._bits._waymask._1._2.value,
            "toIData_0_waymask_1_3": self.bundle.io._dataArray._toIData._0._bits._waymask._1._3.value,
            "toIData_0_bits_blkOffset": self.bundle.io._dataArray._toIData._0._bits._blkOffset.value,
            "toIData_1_valid": self.bundle.io._dataArray._toIData._1._valid.value,
            "toIData_1_bits_vSetIdx_0": self.bundle.io._dataArray._toIData._1._bits_vSetIdx._0.value,
            "toIData_1_bits_vSetIdx_1": self.bundle.io._dataArray._toIData._1._bits_vSetIdx._1.value,
            "toIData_2_valid": self.bundle.io._dataArray._toIData._2._valid.value,
            "toIData_2_bits_vSetIdx_0": self.bundle.io._dataArray._toIData._2._bits_vSetIdx._0.value,
            "toIData_2_bits_vSetIdx_1": self.bundle.io._dataArray._toIData._2._bits_vSetIdx._1.value,
            "toIData_3_valid": self.bundle.io._dataArray._toIData._3._valid.value,
            "toIData_3_bits_vSetIdx_0": self.bundle.io._dataArray._toIData._3._bits_vSetIdx._0.value,
            "toIData_3_bits_vSetIdx_1": self.bundle.io._dataArray._toIData._3._bits_vSetIdx._1.value
        }

    async def monitor_check_meta_ecc_status(self) -> dict:
        """
        检查Meta ECC状态
        Todo: 查找内部信号具体表达式
        """
        # 需要通过内部信号获取
        s1_meta_corrupt_hit = self.dut.GetInternalSignal("ICacheMainPipe_top.ICacheMainPipe.s1_meta_corrupt_hit_num", use_vpi=False)
        
        return {
            "s1_meta_corrupt_hit": s1_meta_corrupt_hit.value if s1_meta_corrupt_hit else None,
            "ecc_enable": self.bundle.io._ecc_enable.value
        }

    async def monitor_pmp_status(self) -> dict:
        """
        监控PMP检查状态,s2阶段也使用本pmp检查
        """
        return {
            "pmp_0_req_addr": self.bundle.io._pmp._0._req_bits_addr.value,
            "pmp_1_req_addr": self.bundle.io._pmp._1._req_bits_addr.value,
            "pmp_0_resp_mmio": self.bundle.io._pmp._0._resp._mmio.value,
            "pmp_1_resp_mmio": self.bundle.io._pmp._1._resp._mmio.value,
        }
    
    async def monitor_mshr_status(self) -> dict:
        """
        监控MSHR操作状态
        """
        return {
            "req_valid": self.bundle.io._mshr._req._valid.value,
            "req_blkPaddr": self.bundle.io._mshr._req._bits._blkPaddr.value,
            "req_vSetIdx": self.bundle.io._mshr._req._bits._vSetIdx.value,
        }

    async def monitor_check_data_ecc_status(self) -> dict:
        """
        检查Data ECC状态
        用于测试CP16: Data ECC校验
        """
        # 需要通过内部信号获取
        s2_data_corrupt_0 = self.dut.GetInternalSignal("ICacheMainPipe_top.ICacheMainPipe.s2_data_corrupt_0", use_vpi=False)
        s2_data_corrupt_1 = self.dut.GetInternalSignal("ICacheMainPipe_top.ICacheMainPipe.s2_data_corrupt_1", use_vpi=False)
        
        return {
            "ecc_enable": self.bundle.io._ecc_enable.value,
            "s2_data_corrupt_0": s2_data_corrupt_0.value if s2_data_corrupt_0 else None,
            "s2_data_corrupt_1": s2_data_corrupt_1.value if s2_data_corrupt_1 else None
        }

    async def monitor_fetch_response(self) -> dict:
        """
        监控IFU响应
        用于测试CP20: 响应IFU
        """
        return {
            "valid": self.bundle.io._fetch._resp._valid.value,
            "doubleline": self.bundle.io._fetch._resp._bits._doubleline.value,
            "vaddr_0": self.bundle.io._fetch._resp._bits._vaddr._0.value,
            "vaddr_1": self.bundle.io._fetch._resp._bits._vaddr._1.value,
            "data": self.bundle.io._fetch._resp._bits._data.value,
            "paddr_0": self.bundle.io._fetch._resp._bits._paddr._0.value,
            "exception_0": self.bundle.io._fetch._resp._bits._exception._0.value,
            "exception_1": self.bundle.io._fetch._resp._bits._exception._1.value,
            "pmp_mmio_0": self.bundle.io._fetch._resp._bits._pmp_mmio._0.value,
            "pmp_mmio_1": self.bundle.io._fetch._resp._bits._pmp_mmio._1.value,
            "itlb_pbmt_0": self.bundle.io._fetch._resp._bits._itlb_pbmt._0.value,
            "itlb_pbmt_1": self.bundle.io._fetch._resp._bits._itlb_pbmt._1.value,
            "backendException": self.bundle.io._fetch._resp._bits._backendException.value,
            "gpaddr": self.bundle.io._fetch._resp._bits._gpaddr.value,
            "isForVSnonLeafPTE": self.bundle.io._fetch._resp._bits._isForVSnonLeafPTE.value
        }

    async def monitor_replacer_touch(self) -> dict:
        return {
            "_0_valid": self.bundle.io._touch._0._valid.value,
            "_0_bits_vSetIdx": self.bundle.io._touch._0._bits._vSetIdx.value,
            "_0_bits_way": self.bundle.io._touch._0._bits._way.value,
            "_1_valid": self.bundle.io._touch._1._valid.value,
            "_1_bits_vSetIdx": self.bundle.io._touch._1._bits._vSetIdx.value,
            "_1_bits_way": self.bundle.io._touch._1._bits._way.value,
        }

    async def monitor_meta_flush(self) -> dict:
        return{
            "0_valid": self.bundle.io._metaArrayFlush._0._valid.value,
            "0_bits_virIdx": self.bundle.io._metaArrayFlush._0._bits._virIdx.value,
            "0_bits_waymask": self.bundle.io._metaArrayFlush._0._bits._waymask.value,
            "1_valid": self.bundle.io._metaArrayFlush._1._valid.value,
            "1_bits_virIdx": self.bundle.io._metaArrayFlush._1._bits._virIdx.value,
            "1_bits_waymask": self.bundle.io._metaArrayFlush._1._bits._waymask.value,
        }

    
    async def monitor_pipeline_status(self) -> dict:
        """
        获取流水线状态
        """
        # 获取内部信号
        s0_fire = self.bundle.ICacheMainPipe._s0_fire
        s1_fire = self.dut.GetInternalSignal("ICacheMainPipe_top.ICacheMainPipe.s1_fire", use_vpi=False)
        s2_fire = self.bundle.ICacheMainPipe._s2._fire
        
        return {
            "s0_fire": s0_fire.value,
            "s1_fire": s1_fire.value if s1_fire else None,
            "s2_fire": s2_fire.value,
            "ecc_enable": self.bundle.io._ecc_enable.value,
            "wayLookupRead_ready": self.bundle.io._wayLookupRead._ready.value,
            "fetch_req_ready": self.bundle.io._fetch._req._ready.value
        }

    async def monitor_error_status(self) -> dict:
        """
        获取错误状态
        """
        return {
            "0_valid": self.bundle.io._errors._0._valid.value,
            "0_paddr": self.bundle.io._errors._0._bits._paddr.value,
            "0_report_to_beu": self.bundle.io._errors._0._bits._report_to_beu.value,
            "1_valid": self.bundle.io._errors._1._valid.value,
            "1_paddr": self.bundle.io._errors._1._bits._paddr.value,
            "1_report_to_beu": self.bundle.io._errors._1._bits._report_to_beu.value,
        }

    # ==================== 增强的内部信号监控API ====================
    
    async def monitor_exception_merge_status(self) -> dict:
        """
        监控异常合并状态 - 针对测试点14: 异常合并
        基于实际RTL信号名称更新
        """
        try:
            # 根据RTL代码，实际信号名称为s1_itlb_exception_0等
            s1_itlb_exception_0 = self.dut.GetInternalSignal("ICacheMainPipe_top.ICacheMainPipe.s1_itlb_exception_0", use_vpi=False)
            s1_itlb_exception_1 = self.dut.GetInternalSignal("ICacheMainPipe_top.ICacheMainPipe.s1_itlb_exception_1", use_vpi=False)
            s2_exception_0 = self.dut.GetInternalSignal("ICacheMainPipe_top.ICacheMainPipe.s2_exception_0", use_vpi=False)
            s2_exception_1 = self.dut.GetInternalSignal("ICacheMainPipe_top.ICacheMainPipe.s2_exception_1", use_vpi=False)
            s2_l2_corrupt_0 = self.dut.GetInternalSignal("ICacheMainPipe_top.ICacheMainPipe.s2_l2_corrupt_0", use_vpi=False)
            s2_exception_out_0 = s2_exception_0.value if s2_exception_0 and s2_exception_0.value != 0 else (3 if s2_l2_corrupt_0 and s2_l2_corrupt_0.value == 1 else 0)

            
            return {
                "s1_itlb_exception_0": s1_itlb_exception_0.value if s1_itlb_exception_0 else None,
                "s1_itlb_exception_1": s1_itlb_exception_1.value if s1_itlb_exception_1 else None,
                "s2_exception_0": s2_exception_0.value if s2_exception_0 else None,
                "s2_exception_1": s2_exception_1.value if s2_exception_1 else None,
                "s2_exception_out_0": s2_exception_out_0,
            }
        except Exception as e:
            print(f"Warning: Could not access internal exception signals: {e}")
            return {}

    async def monitor_mshr_match_status(self) -> dict:
        """
        监控MSHR匹配和数据选择状态 - 针对测试点15: MSHR匹配和数据选择
        基于实际RTL信号名称更新 - RTL中bank级别的MSHR命中信号为s1_bankMSHRHit_0到s1_bankMSHRHit_7
        """
        try:
            # RTL中的实际信号名称
            s1_MSHR_hits_1 = self.dut.GetInternalSignal("ICacheMainPipe_top.ICacheMainPipe.s1_MSHR_hits_1", use_vpi=False)
            s1_bankMSHRHit_7 = self.dut.GetInternalSignal("ICacheMainPipe_top.ICacheMainPipe.s1_bankMSHRHit_7", use_vpi=False)
            s1_bankMSHRHit_0 = self.dut.GetInternalSignal("ICacheMainPipe_top.ICacheMainPipe.s1_bankMSHRHit_0", use_vpi=False)
            s1_bankMSHRHit_1 = self.dut.GetInternalSignal("ICacheMainPipe_top.ICacheMainPipe.s1_bankMSHRHit_1", use_vpi=False)
            s1_bankMSHRHit_2 = self.dut.GetInternalSignal("ICacheMainPipe_top.ICacheMainPipe.s1_bankMSHRHit_2", use_vpi=False)
            s1_bankMSHRHit_3 = self.dut.GetInternalSignal("ICacheMainPipe_top.ICacheMainPipe.s1_bankMSHRHit_3", use_vpi=False)
            s1_bankMSHRHit_4 = self.dut.GetInternalSignal("ICacheMainPipe_top.ICacheMainPipe.s1_bankMSHRHit_4", use_vpi=False)
            s1_bankMSHRHit_5 = self.dut.GetInternalSignal("ICacheMainPipe_top.ICacheMainPipe.s1_bankMSHRHit_5", use_vpi=False)
            s1_bankMSHRHit_6 = self.dut.GetInternalSignal("ICacheMainPipe_top.ICacheMainPipe.s1_bankMSHRHit_6", use_vpi=False)
            
            return {
                "s1_MSHR_hits_1": s1_MSHR_hits_1.value if s1_MSHR_hits_1 else None,
                "s1_bankMSHRHit_0": s1_bankMSHRHit_0.value if s1_bankMSHRHit_0 else None,
                "s1_bankMSHRHit_1": s1_bankMSHRHit_1.value if s1_bankMSHRHit_1 else None,
                "s1_bankMSHRHit_2": s1_bankMSHRHit_2.value if s1_bankMSHRHit_2 else None,
                "s1_bankMSHRHit_3": s1_bankMSHRHit_3.value if s1_bankMSHRHit_3 else None,
                "s1_bankMSHRHit_4": s1_bankMSHRHit_4.value if s1_bankMSHRHit_4 else None,
                "s1_bankMSHRHit_5": s1_bankMSHRHit_5.value if s1_bankMSHRHit_5 else None,
                "s1_bankMSHRHit_6": s1_bankMSHRHit_6.value if s1_bankMSHRHit_6 else None,
                "s1_bankMSHRHit_7": s1_bankMSHRHit_7.value if s1_bankMSHRHit_7 else None,
            }
        except Exception as e:
            print(f"Warning: Could not access internal MSHR match signals: {e}")
            return {}

    async def monitor_data_ecc_detailed_status(self) -> dict:
        """
        监控详细的Data ECC状态 - 针对测试点16: Data ECC校验
        基于实际RTL信号名称更新 - RTL中的bank corrupt信号为s2_bank_corrupt_0到s2_bank_corrupt_7
        """
        try:
            s2_bank_corrupt = []
            # RTL中实际存在的bank corrupt信号名称 (第456-463行)
            for i in range(8):
                try:
                    signal = self.dut.GetInternalSignal(f"ICacheMainPipe_top.ICacheMainPipe.s2_bank_corrupt_{i}", use_vpi=False)
                    s2_bank_corrupt.append(signal.value)
                except:
                    s2_bank_corrupt.append(None)
            
            # RTL中实际存在的data corrupt信号 (第464, 475行)
            s2_data_corrupt_0 = self.dut.GetInternalSignal("ICacheMainPipe_top.ICacheMainPipe.s2_data_corrupt_0", use_vpi=False)
            s2_data_corrupt_1 = self.dut.GetInternalSignal("ICacheMainPipe_top.ICacheMainPipe.s2_data_corrupt_1", use_vpi=False)
            
            return {
                "ecc_enable": self.bundle.io._ecc_enable.value,
                "s2_data_corrupt_0": s2_data_corrupt_0.value,
                "s2_data_corrupt_1": s2_data_corrupt_1.value,
                "s2_bank_corrupt": s2_bank_corrupt,
            }
        except Exception as e:
            print(f"Warning: Could not access detailed data ECC signals: {e}")
            return {"ecc_enable": self.bundle.io._ecc_enable.value}

    async def monitor_s2_mshr_match_status(self) -> dict:
        """
        监控S2阶段MSHR匹配与数据更新状态 - 针对测试点18: 监控MSHR匹配与数据更新
        修正：包含所有8个MSHR信号（0-7）
        """
        try:
            # S2 MSHR匹配信号
            s2_MSHR_hits_1 = self.dut.GetInternalSignal("ICacheMainPipe_top.ICacheMainPipe.s2_MSHR_hits_1", use_vpi=False)
            s2_bankMSHRHit = []
            for i in range(8):
                signal = self.dut.GetInternalSignal(f"ICacheMainPipe_top.ICacheMainPipe.s2_bankMSHRHit_{i}", use_vpi=False)
                s2_bankMSHRHit.append(signal.value if signal else None)
                
            # 8个bank的数据来源MSHR标识（0-7）
            s2_data_is_from_MSHR = []
            for i in range(8):
                signal = self.dut.GetInternalSignal(f"ICacheMainPipe_top.ICacheMainPipe.s2_data_is_from_MSHR_{i}", use_vpi=False)
                s2_data_is_from_MSHR.append(signal.value if signal else None)
            
            if not hasattr(self, '_debug_mshr_printed_detail'):
                self._debug_mshr_printed_detail = True
            
            return {
                "s2_MSHR_hits_1": s2_MSHR_hits_1.value,
                "s2_bankMSHRHit_0": s2_bankMSHRHit[0],
                "s2_bankMSHRHit_1": s2_bankMSHRHit[1], 
                "s2_bankMSHRHit_2": s2_bankMSHRHit[2],
                "s2_bankMSHRHit_3": s2_bankMSHRHit[3],
                "s2_bankMSHRHit_4": s2_bankMSHRHit[4],
                "s2_bankMSHRHit_5": s2_bankMSHRHit[5],
                "s2_bankMSHRHit_6": s2_bankMSHRHit[6],
                "s2_bankMSHRHit_7": s2_bankMSHRHit[7],
                "s2_data_is_from_MSHR_0": s2_data_is_from_MSHR[0],
                "s2_data_is_from_MSHR_1": s2_data_is_from_MSHR[1],
                "s2_data_is_from_MSHR_2": s2_data_is_from_MSHR[2],
                "s2_data_is_from_MSHR_3": s2_data_is_from_MSHR[3],
                "s2_data_is_from_MSHR_4": s2_data_is_from_MSHR[4],
                "s2_data_is_from_MSHR_5": s2_data_is_from_MSHR[5],
                "s2_data_is_from_MSHR_6": s2_data_is_from_MSHR[6],
                "s2_data_is_from_MSHR_7": s2_data_is_from_MSHR[7],
                "s2_bankMSHRHit_all": s2_bankMSHRHit,  # 提供完整的数组形式
                "s2_data_is_from_MSHR_all": s2_data_is_from_MSHR  # 提供完整的数组形式
            }
        except Exception as e:
            print(f"Warning: Could not access S2 MSHR match signals: {e}")
            return {}

    async def monitor_miss_request_status(self) -> dict:
        """
        监控Miss请求发送逻辑状态 - 针对测试点19: Miss请求发送逻辑和合并异常
        基于实际RTL信号名称更新
        """
        try:
            # RTL中实际存在的信号 (第507, 509, 513, 514行)
            s2_should_fetch_0 = self.dut.GetInternalSignal("ICacheMainPipe_top.ICacheMainPipe.s2_should_fetch_0", use_vpi=False)
            s2_should_fetch_1 = self.dut.GetInternalSignal("ICacheMainPipe_top.ICacheMainPipe.s2_should_fetch_1", use_vpi=False)
            s2_has_send_0 = self.dut.GetInternalSignal("ICacheMainPipe_top.ICacheMainPipe.s2_has_send_0", use_vpi=False)
            s2_has_send_1 = self.dut.GetInternalSignal("ICacheMainPipe_top.ICacheMainPipe.s2_has_send_1", use_vpi=False)
            # RTL中相关的信号
            s2_l2_corrupt_0 = self.dut.GetInternalSignal("ICacheMainPipe_top.ICacheMainPipe.s2_l2_corrupt_0", use_vpi=False)  # 第504行
            s2_l2_corrupt_1 = self.dut.GetInternalSignal("ICacheMainPipe_top.ICacheMainPipe.s2_l2_corrupt_1", use_vpi=False)  # 第505行
            s2_exception_0 = self.dut.GetInternalSignal("ICacheMainPipe_top.ICacheMainPipe.s2_exception_0", use_vpi=False)
            s2_exception_1 = self.dut.GetInternalSignal("ICacheMainPipe_top.ICacheMainPipe.s2_exception_1", use_vpi=False)
            s2_doubleline = self.dut.GetInternalSignal("ICacheMainPipe_top.ICacheMainPipe.s2_doubleline", use_vpi=False)
            
            # 计算s2_exception_out_0 = (|s2_exception_0) ? s2_exception_0 : {2{s2_l2_corrupt_0}}
            s2_exception_out_0 = s2_exception_0.value if s2_exception_0 and s2_exception_0.value != 0 else (3 if s2_l2_corrupt_0 and s2_l2_corrupt_0.value == 1 else 0)
            
            # 计算s2_exception_out_1 = s2_doubleline ? ((|s2_exception_1) ? s2_exception_1 : {2{s2_l2_corrupt_1}}) : 0
            if s2_doubleline and s2_doubleline.value:
                s2_exception_out_1 = s2_exception_1.value if s2_exception_1 and s2_exception_1.value != 0 else (3 if s2_l2_corrupt_1 and s2_l2_corrupt_1.value == 1 else 0)
            else:
                s2_exception_out_1 = 0
            
            # 添加其他相关信号
            io_fetch_topdownIcacheMiss = self.bundle.io._fetch._topdownIcacheMiss
            s2_fire = self.bundle.ICacheMainPipe._s2._fire
            
            # Safe value extraction with None checks
            result = {}
            if s2_should_fetch_0 is not None:
                result["s2_should_fetch_0"] = s2_should_fetch_0.value
            else:
                print("DEBUG: s2_should_fetch_0 is None")
                result["s2_should_fetch_0"] = None
                
            if s2_should_fetch_1 is not None:
                result["s2_should_fetch_1"] = s2_should_fetch_1.value
            else:
                print("DEBUG: s2_should_fetch_1 is None")
                result["s2_should_fetch_1"] = None
            
            # 添加其他重要信号
            result["s2_has_send_0"] = s2_has_send_0.value if s2_has_send_0 else None
            result["s2_has_send_1"] = s2_has_send_1.value if s2_has_send_1 else None
            result["s2_l2_corrupt_0"] = s2_l2_corrupt_0.value if s2_l2_corrupt_0 else None
            result["s2_l2_corrupt_1"] = s2_l2_corrupt_1.value if s2_l2_corrupt_1 else None
            result["s2_exception_0"] = s2_exception_0.value if s2_exception_0 else None
            result["s2_exception_1"] = s2_exception_1.value if s2_exception_1 else None
            result["s2_doubleline"] = s2_doubleline.value if s2_doubleline else None
            result["s2_exception_out_0"] = s2_exception_out_0  # 计算出的值
            result["s2_exception_out_1"] = s2_exception_out_1  # 计算出的值
            result["io_fetch_topdownIcacheMiss_0"] = io_fetch_topdownIcacheMiss.value
            result["s2_fire"] = s2_fire.value
            result["mshr_req_valid"] = self.bundle.io._mshr._req._valid.value
            result["mshr_req_ready"] = self.bundle.io._mshr._req._ready.value
                
            return result
        except Exception as e:
            print(f"Warning: Could not access miss request signals: {e}")
            return {
                "mshr_req_valid": self.bundle.io._mshr._req._valid.value,
                "mshr_req_ready": self.bundle.io._mshr._req._ready.value,
            }

    async def monitor_meta_corrupt_status(self) -> dict:
        """
        监控Meta corrupt相关状态，增强Meta ECC监控
        """
        s1_meta_corrupt_hit_num = self.dut.GetInternalSignal("ICacheMainPipe_top.ICacheMainPipe.s1_meta_corrupt_hit_num", use_vpi=False)
        print(f"DEBUG: monitor_meta_corrupt_status - s1_meta_corrupt_hit_num: {s1_meta_corrupt_hit_num.value}")
            
        if s1_meta_corrupt_hit_num is not None:
            return {
                    "s1_meta_corrupt_hit_num": s1_meta_corrupt_hit_num.value,
                    "ecc_enable": self.bundle.io._ecc_enable.value
            }
        else:
            print("ERROR: can't access s1_meta_corrupt_hit_num")



    # ==================== 增强的错误注入API ====================
    
    async def inject_meta_ecc_error(self, 
                                   vSetIdx_0: int = 0,
                                   vSetIdx_1: int = 0,
                                   waymask_0: int = 1,  # 单路命中
                                   waymask_1: int = 0,
                                   ptag_0: int = 0x12345,
                                   ptag_1: int = 0,
                                   wrong_meta_code_0: int = None,  # 如果为None则自动生成错误的ECC码
                                   meta_codes_1: int = 0) -> bool:
        """
        注入Meta ECC错误 - 针对测试点12.2: 单路命中的ECC错误
        计算正确的ECC码然后故意提供错误的ECC码
        """
        try:
            # 计算ptag的正确ECC码 (XOR parity)
            correct_ecc = 0
            temp_ptag = ptag_0
            while temp_ptag:
                correct_ecc ^= temp_ptag & 1
                temp_ptag >>= 1
            
            # 如果没有指定错误ECC码，则使用正确ECC的反值
            if wrong_meta_code_0 is None:
                wrong_meta_code_0 = 1 - correct_ecc
            
            await self.drive_waylookup_read(
                vSetIdx_0=vSetIdx_0,
                vSetIdx_1=vSetIdx_1,
                waymask_0=waymask_0,
                waymask_1=waymask_1,
                ptag_0=ptag_0,
                ptag_1=ptag_1,
                meta_codes_0=wrong_meta_code_0,
                meta_codes_1=meta_codes_1
            )
            print(f"Injected Meta ECC error: ptag=0x{ptag_0:x}, correct_ecc={correct_ecc}, wrong_ecc={wrong_meta_code_0}")
            return True
        except Exception as e:
            print(f"Failed to inject Meta ECC error: {e}")
            return False

    async def inject_multi_way_hit(self,
                                  vSetIdx_0: int = 0,
                                  vSetIdx_1: int = 0,
                                  waymask_0: int = 0b1100,  # 多路命中
                                  waymask_1: int = 0,
                                  ptag_0: int = 0x12345,
                                  ptag_1: int = 0) -> bool:
        """
        注入多路命中错误 - 针对测试点12.3: 多路命中
        """
        try:
            await self.drive_waylookup_read(
                vSetIdx_0=vSetIdx_0,
                vSetIdx_1=vSetIdx_1,
                waymask_0=waymask_0,
                waymask_1=waymask_1,
                ptag_0=ptag_0,
                ptag_1=ptag_1
            )
            print(f"Injected multi-way hit: waymask={bin(waymask_0)}")
            return True
        except Exception as e:
            print(f"Failed to inject multi-way hit: {e}")
            return False

    async def inject_data_ecc_error(self,
                                   bank_index: int = 0,
                                   error_data: int = 0xDEADBEEF,
                                   wrong_code: int = None) -> bool:
        """
        注入Data ECC错误 - 针对测试点16: Data ECC校验
        
        RTL逻辑：s2_bank_corrupt = ^s2_datas != s2_codes
        通过故意提供错误的ECC码来触发Data ECC错误
        """
        try:
            if 0 <= bank_index < 8:
                # 计算error_data的正确ECC码（XOR奇偶校验）
                correct_ecc = 0
                temp_data = error_data
                while temp_data:
                    correct_ecc ^= temp_data & 1
                    temp_data >>= 1
                
                # 如果没有指定错误ECC码，则使用正确ECC的反值
                if wrong_code is None:
                    wrong_code = 1 - correct_ecc
                
                datas = [0] * 8
                codes = [0] * 8
                datas[bank_index] = error_data
                codes[bank_index] = wrong_code
                
                success = await self.drive_data_array_response(datas=datas, codes=codes)
                if success:
                    print(f"Injected Data ECC error in bank {bank_index}: data=0x{error_data:x}, correct_ecc={correct_ecc}, wrong_ecc={wrong_code}")
                    return True
                else:
                    print("Failed to inject Data ECC error: Incomplete data")
                    return False
            else:
                print(f"Invalid bank index: {bank_index}")
                return False
        except Exception as e:
            print(f"Failed to inject Data ECC error: {e}")
            return False

    async def inject_l2_corrupt_response(self,
                                       blkPaddr: int = 0x1000,
                                       vSetIdx: int = 0x10,
                                       corrupt_data: int = 0xBADD4A7A,
                                       corrupt: int = 1) -> bool:
        """
        注入L2 corrupt响应 - 针对测试点21: L2 Corrupt报告
        """
        try:
            success = await self.drive_mshr_response(
                blkPaddr=blkPaddr,
                vSetIdx=vSetIdx,
                data=corrupt_data,
                corrupt=corrupt
            )
            if success:
                print(f"Injected L2 corrupt response: paddr=0x{blkPaddr:x}")
                return True
            else:
                print("Failed to inject L2 corrupt response: MSHR not ready")
                return False
        except Exception as e:
            print(f"Failed to inject L2 corrupt response: {e}")
            return False

    async def setup_mshr_ready(self, ready: bool = True):
        """
        设置MSHR ready信号，用于控制Miss请求接收
        """
        self.bundle.io._mshr._req._ready.value = int(ready)
        await self.bundle.step()
