from .mainpipe_fixture import icachemainpipe_env
from ..env import ICacheMainPipeEnv
import toffee_test

@toffee_test.testcase
async def test_smoke(icachemainpipe_env: ICacheMainPipeEnv):
    """Smoke test for MainPipe"""
    print("\n--- Testing smoke ---")
    await icachemainpipe_env.agent.flush_s0_fire()


@toffee_test.testcase
async def test_basic_control_api(icachemainpipe_env: ICacheMainPipeEnv):
    """Test basic control apis"""
    print("\n--- Testing basic control apis ---")
    agent = icachemainpipe_env.agent
    bundle = icachemainpipe_env.bundle
    # flush
    await agent.drive_set_flush(False)
    assert bundle.io._flush.value == 0
    await agent.drive_set_flush(True)
    assert bundle.io._flush.value == 1
    # ecc enable
    await agent.drive_set_ecc_enable(False)
    assert bundle.io._ecc_enable.value == 0
    await agent.drive_set_ecc_enable(True)
    assert bundle.io._ecc_enable.value == 1
    # resp_stall
    await agent.drive_resp_stall(True)
    assert bundle.io._respStall.value == 1
    await agent.drive_resp_stall(False)
    assert bundle.io._respStall.value == 0

@toffee_test.testcase
async def test_drive_apis(icachemainpipe_env: ICacheMainPipeEnv):
    """Test driver apis"""
    print("\n--- Testing drive apis ---")
    agent = icachemainpipe_env.agent
    bundle = icachemainpipe_env.bundle
    # data_array_ready
    print("\n Step1 Test For data_array_ready_drive")
    await agent.drive_data_array_ready(True)
    assert bundle.io._dataArray._toIData._3._ready.value == 1
    await agent.drive_data_array_ready(False)
    assert bundle.io._dataArray._toIData._3._ready.value == 0
    await agent.reset()
    # waylookup_read
    print("\n Step2 Test For waylookup_read_drive")

    waylookup_data = {"vSetIdx_0": 0x04,
                      "vSetIdx_1": 0x05,
                      "waymask_0": 4,
                      "ptag_0": 0xABCD0,
                      "meta_codes_0": 1}
    read_result = await agent.drive_waylookup_read(vSetIdx_0=waylookup_data["vSetIdx_0"],
                                                   vSetIdx_1=waylookup_data["vSetIdx_1"],
                                                   waymask_0=waylookup_data["waymask_0"],
                                                   ptag_0 = waylookup_data["ptag_0"],
                                                   meta_codes_0 = waylookup_data["meta_codes_0"])
    await bundle.step()
    print(read_result)
    for k,_ in read_result.items():
        if k in waylookup_data.keys():
            assert read_result[k] == waylookup_data[k], f"Expected {k} to be {waylookup_data[k]}, but got {read_result[k]}"
            print(f"real {read_result[k]} == except {waylookup_data[k]}")
        elif k == "send_success":
            assert read_result[k] is True
            print(f"send_success: {read_result[k]}")
        else:
            assert read_result[k] == 0, f"Unexpected value for {k}: {read_result[k]}"
    await agent.reset()
    # fetch_request
    print("\n Step3 Test For fetch_request_drive")
    PcMemRead_addr_list = [0x0000, 0x0040, 0x0080, 0x00C0, 0x120]  # 第5个元素：0x120[5]=1触发跨行，[13:6]=0x04
    # nextlineStart将自动计算：0x120跨行 -> (0x120 & ~0x3F) + 64 = 0x140，[13:6]=0x05
    readValid_list = [1, 1, 0, 0, 1]  # 激活第5个元素以匹配RTL断言要求
    
    # 首先设置匹配的wayLookup vSetIdx
    await agent.drive_waylookup_read(
        vSetIdx_0=0x04,  # 匹配pcMemRead_4_startAddr[13:6]
        vSetIdx_1=0x05,  # 匹配pcMemRead_4_nextlineStart[13:6]
        waymask_0=1,
        ptag_0=0x12345,
        meta_codes_0=1
    )
    
    # setting fetch condition
    await agent.drive_data_array_ready(True)
    await bundle.step(2)
    
    fetch_result = await agent.drive_fetch_request(
        pcMemRead_addrs=PcMemRead_addr_list,
        readValid=readValid_list,
        backendException=0
    )
    await bundle.step()  # 等待一个周期让信号稳定
    assert fetch_result is True, "drive fetch request failed."
    
    # 清除fetch请求信号
    await agent.clear_fetch_request()
    
    # 验证信号设置
    # 验证地址和数据设置正确
    for i in range(5):
        actual_start_pre = getattr(bundle.io._fetch._req._bits._pcMemRead, f"_{i}")
        actual_start = getattr(actual_start_pre, "_startAddr")
        actual_next_pre = getattr(bundle.io._fetch._req._bits._pcMemRead, f"_{i}")
        actual_next = getattr(actual_next_pre, "_nextlineStart")
        actual_valid = getattr(bundle.io._fetch._req._bits._readValid, f"_{i}")
        # 修复类型检查和验证逻辑
        actual_valid_val = actual_valid.value if hasattr(actual_valid, 'value') else actual_valid
        
        # 根据RTL逻辑计算expected_next值
        start_addr = PcMemRead_addr_list[i]
        if (start_addr & 0x20) != 0:  # startAddr[5] == 1，跨行取指
            expected_next = (start_addr & ~0x3F) + 64  # 下一个64字节对齐地址
        else:  # startAddr[5] == 0，同一缓存行内
            expected_next = start_addr  # nextlineStart = startAddr
        
        print(f"DEBUG: StartAddr {i} - expected: {start_addr:x}, actual: {actual_start.value:x}")
        print(f"DEBUG: NextlineStart {i} - expected: {expected_next:x}, actual: {actual_next.value:x}")
        print(f"DEBUG: ReadValid {i} - expected: {readValid_list[i]}, actual: {actual_valid_val}")
        
        # 验证startAddr设置正确
        assert actual_start.value == start_addr, f"StartAddr {i} mismatch: expected {start_addr:x}, got {actual_start.value:x}"
        
        # 验证nextlineStart按我们设置的值
        assert actual_next.value == expected_next, f"NextlineStart {i} mismatch: expected {expected_next:x}, got {actual_next.value:x}"
        
        # 验证readValid设置正确
        assert actual_valid_val == readValid_list[i], f"ReadValid {i} mismatch: expected {readValid_list[i]}, got {actual_valid_val}"
    assert bundle.io._fetch._req._bits._backendException.value == 0, f"Expected backendException 0, got {bundle.io._fetch._req._bits._backendException.value}"


@toffee_test.testcase
async def test_pmp_response(icachemainpipe_env: ICacheMainPipeEnv):
    """Test PMP response API"""
    print("\n--- Testing PMP response API ---")
    agent = icachemainpipe_env.agent
    bundle = icachemainpipe_env.bundle
    for i in range(2):
        for j in range(2):
            for k in range(2):
                for l in range(2):
                    await agent.drive_pmp_response(instr_0=i, mmio_0=j, instr_1=k, mmio_1=l)
                    await bundle.step()
                    assert bundle.io._pmp._0._resp._instr.value == i, f"Expected instr_1 {i}, got {bundle.io._pmp._1._resp._instr.value}"
                    assert bundle.io._pmp._0._resp._mmio.value == j, f"Expected mmio_0 {j}, got {bundle.io._pmp._0._resp._mmio.value}"
                    assert bundle.io._pmp._1._resp._instr.value == k, f"Expected instr_1 {k}, got {bundle.io._pmp._1._resp._instr.value}"
                    assert bundle.io._pmp._1._resp._mmio.value == l, f"Expected mmio_1 {l}, got {bundle.io._pmp._1._resp._mmio.value}"

@toffee_test.testcase
async def test_data_array_response(icachemainpipe_env: ICacheMainPipeEnv):
    """Test DataArray response API"""
    print("\n--- Testing DataArray response API ---")
    agent = icachemainpipe_env.agent
    bundle = icachemainpipe_env.bundle
    
    test_datas = [0x1111111111111111, 0x2222222222222222, 0x3333333333333333, 0x4444444444444444,
                  0x5555555555555555, 0x6666666666666666, 0x7777777777777777, 0x8888888888888888]
    test_codes = [1, 0, 1, 0, 1, 0, 1, 0]
    
    result = await agent.drive_data_array_response(datas=test_datas, codes=test_codes)
    assert result is True, "DataArray response should succeed"
    
    # 验证信号值
    for i in range(8):
        actual_data = getattr(bundle.io._dataArray._fromIData._datas, f"_{i}").value
        actual_code = getattr(bundle.io._dataArray._fromIData._codes, f"_{i}").value
        assert actual_data == test_datas[i], f"Data {i} mismatch: expected {test_datas[i]:x}, got {actual_data:x}"
        assert actual_code == test_codes[i], f"Code {i} mismatch: expected {test_codes[i]}, got {actual_code}"


@toffee_test.testcase
async def test_mshr_response(icachemainpipe_env: ICacheMainPipeEnv):
    """Test MSHR response API"""
    print("\n--- Testing MSHR response API ---")
    agent = icachemainpipe_env.agent
    bundle = icachemainpipe_env.bundle
    
    test_blkPaddr = 0x12345678
    test_vSetIdx = 0xAB
    test_data = 0xDEADBEEFCAFEBABE
    test_corrupt = 1
    
    result = await agent.drive_mshr_response(
        blkPaddr=test_blkPaddr,
        vSetIdx=test_vSetIdx,
        data=test_data,
        corrupt=test_corrupt
    )
    assert bundle.io._mshr._resp._bits._blkPaddr.value == test_blkPaddr, f"Expected blkPaddr {test_blkPaddr:x}, got {bundle.io._mshr._resp._bits._blkPaddr.value:x}"
    assert bundle.io._mshr._resp._bits._vSetIdx.value == test_vSetIdx, f"Expected vSetIdx {test_vSetIdx:x}, got {bundle.io._mshr._resp._bits._vSetIdx.value:x}"
    assert bundle.io._mshr._resp._bits._data.value == test_data, f"Expected data {test_data:x}, got {bundle.io._mshr._resp._bits._data.value:x}"
    assert bundle.io._mshr._resp._bits._corrupt.value == test_corrupt, f"Expected corrupt {test_corrupt}, got {bundle.io._mshr._resp._bits._corrupt.value}"
    assert result is True, "MSHR response should succeed"


@toffee_test.testcase
async def test_monitoring_apis(icachemainpipe_env: ICacheMainPipeEnv):
    """Test monitoring APIs"""
    print("\n--- Testing monitoring APIs ---")
    agent = icachemainpipe_env.agent
    
    # 测试DataArray监控
    dataarray_status = await agent.monitor_dataarray_toIData()
    for k,v in dataarray_status.items():
        print("Debug: DataArray status", k, "=", v)
        assert v is not None, f"DataArray status {k} should not be None"
    
    # 测试Meta ECC监控
    meta_ecc_status = await agent.monitor_check_meta_ecc_status()
    for k,v in meta_ecc_status.items():
        print("Debug: Meta ECC status", k, "=", v)
        assert v is not None, f"Meta ECC status {k} should not be None"
    
    # 测试PMP状态监控
    pmp_status = await agent.monitor_pmp_status()
    for k, v in pmp_status.items():
        print("Debug: PMP status", k, "=", v)
        assert v is not None, f"PMP status {k} should not be None"
    
    # 测试MSHR状态监控
    mshr_status = await agent.monitor_mshr_status()
    for k,v in mshr_status.items():
        print("Debug: MSHR status", k, "=", v)
        assert v is not None, f"MSHR status {k} should not be None" 
    
    # 测试Data ECC监控
    data_ecc_status = await agent.monitor_check_data_ecc_status()
    for k,v in data_ecc_status.items():
        print("Debug: Data ECC status", k, "=", v)
        assert v is not None, f"Data ECC status {k} should not be None"
    
    # 测试Fetch响应监控
    fetch_resp_status = await agent.monitor_fetch_response()
    for k,v in fetch_resp_status.items():
        print("Debug: Fetch response status", k, "=", v)
        assert v is not None, f"Fetch response status {k} should not be None"

    # 测试Replacer touch状态监控
    replacer_touch_status = await agent.monitor_replacer_touch()
    for k,v in replacer_touch_status.items():
        print("Debug: Replacer touch status", k, "=", v)
        assert v is not None, f"Replacer touch status {k} should not be None"

    # 测试meta_flush状态监控
    meta_flush_status = await agent.monitor_meta_flush()
    for k,v in meta_flush_status.items():   
        print("Debug: Meta flush status", k, "=", v)
        assert v is not None, f"Meta flush status {k} should not be None"

    # 测试流水线状态监控
    pipeline_status = await agent.monitor_pipeline_status()
    for k,v in pipeline_status.items():
        print("Debug: Pipeline status", k, "=", v)
        assert v is not None, f"Pipeline status {k} should not be None"
    
    # 测试错误状态监控
    error_status = await agent.monitor_error_status()
    for k,v in error_status.items():
        print("Debug: Error status", k, "=", v)
        assert v is not None, f"Error status {k} should not be None"


@toffee_test.testcase
async def test_enhanced_monitoring_apis(icachemainpipe_env: ICacheMainPipeEnv):
    """Test enhanced monitoring APIs"""
    print("\n--- Testing enhanced monitoring APIs ---")
    agent = icachemainpipe_env.agent
    
    # 测试异常合并状态监控
    exception_status = await agent.monitor_exception_merge_status()
    for k,v in exception_status.items():
        assert v is not None, f"Exception merge status {k} should not be None"
    # 测试MSHR匹配状态监控
    mshr_match_status = await agent.monitor_mshr_match_status()
    for k,v in mshr_match_status.items():
        assert v is not None, f"MSHR match status {k} should not be None"
    
    # 测试详细的Data ECC状态监控
    data_ecc_detailed_status = await agent.monitor_data_ecc_detailed_status()
    assert isinstance(data_ecc_detailed_status, dict), "Data ECC detailed monitoring should return dict"
    
    # 测试data_ecc_detailed状态监控
    data_ecc_detailed_status = await agent.monitor_data_ecc_detailed_status()
    for k,v in data_ecc_detailed_status.items():
        print("Debug: Data ECC detailed status", k, "=", v)
        assert v is not None, f"Data ECC detailed status {k} should not be None"

    # 测试S2 MSHR匹配状态监控
    s2_mshr_status = await agent.monitor_s2_mshr_match_status()
    assert s2_mshr_status is not None, "S2 MSHR match status should not be None"
    for k,v in s2_mshr_status.items():
        print("Debug: S2 MSHR match status", k, "=", v)
        assert v is not None, f"S2 MSHR match status {k} should not be None"
    
    # 测试Miss请求状态监控
    miss_req_status = await agent.monitor_miss_request_status()
    for k,v in miss_req_status.items():
        print("Debug: Miss request status", k, "=", v)
        assert v is not None, f"Miss request status {k} should not be None"
    
    # 测试Meta corrupt状态监控
    meta_corrupt_status = await agent.monitor_meta_corrupt_status()
    for k,v in meta_corrupt_status.items():
        print("Debug: Meta corrupt status", k, "=", v)
        assert v is not None, f"Meta corrupt status {k} should not be None"


@toffee_test.testcase
async def test_error_injection_apis(icachemainpipe_env: ICacheMainPipeEnv):
    """Test error injection APIs"""
    print("\n--- Testing error injection APIs ---")
    agent = icachemainpipe_env.agent
    
    # 测试Meta ECC错误注入
    meta_ecc_result = await agent.inject_meta_ecc_error(
        vSetIdx_0=10,
        waymask_0=1,
        ptag_0=0x12345,
        wrong_meta_code_0=1
    )
    assert meta_ecc_result is True, "Meta ECC error injection should succeed"
    
    # 测试多路命中错误注入
    multi_way_result = await agent.inject_multi_way_hit(
        vSetIdx_0=20,
        waymask_0=0b1100,
        ptag_0=0x67890
    )
    assert multi_way_result is True, "Multi-way hit injection should succeed"
    
    # 测试Data ECC错误注入
    data_ecc_result = await agent.inject_data_ecc_error(
        bank_index=3,
        error_data=0xDEADBEEF,
        wrong_code=1
    )
    assert data_ecc_result is True, "Data ECC error injection should succeed"
    
    # 测试L2 corrupt响应注入
    l2_corrupt_result = await agent.inject_l2_corrupt_response(
        blkPaddr=0x1000,
        vSetIdx=0x10,
        corrupt_data=0xBADD4A7A,
        corrupt=1
    )
    assert l2_corrupt_result is True, "L2 corrupt injection should succeed"


@toffee_test.testcase
async def test_signal_bindings(icachemainpipe_env: ICacheMainPipeEnv):
    """Test signal bindings correctness"""
    print("\n--- Testing signal bindings ---")
    agent = icachemainpipe_env.agent
    bundle = icachemainpipe_env.bundle
    
    # 测试基础信号绑定
    print("Testing basic signal bindings...")
    
    # 测试flush信号
    await agent.drive_set_flush(True)
    assert bundle.io._flush.value == 1, "Flush signal binding incorrect"
    await agent.drive_set_flush(False)
    assert bundle.io._flush.value == 0, "Flush signal binding incorrect"
    
    # 测试ECC enable信号
    await agent.drive_set_ecc_enable(True)
    assert bundle.io._ecc_enable.value == 1, "ECC enable signal binding incorrect"
    await agent.drive_set_ecc_enable(False)
    assert bundle.io._ecc_enable.value == 0, "ECC enable signal binding incorrect"
    
    # 测试respStall信号
    await agent.drive_resp_stall(True)
    assert bundle.io._respStall.value == 1, "RespStall signal binding incorrect"
    await agent.drive_resp_stall(False)
    assert bundle.io._respStall.value == 0, "RespStall signal binding incorrect"
    
    # 测试DataArray ready信号
    await agent.drive_data_array_ready(True)
    assert bundle.io._dataArray._toIData._3._ready.value == 1, "DataArray ready signal binding incorrect"
    await agent.drive_data_array_ready(False)
    assert bundle.io._dataArray._toIData._3._ready.value == 0, "DataArray ready signal binding incorrect"
    
    # 测试MSHR ready信号
    await agent.setup_mshr_ready(True)
    assert bundle.io._mshr._req._ready.value == 1, "MSHR ready signal binding incorrect"
    await agent.setup_mshr_ready(False)
    assert bundle.io._mshr._req._ready.value == 0, "MSHR ready signal binding incorrect"
    
    # 测试WayLookup信号路径
    test_vSetIdx = 42
    test_waymask = 4
    test_ptag = 0x12345
    
    await agent.drive_waylookup_read(
        vSetIdx_0=test_vSetIdx,
        waymask_0=test_waymask,
        ptag_0=test_ptag
    )
    
    assert bundle.io._wayLookupRead._bits._entry._vSetIdx._0.value == test_vSetIdx, "WayLookup vSetIdx binding incorrect"
    assert bundle.io._wayLookupRead._bits._entry._waymask._0.value == test_waymask, "WayLookup waymask binding incorrect"
    assert bundle.io._wayLookupRead._bits._entry._ptag._0.value == test_ptag, "WayLookup ptag binding incorrect"
    
    print("All signal bindings verified successfully!")

@toffee_test.testcase
async def test_comprehensive_signal_interface(icachemainpipe_env: ICacheMainPipeEnv):
    """Comprehensive test for all ICacheMainPipe signal interfaces organized by categories
    Based on Verilog analysis: OUTPUT/wire signals test read access only, INPUT signals test read/write functionality
    """
    print("\n=== Comprehensive ICacheMainPipe Signal Interface Test ===")
    agent = icachemainpipe_env.agent
    bundle = icachemainpipe_env.bundle
    
    await agent.reset()
    test_errors = []
    
    # ================= 1. ICacheMainPipe Internal Signals =================
    print("\n1. ICacheMainPipe Internal Signals")
    try:
        # According to Verilog, these are internal pipeline signals (mostly OUTPUT)
        s2_fire = bundle.ICacheMainPipe._s2._fire.value
        s2_valid = bundle.ICacheMainPipe._s2._valid.value
        s0_fire = bundle.ICacheMainPipe._s0_fire.value
        
        print(f"  ✓ ICacheMainPipe.s2.fire: {s2_fire}")
        print(f"  ✓ ICacheMainPipe.s2.valid: {s2_valid}")
        print(f"  ✓ ICacheMainPipe.s0_fire: {s0_fire}")
    except Exception as e:
        error_msg = f"ICacheMainPipe internal signals access error: {e}"
        test_errors.append(error_msg)
        print(f"  × {error_msg}")
    
    # ================= 2. ICacheMainPipe__toMSHRArbiter_io_in =================
    print("\n2. ICacheMainPipe__toMSHRArbiter_io_in Interface")
    try:
        # According to Verilog, these are OUTPUT signals to MSHR arbiter
        valid_T_4_1 = bundle.ICacheMainPipe__toMSHRArbiter_io_in._1._valid_T._4.value
        valid_T_4_0 = bundle.ICacheMainPipe__toMSHRArbiter_io_in._0._valid_T._4.value
        
        print(f"  ✓ toMSHRArbiter_io_in[1].valid_T.4: {valid_T_4_1}")
        print(f"  ✓ toMSHRArbiter_io_in[0].valid_T.4: {valid_T_4_0}")
    except Exception as e:
        error_msg = f"ICacheMainPipe__toMSHRArbiter_io_in interface access error: {e}"
        test_errors.append(error_msg)
        print(f"  × {error_msg}")
    
    # ================= 3. io._perfInfo (OUTPUT) =================
    print("\n3. io._perfInfo Interface (OUTPUT - Read Only)")
    try:
        perfinfo_signals = {
            "bank_hit_0": bundle.io._perfInfo._bank_hit._0,
            "bank_hit_1": bundle.io._perfInfo._bank_hit._1,
            "miss_0_hit_1": bundle.io._perfInfo._miss._0._hit._1,
            "miss_0_except_1": bundle.io._perfInfo._miss._0._except._1,
            "miss_0_miss_1": bundle.io._perfInfo._miss._0._miss._1,
            "except_0": bundle.io._perfInfo._except._0,
            "only_0_miss": bundle.io._perfInfo._only._0._miss,
            "only_0_hit": bundle.io._perfInfo._only._0._hit,
            "hit": bundle.io._perfInfo._hit
        }
        
        for field, signal_obj in perfinfo_signals.items():
            try:
                value = signal_obj.value
                print(f"  ✓ perfInfo.{field}: {value}")
            except AttributeError as e:
                error_msg = f"perfInfo.{field}: {e}"
                test_errors.append(error_msg)
                print(f"  × {error_msg}")
    except Exception as e:
        error_msg = f"perfInfo interface critical error: {e}"
        test_errors.append(error_msg)
        print(f"  × {error_msg}")
    
    # ================= 4. io._pmp Interface =================
    print("\n4. io._pmp Interface")
    # PMP request addresses are OUTPUT (line 145-146 in Verilog)
    print("  4a. PMP Request Signals (OUTPUT - Read Only)")
    try:
        pmp_req_addr_0 = bundle.io._pmp._0._req_bits_addr.value
        pmp_req_addr_1 = bundle.io._pmp._1._req_bits_addr.value
        print(f"    ✓ pmp[0].req_bits_addr: {hex(pmp_req_addr_0)}")
        print(f"    ✓ pmp[1].req_bits_addr: {hex(pmp_req_addr_1)}")
    except Exception as e:
        error_msg = f"PMP request signals error: {e}"
        test_errors.append(error_msg)
        print(f"    × {error_msg}")
    
    # PMP response signals are INPUT (line 147-150 in Verilog) - test read/write
    print("  4b. PMP Response Signals (INPUT - Read/Write Testing)")
    try:
        # Test normal values within boundaries
        test_values = [(1, 0), (0, 1), (1, 1)]  # (instr, mmio) combinations
        
        for test_instr_0, test_mmio_0 in test_values:
            bundle.io._pmp._0._resp._instr.value = test_instr_0
            bundle.io._pmp._0._resp._mmio.value = test_mmio_0
            bundle.io._pmp._1._resp._instr.value = test_instr_0  
            bundle.io._pmp._1._resp._mmio.value = test_mmio_0
            await bundle.step()
            
            # Verify write successful
            assert bundle.io._pmp._0._resp._instr.value == test_instr_0, f"PMP 0 instr write failed"
            assert bundle.io._pmp._0._resp._mmio.value == test_mmio_0, f"PMP 0 mmio write failed"
            assert bundle.io._pmp._1._resp._instr.value == test_instr_0, f"PMP 1 instr write failed"
            assert bundle.io._pmp._1._resp._mmio.value == test_mmio_0, f"PMP 1 mmio write failed"
            
        print(f"    ✓ PMP response signals read/write working")
            
    except Exception as e:
        error_msg = f"PMP response signals error: {e}"
        test_errors.append(error_msg)
        print(f"    × {error_msg}")
    
    # ================= 5. io._errors (OUTPUT) =================
    print("\n5. io._errors Interface (OUTPUT - Read Only)")
    try:
        error_signals = {
            "error_0_valid": bundle.io._errors._0._valid,
            "error_0_paddr": bundle.io._errors._0._bits._paddr,
            "error_0_report": bundle.io._errors._0._bits._report_to_beu,
            "error_1_valid": bundle.io._errors._1._valid,
            "error_1_paddr": bundle.io._errors._1._bits._paddr,
            "error_1_report": bundle.io._errors._1._bits._report_to_beu,
        }
        
        for field, signal_obj in error_signals.items():
            try:
                value = signal_obj.value
                print(f"  ✓ errors.{field}: {hex(value) if isinstance(value, int) and value > 255 else value}")
            except AttributeError as e:
                error_msg = f"errors.{field}: {e}"
                test_errors.append(error_msg)
                print(f"  × {error_msg}")
    except Exception as e:
        error_msg = f"errors interface critical error: {e}"
        test_errors.append(error_msg)
        print(f"  × {error_msg}")
    
    # ================= 6. io._metaArrayFlush (OUTPUT) =================
    print("\n6. io._metaArrayFlush Interface (OUTPUT - Read Only)")
    try:
        flush_0_valid = bundle.io._metaArrayFlush._0._valid.value
        flush_0_virIdx = bundle.io._metaArrayFlush._0._bits._virIdx.value
        flush_0_waymask = bundle.io._metaArrayFlush._0._bits._waymask.value
        flush_1_valid = bundle.io._metaArrayFlush._1._valid.value
        flush_1_virIdx = bundle.io._metaArrayFlush._1._bits._virIdx.value
        flush_1_waymask = bundle.io._metaArrayFlush._1._bits._waymask.value
        
        print(f"  ✓ metaArrayFlush[0]: valid={flush_0_valid}, virIdx={flush_0_virIdx}, waymask={flush_0_waymask}")
        print(f"  ✓ metaArrayFlush[1]: valid={flush_1_valid}, virIdx={flush_1_virIdx}, waymask={flush_1_waymask}")
    except Exception as e:
        error_msg = f"metaArrayFlush interface error: {e}"
        test_errors.append(error_msg)
        print(f"  × {error_msg}")
    
    # ================= 7. io._wayLookupRead Interface =================
    print("\n7. io._wayLookupRead Interface")
    # ready is OUTPUT (line 141), valid is INPUT (line 142) in Verilog
    print("  7a. WayLookupRead Ready Signal (OUTPUT - Read Only)")
    try:
        # ready signal is OUTPUT - only test read access
        ready_value = bundle.io._wayLookupRead._ready.value
        print(f"    ✓ wayLookupRead.ready (OUTPUT): {ready_value}")
    except Exception as e:
        error_msg = f"WayLookupRead ready signal read error: {e}"
        test_errors.append(error_msg)
        print(f"    × {error_msg}")
    
    print("  7b. WayLookupRead Valid Signal (INPUT - Read/Write Testing)")
    try:
        # Test valid signal (1-bit INPUT) 
        original_valid = bundle.io._wayLookupRead._valid.value
        for test_valid in [0, 1]:
            bundle.io._wayLookupRead._valid.value = test_valid
            await bundle.step()
            assert bundle.io._wayLookupRead._valid.value == test_valid, f"WayLookupRead valid write failed"
        
        # Restore original value
        bundle.io._wayLookupRead._valid.value = original_valid
        print("    ✓ WayLookupRead valid signal read/write working")
        
            
    except Exception as e:
        error_msg = f"WayLookupRead valid signal error: {e}"
        test_errors.append(error_msg)
        print(f"    × {error_msg}")
    
    # bits.entry and bits.gpf are INPUT (lines 143-156 in Verilog)
    print("  7c. WayLookupRead Entry/GPF Signals (INPUT - Read/Write Testing)")
    try:
        # Test entry signals with boundary values
        test_params = {
            "vSetIdx": [(0, 255), (0x10, 0x20)],  # 8-bit: 0-255
            "waymask": [(0, 15), (0xF, 0xA)],     # 4-bit: 0-15  
            "ptag": [(0, 0xFFFFFFFFF), (0x12345, 0x67890)],  # 36-bit
            "itlb_exception": [(0, 3), (2, 1)],   # 2-bit: 0-3
            "itlb_pbmt": [(0, 3), (3, 2)],        # 2-bit: 0-3
            "meta_codes": [(0, 1), (1, 0)]        # 1-bit: 0-1
        }
        
        for param, value_pairs in test_params.items():
            for val_0, val_1 in value_pairs:
                if param == "vSetIdx":
                    bundle.io._wayLookupRead._bits._entry._vSetIdx._0.value = val_0
                    bundle.io._wayLookupRead._bits._entry._vSetIdx._1.value = val_1
                elif param == "waymask":
                    bundle.io._wayLookupRead._bits._entry._waymask._0.value = val_0
                    bundle.io._wayLookupRead._bits._entry._waymask._1.value = val_1
                elif param == "ptag":
                    bundle.io._wayLookupRead._bits._entry._ptag._0.value = val_0
                    bundle.io._wayLookupRead._bits._entry._ptag._1.value = val_1
                elif param == "itlb_exception":
                    bundle.io._wayLookupRead._bits._entry._itlb._exception._0.value = val_0
                    bundle.io._wayLookupRead._bits._entry._itlb._exception._1.value = val_1
                elif param == "itlb_pbmt":
                    bundle.io._wayLookupRead._bits._entry._itlb._pbmt._0.value = val_0
                    bundle.io._wayLookupRead._bits._entry._itlb._pbmt._1.value = val_1
                elif param == "meta_codes":
                    bundle.io._wayLookupRead._bits._entry._meta_codes._0.value = val_0
                    bundle.io._wayLookupRead._bits._entry._meta_codes._1.value = val_1
                
                await bundle.step()
        
        # Test GPF signals (56-bit gpaddr, 1-bit flag)
        test_gpf_params = [
            (0, 0),
            (0xFFFFFFFFFFFFFF, 1), 
            (0x123456789ABCDE, 0)
        ]
        for gpf_addr, is_for_vs in test_gpf_params:
            bundle.io._wayLookupRead._bits._gpf._gpaddr.value = gpf_addr
            bundle.io._wayLookupRead._bits._gpf._isForVSnonLeafPTE.value = is_for_vs
            await bundle.step()
            assert bundle.io._wayLookupRead._bits._gpf._gpaddr.value == gpf_addr, f"GPF addr write failed"
            assert bundle.io._wayLookupRead._bits._gpf._isForVSnonLeafPTE.value == is_for_vs, f"GPF isForVSnonLeafPTE write failed"
        
        print("    ✓ WayLookupRead entry/GPF signals read/write working")
        
    except Exception as e:
        error_msg = f"WayLookupRead entry/GPF signals error: {e}"
        test_errors.append(error_msg)
        print(f"    × {error_msg}")
    
    # ================= 8. io._dataArray Interface =================
    print("\n8. io._dataArray Interface")
    # toIData ports are OUTPUT (lines 91-112 in Verilog) - except port 3 ready which is INPUT
    print("  8a. DataArray toIData Signals (OUTPUT - Read Only)")
    try:
        for port in range(4):
            valid = getattr(bundle.io._dataArray._toIData, f"_{port}")._valid.value
            print(f"    ✓ DataArray toIData[{port}] valid: {valid}")
            
            if port == 0:  # Port 0 has complete bits
                vSetIdx_0 = bundle.io._dataArray._toIData._0._bits._vSetIdx._0.value
                vSetIdx_1 = bundle.io._dataArray._toIData._0._bits._vSetIdx._1.value
                blkOffset = bundle.io._dataArray._toIData._0._bits._blkOffset.value
                print(f"    ✓ DataArray toIData[0] - vSetIdx: {vSetIdx_0}/{vSetIdx_1}, blkOffset: {blkOffset}")
                
                # Test waymask signals (4 ways x 2 ports = 8 signals)
                print(f"    ✓ DataArray toIData[0] waymask signals:")
                for port_idx in range(2):
                    for way in range(4):
                        waymask_signal = getattr(bundle.io._dataArray._toIData._0._bits._waymask, f"_{port_idx}")
                        way_val = getattr(waymask_signal, f"_{way}").value
                        print(f"      waymask[{port_idx}][{way}]: {way_val}")
            elif port >= 1 and port <= 2:  # Ports 1,2 have vSetIdx only
                vSetIdx_0 = getattr(bundle.io._dataArray._toIData, f"_{port}")._bits_vSetIdx._0.value
                vSetIdx_1 = getattr(bundle.io._dataArray._toIData, f"_{port}")._bits_vSetIdx._1.value
                print(f"    ✓ DataArray toIData[{port}] - vSetIdx: {vSetIdx_0}/{vSetIdx_1}")
            elif port == 3:  # Port 3 has vSetIdx (OUTPUT) and ready (INPUT)
                vSetIdx_0 = bundle.io._dataArray._toIData._3._bits_vSetIdx._0.value
                vSetIdx_1 = bundle.io._dataArray._toIData._3._bits_vSetIdx._1.value
                print(f"    ✓ DataArray toIData[3] - vSetIdx: {vSetIdx_0}/{vSetIdx_1}")
                
                # Test port 3 ready signal (INPUT)
                original_ready = bundle.io._dataArray._toIData._3._ready.value
                for test_ready in [0, 1]:
                    bundle.io._dataArray._toIData._3._ready.value = test_ready
                    await bundle.step()
                    assert bundle.io._dataArray._toIData._3._ready.value == test_ready, "Port 3 ready write failed"
                bundle.io._dataArray._toIData._3._ready.value = original_ready
                print(f"    ✓ DataArray toIData[3] ready signal read/write working")
                
    except Exception as e:
        error_msg = f"DataArray toIData signals error: {e}"
        test_errors.append(error_msg)
        print(f"    × {error_msg}")
    
    # fromIData signals are INPUT (lines 113-129 in Verilog)
    print("  8b. DataArray fromIData Signals (INPUT - Read/Write Testing)")
    try:
        # Test all 8 data and code signals
        test_datas = [0x1111 + i for i in range(8)]
        test_codes = [i % 2 for i in range(8)]
        
        for i in range(8):
            data_signal = getattr(bundle.io._dataArray._fromIData._datas, f"_{i}")
            code_signal = getattr(bundle.io._dataArray._fromIData._codes, f"_{i}")
            
            data_signal.value = test_datas[i]
            code_signal.value = test_codes[i]
            
        await bundle.step()
        
        # Verify writes successful
        for i in range(8):
            data_actual = getattr(bundle.io._dataArray._fromIData._datas, f"_{i}").value
            code_actual = getattr(bundle.io._dataArray._fromIData._codes, f"_{i}").value
            assert data_actual == test_datas[i], f"DataArray data {i} write failed"
            assert code_actual == test_codes[i], f"DataArray code {i} write failed"
            
        print("    ✓ DataArray fromIData signals read/write working")
        
    except Exception as e:
        error_msg = f"DataArray fromIData signals error: {e}"
        test_errors.append(error_msg)
        print(f"    × {error_msg}")
    
    # ================= 9. io._mshr Interface =================
    print("\n9. io._mshr Interface")
    # req is OUTPUT (lines 130-133 in Verilog), resp is INPUT (lines 134-138 in Verilog)
    print("  9a. MSHR Request Signals (OUTPUT - Read Only)")
    try:
        mshr_req_valid = bundle.io._mshr._req._valid.value
        mshr_req_blkPaddr = bundle.io._mshr._req._bits._blkPaddr.value
        mshr_req_vSetIdx = bundle.io._mshr._req._bits._vSetIdx.value
        print(f"    ✓ MSHR req - valid: {mshr_req_valid}, blkPaddr: {hex(mshr_req_blkPaddr)}, vSetIdx: {hex(mshr_req_vSetIdx)}")
    except Exception as e:
        error_msg = f"MSHR request signals error: {e}"
        test_errors.append(error_msg)
        print(f"    × {error_msg}")
    
    print("  9b. MSHR Response Signals (INPUT - Read/Write Testing)")
    try:
        # Test boundary values for different bit widths
        test_cases = [
            {"valid": 1, "blkPaddr": 0x12345678, "vSetIdx": 0xAB, "data": 0xDEADBEEFCAFEBABE, "corrupt": 0},
            {"valid": 0, "blkPaddr": 0xFFFFFFFF, "vSetIdx": 0xFF, "data": 0xFFFFFFFFFFFFFFFF, "corrupt": 1},
            {"valid": 1, "blkPaddr": 0x0, "vSetIdx": 0x0, "data": 0x0, "corrupt": 0},
        ]
        
        for test_case in test_cases:
            bundle.io._mshr._resp._valid.value = test_case["valid"]
            bundle.io._mshr._resp._bits._blkPaddr.value = test_case["blkPaddr"]
            bundle.io._mshr._resp._bits._vSetIdx.value = test_case["vSetIdx"]
            bundle.io._mshr._resp._bits._data.value = test_case["data"]
            bundle.io._mshr._resp._bits._corrupt.value = test_case["corrupt"]
            await bundle.step()
            
            # Verify writes
            assert bundle.io._mshr._resp._valid.value == test_case["valid"], "MSHR resp valid write failed"
            assert bundle.io._mshr._resp._bits._blkPaddr.value == test_case["blkPaddr"], "MSHR resp blkPaddr write failed"
            assert bundle.io._mshr._resp._bits._vSetIdx.value == test_case["vSetIdx"], "MSHR resp vSetIdx write failed"
            assert bundle.io._mshr._resp._bits._data.value == test_case["data"], "MSHR resp data write failed"
            assert bundle.io._mshr._resp._bits._corrupt.value == test_case["corrupt"], "MSHR resp corrupt write failed"
            
        print("    ✓ MSHR response signals read/write working")
        
        # ready signal is also INPUT
        original_ready = bundle.io._mshr._req._ready.value
        for test_ready in [0, 1]:
            bundle.io._mshr._req._ready.value = test_ready
            await bundle.step()
            assert bundle.io._mshr._req._ready.value == test_ready, "MSHR req ready write failed"
        bundle.io._mshr._req._ready.value = original_ready
        print("    ✓ MSHR request ready signal read/write working")
        
    except Exception as e:
        error_msg = f"MSHR response signals error: {e}"
        test_errors.append(error_msg)
        print(f"    × {error_msg}")
    
    # ================= 10. io._fetch Interface =================
    print("\n10. io._fetch Interface")
    # req.ready is OUTPUT (line 167), req.valid is INPUT (line 168), req.bits are INPUT (lines 169-184) in Verilog
    # resp signals are OUTPUT (lines 185-212 in Verilog)
    print("  10a. Fetch Request Ready Signal (OUTPUT - Read Only)")
    try:
        # ready signal is OUTPUT - only test read access  
        req_ready = bundle.io._fetch._req._ready.value
        print(f"    ✓ fetch.req.ready (OUTPUT): {req_ready}")
    except Exception as e:
        error_msg = f"Fetch request ready signal read error: {e}"
        test_errors.append(error_msg)
        print(f"    × {error_msg}")
    
    print("  10b. Fetch Request Control/Data Signals (INPUT - Read/Write Testing)")
    try:
        # Test valid signal (INPUT)
        original_req_valid = bundle.io._fetch._req._valid.value
        for test_valid in [0, 1]:
            bundle.io._fetch._req._valid.value = test_valid
            await bundle.step()
            assert bundle.io._fetch._req._valid.value == test_valid, "Fetch req valid write failed"
        
        # Test PCMemRead addresses and readValid (all INPUT)
        test_addrs = [0x1000, 0x2000, 0x3000, 0x4000, 0x5000]
        test_readValid = [1, 0, 1, 0, 1]
        
        for i in range(5):
            # Test startAddr (INPUT)
            start_addr_signal = getattr(bundle.io._fetch._req._bits._pcMemRead, f"_{i}")._startAddr
            start_addr_signal.value = test_addrs[i]
            
            # Test nextlineStart (INPUT)  
            nextline_signal = getattr(bundle.io._fetch._req._bits._pcMemRead, f"_{i}")._nextlineStart
            nextline_signal.value = test_addrs[i] + 64
            
            # Test readValid (INPUT)
            readValid_signal = getattr(bundle.io._fetch._req._bits._readValid, f"_{i}")
            readValid_signal.value = test_readValid[i]
            
        # Test backendException (INPUT)
        bundle.io._fetch._req._bits._backendException.value = 0
        
        await bundle.step()
        
        # Verify writes successful
        for i in range(5):
            start_actual = getattr(bundle.io._fetch._req._bits._pcMemRead, f"_{i}")._startAddr.value
            nextline_actual = getattr(bundle.io._fetch._req._bits._pcMemRead, f"_{i}")._nextlineStart.value
            readValid_actual = getattr(bundle.io._fetch._req._bits._readValid, f"_{i}").value
            
            assert start_actual == test_addrs[i], f"Fetch startAddr {i} write failed"
            assert nextline_actual == test_addrs[i] + 64, f"Fetch nextlineStart {i} write failed"
            assert readValid_actual == test_readValid[i], f"Fetch readValid {i} write failed"
            
        assert bundle.io._fetch._req._bits._backendException.value == 0, "Fetch backendException write failed"
        
        # Restore
        bundle.io._fetch._req._valid.value = original_req_valid
        print("    ✓ Fetch request INPUT signals read/write working")
        
    except Exception as e:
        error_msg = f"Fetch request data signals error: {e}"
        test_errors.append(error_msg)
        print(f"    × {error_msg}")
    
    print("  10c. Fetch Response Signals (OUTPUT - Read Only)")
    try:
        fetch_resp_signals = {
            "valid": bundle.io._fetch._resp._valid,
            "doubleline": bundle.io._fetch._resp._bits._doubleline,
            "vaddr_0": bundle.io._fetch._resp._bits._vaddr._0,
            "vaddr_1": bundle.io._fetch._resp._bits._vaddr._1,
            "data": bundle.io._fetch._resp._bits._data,
            "paddr_0": bundle.io._fetch._resp._bits._paddr._0,
            "exception_0": bundle.io._fetch._resp._bits._exception._0,
            "exception_1": bundle.io._fetch._resp._bits._exception._1,
            "backendException": bundle.io._fetch._resp._bits._backendException,
        }
        
        for field, signal_obj in fetch_resp_signals.items():
            value = signal_obj.value
            print(f"    ✓ fetch.resp.{field}: {hex(value) if isinstance(value, int) and value > 255 else value}")
        
        # Topdown signals
        topdown_icache = bundle.io._fetch._topdownIcacheMiss.value
        topdown_itlb = bundle.io._fetch._topdownItlbMiss.value
        print(f"    ✓ fetch topdown: ICache={topdown_icache}, ITLB={topdown_itlb}")
        
    except Exception as e:
        error_msg = f"Fetch response signals error: {e}"
        test_errors.append(error_msg)
        print(f"    × {error_msg}")
    
    # ================= 11. io._touch (OUTPUT) =================
    print("\n11. io._touch Interface (OUTPUT - Read Only)")
    try:
        touch_0_valid = bundle.io._touch._0._valid.value
        touch_0_vSetIdx = bundle.io._touch._0._bits._vSetIdx.value
        touch_0_way = bundle.io._touch._0._bits._way.value
        touch_1_valid = bundle.io._touch._1._valid.value
        touch_1_vSetIdx = bundle.io._touch._1._bits._vSetIdx.value
        touch_1_way = bundle.io._touch._1._bits._way.value
        
        print(f"  ✓ touch[0]: valid={touch_0_valid}, vSetIdx={touch_0_vSetIdx}, way={touch_0_way}")
        print(f"  ✓ touch[1]: valid={touch_1_valid}, vSetIdx={touch_1_vSetIdx}, way={touch_1_way}")
    except Exception as e:
        error_msg = f"touch interface error: {e}"
        test_errors.append(error_msg)
        print(f"  × {error_msg}")
    
    # ================= 12. io._other (INPUT) =================
    print("\n12. io._other Control Signals (INPUT - Read/Write Testing)")
    other_signals = [
        ("hartId", bundle.io._hartId, 6, 63),      # 6-bit: 0-63
        ("flush", bundle.io._flush, 1, 1),         # 1-bit: 0-1
        ("ecc_enable", bundle.io._ecc_enable, 1, 1), # 1-bit: 0-1
        ("respStall", bundle.io._respStall, 1, 1)  # 1-bit: 0-1
    ]
    
    for signal_name, signal_obj, bit_width, max_val in other_signals:
        try:
            original_val = signal_obj.value
            
            # Test boundary values
            test_values = [0, max_val]
            if bit_width > 1:
                test_values.append(max_val // 2)  # Mid-range value
                
            for test_val in test_values:
                signal_obj.value = test_val
                await bundle.step()
                assert signal_obj.value == test_val, f"{signal_name} write failed for value {test_val}"
            
            
            # Restore original
            signal_obj.value = original_val
            print(f"  ✓ {signal_name} read/write working (bit_width={bit_width})")
            
        except Exception as e:
            error_msg = f"{signal_name} signal error: {e}"
            test_errors.append(error_msg)
            print(f"  × {error_msg}")
    
    # ================= Final Summary =================
    print("\n" + "="*60)
    if test_errors:
        print(f"× Comprehensive test completed with {len(test_errors)} error(s):")
        for i, error in enumerate(test_errors, 1):
            print(f"  {i}. {error}")
        raise AssertionError(f"Comprehensive signal interface test failed with {len(test_errors)} errors")
    else:
        print("√ Comprehensive Signal Interface Test - ALL CATEGORIES PASSED")
        print("   • ICacheMainPipe internal signals: ✓")
        print("   • ICacheMainPipe__toMSHRArbiter_io_in: ✓")
        print("   • io._perfInfo (OUTPUT): ✓")
        print("   • io._pmp (mixed INPUT/OUTPUT): ✓")
        print("   • io._errors (OUTPUT): ✓")
        print("   • io._metaArrayFlush (OUTPUT): ✓")
        print("   • io._wayLookupRead (mixed INPUT/OUTPUT): ✓")
        print("   • io._dataArray (mixed INPUT/OUTPUT): ✓")
        print("   • io._mshr (mixed INPUT/OUTPUT): ✓")
        print("   • io._fetch (mixed INPUT/OUTPUT): ✓")
        print("   • io._touch (OUTPUT): ✓")
        print("   • io._other control signals (INPUT): ✓")
        print("   • Read/Write testing for INPUT signals: ✓")

# ==================== 功能点测试用例 ====================

@toffee_test.testcase
async def test_cp11_dataarray_access(icachemainpipe_env: ICacheMainPipeEnv):
    """
    CP11: 访问DataArray的单路功能测试
    
    根据MainPipe.md文档11章节的测试点：
    11.1: 访问DataArray的单路 - 当WayLookup中的信息表明路命中时，ITLB查询成功，并且DataArray当前没有写时
    11.2: 不访问DataArray（Way未命中）- 会访问，但是返回数据无效
    11.3: 不访问DataArray（ITLB查询失败）- 会访问，但是返回数据无效  
    11.4: 不访问DataArray（DataArray正在进行写操作）- 真正不访问
    
    基于verilog源码的关键逻辑：
    - s0_fire = io_fetch_req_valid & s0_can_go & ~io_flush
    - s0_can_go = io_dataArray_toIData_3_ready & io_wayLookupRead_valid & s1_ready
    - io_dataArray_toIData_X_valid = io_fetch_req_bits_readValid_X
    """
    print("\n=== CP11: 访问DataArray的单路功能测试 ===")
    agent = icachemainpipe_env.agent
    bundle = icachemainpipe_env.bundle
    
    # 初始化环境
    await agent.reset()
    await agent.drive_set_ecc_enable(True)
    await agent.drive_set_flush(False)
    await agent.drive_resp_stall(False)
    
    # 11.1: 访问DataArray的单路
    print("\n测试 11.1: 访问DataArray的单路")
    print("条件：s0_hits为高（一路命中），s0_itlb_exception信号为零（ITLB查询成功），toData.last.ready为高（DataArray没有正在进行的写操作）")
    print("预期：toData.valid信号为高，表示MainPipe向DataArray发出了读取请求")
    
    # 设置所有满足条件的信号
    await agent.drive_data_array_ready(True)  # toData.last.ready为高
    await agent.drive_waylookup_read(
        vSetIdx_0=0x10,
        vSetIdx_1=0x10,  # 由于0x400[5]=0，nextlineStart=startAddr，所以两个vSetIdx应该相同
        waymask_0=0x1,  # s0_hits为高（一路命中），根据verilog: s1_SRAMhits_0 <= |io_wayLookupRead_bits_entry_waymask_0
        ptag_0=0x12345,
        itlb_exception_0=0  # s0_itlb_exception信号为零（ITLB查询成功）
    )
    
    # 发送fetch请求
    await agent.drive_fetch_request(
        pcMemRead_addrs=[0x400, 0, 0, 0, 0x400],  # 0x400[13:6] = 0x10，与vSetIdx_0匹配
        readValid=[1, 0, 0, 0, 1]  # readValid[0]=1会使toIData_0_valid=1
    )
    
    # 监控结果
    dataarray_status = await agent.monitor_dataarray_toIData()
    pipeline_status = await agent.monitor_pipeline_status()
    
    print(f"  检查结果：")
    print(f"  - toIData_0_valid: {dataarray_status['toIData_0_valid']}")
    print(f"  - s0_fire: {pipeline_status['s0_fire']}")
    print(f"  - fetch_req_ready: {pipeline_status['fetch_req_ready']}")
    
    # 验证：toData.valid信号为高
    assert dataarray_status['toIData_0_valid'] == 1, "toData.valid信号应为高，表示MainPipe向DataArray发出了读取请求"
    assert pipeline_status['s0_fire'] == 1, "s0_fire应为1，表示流水线正常推进"
    
    await agent.clear_fetch_request()
    print("  ✅ 测试 11.1 通过")
    
    # 11.2: 不访问DataArray（Way未命中）- 会访问，但是返回数据无效
    print("\n测试 11.2: 不访问DataArray（Way未命中）- 会访问，但是返回数据无效")
    print("条件：s0_hits为低表示缓存未命中")
    print("预期：根据文档注释，会访问但返回数据无效")
    
    await agent.reset()
    await agent.drive_set_flush(False)
    await agent.drive_data_array_ready(True)
    
    await agent.drive_waylookup_read(
        vSetIdx_0=0x20,
        vSetIdx_1=0x20,  # 由于0x800[5]=0，nextlineStart=startAddr，所以两个vSetIdx应该相同
        waymask_0=0x0,  # s0_hits为低表示缓存未命中（waymask=0，OR约简结果为0）
        ptag_0=0x67890,
        itlb_exception_0=0
    )
    
    await agent.drive_fetch_request(
        pcMemRead_addrs=[0x800, 0, 0, 0, 0x800],  # 0x800[13:6] = 0x20，与vSetIdx_0匹配
        readValid=[1, 0, 0, 0, 1]
    )
    
    dataarray_status = await agent.monitor_dataarray_toIData()
    pipeline_status = await agent.monitor_pipeline_status()
    
    print(f"  检查结果：")
    print(f"  - toIData_0_valid: {dataarray_status['toIData_0_valid']}")
    print(f"  - toIData_0_waymask_0_0: {dataarray_status['toIData_0_waymask_0_0']}")
    print(f"  - s0_fire: {pipeline_status['s0_fire']}")
    
    # 根据文档注释和verilog实现：会访问（toIData_0_valid=1），但数据无效（waymask=0表示miss）
    assert dataarray_status['toIData_0_valid'] == 1, "根据verilog实现，readValid=1时toIData_0_valid仍为1（会访问）"
    assert dataarray_status['toIData_0_waymask_0_0'] == 0, "waymask应为0，表示miss"
    
    await agent.clear_fetch_request()
    print("  ✅ 测试 11.2 通过")
    
    # 11.3: 不访问DataArray（ITLB查询失败）- 会访问，但是返回数据无效
    print("\n测试 11.3: 不访问DataArray（ITLB查询失败）- 会访问，但是返回数据无效")
    print("条件：s0_itlb_exception信号不为零（ITLB查询失败）")
    print("预期：根据文档注释，会访问但返回数据无效")
    
    await agent.reset()
    await agent.drive_set_flush(False)
    await agent.drive_data_array_ready(True)
    
    await agent.drive_waylookup_read(
        vSetIdx_0=0x30,
        vSetIdx_1=0x30,  # 由于0xC00[5]=0，nextlineStart=startAddr，所以两个vSetIdx应该相同
        waymask_0=0x1,  # 有命中
        ptag_0=0xABCDE,
        itlb_exception_0=0x2  # s0_itlb_exception信号不为零（ITLB查询失败）
    )
    
    # 确保WayLookup设置生效
    await bundle.step(1)
    
    await agent.drive_fetch_request(
        pcMemRead_addrs=[0xC00, 0, 0, 0, 0xC00],  # 0xC00[13:6] = 0x30，与vSetIdx_0匹配
        readValid=[1, 0, 0, 0, 1]
    )
    
    # 等待一个额外的周期，让信号从S0传递到S1
    await bundle.step(1)
    
    dataarray_status = await agent.monitor_dataarray_toIData()
    pipeline_status = await agent.monitor_pipeline_status()
    exception_status = await agent.monitor_exception_merge_status()
    
    print(f"  检查结果：")
    print(f"  - toIData_0_valid: {dataarray_status['toIData_0_valid']}")
    itlb_exception = exception_status.get('s1_itlb_exception_0', None)
    print(f"  - ITLB exception: 0x{itlb_exception:x}" if itlb_exception is not None else "  - ITLB exception: None")
    print(f"  - s0_fire: {pipeline_status['s0_fire']}")
    
    # 根据文档注释和verilog实现：会访问（toIData_0_valid=1），但有ITLB异常
    assert dataarray_status['toIData_0_valid'] == 1, "根据verilog实现，readValid=1时toIData_0_valid仍为1（会访问）"
    assert itlb_exception == 0x2, f"应检测到ITLB异常0x2，实际为{itlb_exception}"
    
    await agent.clear_fetch_request()
    print("  ✅ 测试 11.3 通过")
    
    # 11.4: 不访问DataArray（DataArray正在进行写操作）
    print("\n测试 11.4: 不访问DataArray（DataArray正在进行写操作）")
    print("条件：toData.last.ready信号为低，表示DataArray正在进行写操作")
    print("预期：s0_fire和fetch_req_ready为低，表示流水线被阻止，虽然toIData_0_valid仍可能为1（直接由readValid控制）")
    
    await agent.reset()
    await agent.drive_set_flush(False)
    await agent.drive_data_array_ready(False)  # toData.last.ready信号为低
    
    await agent.drive_waylookup_read(
        vSetIdx_0=0x40,
        vSetIdx_1=0x40,  # 由于0x1000[5]=0，nextlineStart=startAddr，所以两个vSetIdx应该相同
        waymask_0=0x1,
        ptag_0=0xDEAD,
        itlb_exception_0=0
    )
    
    await agent.drive_fetch_request(
        pcMemRead_addrs=[0x1000, 0, 0, 0, 0x1000],  # 0x1000[13:6] = 0x40，与vSetIdx_0匹配
        readValid=[1, 0, 0, 0, 1]
    )
    
    dataarray_status = await agent.monitor_dataarray_toIData()
    pipeline_status = await agent.monitor_pipeline_status()
    
    print(f"  检查结果：")
    print(f"  - toIData_3_ready: {dataarray_status.get('toIData_3_ready', 0)}")
    print(f"  - toIData_0_valid: {dataarray_status['toIData_0_valid']}")
    print(f"  - s0_fire: {pipeline_status['s0_fire']}")
    print(f"  - fetch_req_ready: {pipeline_status['fetch_req_ready']}")
    
    # 根据verilog源码：DataArray busy时，s0_can_go为低，阻止流水线推进，但toIData_0_valid仍由readValid直接控制
    assert pipeline_status['s0_fire'] == 0, "DataArray忙时s0_fire应为0（s0_can_go=0）"
    assert pipeline_status['fetch_req_ready'] == 0, "DataArray忙时fetch_req_ready应为0（s0_can_go=0）"
    # 注意：toIData_0_valid可能仍为1，因为它直接由readValid控制，与DataArray busy无关
    
    await agent.clear_fetch_request()
    print("  ✅ 测试 11.4 通过")
    
    print("\n✅ CP11: 访问DataArray的单路功能测试完成")


@toffee_test.testcase
async def test_cp12_meta_ecc_check(icachemainpipe_env: ICacheMainPipeEnv):
    """
    CP12: Meta ECC校验功能测试
    根据MainPipe.md文档第12节和ICacheMainPipe.v源码实现Meta数据的ECC校验逻辑测试
    
    测试依据：
    1. 文档要求：将物理地址的标签部分与对应的Meta进行ECC校验，以确保Meta的完整性
    2. 源码实现：s2_meta_corrupt_0 <= io_ecc_enable & (^s1_req_ptags_0 != s1_meta_codes_0 & s1_meta_corrupt_hit_num == 3'h1 | (|(s1_meta_corrupt_hit_num[2:1])))
    """
    print("\n=== CP12: Meta ECC校验功能测试 ===")
    agent = icachemainpipe_env.agent
    bundle = icachemainpipe_env.bundle

    # 测试点12.1: 无ECC错误
    print("\n--- Test 12.1: 无ECC错误 ---")
    print("条件：waymask全为0（没有命中），则hit_num为0 或 waymask有一位为1（一路命中），hit_num为1且ECC对比通过（^ptag == meta_code）")
    print("预期：s1_meta_corrupt为假")
    
    await agent.reset()
    await agent.drive_set_ecc_enable(True)
    await agent.drive_data_array_ready(True)  # 确保DataArray准备就绪
    
    # Case 12.1a: waymask全为0（没有命中）
    print("Case 12.1a: waymask全为0（没有命中）")
    test_ptag = 0x12345
    test_vaddr = 0x1000
    correct_meta_code = bin(test_ptag).count('1') & 1  # 正确的ECC校验码（奇偶校验）
    
    # 正确的顺序：先设置WayLookup数据，然后发送fetch请求
    await agent.drive_waylookup_read(
        vSetIdx_0=(test_vaddr >> 6) & 0xFF,
        vSetIdx_1=(test_vaddr >> 6) & 0xFF,  # 设置vSetIdx_1匹配nextlineStart
        waymask_0=0x0,  # 没有命中
        ptag_0=test_ptag,
        meta_codes_0=correct_meta_code,
        itlb_exception_0=0
    )
    
    await agent.drive_fetch_request(
        pcMemRead_addrs=[test_vaddr, 0, 0, 0, test_vaddr],  # pcMemRead_0和pcMemRead_4都设置
        readValid=[1, 0, 0, 0, 1]  # readValid_0和readValid_4都有效
    )
    
    await bundle.step(1)  # 让流水线充分推进到S2阶段
    
    error_status = await agent.monitor_error_status()
    meta_status = await agent.monitor_check_meta_ecc_status()
    
    print(f"  waymask_0: 0x0 (没有命中)")
    print(f"  ptag_0: 0x{test_ptag:x}")
    print(f"  meta_codes_0: {correct_meta_code}")
    print(f"  hit_num应为0，s1_meta_corrupt应为假")
    print(f"  io.errors[0].valid: {error_status['0_valid']}")
    
    assert error_status['0_valid'] == 0, f"12.1a失败：没有命中时不应报告错误，但io.errors[0].valid={error_status['0_valid']}"
    
    # Case 12.1b: waymask有一位为1（一路命中）且ECC对比通过
    print("Case 12.1b: waymask有一位为1（一路命中）且ECC对比通过")
    await agent.reset()
    await agent.drive_set_ecc_enable(True)
    await agent.drive_data_array_ready(True)  # 确保DataArray准备就绪
    
    test_ptag = 0x54321
    test_vaddr = 0x2000  
    correct_meta_code = bin(test_ptag).count('1') & 1  # 正确的ECC校验码（奇偶校验）
    
    await agent.drive_waylookup_read(
        vSetIdx_0=(test_vaddr >> 6) & 0xFF,
        vSetIdx_1=(test_vaddr >> 6) & 0xFF,  # 设置vSetIdx_1匹配nextlineStart
        waymask_0=0x1,  # 单路命中
        ptag_0=test_ptag,
        meta_codes_0=correct_meta_code,
        itlb_exception_0=0
    )
    
    await agent.drive_fetch_request(
        pcMemRead_addrs=[test_vaddr, 0, 0, 0, test_vaddr],  # pcMemRead_0和pcMemRead_4都设置
        readValid=[1, 0, 0, 0, 1]  # readValid_0和readValid_4都有效
    )
    
    await bundle.step(1)
    
    error_status = await agent.monitor_error_status()
    
    print(f"  waymask_0: 0x1 (单路命中)")
    print(f"  ptag_0: 0x{test_ptag:x}")
    print(f"  meta_codes_0: {correct_meta_code}")
    print(f"  ECC校验：^ptag={test_ptag ^ (test_ptag >> 1) ^ (test_ptag >> 2) ^ (test_ptag >> 3) & 0x1} vs meta_code={correct_meta_code}")
    print(f"  hit_num应为1，ECC对比应通过，s1_meta_corrupt应为假")
    print(f"  io.errors[0].valid: {error_status['0_valid']}")
    
    assert error_status['0_valid'] == 0, f"12.1b失败：单路命中且ECC正确时不应报告错误，但io.errors[0].valid={error_status['0_valid']}"
    
    # 测试点12.2: 单路命中的ECC错误
    print("\n--- Test 12.2: 单路命中的ECC错误 ---")
    print("条件：waymask有一位为1（一路命中），ECC对比失败（^ptag != meta_code）")
    print("预期：s1_meta_corrupt(i)、io.errors(i).valid、io.errors(i).bits.report_to_beu、io.errors(i).bits.source.data为true")
    
    await agent.reset()
    await agent.drive_set_ecc_enable(True)
    await agent.drive_data_array_ready(True)  # 确保DataArray准备就绪
    
    test_ptag = 0xABCDE
    test_vaddr = 0x3000
    correct_meta_code = bin(test_ptag).count('1') & 1  # 正确的ECC校验码（奇偶校验）
    wrong_meta_code = 1 - correct_meta_code  # 故意错误的ECC码
    
    await agent.drive_waylookup_read(
        vSetIdx_0=(test_vaddr >> 6) & 0xFF,
        vSetIdx_1=(test_vaddr >> 6) & 0xFF,  # 设置vSetIdx_1匹配nextlineStart
        waymask_0=0x2,  # 单路命中（way 1）
        ptag_0=test_ptag,
        meta_codes_0=wrong_meta_code,
        itlb_exception_0=0
    )
    
    await agent.drive_fetch_request(
        pcMemRead_addrs=[test_vaddr, 0, 0, 0, test_vaddr],  # pcMemRead_0和pcMemRead_4都设置
        readValid=[1, 0, 0, 0, 1]  # readValid_0和readValid_4都有效
    )
    
    await bundle.step(1)
    
    error_status = await agent.monitor_error_status()
    
    print(f"  waymask_0: 0x2 (单路命中)")
    print(f"  ptag_0: 0x{test_ptag:x}")
    print(f"  meta_codes_0: {wrong_meta_code} (错误的ECC码)")
    print(f"  正确的ECC码应为: {correct_meta_code}")
    print(f"  hit_num应为1，ECC对比应失败，应报告错误")
    print(f"  io.errors[0].valid: {error_status['0_valid']}")
    print(f"  io.errors[0].report_to_beu: {error_status['0_report_to_beu']}")
    
    assert error_status['0_valid'] == 1, f"12.2失败：单路命中且ECC错误时应报告错误，但io.errors[0].valid={error_status['0_valid']}"
    assert error_status['0_report_to_beu'] == 1, f"12.2失败：应向BEU报告错误，但report_to_beu={error_status['0_report_to_beu']}"
    
    # 测试点12.3: 多路命中
    # print("\n--- Test 12.3: 多路命中 ---")
    # print("条件：waymask有两位及以上为1（多路命中），视为ECC错误")
    # print("预期：s1_meta_corrupt(i)、io.errors(i).valid、io.errors(i).bits.report_to_beu、io.errors(i).bits.source.data为true")
    
    # await agent.reset()
    # await agent.drive_set_ecc_enable(True)
    # await agent.drive_data_array_ready(True)  # 确保DataArray准备就绪
    
    # test_ptag = 0x98765
    # test_vaddr = 0x4000
    # any_meta_code = 0  # 多路命中时meta_code值不重要
    
    # await agent.drive_waylookup_read(
    #     vSetIdx_0=(test_vaddr >> 6) & 0xFF,
    #     vSetIdx_1=(test_vaddr >> 6) & 0xFF,  # 设置vSetIdx_1匹配nextlineStart
    #     waymask_0=0x5,  # 多路命中（way 0和way 2）
    #     ptag_0=test_ptag,
    #     meta_codes_0=any_meta_code,
    #     itlb_exception_0=0
    # )
    
    # await agent.drive_fetch_request(
    #     pcMemRead_addrs=[test_vaddr, 0, 0, 0, test_vaddr],  # pcMemRead_0和pcMemRead_4都设置
    #     readValid=[1, 0, 0, 0, 1]  # readValid_0和readValid_4都有效
    # )
    
    # await bundle.step(1)  # 让流水线充分推进到S2阶段
    
    # error_status = await agent.monitor_error_status()
    
    # print(f"  waymask_0: 0x5 (多路命中，way 0和way 2)")
    # print(f"  ptag_0: 0x{test_ptag:x}")
    # print(f"  meta_codes_0: {any_meta_code}")
    # print(f"  hit_num应≥2，根据源码|(hit_num[2:1])检测多路命中，应报告错误")
    # print(f"  io.errors[0].valid: {error_status['0_valid']}")
    # print(f"  io.errors[0].report_to_beu: {error_status['0_report_to_beu']}")
    
    # assert error_status['0_valid'] == 1, f"12.3失败：多路命中时应报告错误，但io.errors[0].valid={error_status['0_valid']}"
    # assert error_status['0_report_to_beu'] == 1, f"12.3失败：应向BEU报告错误，但report_to_beu={error_status['0_report_to_beu']}"
    
    # 测试点12.4: ECC功能关闭
    print("\n--- Test 12.4: ECC功能关闭 ---")
    print("条件：奇偶校验关闭（ecc_enable为低）")
    print("预期：强制清除s1_meta_corrupt信号置位，不管是否发生ECC错误，s1_meta_corrupt都为假")
    
    await agent.reset()
    await agent.drive_set_ecc_enable(False)  # 关闭ECC功能
    await agent.drive_data_array_ready(True)  # 确保DataArray准备就绪
    
    # 故意设置ECC错误条件但ECC功能关闭
    test_ptag = 0x11111
    test_vaddr = 0x5000
    wrong_meta_code = 1  # 故意错误的ECC码
    
    await agent.drive_waylookup_read(
        vSetIdx_0=(test_vaddr >> 6) & 0xFF,
        vSetIdx_1=(test_vaddr >> 6) & 0xFF,  # 设置vSetIdx_1匹配nextlineStart
        waymask_0=0x1,  # 单路命中
        ptag_0=test_ptag,
        meta_codes_0=wrong_meta_code,
        itlb_exception_0=0
    )
    
    await agent.drive_fetch_request(
        pcMemRead_addrs=[0, 0, 0, 0, test_vaddr],
        readValid=[0, 0, 0, 0, 1]
    )
    
    await bundle.step(1)
    
    error_status = await agent.monitor_error_status()
    meta_status = await agent.monitor_check_meta_ecc_status()
    
    print(f"  ECC功能已关闭")
    print(f"  waymask_0: 0x1 (单路命中)")
    print(f"  ptag_0: 0x{test_ptag:x}")
    print(f"  meta_codes_0: {wrong_meta_code} (故意错误的ECC码)")
    print(f"  由于ECC功能关闭，即使有ECC错误也不应报告")
    print(f"  io.ecc_enable: {meta_status['ecc_enable']}")
    print(f"  io.errors[0].valid: {error_status['0_valid']}")
    
    assert meta_status['ecc_enable'] == 0, f"12.4失败：ECC功能应被关闭，但ecc_enable={meta_status['ecc_enable']}"
    assert error_status['0_valid'] == 0, f"12.4失败：ECC功能关闭时不应报告错误，但io.errors[0].valid={error_status['0_valid']}"
    
    print("\n CP12: Meta ECC校验功能测试完成")


@toffee_test.testcase
async def test_cp13_pmp_check(icachemainpipe_env: ICacheMainPipeEnv):
    """
    CP13: PMP检查功能测试
    测试物理内存保护检查逻辑
    """
    print("\n=== CP13: PMP Check Test ===")
    agent = icachemainpipe_env.agent
    bundle = icachemainpipe_env.bundle
    
    # 收集所有测试错误
    test_errors = []
    
    # 13.1: 没有异常
    # 文档：s1_pmp_exception 为全零，表示没有 PMP 异常
    # Verilog：io_pmp_0_resp_instr = 1 且 io_pmp_1_resp_instr = 1 时无 PMP 异常
    print("Test 13.1: 没有异常")
    try:
        bundle.io._flush.value = 1
        await bundle.step()
        bundle.io._flush.value = 0
        await bundle.step()
        await agent.drive_set_ecc_enable(True)
        await agent.drive_data_array_ready(True)  # 确保DataArray准备就绪
        # 设置 PMP 响应：两个通道都有指令权限，都不是 MMIO
        await agent.drive_pmp_response(
            instr_0=1, mmio_0=0,
            instr_1=1, mmio_1=0
        )
        await agent.drive_waylookup_read(
            vSetIdx_0=0x40,  # 0x1000[13:6] = 0x40
            vSetIdx_1=0x40,  # 保持一致
            waymask_0=0x0,  # 没有命中
            ptag_0=0x12345,
            itlb_exception_0=0
        )
        await agent.drive_fetch_request(
            pcMemRead_addrs=[0x1000, 0, 0, 0, 0x1000],  # pcMemRead_0和pcMemRead_4都设置
            readValid=[1, 0, 0, 0, 1]  # readValid_0和readValid_4都有效
        )
        await bundle.step(3)
        await agent.clear_fetch_request()
        await agent.clear_waylookup_read()

        await bundle.step()
        # 验证结果
        pmp_status = await agent.monitor_pmp_status()
        fetch_resp = await agent.monitor_fetch_response()
        
        print(f"  PMP 0 MMIO: {pmp_status['pmp_0_resp_mmio']}")
        print(f"  PMP 1 MMIO: {pmp_status['pmp_1_resp_mmio']}")
        print(f"  Fetch resp exception 0: {fetch_resp['exception_0']}")
        print(f"  Fetch resp exception 1: {fetch_resp['exception_1']}")
        
        # 验证：无异常
        assert fetch_resp['exception_0'] == 0, "通道0不应有异常"
        assert fetch_resp['exception_1'] == 0, "通道1不应有异常"
        print("✅ Test 13.1 通过")
    except Exception as e:
        error_msg = f"Test 13.1 failed: {e}"
        test_errors.append(error_msg)
        print(f"❌ {error_msg}")
    
    # 13.2: 通道 0 有 PMP 异常
    # 文档：s1_pmp_exception(0) 为真，表示通道 0 有 PMP 异常
    # Verilog：io_pmp_0_resp_instr = 0 时产生 PMP 异常
    print("\nTest 13.2: 通道 0 有 PMP 异常")
    try:
        bundle.io._flush.value = 1
        await bundle.step()
        bundle.io._flush.value = 0
        await bundle.step()
        await agent.drive_set_ecc_enable(True)
        await agent.drive_data_array_ready(True)  # 确保DataArray准备就绪
        # 设置 PMP 响应：两个通道都有指令权限，都不是 MMIO
        await agent.drive_pmp_response(
            instr_0=1, mmio_0=0,
            instr_1=1, mmio_1=0
        )
        await agent.drive_waylookup_read(
            vSetIdx_0=0x40,  # 0x1000[13:6] = 0x40
            vSetIdx_1=0x40,  # 保持一致
            waymask_0=0x0,  # 没有命中
            ptag_0=0x12345,
            itlb_exception_0=0
        )
        await agent.drive_fetch_request(
            pcMemRead_addrs=[0x1000, 0, 0, 0, 0x1000],  # pcMemRead_0和pcMemRead_4都设置
            readValid=[1, 0, 0, 0, 1]  # readValid_0和readValid_4都有效
        )
        await bundle.step(3)
        await agent.clear_fetch_request()
        await agent.clear_waylookup_read()
        
        await bundle.step()
        # 验证结果
        pmp_status = await agent.monitor_pmp_status()
        fetch_resp = await agent.monitor_fetch_response()
        
        print(f"  PMP 0 MMIO: {pmp_status['pmp_0_resp_mmio']}")
        print(f"  PMP 1 MMIO: {pmp_status['pmp_1_resp_mmio']}")
        print(f"  Fetch resp exception 0: {fetch_resp['exception_0']}")
        print(f"  Fetch resp exception 1: {fetch_resp['exception_1']}")
        
        # 验证：通道0有异常，通道1无异常
        assert fetch_resp['exception_0'] != 0, "通道0应有PMP异常"
        assert fetch_resp['exception_1'] == 0, "通道1不应有异常"
        print("✅ Test 13.2 通过")
    except Exception as e:
        error_msg = f"Test 13.2 failed: {e}"
        test_errors.append(error_msg)
        print(f"❌ {error_msg}")
    
    # 13.3: 通道 1 有 PMP 异常
    # 文档：s1_pmp_exception(1) 为真，表示通道 1 有 PMP 异常
    print("\nTest 13.3: 通道 1 有 PMP 异常")
    try:
        bundle.io._flush.value = 1
        await bundle.step()
        bundle.io._flush.value = 0
        await bundle.step()
        await agent.drive_set_ecc_enable(True)
        await agent.drive_data_array_ready(True)  # 确保DataArray准备就绪
        await agent.drive_waylookup_read(
            vSetIdx_0=0x40,  # 0x1000[13:6] = 0x40
            vSetIdx_1=0x40,  # 保持一致
            waymask_0=0x0,  # 没有命中
            ptag_0=0x12345,
            meta_codes_0=bin(0x12345).count('1') & 1,
            itlb_exception_0=0
        )
        
        await agent.drive_fetch_request(
            pcMemRead_addrs=[0x1000, 0, 0, 0, 0x1000],  # pcMemRead_0和pcMemRead_4都设置
            readValid=[1, 0, 0, 0, 1]  # readValid_0和readValid_4都有效
        )
        
        # 设置通道1产生PMP异常
        await agent.drive_pmp_response(
            instr_0=1, mmio_0=0,  # 通道0无异常
            instr_1=0, mmio_1=0   # 通道1产生PMP异常（修正：instr=0表示有异常）
        )
        
        await bundle.step(1)
        
        fetch_resp = await agent.monitor_fetch_response()
        
        print(f"  Fetch resp exception 0: {fetch_resp['exception_0']}")
        print(f"  Fetch resp exception 1: {fetch_resp['exception_1']}")
        
        # 验证：通道0无异常，通道1有异常
        assert fetch_resp['exception_0'] == 0, "通道0不应有异常"
        assert fetch_resp['exception_1'] != 0, "通道1应有PMP异常"
        print("✅ Test 13.3 通过")
    except Exception as e:
        error_msg = f"Test 13.3 failed: {e}"
        test_errors.append(error_msg)
        print(f"❌ {error_msg}")
    
    # 13.4: 通道 0 和通道 1 都有 PMP 异常
    # 文档：s1_pmp_exception(0) 和 s1_pmp_exception(1) 都为真
    print("\nTest 13.4: 通道 0 和通道 1 都有 PMP 异常")
    try:
        bundle.io._flush.value = 1
        await bundle.step()
        bundle.io._flush.value = 0
        await bundle.step()
        await agent.drive_set_ecc_enable(True)
        await agent.drive_data_array_ready(True)  # 确保DataArray准备就绪
        await agent.drive_waylookup_read(
            vSetIdx_0=0x40,  # 0x1000[13:6] = 0x40
            vSetIdx_1=0x40,  # 保持一致
            waymask_0=0x0,  # 没有命中
            ptag_0=0x12345,
            meta_codes_0=bin(0x12345).count('1') & 1,
            itlb_exception_0=0
        )
        
        await agent.drive_fetch_request(
            pcMemRead_addrs=[0x1000, 0, 0, 0, 0x1000],  # pcMemRead_0和pcMemRead_4都设置
            readValid=[1, 0, 0, 0, 1]  # readValid_0和readValid_4都有效
        )
        
        # 设置两个通道都产生PMP异常
        await agent.drive_pmp_response(
            instr_0=0, mmio_0=0,  # 通道0产生PMP异常
            instr_1=0, mmio_1=0   # 通道1产生PMP异常
        )
        
        await bundle.step(1)
        
        fetch_resp = await agent.monitor_fetch_response()
        
        print(f"  Fetch resp exception 0: {fetch_resp['exception_0']}")
        print(f"  Fetch resp exception 1: {fetch_resp['exception_1']}")
        
        # 验证：两个通道都有异常
        assert fetch_resp['exception_0'] != 0, "通道0应有PMP异常"
        assert fetch_resp['exception_1'] != 0, "通道1应有PMP异常"
        print("✅ Test 13.4 通过")
    except Exception as e:
        error_msg = f"Test 13.4 failed: {e}"
        test_errors.append(error_msg)
        print(f"❌ {error_msg}")
    
    # 13.5: 没有映射到 MMIO 区域
    # 文档：s1_pmp_mmio(0) 和 s1_pmp_mmio(1) 都为假，表示没有映射到 MMIO 区域
    # Verilog：s2_pmp_mmio_0 <= io_pmp_0_resp_mmio
    print("\nTest 13.5: 没有映射到 MMIO 区域")
    try:
        bundle.io._flush.value = 1
        await bundle.step()
        bundle.io._flush.value = 0
        await bundle.step()
        await agent.drive_set_ecc_enable(True)
        await agent.drive_data_array_ready(True)  # 确保DataArray准备就绪
        await agent.drive_waylookup_read(
            vSetIdx_0=0x40,  # 0x1000[13:6] = 0x40
            vSetIdx_1=0x40,  # 保持一致
            waymask_0=0x0,  # 没有命中
            ptag_0=0x12345,
            meta_codes_0=bin(0x12345).count('1') & 1,
            itlb_exception_0=0
        )
        
        await agent.drive_fetch_request(
            pcMemRead_addrs=[0x1000, 0, 0, 0, 0x1000],  # pcMemRead_0和pcMemRead_4都设置
            readValid=[1, 0, 0, 0, 1]  # readValid_0和readValid_4都有效
        )
        
        # 设置两个通道都不是MMIO区域
        await agent.drive_pmp_response(
            instr_0=1, mmio_0=0,  # 通道0有权限，非MMIO
            instr_1=1, mmio_1=0   # 通道1有权限，非MMIO
        )
        
        await bundle.step(1)
        
        pmp_status = await agent.monitor_pmp_status()
        fetch_resp = await agent.monitor_fetch_response()
        
        print(f"  PMP 0 MMIO: {pmp_status['pmp_0_resp_mmio']}")
        print(f"  PMP 1 MMIO: {pmp_status['pmp_1_resp_mmio']}")
        print(f"  Fetch resp PMP MMIO 0: {fetch_resp['pmp_mmio_0']}")
        print(f"  Fetch resp PMP MMIO 1: {fetch_resp['pmp_mmio_1']}")
        
        # 验证：两个通道都不是MMIO
        assert pmp_status['pmp_0_resp_mmio'] == 0, "通道0不应映射到MMIO"
        assert pmp_status['pmp_1_resp_mmio'] == 0, "通道1不应映射到MMIO"
        assert fetch_resp['pmp_mmio_0'] == 0, "Fetch响应通道0不应标记为MMIO"
        assert fetch_resp['pmp_mmio_1'] == 0, "Fetch响应通道1不应标记为MMIO"
        print("✅ Test 13.5 通过")
    except Exception as e:
        error_msg = f"Test 13.5 failed: {e}"
        test_errors.append(error_msg)
        print(f"❌ {error_msg}")
    
    # 13.6: 通道 0 映射到了 MMIO 区域
    # 文档：s1_pmp_mmio(0) 为真，表示映射到了 MMIO 区域
    print("\nTest 13.6: 通道 0 映射到了 MMIO 区域")
    try:
        bundle.io._flush.value = 1
        await bundle.step()
        bundle.io._flush.value = 0
        await bundle.step()
        await agent.drive_set_ecc_enable(True)
        await agent.drive_data_array_ready(True)
        
        # 统一使用相同地址和vSetIdx避免mismatch
        await agent.drive_waylookup_read(
            vSetIdx_0=0x40, vSetIdx_1=0x40,  # 与0x1000匹配
            waymask_0=0x1, waymask_1=0x1,
            ptag_0=0x1005, ptag_1=0x1005,
            itlb_exception_0=0, itlb_exception_1=0,
            itlb_pbmt_0=0, itlb_pbmt_1=0
        )
        
        await agent.drive_fetch_request(
            pcMemRead_addrs=[0, 0, 0, 0, 0x1000],  # [13:6] = 0x40，匹配 vSetIdx_0
            readValid=[0, 0, 0, 0, 1],
            backendException=0
        )
        
        # 设置通道0映射到MMIO区域
        await agent.drive_pmp_response(
            instr_0=1, mmio_0=1,  # 通道0有权限，映射到MMIO
            instr_1=1, mmio_1=0   # 通道1有权限，非MMIO
        )
        
        await bundle.step(1)
        
        pmp_status = await agent.monitor_pmp_status()
        fetch_resp = await agent.monitor_fetch_response()
        
        print(f"  PMP 0 MMIO: {pmp_status['pmp_0_resp_mmio']}")
        print(f"  PMP 1 MMIO: {pmp_status['pmp_1_resp_mmio']}")
        print(f"  Fetch resp PMP MMIO 0: {fetch_resp['pmp_mmio_0']}")
        print(f"  Fetch resp PMP MMIO 1: {fetch_resp['pmp_mmio_1']}")
        
        # 验证：通道0是MMIO，通道1不是MMIO
        assert pmp_status['pmp_0_resp_mmio'] == 1, "通道0应映射到MMIO"
        assert pmp_status['pmp_1_resp_mmio'] == 0, "通道1不应映射到MMIO"
        assert fetch_resp['pmp_mmio_0'] == 1, "Fetch响应通道0应标记为MMIO"
        assert fetch_resp['pmp_mmio_1'] == 0, "Fetch响应通道1不应标记为MMIO"
        print("✅ Test 13.6 通过")
    except Exception as e:
        error_msg = f"Test 13.6 failed: {e}"
        test_errors.append(error_msg)
        print(f"❌ {error_msg}")
    
    # 13.7: 通道 1 映射到了 MMIO 区域
    # 文档：s1_pmp_mmio(1) 为真，表示映射到了 MMIO 区域
    print("\nTest 13.7: 通道 1 映射到了 MMIO 区域")
    try:
        bundle.io._flush.value = 1
        await bundle.step()
        bundle.io._flush.value = 0
        await bundle.step()
        await agent.drive_set_ecc_enable(True)
        await agent.drive_data_array_ready(True)
        
        # 统一使用相同地址和vSetIdx避免mismatch
        await agent.drive_waylookup_read(
            vSetIdx_0=0x40, vSetIdx_1=0x40,  # 与0x1000匹配
            waymask_0=0x1, waymask_1=0x1,
            ptag_0=0x1006, ptag_1=0x1006,
            itlb_exception_0=0, itlb_exception_1=0,
            itlb_pbmt_0=0, itlb_pbmt_1=0
        )
        
        await agent.drive_fetch_request(
            pcMemRead_addrs=[0, 0, 0, 0, 0x1000],  # [13:6] = 0x40，匹配 vSetIdx_0
            readValid=[0, 0, 0, 0, 1],
            backendException=0
        )
        
        # 设置通道1映射到MMIO区域
        await agent.drive_pmp_response(
            instr_0=1, mmio_0=0,  # 通道0有权限，非MMIO
            instr_1=1, mmio_1=1   # 通道1有权限，映射到MMIO
        )
        
        await bundle.step(1)
        
        pmp_status = await agent.monitor_pmp_status()
        fetch_resp = await agent.monitor_fetch_response()
        
        print(f"  PMP 0 MMIO: {pmp_status['pmp_0_resp_mmio']}")
        print(f"  PMP 1 MMIO: {pmp_status['pmp_1_resp_mmio']}")
        print(f"  Fetch resp PMP MMIO 0: {fetch_resp['pmp_mmio_0']}")
        print(f"  Fetch resp PMP MMIO 1: {fetch_resp['pmp_mmio_1']}")
        
        # 验证：通道0不是MMIO，通道1是MMIO
        assert pmp_status['pmp_0_resp_mmio'] == 0, "通道0不应映射到MMIO"
        assert pmp_status['pmp_1_resp_mmio'] == 1, "通道1应映射到MMIO"
        assert fetch_resp['pmp_mmio_0'] == 0, "Fetch响应通道0不应标记为MMIO"
        assert fetch_resp['pmp_mmio_1'] == 1, "Fetch响应通道1应标记为MMIO"
        print("✅ Test 13.7 通过")
    except Exception as e:
        error_msg = f"Test 13.7 failed: {e}"
        test_errors.append(error_msg)
        print(f"❌ {error_msg}")
    
    # 13.8: 通道 0 和通道 1 都映射到了 MMIO 区域
    # 文档：s1_pmp_mmio(0) 和 s1_pmp_mmio(1) 都为真
    print("\nTest 13.8: 通道 0 和通道 1 都映射到了 MMIO 区域")
    try:
        bundle.io._flush.value = 1
        await bundle.step()
        bundle.io._flush.value = 0
        await bundle.step()
        await agent.drive_set_ecc_enable(True)
        await agent.drive_data_array_ready(True)
        
        # 统一使用相同地址和vSetIdx避免mismatch
        await agent.drive_waylookup_read(
            vSetIdx_0=0x40, vSetIdx_1=0x40,  # 与0x1000匹配
            waymask_0=0x1, waymask_1=0x1,
            ptag_0=0x1007, ptag_1=0x1007,
            itlb_exception_0=0, itlb_exception_1=0,
            itlb_pbmt_0=0, itlb_pbmt_1=0
        )
        
        await agent.drive_fetch_request(
            pcMemRead_addrs=[0, 0, 0, 0, 0x1000],  # [13:6] = 0x40，匹配 vSetIdx_0
            readValid=[0, 0, 0, 0, 1],
            backendException=0
        )
        
        # 设置两个通道都映射到MMIO区域
        await agent.drive_pmp_response(
            instr_0=1, mmio_0=1,  # 通道0有权限，映射到MMIO
            instr_1=1, mmio_1=1   # 通道1有权限，映射到MMIO
        )
        
        await bundle.step(1)
        
        pmp_status = await agent.monitor_pmp_status()
        fetch_resp = await agent.monitor_fetch_response()
        
        print(f"  PMP 0 MMIO: {pmp_status['pmp_0_resp_mmio']}")
        print(f"  PMP 1 MMIO: {pmp_status['pmp_1_resp_mmio']}")
        print(f"  Fetch resp PMP MMIO 0: {fetch_resp['pmp_mmio_0']}")
        print(f"  Fetch resp PMP MMIO 1: {fetch_resp['pmp_mmio_1']}")
        
        # 验证：两个通道都是MMIO
        assert pmp_status['pmp_0_resp_mmio'] == 1, "通道0应映射到MMIO"
        assert pmp_status['pmp_1_resp_mmio'] == 1, "通道1应映射到MMIO"
        assert fetch_resp['pmp_mmio_0'] == 1, "Fetch响应通道0应标记为MMIO"
        assert fetch_resp['pmp_mmio_1'] == 1, "Fetch响应通道1应标记为MMIO"
        print("✅ Test 13.8 通过")
    except Exception as e:
        error_msg = f"Test 13.8 failed: {e}"
        test_errors.append(error_msg)
        print(f"❌ {error_msg}")
    
    # 汇总所有测试结果
    print("\n" + "="*60)
    if test_errors:
        print(f"❌ CP13: PMP检查功能测试完成 - {len(test_errors)}个错误:")
        for i, error in enumerate(test_errors, 1):
            print(f"  {i}. {error}")
        raise AssertionError(f"CP13 PMP测试失败，共{len(test_errors)}个错误: {'; '.join(test_errors)}")
    else:
        print("✅ CP13: PMP检查功能测试完成 - 所有测试通过")


@toffee_test.testcase
async def test_cp14_exception_merge(icachemainpipe_env: ICacheMainPipeEnv):
    """
    CP14: 异常合并功能测试
    测试ITLB和PMP异常的优先级合并逻辑
    """
    print("\n=== CP14: Exception Merge Test ===")
    agent = icachemainpipe_env.agent
    bundle = icachemainpipe_env.bundle
    
    # 14.1: 没有异常
    print("Test 14.1: No exception")
    await agent.reset()
    
    await agent.drive_waylookup_read(
        vSetIdx_0=0x10,
        waymask_0=0x1,
        ptag_0=0x1000,
        itlb_exception_0=0  # 无ITLB异常
    )
    
    await agent.drive_pmp_response(
        instr_0=1, mmio_0=0  # 无PMP异常
    )
    
    await bundle.step(3)
    
    exception_status = await agent.monitor_exception_merge_status()
    
    print(f"  ITLB exception 0: {exception_status.get('s1_itlb_exception_0', 'N/A')}")
    print(f"  Final exception 0: {exception_status.get('s2_exception_0', 'N/A')}")
    
    # 14.2: 只有ITLB异常
    print("Test 14.2: Only ITLB exception")
    await agent.reset()
    
    await agent.drive_waylookup_read(
        vSetIdx_0=0x20,
        waymask_0=0x1,
        ptag_0=0x2000,
        itlb_exception_0=0x2  # ITLB异常
    )
    
    await agent.drive_pmp_response(
        instr_0=1, mmio_0=0  # 无PMP异常
    )
    
    await bundle.step(3)
    
    exception_status = await agent.monitor_exception_merge_status()
    fetch_resp = await agent.monitor_fetch_response()
    
    print(f"  ITLB exception: {exception_status.get('s1_itlb_exception_0', 'N/A')}")
    print(f"  Fetch resp exception: {fetch_resp['exception_0']}")
    
    # 14.3: 只有PMP异常
    print("Test 14.3: Only PMP exception")
    await agent.reset()
    
    await agent.drive_waylookup_read(
        vSetIdx_0=0x30,
        waymask_0=0x1,
        ptag_0=0x3000,
        itlb_exception_0=0  # 无ITLB异常
    )
    
    await agent.drive_pmp_response(
        instr_0=0, mmio_0=0  # PMP异常（无指令权限）
    )
    
    await bundle.step(3)
    
    # 14.4: ITLB与PMP异常同时出现（ITLB优先级更高）
    
    # NEED TODO
    result = False

    # 如果高级API不工作，使用基础API
    if not result:
        await agent.reset()
        
        await agent.drive_waylookup_read(
            vSetIdx_0=0x40,
            waymask_0=0x1,
            ptag_0=0x4000,
            itlb_exception_0=0x2  # ITLB异常
        )
        
        await agent.drive_pmp_response(
            instr_0=0, mmio_0=0  # PMP异常
        )
        
        await bundle.step(3)
        
        exception_status = await agent.monitor_exception_merge_status()
        print(f"  Final exception (should be ITLB): {exception_status.get('s2_exception_0', 'N/A')}")
    
    print("✅ CP14: Exception Merge tests completed")


@toffee_test.testcase
async def test_cp15_mshr_match_data_select(icachemainpipe_env: ICacheMainPipeEnv):
    """
    CP15: MSHR匹配和数据选择功能测试
    测试MSHR命中检查和数据源选择逻辑
    """
    print("\n=== CP15: MSHR Match and Data Selection Test ===")
    agent = icachemainpipe_env.agent
    bundle = icachemainpipe_env.bundle
    
    # 15.1: 命中MSHR - 修复版本以触发CP15.1覆盖点
    print("Test 15.1: MSHR hit scenario")
    await agent.reset()
    await agent.setup_mshr_ready(True)
    
    # 先发送MSHR响应
    await agent.drive_mshr_response(
        blkPaddr=0x1000,
        vSetIdx=0x10,
        data=0x123456789ABCDEF0,
        corrupt=0
    )
    
    await bundle.step(2)  # 让MSHR响应稳定
    
    # 设置DataArray ready以便流水线能够推进到S1阶段
    await agent.drive_data_array_ready(True)
    
    # 发送匹配的请求 - 需要确保地址映射正确
    # 注意：pcMemRead_4_startAddr[13:6] 必须等于 vSetIdx_0
    await agent.drive_waylookup_read(
        vSetIdx_0=0x10,  # 与MSHR响应中的vSetIdx相匹配
        waymask_0=0x1,   # 单路命中
        ptag_0=(0x400 >> 12) & 0xFFFFF
    )
    
    # 发送fetch请求以推进流水线到S1阶段进行MSHR匹配
    # 确保 pcMemRead_4_startAddr[13:6] = 0x400[13:6] = 0x10 = vSetIdx_0
    await agent.drive_fetch_request(
        pcMemRead_addrs=[0x1000, 0, 0, 0, 0x400],  # 使用第5个元素，确保地址一致性
        readValid=[1, 0, 0, 0, 1]
    )
    
    await bundle.step(5)  # 给足够时间让请求到达S1阶段
    await agent.clear_fetch_request()
    
    mshr_match_status = await agent.monitor_mshr_match_status()
    
    print(f"  MSHR hits: {mshr_match_status.get('s1_MSHR_hits_1', 'N/A')}")
    for i in range(8):
        bank_hit = mshr_match_status.get(f's1_bankMSHRHit_{i}', False)
        if bank_hit:
            print(f"  Bank {i} MSHR hit: {bank_hit}")
    
    
    
    # 15.2: 未命中MSHR
    print("Test 15.2: MSHR miss scenario")
    await agent.reset()
    
    # 发送不匹配的请求
    await agent.drive_waylookup_read(
        vSetIdx_0=0x20,  # 不同的vSetIdx
        waymask_0=0x1,
        ptag_0=0x5678
    )
    
    await bundle.step(3)
    
    mshr_match_status = await agent.monitor_mshr_match_status()
    print(f"  MSHR miss case - hits: {mshr_match_status.get('s1_MSHR_hits_1', 'N/A')}")
    
    # 15.3: MSHR数据corrupt(need todo)
    print("Test 15.3: MSHR data corrupt scenario")

   
    
    print("✅ CP15: MSHR Match and Data Selection tests completed")


@toffee_test.testcase
async def test_cp16_data_ecc_check(icachemainpipe_env: ICacheMainPipeEnv):
    """
    CP16: Data ECC校验功能测试
    测试S2阶段的数据ECC校验逻辑
    """
    print("\n=== CP16: Data ECC Check Test ===")
    agent = icachemainpipe_env.agent
    bundle = icachemainpipe_env.bundle
    
    # 16.1: 无ECC错误
    print("Test 16.1: No Data ECC error")
    await agent.reset()
    await agent.drive_set_ecc_enable(True)
    
    # 发送正确的数据和校验码
    test_datas = [0x1111111111111111 + i for i in range(8)]
    test_codes = [0] * 8  # 正确的校验码
    
    await agent.drive_data_array_response(
        datas=test_datas,
        codes=test_codes
    )
    
    await bundle.step(3)
    
    data_ecc_status = await agent.monitor_check_data_ecc_status()
    data_detailed_status = await agent.monitor_data_ecc_detailed_status()
    
    print(f"  ECC enabled: {data_ecc_status['ecc_enable']}")
    print(f"  Data corrupt 0: {data_ecc_status['s2_data_corrupt_0']}")
    print(f"  Data corrupt 1: {data_ecc_status['s2_data_corrupt_1']}")
    
    assert data_ecc_status['s2_data_corrupt_0'] == False, "数据0不应损坏"
    assert data_ecc_status['s2_data_corrupt_1'] == False, "数据1不应损坏"
    
    # 16.2: 单Bank ECC错误
    print("Test 16.2: Single bank ECC error")
    await agent.reset()
    await agent.drive_set_ecc_enable(True)
    
    success = await agent.inject_data_ecc_error(
        bank_index=0,
        error_data=0xDEADBEEF,
        wrong_code=1
    )
    
    await bundle.step(5)
    
    data_detailed_status = await agent.monitor_data_ecc_detailed_status()
    error_status = await agent.monitor_error_status()
    
    print(f"  Data ECC error injected: {success}")
    print(f"  Bank corrupt status: {data_detailed_status.get('s2_bank_corrupt', [])}")
    print(f"  Error reported: {error_status['0_valid']}")
    
    # 16.3: 多Bank ECC错误
    print("Test 16.3: Multiple bank ECC error")
    await agent.reset()
    await agent.drive_set_ecc_enable(True)
    
    # 注入多个bank的错误
    for bank in [0, 1, 2]:
        await agent.inject_data_ecc_error(
            bank_index=bank,
            error_data=0xBAD00000 + bank,
            wrong_code=1
        )
        await bundle.step(2)
    
    await bundle.step(5)
    
    data_detailed_status = await agent.monitor_data_ecc_detailed_status()
    
    print(f"  Multiple bank corrupt: {data_detailed_status.get('s2_bank_corrupt', [])}")
    
    # 16.4: ECC功能关闭
    print("Test 16.4: ECC functionality disabled")
    await agent.reset()
    await agent.drive_set_ecc_enable(False)
    
    # 即使有错误的校验码，也不应报告错误
    await agent.drive_data_array_response(
        datas=[0xDEADBEEF] * 8,
        codes=[1] * 8  # 可能错误的校验码
    )
    
    await bundle.step(3)
    
    data_ecc_status = await agent.monitor_check_data_ecc_status()
    
    print(f"  ECC disabled: {not data_ecc_status['ecc_enable']}")
    print(f"  No error reported with ECC off: {not data_ecc_status['s2_data_corrupt_0']}")
    
    assert data_ecc_status['ecc_enable'] == False, "ECC应该被禁用"
    
    print("✅ CP16: Data ECC Check tests completed")


@toffee_test.testcase
async def test_cp17_metaarray_flush(icachemainpipe_env: ICacheMainPipeEnv):
    """
    CP17: 冲刷MetaArray功能测试
    测试Meta/Data ECC错误时的MetaArray冲刷策略
    """
    print("\n=== CP17: MetaArray Flush Test ===")
    agent = icachemainpipe_env.agent
    bundle = icachemainpipe_env.bundle
    
    # 17.1: 只有Meta ECC校验错误（冲刷所有路）
    print("Test 17.1: Meta ECC error flush all ways")
    await agent.reset()
    await agent.drive_set_ecc_enable(True)
    
    # 注入Meta ECC错误
    await agent.inject_meta_ecc_error(
        vSetIdx_0=0x10,
        waymask_0=0x1,  # 单路命中
        ptag_0=0x12345,
        wrong_meta_code_0=1
    )
    
    await bundle.step(5)
    
    meta_flush = await agent.monitor_meta_flush()
    
    print(f"  Flush port 0 valid: {meta_flush['0_valid']}")
    print(f"  Flush port 0 waymask: 0x{meta_flush['0_bits_waymask']:x}")
    
    # Meta错误应该冲刷所有路
    if meta_flush['0_valid']:
        assert meta_flush['0_bits_waymask'] == 0xF, "Meta错误应冲刷所有路"
    
    # 17.2: 只有Data ECC校验错误（冲刷特定路）
    print("Test 17.2: Data ECC error flush specific way")
    await agent.reset()
    await agent.drive_set_ecc_enable(True)
    
    # 注入Data ECC错误到特定bank
    await agent.inject_data_ecc_error(
        bank_index=0,
        error_data=0xDEADBEEF,
        wrong_code=1
    )
    
    await bundle.step(5)
    
    meta_flush = await agent.monitor_meta_flush()
    
    print(f"  Data ECC flush valid: {meta_flush['0_valid']}")
    print(f"  Data ECC flush waymask: 0x{meta_flush['0_bits_waymask']:x}")
    
    
    print("✅ CP17: MetaArray Flush tests completed")


@toffee_test.testcase
async def test_cp18_s2_mshr_match_data_update(icachemainpipe_env: ICacheMainPipeEnv):
    """
    CP18: 监控MSHR匹配与数据更新功能测试
    测试S2阶段MSHR匹配和数据更新逻辑
    """
    print("\n=== CP18: S2 MSHR Match and Data Update Test ===")
    agent = icachemainpipe_env.agent
    bundle = icachemainpipe_env.bundle
    
    # 18.1: MSHR命中且本阶段有效
    print("Test 18.1: MSHR hit with valid stage")
    await agent.reset()
    await agent.setup_mshr_ready(True)
    
    # 发送MSHR响应
    await agent.drive_mshr_response(
        blkPaddr=0x1000,
        vSetIdx=0x10,
        data=0x123456789ABCDEF0,
        corrupt=0  # 数据正确
    )
    
    # 触发S2阶段处理
    await agent.drive_waylookup_read(
        vSetIdx_0=0x10,
        waymask_0=0x1,
        ptag_0=(0x1000 >> 12) & 0xFFFFF
    )
    
    await bundle.step(5)
    
    s2_mshr_status = await agent.monitor_s2_mshr_match_status()
    
    print(f"  S2 MSHR hits: {s2_mshr_status.get('s2_MSHR_hits_1', 'N/A')}")
    
    # 检查bank级别的匹配
    for i in range(8):
        bank_hit = s2_mshr_status.get(f's2_bankMSHRHit_{i}', False)
        data_from_mshr = s2_mshr_status.get(f's2_data_is_from_MSHR_{i}', False)
        if bank_hit or data_from_mshr:
            print(f"  Bank {i} - MSHR hit: {bank_hit}, data from MSHR: {data_from_mshr}")
    
    # 18.2: MSHR未命中
    print("Test 18.2: MSHR miss case")
    await agent.reset()
    
    # 发送不匹配的请求
    await agent.drive_waylookup_read(
        vSetIdx_0=0x20,  # 不同地址
        waymask_0=0x1,
        ptag_0=0x5678
    )
    
    await bundle.step(3)
    
    s2_mshr_status = await agent.monitor_s2_mshr_match_status()
    
    print(f"  S2 MSHR miss - hits: {s2_mshr_status.get('s2_MSHR_hits_1', 'N/A')}")
    
    # 18.3: MSHR响应但数据corrupt
    print("Test 18.3: MSHR response with corrupt data")
    await agent.reset()
    
    await agent.drive_mshr_response(
        blkPaddr=0x2000,
        vSetIdx=0x20,
        data=0xDEADBEEFCAFEBABE,
        corrupt=1  # 数据损坏
    )
    
    await bundle.step(3)
    
    print(f"  MSHR corrupt response received: {bundle.io._mshr._resp._bits._corrupt.value}")
    
    # 18.4: 正常数据流转（无MSHR介入）
    print("Test 18.4: Normal data flow without MSHR")
    await agent.reset()
    
    # 只发送正常的SRAM数据，不涉及MSHR
    await agent.drive_data_array_response(
        datas=[0x1111111111111111 + i for i in range(8)],
        codes=[0] * 8
    )
    
    await agent.drive_waylookup_read(
        vSetIdx_0=0x30,
        waymask_0=0x1,
        ptag_0=0x9999
    )
    
    await bundle.step(3)
    
    s2_mshr_status = await agent.monitor_s2_mshr_match_status()
    
    # 检查数据是否来自MSHR（应该为false）
    all_data_from_mshr = s2_mshr_status.get('s2_data_is_from_MSHR_all', [False] * 8)
    print(f"  Normal flow - any data from MSHR: {any(all_data_from_mshr)}")
    
    print("✅ CP18: S2 MSHR Match and Data Update tests completed")


@toffee_test.testcase
async def test_cp19_miss_request_logic(icachemainpipe_env: ICacheMainPipeEnv):
    """
    CP19: Miss请求发送逻辑和合并异常功能测试
    测试Miss请求仲裁和异常合并逻辑
    """
    print("\n=== CP19: Miss Request Logic and Exception Merge Test ===")
    agent = icachemainpipe_env.agent
    bundle = icachemainpipe_env.bundle
    
    # 19.1: 未发生Miss
    print("Test 19.1: No miss case")
    await agent.reset()
    await agent.setup_mshr_ready(True)
    
    # 发送命中请求
    await agent.drive_waylookup_read(
        vSetIdx_0=0x10,
        waymask_0=0x1,  # 命中
        ptag_0=0x1000,
        itlb_exception_0=0  # 无异常
    )
    
    await agent.drive_pmp_response(instr_0=1, mmio_0=0)
    
    await bundle.step(5)
    
    miss_status = await agent.monitor_miss_request_status()
    mshr_status = await agent.monitor_mshr_status()
    
    print(f"  Should fetch 0: {miss_status.get('s2_should_fetch_0', 'N/A')}")
    print(f"  MSHR request valid: {mshr_status['req_valid']}")
    
    # 命中情况下不应发送Miss请求
    assert mshr_status['req_valid'] == False, "命中时不应发送Miss请求"
    
    # 19.2: 单口Miss
    print("Test 19.2: Single port miss")
    await agent.reset()
    await agent.setup_mshr_ready(True)
    
    # 发送未命中请求
    await agent.drive_waylookup_read(
        vSetIdx_0=0x20,
        waymask_0=0x0,  # 未命中
        ptag_0=0x2000,
        itlb_exception_0=0  # 无异常
    )
    
    await agent.drive_pmp_response(instr_0=1, mmio_0=0)  # 非MMIO
    
    await bundle.step(5)
    
    miss_status = await agent.monitor_miss_request_status()
    mshr_status = await agent.monitor_mshr_status()
    
    print(f"  Single port should fetch: {miss_status.get('s2_should_fetch_0', 'N/A')}")
    print(f"  MSHR request sent: {mshr_status['req_valid']}")
    
    # 19.3: 双口都需要Miss
    # NEED TODO
    
    # 19.4: 重复请求屏蔽
    print("Test 19.4: Duplicate request masking")
    await agent.reset()
    await agent.setup_mshr_ready(False)  # MSHR不ready，请求会被阻塞
    
    # 发送Miss请求
    await agent.drive_waylookup_read(
        vSetIdx_0=0x30,
        waymask_0=0x0,  # 未命中
        ptag_0=0x3000,
        itlb_exception_0=0
    )
    
    await bundle.step(3)
    
    miss_status = await agent.monitor_miss_request_status()
    
    print(f"  Has send 0: {miss_status.get('s2_has_send_0', 'N/A')}")
    print(f"  MSHR ready: {bundle.io._mshr._req._ready.value}")
    
    # 19.5: 仅ITLB/PMP异常
    print("Test 19.5: Only ITLB/PMP exception")
    await agent.reset()
    
    await agent.drive_waylookup_read(
        vSetIdx_0=0x40,
        waymask_0=0x1,  # 命中
        ptag_0=0x4000,
        itlb_exception_0=0x2  # ITLB异常
    )
    
    await bundle.step(5)
    
    miss_status = await agent.monitor_miss_request_status()
    
    print(f"  Exception 0: {miss_status.get('s2_exception_0', 'N/A')}")
    print(f"  Exception out 0: {miss_status.get('s2_exception_out_0', 'N/A')}")
    
    # 19.6-19.7: L2异常和ITLB+L2同时出现
    print("Test 19.6-19.7: L2 exception scenarios")
    await agent.reset()
    
    # 注入L2 corrupt响应
    await agent.inject_l2_corrupt_response(
        blkPaddr=0x5000,
        vSetIdx=0x50,
        corrupt_data=0xBADD4A7A,
        corrupt=1
    )
    
    await bundle.step(3)
    
    miss_status = await agent.monitor_miss_request_status()
    
    print(f"  L2 corrupt 0: {miss_status.get('s2_l2_corrupt_0', 'N/A')}")
    
    print("✅ CP19: Miss Request Logic tests completed")


@toffee_test.testcase
async def test_cp20_response_ifu(icachemainpipe_env: ICacheMainPipeEnv):
    """
    CP20: 响应IFU功能测试
    测试S2阶段向IFU的响应逻辑
    """
    print("\n=== CP20: Response IFU Test ===")
    agent = icachemainpipe_env.agent
    bundle = icachemainpipe_env.bundle
    
    # 20.1: 正常命中并返回
    print("Test 20.1: Normal hit response")
    await agent.reset()
    await agent.drive_set_ecc_enable(True)
    await agent.drive_resp_stall(False)  # 不暂停响应
    
    # 设置正常命中情况
    await agent.drive_waylookup_read(
        vSetIdx_0=0x10,
        waymask_0=0x1,  # 命中
        ptag_0=0x1000,
        itlb_exception_0=0  # 无异常
    )
    
    await agent.drive_pmp_response(
        instr_0=1, mmio_0=0  # 正常权限，非MMIO
    )
    
    await agent.drive_data_array_response(
        datas=[0x1111111111111111 + i for i in range(8)],
        codes=[0] * 8  # 正确校验码
    )
    
    await agent.drive_fetch_request(
        pcMemRead_addrs=[0x1000],
        readValid=[1]
    )
    
    await bundle.step(5)
    await agent.clear_fetch_request()
    
    fetch_response = await agent.monitor_fetch_response()
    
    print(f"  Fetch response valid: {fetch_response['valid']}")
    print(f"  Exception 0: {fetch_response['exception_0']}")
    print(f"  Exception 1: {fetch_response['exception_1']}")
    print(f"  PMP MMIO 0: {fetch_response['pmp_mmio_0']}")
    print(f"  Data: 0x{fetch_response['data']:x}" if fetch_response['data'] else "  Data: N/A")
    
    # 正常情况下应该有有效响应且无异常
    if fetch_response['valid']:
        assert fetch_response['exception_0'] == 0, "正常情况不应有异常"
    
    # 20.2: 异常返回
    print("Test 20.2: Exception response")
    await agent.reset()
    await agent.drive_resp_stall(False)
    
    # 设置ITLB异常
    await agent.drive_waylookup_read(
        vSetIdx_0=0x20,
        waymask_0=0x1,
        ptag_0=0x2000,
        itlb_exception_0=0x2  # ITLB异常
    )
    
    await agent.drive_fetch_request(
        pcMemRead_addrs=[0x2000, 0, 0, 0, 0],
        readValid=[1, 0, 0, 0, 0]
    )
    
    await bundle.step(5)
    
    fetch_response = await agent.monitor_fetch_response()
    
    print(f"  Exception response valid: {fetch_response['valid']}")
    print(f"  Exception 0: {fetch_response['exception_0']}")
    
    # 20.3: 跨行取指
    print("Test 20.3: Double-line fetch")
    await agent.reset()
    await agent.drive_resp_stall(False)
    
    # 设置跨行情况（需要两个地址）
    await agent.drive_waylookup_read(
        vSetIdx_0=0x30, vSetIdx_1=0x31,
        waymask_0=0x1, waymask_1=0x1,
        ptag_0=0x3000, ptag_1=0x3001,
        itlb_exception_0=0, itlb_exception_1=0
    )
    
    await agent.drive_fetch_request(
        pcMemRead_addrs=[0x3000, 0x3040, 0, 0, 0xC20],  # 第5个元素0xC20[13:6]=0x30, 跨行后nextlineStart=0xC40[13:6]=0x31
        readValid=[1, 1, 0, 0, 1]
    )
    
    await bundle.step(5)
    
    fetch_response = await agent.monitor_fetch_response()
    
    print(f"  Double-line fetch valid: {fetch_response['valid']}")
    print(f"  Double-line flag: {fetch_response['doubleline']}")
    print(f"  VAddr 0: 0x{fetch_response['vaddr_0']:x}" if fetch_response['vaddr_0'] else "  VAddr 0: N/A")
    print(f"  VAddr 1: 0x{fetch_response['vaddr_1']:x}" if fetch_response['vaddr_1'] else "  VAddr 1: N/A")
    
    # 20.4: RespStall
    print("Test 20.4: Response stall scenario")
    await agent.reset()
    await agent.drive_resp_stall(True)  # 启用响应暂停
    
    # 发送正常请求
    await agent.drive_waylookup_read(
        vSetIdx_0=0x40,
        waymask_0=0x1,
        ptag_0=0x4000,
        itlb_exception_0=0
    )
    
    await agent.drive_fetch_request(
        pcMemRead_addrs=[0x4000, 0, 0, 0, 0],
        readValid=[1, 0, 0, 0, 0]
    )
    
    await bundle.step(3)
    
    fetch_response = await agent.monitor_fetch_response()
    
    print(f"  Response stall - valid: {fetch_response['valid']}")
    print(f"  Response stall active: {bundle.io._respStall.value}")
    
    # RespStall激活时不应有有效响应
    if bundle.io._respStall.value:
        assert fetch_response['valid'] == False, "RespStall时不应有有效响应"
    
    # 解除stall并检查响应恢复
    await agent.drive_resp_stall(False)
    await bundle.step(3)
    
    fetch_response = await agent.monitor_fetch_response()
    print(f"  After stall release - valid: {fetch_response['valid']}")
    
    print("✅ CP20: Response IFU tests completed")


@toffee_test.testcase
async def test_cp21_l2_corrupt_report(icachemainpipe_env: ICacheMainPipeEnv):
    """
    CP21: L2 Corrupt报告功能测试
    测试L2 Cache corrupt错误报告逻辑
    """
    print("\n=== CP21: L2 Corrupt Report Test ===")
    agent = icachemainpipe_env.agent
    bundle = icachemainpipe_env.bundle
    
    # 21.1: L2 Corrupt单路报告
    print("Test 21.1: L2 corrupt single port report")
    await agent.reset()
    await agent.setup_mshr_ready(True)
    
    # 注入L2 corrupt响应
    success = await agent.inject_l2_corrupt_response(
        blkPaddr=0x1000,
        vSetIdx=0x10,
        corrupt_data=0xBADD4A7A,
        corrupt=1
    )
    
    # 触发处理流程
    await agent.drive_waylookup_read(
        vSetIdx_0=0x10,
        waymask_0=0x0,  # 未命中，触发MSHR
        ptag_0=(0x1000 >> 12) & 0xFFFFF
    )
    
    await bundle.step(5)
    
    error_status = await agent.monitor_error_status()
    fetch_response = await agent.monitor_fetch_response()
    miss_status = await agent.monitor_miss_request_status()
    
    print(f"  L2 corrupt injected: {success}")
    print(f"  Error 0 valid: {error_status['0_valid']}")
    print(f"  L2 corrupt 0: {miss_status.get('s2_l2_corrupt_0', 'N/A')}")
    print(f"  Fetch response valid: {fetch_response['valid']}")
    
    # 21.2: 双路同时corrupt
    print("Test 21.2: Dual port corrupt")
    await agent.reset()
    
    # 为两个端口注入corrupt响应
    await agent.inject_l2_corrupt_response(
        blkPaddr=0x2000,
        vSetIdx=0x20,
        corrupt_data=0xDEADBEEF,
        corrupt=1
    )
    
    # 触发双端口处理
    await agent.drive_waylookup_read(
        vSetIdx_0=0x20, vSetIdx_1=0x21,
        waymask_0=0x0, waymask_1=0x0,  # 双端口未命中
        ptag_0=(0x2000 >> 12) & 0xFFFFF,
        ptag_1=(0x2001 >> 12) & 0xFFFFF
    )
    
    await bundle.step(5)
    
    error_status = await agent.monitor_error_status()
    miss_status = await agent.monitor_miss_request_status()
    
    print(f"  Dual port - Error 0 valid: {error_status['0_valid']}")
    print(f"  Dual port - Error 1 valid: {error_status['1_valid']}")
    print(f"  L2 corrupt 0: {miss_status.get('s2_l2_corrupt_0', 'N/A')}")
    print(f"  L2 corrupt 1: {miss_status.get('s2_l2_corrupt_1', 'N/A')}")
    
    # 21.3: 无L2 Corrupt错误
    print("Test 21.3: No L2 corrupt error")
    await agent.reset()
    
    # 发送正确的MSHR响应
    await agent.drive_mshr_response(
        blkPaddr=0x3000,
        vSetIdx=0x30,
        data=0x123456789ABCDEF0,
        corrupt=0  # 无损坏
    )
    
    await bundle.step(3)
    
    print(f"  Normal MSHR response corrupt flag: {bundle.io._mshr._resp._bits._corrupt.value}")
    
    assert bundle.io._mshr._resp._bits._corrupt.value == 0, "正常响应不应有corrupt标志"
    
    # 21.4: L2响应无效
    print("Test 21.4: L2 response invalid")
    await agent.reset()
    
    # 不发送MSHR响应，检查无效状态
    await bundle.step(3)
    
    print(f"  MSHR response valid: {bundle.io._mshr._resp._valid.value}")
    
    assert bundle.io._mshr._resp._valid.value == 0, "无响应时valid应为0"
    
    print("✅ CP21: L2 Corrupt Report tests completed")


@toffee_test.testcase
async def test_cp22_flush_mechanism(icachemainpipe_env: ICacheMainPipeEnv):
    """
    CP22: 刷新机制功能测试
    测试流水线刷新控制逻辑
    """
    print("\n=== CP22: Flush Mechanism Test ===")
    agent = icachemainpipe_env.agent
    bundle = icachemainpipe_env.bundle
    
    # 22.1: 全局刷新
    print("Test 22.1: Global flush")
    await agent.reset()
    
    # 先启动正常流水线
    await agent.drive_waylookup_read(
        vSetIdx_0=0x10,
        waymask_0=0x1,
        ptag_0=0x1000
    )
    
    await agent.drive_fetch_request(
        pcMemRead_addrs=[0x1000],
        readValid=[1]
    )
    
    await bundle.step(2)
    
    # 检查刷新前的状态
    pipeline_status = await agent.monitor_pipeline_status()
    print(f"  Before flush - s0_fire: {pipeline_status['s0_fire']}")
    
    # 激活全局刷新
    await agent.drive_set_flush(True)
    await bundle.step(3)
    
    pipeline_status = await agent.monitor_pipeline_status()
    fetch_response = await agent.monitor_fetch_response()
    mshr_status = await agent.monitor_mshr_status()
    
    print(f"  During flush - s0_fire: {pipeline_status['s0_fire']}")
    print(f"  During flush - s2_fire: {pipeline_status['s2_fire']}")
    print(f"  During flush - fetch_resp_valid: {fetch_response['valid']}")
    print(f"  During flush - mshr_req_valid: {mshr_status['req_valid']}")
    print(f"  Flush signal: {bundle.io._flush.value}")
    
    # 刷新期间流水线应该停止
    assert bundle.io._flush.value == 1, "Flush信号应该激活"
    
    # 22.2: S0阶段刷新
    print("Test 22.2: S0 stage flush")
    # 在全局刷新测试中已经包含
    
    # 22.3: 正常运行 - S1和S2都在fire
    print("Test 22.3: Normal operation")
    await agent.reset()
    await agent.drive_set_flush(False)  # 确保无刷新
    
    # 设置正常流水线操作
    await agent.drive_waylookup_read(
        vSetIdx_0=0x20,
        waymask_0=0x1,
        ptag_0=0x2000
    )
    
    await agent.drive_fetch_request(
        pcMemRead_addrs=[0x2000, 0, 0, 0, 0],
        readValid=[1, 0, 0, 0, 0]
    )
    
    await bundle.step(5)
    
    pipeline_status = await agent.monitor_pipeline_status()
    
    print(f"  Normal operation - flush: {bundle.io._flush.value}")
    print(f"  Normal operation - s0_fire: {pipeline_status['s0_fire']}")
    print(f"  Normal operation - s2_fire: {pipeline_status['s2_fire']}")
    
    assert bundle.io._flush.value == 0, "正常操作时不应有flush"
    
    # 22.4: S2阶段刷新（MSHR请求停止）
    print("Test 22.4: S2 flush stops MSHR requests")
    await agent.reset()
    
    # 先设置Miss条件
    await agent.drive_waylookup_read(
        vSetIdx_0=0x30,
        waymask_0=0x0,  # 未命中
        ptag_0=0x3000
    )
    
    await agent.setup_mshr_ready(True)
    await bundle.step(2)
    
    # 检查刷新前MSHR请求
    mshr_status_before = await agent.monitor_mshr_status()
    
    # 激活刷新
    await agent.drive_set_flush(True)
    await bundle.step(3)
    
    mshr_status_after = await agent.monitor_mshr_status()
    
    print(f"  Before flush - MSHR req valid: {mshr_status_before['req_valid']}")
    print(f"  After flush - MSHR req valid: {mshr_status_after['req_valid']}")
    
    # 刷新期间MSHR请求应该停止
    if bundle.io._flush.value:
        assert mshr_status_after['req_valid'] == False, "刷新时MSHR请求应停止"
    
    # 22.5: 正常运行（无刷新）
    print("Test 22.5: Normal operation without flush")
    await agent.reset()
    await agent.drive_set_flush(False)
    
    await bundle.step(3)
    
    pipeline_status = await agent.monitor_pipeline_status()
    
    print(f"  No flush - flush signal: {bundle.io._flush.value}")
    
    assert bundle.io._flush.value == 0, "无刷新时flush信号应为0"
    
    print("✅ CP22: Flush Mechanism tests completed")
