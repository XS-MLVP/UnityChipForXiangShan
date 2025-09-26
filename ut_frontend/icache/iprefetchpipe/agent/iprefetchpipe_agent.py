import asyncio
from toffee import Agent
from ..bundle import IPrefetchPipeBundle
import random


class IPrefetchPipeAgent(Agent):
    def __init__(self, bundle: IPrefetchPipeBundle, dut=None):
        super().__init__(bundle)
        self.bundle = bundle
        self.dut = dut
        bundle.set_all(0)



    async def receive_prefetch(self):
        self.bundle.io._req._bits._startAddr.value = random.randint(0, (1<<49)-1)<<1
        self.bundle.io._req._bits._nextlineStart.value = random.randint(0, (1<<49)-1)<<1
        self.bundle.io._req._bits._isSoftPrefetch.value = random.getrandbits(1)
        self.bundle.io._req._bits._ftqIdx._flag.value = random.getrandbits(1)
        self.bundle.io._req._bits._ftqIdx._value.value = random.randint(0, (1<<6)-1)
        self.bundle.io._req._bits._backendException.value = random.randint(0, (1<<6)-1)

        # set s0_fire
        self.bundle.io._req._valid.value = 1
        self.bundle.io._metaRead._toIMeta._ready.value = 1
        await self.bundle.step()
        self.bundle.io._flush.value = 0

        await self.bundle.step()

        assert (
            self.bundle.IPrefetchPipe._s1._req._vaddr._0.value
            == self.bundle.io._req._bits._startAddr.value
        ), "vaddr_0 is not equal"
        assert (
            self.bundle.IPrefetchPipe._s1._req._vaddr._1.value
            == self.bundle.io._req._bits._nextlineStart.value
        ), "vaddr_1 is not equal"
        assert (
            self.bundle.IPrefetchPipe._s1._isSoftPrefetch.value
            == self.bundle.io._req._bits._isSoftPrefetch.value
        ), "isSoftPrefetch is not equal"
        assert self.bundle.IPrefetchPipe._s1._doubleline.value == int(
            (bin(self.bundle.io._req._bits._startAddr.value)[2:])[-6]
        ), "doubleline is not equal"
        assert (
            self.bundle.IPrefetchPipe._s1._req._ftqIdx._flag.value
            == self.bundle.io._req._bits._ftqIdx._flag.value
        ), "ftqIdx_flag is not equal"
        assert (
            self.bundle.IPrefetchPipe._s1._req._ftqIdx._value.value
            == self.bundle.io._req._bits._ftqIdx._value.value
        ), "ftqIdx_value is not equal"
        assert (
            self.bundle.IPrefetchPipe._s1._backendException._0.value
            == self.bundle.io._req._bits._backendException.value
        ), "backendException_0 is not equal"
        assert (
            self.bundle.IPrefetchPipe._s1._backendException._1.value
            == self.bundle.io._req._bits._backendException.value
        ), "backendException_1 is not equal"

        await self.bundle.step(2)

    # ==================== 基础控制API ====================
    
    async def reset_dut(self):
        """Reset the DUT"""
        self.bundle.reset.value = 1
        await self.bundle.step(5)
        self.bundle.reset.value = 0
        await self.bundle.step(5)
        print("DUT reset completed")

    async def set_prefetch_enable(self, enable: bool = True):
        """
        Set CSR prefetch enable signal
        
        Args:
            enable: True to enable prefetch, False to disable
            
        Note:
            This controls the global prefetch functionality.
            When disabled, prefetch requests may be ignored.
        """
        self.bundle.io._csr_pf_enable.value = int(enable)
        await self.bundle.step()
        print(f"Prefetch enable set to {enable}")
        
    async def get_prefetch_enable(self) -> bool:
        """Get current prefetch enable status"""
        return bool(self.bundle.io._csr_pf_enable.value)

    async def drive_flush(self, flush_type: str = "global", **kwargs):
        """
        Drive flush signals with enhanced BPU flush support
        
        Args:
            flush_type: "global", "bpu_s2", or "bpu_s3"
            **kwargs: Additional parameters for BPU flush:
                - ftq_flag: FTQ flag for BPU flush (default: 1)
                - ftq_value: FTQ value for BPU flush (default: 0)
                - duration_cycles: How long to hold the flush signal (default: 1)
        """
        duration = kwargs.get('duration_cycles', 1)
        
        if flush_type == "global":
            self.bundle.io._flush.value = 1
            await self.bundle.step(duration)
            self.bundle.io._flush.value = 0
            await self.bundle.step()
            print("Global flush completed")
            
        elif flush_type == "bpu_s2":
            ftq_flag = kwargs.get('ftq_flag', 1)
            ftq_value = kwargs.get('ftq_value', 0)
            
            self.bundle.io._flushFromBpu._s2._valid.value = 1
            self.bundle.io._flushFromBpu._s2._bits._flag.value = ftq_flag
            self.bundle.io._flushFromBpu._s2._bits._value.value = ftq_value
            await self.bundle.step(duration)
            
            # Clear flush signals
            self.bundle.io._flushFromBpu._s2._valid.value = 0
            self.bundle.io._flushFromBpu._s2._bits._flag.value = 0
            self.bundle.io._flushFromBpu._s2._bits._value.value = 0
            await self.bundle.step()
            print(f"BPU S2 flush completed (flag={ftq_flag}, value={ftq_value})")
            
        elif flush_type == "bpu_s3":
            ftq_flag = kwargs.get('ftq_flag', 1)
            ftq_value = kwargs.get('ftq_value', 0)
            
            self.bundle.io._flushFromBpu._s3._valid.value = 1
            self.bundle.io._flushFromBpu._s3._bits._flag.value = ftq_flag
            self.bundle.io._flushFromBpu._s3._bits._value.value = ftq_value
            await self.bundle.step(duration)
            
            # Clear flush signals
            self.bundle.io._flushFromBpu._s3._valid.value = 0
            self.bundle.io._flushFromBpu._s3._bits._flag.value = 0
            self.bundle.io._flushFromBpu._s3._bits._value.value = 0
            await self.bundle.step()
            print(f"BPU S3 flush completed (flag={ftq_flag}, value={ftq_value})")
            
        else:
            raise ValueError(f"Unknown flush_type: {flush_type}")

    async def get_flush_status(self) -> dict:
        """Get current flush signal status"""
        return {
            "global_flush": bool(self.bundle.io._flush.value),
            "bpu_s2_flush": {
                "valid": bool(self.bundle.io._flushFromBpu._s2._valid.value),
                "flag": self.bundle.io._flushFromBpu._s2._bits._flag.value,
                "value": self.bundle.io._flushFromBpu._s2._bits._value.value
            },
            "bpu_s3_flush": {
                "valid": bool(self.bundle.io._flushFromBpu._s3._valid.value),
                "flag": self.bundle.io._flushFromBpu._s3._bits._flag.value,
                "value": self.bundle.io._flushFromBpu._s3._bits._value.value
            },
            "itlb_flush_pipe": bool(self.bundle.io._itlbFlushPipe.value)
        }

    # ==================== S0阶段 - 接收预取请求API ====================
    
    async def drive_prefetch_request(self,
                                   startAddr: int = None,
                                   isSoftPrefetch: bool = False,
                                   ftqIdx_flag: int = 0,
                                   ftqIdx_value: int = 0,
                                   backendException: int = 0,
                                   wait_for_ready: bool = True,
                                   timeout_cycles: int = 10,
                                   force_nextlineStart: int = None) -> dict:
        """
        Drive a prefetch request to S0 stage following IPrefetchPipe protocol
        
        Args:
            startAddr: Starting address for prefetch (if None, generates random aligned addr)
            isSoftPrefetch: Whether this is a software prefetch
            ftqIdx_flag: FTQ index flag
            ftqIdx_value: FTQ index value  
            backendException: Backend exception code
            wait_for_ready: Whether to wait for ready signal before sending
            timeout_cycles: Maximum cycles to wait
            force_nextlineStart: Manual override for nextline address (for testing)
            
        Note:
            - nextlineStart = startAddr + 0x40 (next cache line address)
            - startAddr[5] bit determines if this is double-line prefetch
            - Double-line: both startAddr and nextlineStart cache lines are prefetched
            - Single-line: only startAddr cache line is prefetched
            
        Returns:
            dict with request status, actual values sent, and s0_fire detection
        """
        # Generate valid startAddr if not provided
        if startAddr is None:
            # Generate a cache-line aligned address (64-byte aligned)
            startAddr = (random.randint(0, (1<<43)-1) << 6)
            
        # Calculate nextlineStart - always the next cache line (64 bytes later)
        is_doubleline = bool((startAddr >> 5) & 1)  # Bit 5 determines double-line prefetch
        
        if force_nextlineStart is not None:
            # Allow manual override for testing
            nextlineStart = force_nextlineStart
        else:
            # nextlineStart is always the start of next cache line
            nextlineStart = startAddr + 0x40  # +64 bytes for next cache line
            
        req_info = {}
        req_info["send_success"] = False
        req_info["s0_fire_detected"] = False
        
        print(f"Attempting to send prefetch request:")
        print(f"  startAddr: 0x{startAddr:x}")
        print(f"  nextlineStart: 0x{nextlineStart:x}")
        print(f"  is_doubleline: {is_doubleline} (startAddr[5]={bool(startAddr & 0x20)})")
        print(f"  isSoftPrefetch: {isSoftPrefetch}")
        print(f"  timeout: {timeout_cycles} cycles")
        
        for i in range(timeout_cycles):
            # Check IPrefetchPipe readiness
            pipe_ready = (self.bundle.io._req._ready.value == 1)
            
            if pipe_ready or not wait_for_ready:
                # Set up request data
                self.bundle.io._req._bits._startAddr.value = startAddr
                self.bundle.io._req._bits._nextlineStart.value = nextlineStart
                self.bundle.io._req._bits._isSoftPrefetch.value = int(isSoftPrefetch)
                self.bundle.io._req._bits._ftqIdx._flag.value = ftqIdx_flag
                self.bundle.io._req._bits._ftqIdx._value.value = ftqIdx_value
                self.bundle.io._req._bits._backendException.value = backendException
                
                # Assert valid signal
                self.bundle.io._req._valid.value = 1
                
                await self.bundle.step()
                
                # Check if request was accepted by simulating s0_fire condition
                # s0_fire = io_req_valid & s0_can_go & ~(flush signals)
                valid_asserted = (self.bundle.io._req._valid.value == 1)
                ready_active = (self.bundle.io._req._ready.value == 1)
                no_global_flush = (self.bundle.io._flush.value == 0)
                
                # Note: We can't check all flush signals (like from_bpu_s0_flush_probe) 
                # as they are internal, but we check the main ones
                s0_fire_conditions_met = valid_asserted and ready_active and no_global_flush
                
                if s0_fire_conditions_met:
                    req_info["send_success"] = True
                    req_info["s0_fire_detected"] = True
                    req_info.update({
                        "startAddr": startAddr,
                        "nextlineStart": nextlineStart,
                        "isSoftPrefetch": isSoftPrefetch,
                        "ftqIdx_flag": ftqIdx_flag,
                        "ftqIdx_value": ftqIdx_value,
                        "backendException": backendException,
                        "doubleline": is_doubleline,
                        "cycle_accepted": i + 1,
                        "cache_line_0": f"0x{startAddr >> 6:x}",
                        "cache_line_1": f"0x{nextlineStart >> 6:x}" if is_doubleline else "N/A"
                    })
                    print(f"✓ Prefetch request accepted at cycle {i+1}")
                    print(f"  Cache line 0: 0x{startAddr >> 6:x} (startAddr)")
                    if is_doubleline:
                        print(f"  Cache line 1: 0x{nextlineStart >> 6:x} (nextlineStart)")
                    
                    # Note: valid signal should remain asserted until caller decides to deassert
                    # This follows proper ready/valid handshake protocol
                    return req_info
                else:
                    print(f"✗ Request conditions not met (cycle {i+1}): "
                          f"valid={valid_asserted}, ready={ready_active}, no_flush={no_global_flush}")
                    
                # Keep valid asserted for next cycle attempt (proper handshake protocol)
                await self.bundle.step()
            else:
                print(f"⧗ IPrefetchPipe not ready (cycle {i+1})")
                await self.bundle.step()
        
        print(f"✗ Timeout: Prefetch request not accepted after {timeout_cycles} cycles")
        # Keep valid signal as-is, let caller manage signal lifecycle
        return req_info

    async def deassert_prefetch_request(self):
        """
        Deassert the prefetch request valid signal
        
        This should be called by the test after drive_prefetch_request succeeds
        to properly manage the valid signal lifecycle according to ready/valid protocol
        """
        self.bundle.io._req._valid.value = 0
        await self.bundle.step()
        print("Prefetch request valid signal deasserted")

    # ==================== ITLB交互API ====================
    
    async def get_itlb_request_status(self) -> dict:
        """Get current ITLB request status for both ports"""
        return {
            "port_0": {
                "req_valid": bool(self.bundle.io._itlb._0._req._valid.value),
                "req_vaddr": self.bundle.io._itlb._0._req._bits_vaddr.value
            },
            "port_1": {
                "req_valid": bool(self.bundle.io._itlb._1._req._valid.value),
                "req_vaddr": self.bundle.io._itlb._1._req._bits_vaddr.value
            }
        }

    async def drive_itlb_response(self,
                                 port: int = 0,
                                 paddr: int = None,
                                 af: bool = False,
                                 pf: bool = False,
                                 gpf: bool = False,
                                 pbmt_nc: bool = False,
                                 pbmt_io: bool = False,
                                 miss: bool = False,
                                 gpaddr: int = 0,
                                 isForVSnonLeafPTE: bool = False) -> dict:
        """
        Drive ITLB response for address translation
        """
        if paddr is None:
            paddr = random.randint(0, (1<<50)-1)
            
        print(f"Driving ITLB response for port {port}")
        result = False
        
        # Validate exception signals - ensure at most one is active (one-hot encoding required by hardware)
        exception_count = sum([af, pf, gpf])
        if exception_count > 1:
            print(f"Error: Multiple exception flags set (af={af}, pf={pf}, gpf={gpf})")
            print("Hardware requires one-hot encoding - at most one exception can be active")
            result = False
            return {
                "result": result,
                "port": port,
                "error": "Invalid exception combination: multiple exceptions cannot be active simultaneously"
            }
        
        # Set ITLB response
        itlb_bundle = getattr(self.bundle.io._itlb, f"_{port}")
        
        itlb_bundle._resp_bits._paddr._0.value = paddr
        itlb_bundle._resp_bits._excp._0._af_instr.value = int(af)
        itlb_bundle._resp_bits._excp._0._pf_instr.value = int(pf)
        itlb_bundle._resp_bits._excp._0._gpf_instr.value = int(gpf)
        itlb_bundle._resp_bits._pbmt._0.value = int(pbmt_nc) | (int(pbmt_io) << 1)
        itlb_bundle._resp_bits._miss.value = int(miss)
        itlb_bundle._resp_bits._gpaddr._0.value = gpaddr
        itlb_bundle._resp_bits._isForVSnonLeafPTE.value = int(isForVSnonLeafPTE)
        
        await self.bundle.step()
        
        # Read back actual values from DUT
        actual_paddr = itlb_bundle._resp_bits._paddr._0.value
        actual_af = bool(itlb_bundle._resp_bits._excp._0._af_instr.value)
        actual_pf = bool(itlb_bundle._resp_bits._excp._0._pf_instr.value)
        actual_gpf = bool(itlb_bundle._resp_bits._excp._0._gpf_instr.value)
        pbmt_value = itlb_bundle._resp_bits._pbmt._0.value
        actual_pbmt_nc = bool(pbmt_value & 1)
        actual_pbmt_io = bool(pbmt_value & 2)
        actual_miss = bool(itlb_bundle._resp_bits._miss.value)
        actual_gpaddr = itlb_bundle._resp_bits._gpaddr._0.value
        actual_isForVSnonLeafPTE = bool(itlb_bundle._resp_bits._isForVSnonLeafPTE.value)
        result = True
        
        return {
            "result": result,
            "port": port,
            "paddr": actual_paddr,
            "af": actual_af,
            "pf": actual_pf,
            "gpf": actual_gpf,
            "pbmt_nc": actual_pbmt_nc,
            "pbmt_io": actual_pbmt_io,
            "miss": actual_miss,
            "gpaddr": actual_gpaddr,
            "isForVSnonLeafPTE": actual_isForVSnonLeafPTE
        }

    # ==================== PMP交互API ====================
    
    async def get_pmp_request_status(self) -> dict:
        """Get current PMP request status for both ports"""
        return {
            "port_0": {
                "req_addr": self.bundle.io._pmp._0._req_bits_addr.value
            },
            "port_1": {
                "req_addr": self.bundle.io._pmp._1._req_bits_addr.value
            }
        }

    async def drive_pmp_response(self,
                               port: int = 0,
                               mmio: bool = False,
                               instr_af: bool = False) -> dict:
        """
        Drive PMP response for permission check
        """
        print(f"Driving PMP response for port {port}")
        
        pmp_bundle = getattr(self.bundle.io._pmp, f"_{port}")
        pmp_bundle._resp._mmio.value = int(mmio)
        pmp_bundle._resp._instr.value = int(instr_af)
        
        await self.bundle.step()
        
        return {
            "port": port,
            "mmio": bool(pmp_bundle._resp._mmio.value),
            "instr_af": bool(pmp_bundle._resp._instr.value)
        }

    # ==================== MetaArray交互API ====================
    
    async def get_meta_request_status(self) -> dict:
        """Get current MetaArray request status"""
        return {
            "toIMeta_valid": bool(self.bundle.io._metaRead._toIMeta._valid.value),
            "toIMeta_ready": bool(self.bundle.io._metaRead._toIMeta._ready.value),
            "vSetIdx_0": self.bundle.io._metaRead._toIMeta._bits._vSetIdx._0.value,
            "vSetIdx_1": self.bundle.io._metaRead._toIMeta._bits._vSetIdx._1.value,
            "isDoubleLine": bool(self.bundle.io._metaRead._toIMeta._bits._isDoubleLine.value)
        }
    
    async def wait_for_itlb_response(self, port: int = 0, timeout_cycles: int = 10) -> bool:
        """
        Wait for ITLB response to be available before driving meta response
        
        Args:
            port: Port number (0 or 1)
            timeout_cycles: Maximum cycles to wait
            
        Returns:
            True if ITLB response is available, False if timeout
        """
        print(f"Waiting for ITLB response on port {port}, timeout: {timeout_cycles} cycles")
        
        for i in range(timeout_cycles):
            if port == 0:
                miss = self.bundle.io._itlb._0._resp_bits._miss.value
                paddr = self.bundle.io._itlb._0._resp_bits._paddr._0.value
            else:
                miss = self.bundle.io._itlb._1._resp_bits._miss.value
                paddr = self.bundle.io._itlb._1._resp_bits._paddr._0.value
            
            # ITLB response is ready when miss=0 and paddr is valid
            if miss == 0 and paddr != 0:
                print(f"ITLB response ready on port {port} (cycle {i+1}): paddr=0x{paddr:x}")
                return True
            
            await self.bundle.step()
        
        print(f"ITLB response timeout on port {port} after {timeout_cycles} cycles")
        return False
    
    async def drive_meta_response(self,
                                 port: int = 0,
                                 hit_ways: list = None,
                                 tags: list = None,
                                 valid_bits: list = None,
                                 codes: list = None,
                                 target_paddr: int = None) -> dict:
        """
        Drive MetaArray response for cache metadata
        
        Args:
            port: Port number (0 or 1)
            hit_ways: [way0, way1, way2, way3] - which ways should hit (0/1 or False/True)
            tags: [tag0, tag1, tag2, tag3] - tag for each way (if None, auto-generated based on hit_ways)
            valid_bits: [v0, v1, v2, v3] - valid bit for each way (if None, auto-generated based on hit_ways)
            codes: [c0, c1, c2, c3] - ECC code for each way (if None, defaults to 0)
            target_paddr: Physical address to match against (if None, will try to get from ITLB response)
            
        Note: If hit_ways is provided but tags is None, tags will be auto-generated to create
              the specified hit pattern based on the target physical address from ITLB response.
        """
        if hit_ways is None:
            hit_ways = [0, 0, 0, 0]  # Default: no hits
        if codes is None:
            codes = [0, 0, 0, 0]  # Default ECC codes
            
        # Convert hit_ways to consistent format (handle both int and bool)
        hit_ways = [bool(h) for h in hit_ways]
        
        # Get target physical tag from ITLB response or parameter
        if target_paddr is None:
            # Try to get physical address from ITLB response
            if port == 0:
                target_paddr = self.bundle.io._itlb._0._resp_bits._paddr._0.value
            else:
                target_paddr = self.bundle.io._itlb._1._resp_bits._paddr._0.value
            
            if target_paddr == 0:
                print(f"Warning: No valid physical address from ITLB for port {port}, using default")
                target_paddr = 0x80001000  # Default fallback address
        
        # Extract tag from physical address (bits [47:12])
        target_tag = (target_paddr >> 12) & 0xFFFFFFFFF  # 36-bit tag
            
        # Auto-generate tags and valid_bits based on hit_ways if not provided
        if tags is None or valid_bits is None:
            auto_tags = []
            auto_valid_bits = []
            
            for way in range(4):
                if hit_ways[way]:
                    # Hit: use matching tag and set valid
                    auto_tags.append(target_tag)
                    auto_valid_bits.append(1)
                else:
                    # Miss: use different tag or invalid bit
                    auto_tags.append(target_tag + way + 1)  # Different tag
                    auto_valid_bits.append(0)  # Invalid to ensure miss
            
            if tags is None:
                tags = auto_tags
            if valid_bits is None:
                valid_bits = auto_valid_bits
            
        print(f"Driving MetaArray response for port {port}")
        print(f"  target_paddr=0x{target_paddr:x}, target_tag=0x{target_tag:x}")
        print(f"  hit_ways={hit_ways}")
        print(f"  tags={[hex(t) for t in tags]}")
        print(f"  valid_bits={valid_bits}")
        print(f"  codes={codes}")
        
        meta_resp = self.bundle.io._metaRead._fromIMeta
        
        # Set signals for each way
        for way in range(4):
            tag_signal = getattr(getattr(meta_resp._metas, f"_{port}"), f"_{way}")._tag
            valid_signal = getattr(getattr(meta_resp._entryValid, f"_{port}"), f"_{way}")
            code_signal = getattr(getattr(meta_resp._codes, f"_{port}"), f"_{way}")
            
            tag_signal.value = tags[way]
            valid_signal.value = valid_bits[way]
            code_signal.value = codes[way]
        
        await self.bundle.step()
        
        # Return actual values from DUT
        actual_tags = []
        actual_valid_bits = []
        actual_codes = []
        
        for way in range(4):
            tag_signal = getattr(getattr(meta_resp._metas, f"_{port}"), f"_{way}")._tag
            valid_signal = getattr(getattr(meta_resp._entryValid, f"_{port}"), f"_{way}")
            code_signal = getattr(getattr(meta_resp._codes, f"_{port}"), f"_{way}")
            
            actual_tags.append(tag_signal.value)
            actual_valid_bits.append(valid_signal.value)
            actual_codes.append(code_signal.value)
        
        return {
            "port": port,
            "target_paddr": target_paddr,
            "target_tag": target_tag,
            "hit_ways": hit_ways,  # Include for backward compatibility with tests
            "tags": actual_tags,   # Keep original key name for compatibility
            "valid_bits": actual_valid_bits,  # Keep original key name for compatibility
            "codes": actual_codes
        }

    # ==================== WayLookup交互API ====================
    
    async def check_waylookup_request(self, timeout_cycles: int = 10) -> dict:
        """
        Check if WayLookup request is sent
        """
        print(f"Checking WayLookup request, timeout: {timeout_cycles} cycles")
        
        for i in range(timeout_cycles):
            if self.bundle.io._wayLookupWrite._valid.value == 1 and self.bundle.io._wayLookupWrite._ready.value == 1:
                waylookup_info = {
                    "request_sent": True,
                    "vSetIdx_0": self.bundle.io._wayLookupWrite._bits._entry._vSetIdx._0.value,
                    "vSetIdx_1": self.bundle.io._wayLookupWrite._bits._entry._vSetIdx._1.value,
                    "waymask_0": self.bundle.io._wayLookupWrite._bits._entry._waymask._0.value,
                    "waymask_1": self.bundle.io._wayLookupWrite._bits._entry._waymask._1.value,
                    "ptag_0": self.bundle.io._wayLookupWrite._bits._entry._ptag._0.value,
                    "ptag_1": self.bundle.io._wayLookupWrite._bits._entry._ptag._1.value,
                    "exception_0": self.bundle.io._wayLookupWrite._bits._entry._itlb._exception._0.value,
                    "exception_1": self.bundle.io._wayLookupWrite._bits._entry._itlb._exception._1.value,
                    "pbmt_0": self.bundle.io._wayLookupWrite._bits._entry._itlb._pbmt._0.value,
                    "pbmt_1": self.bundle.io._wayLookupWrite._bits._entry._itlb._pbmt._1.value,
                    "meta_codes_0": self.bundle.io._wayLookupWrite._bits._entry._meta_codes._0.value,
                    "meta_codes_1": self.bundle.io._wayLookupWrite._bits._entry._meta_codes._1.value,
                    "gpf_gpaddr": self.bundle.io._wayLookupWrite._bits._gpf._gpaddr.value,
                    "gpf_isForVSnonLeafPTE": self.bundle.io._wayLookupWrite._bits._gpf._isForVSnonLeafPTE.value
                }
                print(f"WayLookup request detected (cycle {i+1})")
                return waylookup_info
            
            await self.bundle.step()
        
        print(f"No WayLookup request detected after {timeout_cycles} cycles")
        return {"request_sent": False}

    async def set_waylookup_ready(self, ready: bool = True):
        """Set WayLookup ready signal"""
        self.bundle.io._wayLookupWrite._ready.value = int(ready)
        print(f"WayLookup ready set to {ready}")

    # ==================== MSHR交互API ====================
    
    async def drive_mshr_response(self,
                                 corrupt: bool = False,
                                 waymask: int = 0,
                                 blkPaddr: int = None,
                                 vSetIdx: int = None) -> dict:
        """
        Drive MSHR response for miss unit feedback
        """
        if blkPaddr is None:
            blkPaddr = random.randint(0, (1<<42)-1)
        if vSetIdx is None:
            vSetIdx = random.randint(0, (1<<8)-1)
            
        print("Driving MSHR response")
        
        self.bundle.io._MSHRResp._valid.value = 1
        self.bundle.io._MSHRResp._bits._corrupt.value = int(corrupt)
        self.bundle.io._MSHRResp._bits._waymask.value = waymask
        self.bundle.io._MSHRResp._bits._blkPaddr.value = blkPaddr
        self.bundle.io._MSHRResp._bits._vSetIdx.value = vSetIdx
        
        await self.bundle.step()
        
        # Read back actual values from DUT before clearing
        actual_corrupt = self.bundle.io._MSHRResp._bits._corrupt.value
        actual_waymask = self.bundle.io._MSHRResp._bits._waymask.value
        actual_blkPaddr = self.bundle.io._MSHRResp._bits._blkPaddr.value
        actual_vSetIdx = self.bundle.io._MSHRResp._bits._vSetIdx.value
        
        return {
            "corrupt": bool(actual_corrupt),
            "waymask": actual_waymask,
            "blkPaddr": actual_blkPaddr,
            "vSetIdx": actual_vSetIdx
        }

    async def clear_mshr_response(self):
        # Clear valid
        self.bundle.io._MSHRResp._valid.value = 0
        await self.bundle.step()

    async def check_mshr_request(self, timeout_cycles: int = 10) -> dict:
        """
        Check if MSHR request is sent to miss unit
        """
        print(f"Checking MSHR request, timeout: {timeout_cycles} cycles")
        
        for i in range(timeout_cycles):
            if self.bundle.io._MSHRReq._valid.value == 1 and self.bundle.io._MSHRReq._ready.value == 1:
                mshr_info = {
                    "request_sent": True,
                    "blkPaddr": self.bundle.io._MSHRReq._bits._blkPaddr.value,
                    "vSetIdx": self.bundle.io._MSHRReq._bits._vSetIdx.value
                }
                print(f"MSHR request detected (cycle {i+1})")
                return mshr_info
            
            await self.bundle.step()
        
        print(f"No MSHR request detected after {timeout_cycles} cycles")
        return {"request_sent": False}

    async def set_mshr_ready(self, ready: bool = True):
        """Set MSHR ready signal"""
        self.bundle.io._MSHRReq._ready.value = int(ready)
        await self.bundle.step()
        print(f"MSHR ready set to {ready}")

    # ==================== 状态查询API ====================
    
    async def get_pipeline_status(self, dut = None) -> dict:
        """
        Get comprehensive pipeline status for all stages (S0, S1, S2)
        Returns detailed information about each pipeline stage including:
        - Valid/Ready signals for each stage
        - Fire signals indicating stage transitions
        - State machine status
        - Flush signals
        - Request acceptance capability
        """
        if dut == None:
            print("!!!!! get pipelineline status need dut to get internal signals! !!!")
            return
        try:
            # S0 Stage - Use bundle signals (already bound)
            s0_fire = bool(self.bundle.IPrefetchPipe._s0._fire.value)
            s0_can_go = bool(self.bundle.IPrefetchPipe._s0._can_go.value)
            s0_flush_probe = bool(self.bundle.IPrefetchPipe._from_bpu_s0_flush_probe.value)
            
            # S1 Stage - Use bundle signals (already bound)
            s1_valid = bool(self.bundle.IPrefetchPipe._s1._valid.value)
            s1_ready = bool(self.bundle.IPrefetchPipe._s1._ready.value)
            s1_flush = bool(self.bundle.IPrefetchPipe._s1._flush.value)
            s1_is_soft_prefetch = bool(self.bundle.IPrefetchPipe._s1._isSoftPrefetch.value)
            s1_doubleline = bool(self.bundle.IPrefetchPipe._s1._doubleline.value)
            
            # S1 Stage - Additional signals via GetInternalSignal
            s1_fire = None
            try:
                s1_fire = bool(dut.GetInternalSignal("IPrefetchPipe_top.IPrefetchPipe.s1_fire", use_vpi=False).value)
            except:
                print("s1 fire signals can not access.")
                return
            # S2 Stage - Use GetInternalSignal (not bound in bundle)
            s2_valid = None
            s2_ready = None
            s2_fire = None
            s2_finish = None
            try:
                s2_valid = bool(dut.GetInternalSignal("IPrefetchPipe_top.IPrefetchPipe.s2_valid", use_vpi=False).value)
                s2_ready = bool(dut.GetInternalSignal("IPrefetchPipe_top.IPrefetchPipe.s2_ready", use_vpi=False).value)
                s2_fire = bool(dut.GetInternalSignal("IPrefetchPipe_top.IPrefetchPipe.s2_fire", use_vpi=False).value)
                s2_finish = bool(dut.GetInternalSignal("IPrefetchPipe_top.IPrefetchPipe.s2_finish", use_vpi=False).value)
            except:
                print("some s2 signals can not access.")
                return
            
            # State Machine - Use bundle signal
            state_value = int(self.bundle.IPrefetchPipe._state.value)
            state_name = {
                0: "m_idle",
                1: "m_itlbResend", 
                2: "m_metaResend",
                3: "m_enqWay",
                4: "m_enterS2"
            }.get(state_value, f"unknown_{state_value}")
            
            # Global Control Signals - Use bundle signals
            global_flush = bool(self.bundle.io._flush.value)
            csr_pf_enable = bool(self.bundle.io._csr_pf_enable.value)
            itlb_flush_pipe = bool(self.bundle.io._itlbFlushPipe.value)
            
            # Request Interface - Use bundle signals
            req_valid = bool(self.bundle.io._req._valid.value)
            req_ready = bool(self.bundle.io._req._ready.value)
            
            # BPU Flush Signals - Use bundle signals
            bpu_s2_flush = bool(self.bundle.io._flushFromBpu._s2._valid.value)
            bpu_s3_flush = bool(self.bundle.io._flushFromBpu._s3._valid.value)
            
            return {
                # S0 Stage Status
                "s0": {
                    "fire": s0_fire,
                    "can_go": s0_can_go,
                    "bpu_flush_probe": s0_flush_probe,
                    "ready_to_accept": req_ready and not global_flush
                },
                
                # S1 Stage Status  
                "s1": {
                    "valid": s1_valid,
                    "ready": s1_ready,
                    "fire": s1_fire,
                    "flush": s1_flush,
                    "is_soft_prefetch": s1_is_soft_prefetch,
                    "doubleline": s1_doubleline
                },
                
                # S2 Stage Status
                "s2": {
                    "valid": s2_valid,
                    "ready": s2_ready, 
                    "fire": s2_fire,
                    "finish": s2_finish
                },
                
                # State Machine
                "state_machine": {
                    "current_state": state_name,
                    "state_value": state_value
                },
                
                # Global Control
                "control": {
                    "global_flush": global_flush,
                    "csr_pf_enable": csr_pf_enable,
                    "itlb_flush_pipe": itlb_flush_pipe,
                    "req_valid": req_valid,
                    "req_ready": req_ready
                },
                
                # BPU Flush Status
                "bpu_flush": {
                    "stage2": bpu_s2_flush,
                    "stage3": bpu_s3_flush
                },
                
                # Pipeline Activity Summary
                "summary": {
                    "pipeline_active": s1_valid or (s2_valid if s2_valid is not None else False),
                    "accepting_requests": req_ready and not global_flush,
                    "any_stage_flushing": global_flush or s1_flush or s0_flush_probe,
                    "state_machine_idle": state_value == 0
                }
            }
            
        except Exception as e:
            # Error fallback - return basic status
            return {
                "error": f"Failed to read pipeline status: {str(e)}",
                "basic_status": {
                    "req_ready": bool(self.bundle.io._req._ready.value) if hasattr(self.bundle.io._req, '_ready') else False,
                    "req_valid": bool(self.bundle.io._req._valid.value) if hasattr(self.bundle.io._req, '_valid') else False,
                    "global_flush": bool(self.bundle.io._flush.value) if hasattr(self.bundle.io, '_flush') else False
                }
            }

    # ==================== 辅助验证API ====================
    
    async def setup_environment(self, prefetch_enable: bool = True):
        """
        Setup basic environment for testing
        
        Args:
            prefetch_enable: Whether to enable prefetch functionality
        """
        print("Setting up IPrefetchPipe test environment...")
        
        # Reset DUT
        await self.reset_dut()
        
        # Set prefetch enable
        await self.set_prefetch_enable(prefetch_enable)
        
        # Set basic ready signals
        self.bundle.io._metaRead._toIMeta._ready.value = 1
        self.bundle.io._wayLookupWrite._ready.value = 1
        self.bundle.io._MSHRReq._ready.value = 1
        
        # Clear flush signals
        self.bundle.io._flush.value = 0
        self.bundle.io._flushFromBpu._s2._valid.value = 0
        self.bundle.io._flushFromBpu._s2._bits._flag.value = 0
        self.bundle.io._flushFromBpu._s2._bits._value.value = 0
        self.bundle.io._flushFromBpu._s3._valid.value = 0
        self.bundle.io._flushFromBpu._s3._bits._flag.value = 0
        self.bundle.io._flushFromBpu._s3._bits._value.value = 0
        self.bundle.io._itlb._0._resp_bits._excp._0._af_instr.value = 0
        self.bundle.io._itlb._0._resp_bits._excp._0._pf_instr.value = 0
        self.bundle.io._itlb._0._resp_bits._excp._0._gpf_instr.value = 0
        self.bundle.io._MSHRResp._valid.value = 0
        
        await self.bundle.step(2)
        print(f"Environment setup completed (prefetch_enable={prefetch_enable})")

    async def wait_for_condition(self, condition_func, timeout_cycles: int = 100) -> bool:
        """Wait for a custom condition to be true"""
        for _ in range(timeout_cycles):
            if await condition_func():
                return True
            await self.bundle.step()
        return False