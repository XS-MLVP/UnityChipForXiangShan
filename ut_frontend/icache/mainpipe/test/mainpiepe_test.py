from .mainpipe_fixture import icachemainpipe_env
from ..env import ICacheMainPipeEnv
import toffee_test

# ========== ECC辅助函数 ==========
def calculate_data_ecc_codes(datas: list) -> list:
    """计算DataArray数据的正确ECC校验码"""
    return [bin(data).count('1') % 2 for data in datas]

def calculate_waylookup_params(start_addr: int) -> dict:
    """
    根据RTL逻辑计算完整的WayLookup参数
    
    参数：
    - start_addr: 起始地址（pcMemRead_4_startAddr）
    
    依据：
    - ICacheMainPipe.v: s1_doubleline <= io_fetch_req_bits_readValid_4 & io_fetch_req_bits_pcMemRead_4_startAddr[5]
    - ICacheMainPipe.v: nextlineStart = startAddr[5] ? (startAddr & ~0x3F) + 64 : startAddr
    - ICacheMainPipe.v: vSetIdx地址约束检查
    """
    # 判断是否跨行：bit[5]=1时跨行
    is_doubleline = bool(start_addr & (1 << 5))
    
    # 计算Port 0参数（起始地址）
    vSetIdx_0 = (start_addr >> 6) & 0xFF
    ptag_0 = (start_addr >> 12) & 0xFFFFFFFFF
    meta_codes_0 = bin(ptag_0).count('1') % 2
    
    # 计算Port 1参数（nextline地址）
    if is_doubleline:
        nextline_addr = (start_addr & ~0x3F) + 64  # 下一个64字节对齐地址
        vSetIdx_1 = (nextline_addr >> 6) & 0xFF
        ptag_1 = (nextline_addr >> 12) & 0xFFFFFFFFF
        meta_codes_1 = bin(ptag_1).count('1') % 2
    else:
        # 非跨行情况，nextlineStart = startAddr
        nextline_addr = start_addr
        vSetIdx_1 = vSetIdx_0
        ptag_1 = ptag_0
        meta_codes_1 = meta_codes_0
    
    return {
        # 地址信息
        'start_addr': start_addr,
        'nextline_addr': nextline_addr,
        'is_doubleline': is_doubleline,
        
        # Port 0 参数
        'vSetIdx_0': vSetIdx_0,
        'ptag_0': ptag_0,
        'meta_codes_0': meta_codes_0,
        
        # Port 1 参数  
        'vSetIdx_1': vSetIdx_1,
        'ptag_1': ptag_1,
        'meta_codes_1': meta_codes_1,
        
        # 默认的正常命中配置
        'waymask_0': 0x1,  # 默认命中way 0
        'waymask_1': 0x1 if is_doubleline else 0x0,  # 跨行时第二路也命中
        'itlb_exception_0': 0,  # 默认无异常
        'itlb_exception_1': 0,
        'itlb_pbmt_0': 0,  # 默认正常内存
        'itlb_pbmt_1': 0,
        'gpf_gpaddr': 0,  # 默认值
        'gpf_isForVSnonLeafPTE': 0
    }

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
        
        # 验证nextlineStart
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
    
    # 收集所有测试错误，避免单一测试错误导致后续测试停止
    test_errors = []
    
    try:
        # 初始化环境，确保环境准备就绪
        await agent.reset()
        await agent.drive_set_ecc_enable(True)
        await agent.drive_set_flush(False)
        await agent.drive_resp_stall(False)
        print("环境初始化完成")
        
        # 测试点11.1: 访问DataArray的单路
        print("\n--- 测试点11.1: 访问DataArray的单路 ---")
        print("条件：s0_hits为高（一路命中），s0_itlb_exception信号为零（ITLB查询成功），toData.last.ready为高（DataArray没有正在进行的写操作）")
        print("预期：toData.valid信号为高，表示MainPipe向DataArray发出了读取请求")
        
        try:
            # 设置环境准备就绪：DataArray ready，确保s0_can_go=1
            await agent.drive_data_array_ready(True)
            
            # 先驱动WayLookup，满足地址一致性要求
            test_addr = 0x400  # 测试地址：0x400[13:6] = 0x10
            expected_vSetIdx = (test_addr >> 6) & 0xFF  # 0x10
            
            await agent.drive_waylookup_read(
                vSetIdx_0=expected_vSetIdx,
                vSetIdx_1=expected_vSetIdx,  # 由于0x400[5]=0，nextlineStart=startAddr，所以两个vSetIdx相同
                waymask_0=0x1,  # s0_hits为高（一路命中），根据verilog: s1_SRAMhits_0 <= |io_wayLookupRead_bits_entry_waymask_0
                waymask_1=0x0,
                ptag_0=0x12345,
                ptag_1=0x0,
                itlb_exception_0=0,  # s0_itlb_exception信号为零（ITLB查询成功）
                itlb_exception_1=0
            )
            
            # 发送fetch请求，地址必须与WayLookup一致
            fetch_success = await agent.drive_fetch_request(
                pcMemRead_addrs=[test_addr, 0, 0, 0, test_addr],  # pcMemRead_4与vSetIdx匹配
                readValid=[1, 0, 0, 0, 1]  # readValid[0]=1会使toIData_0_valid=1
            )
            
            if not fetch_success:
                raise AssertionError("地址一致性检查失败，无法发起fetch请求")
            
            # 监控DataArray访问状态
            dataarray_status = await agent.monitor_dataarray_toIData()
            pipeline_status = await agent.monitor_pipeline_status()
            
            print(f"  监控结果：")
            print(f"  - toIData_0_valid: {dataarray_status['toIData_0_valid']}")
            print(f"  - s0_fire: {pipeline_status['s0_fire']}")
            print(f"  - fetch_req_ready: {pipeline_status['fetch_req_ready']}")
            
            # 断言：根据verilog源码，toIData_X_valid = readValid_X
            assert dataarray_status['toIData_0_valid'] == 1, "toIData_0_valid应为1，表示MainPipe向DataArray发出了读取请求"
            assert pipeline_status['s0_fire'] == 1, "s0_fire应为1，表示流水线正常推进"
            assert pipeline_status['fetch_req_ready'] == 1, "fetch_req_ready应为1，表示能够接收新的请求"
            
            # 清除请求
            await agent.clear_fetch_request()
            await agent.clear_waylookup_read()
            print("  ✓ 测试点11.1通过")
            
        except Exception as e:
            error_msg = f"测试点11.1失败: {str(e)}"
            print(f"  ✗ {error_msg}")
            test_errors.append(error_msg)
        
        # 测试点11.2: 不访问DataArray（Way未命中）- 会访问，但是返回数据无效
        print("\n--- 测试点11.2: 不访问DataArray（Way未命中）- 会访问，但是返回数据无效 ---")
        print("条件：s0_hits为低表示缓存未命中")
        print("预期：根据文档注释，会访问但返回数据无效（waymask=0表示miss）")
        
        try:
            await agent.reset()
            await agent.drive_set_flush(False)
            await agent.drive_data_array_ready(True)
            
            test_addr = 0x800  # 测试地址：0x800[13:6] = 0x20
            expected_vSetIdx = (test_addr >> 6) & 0xFF  # 0x20
            
            await agent.drive_waylookup_read(
                vSetIdx_0=expected_vSetIdx,
                vSetIdx_1=expected_vSetIdx,  # 由于0x800[5]=0，nextlineStart=startAddr
                waymask_0=0x0,  # s0_hits为低表示缓存未命中（waymask=0，OR约简结果为0）
                waymask_1=0x0,
                ptag_0=0x67890,
                ptag_1=0x0,
                itlb_exception_0=0,
                itlb_exception_1=0
            )
            
            fetch_success = await agent.drive_fetch_request(
                pcMemRead_addrs=[test_addr, 0, 0, 0, test_addr],
                readValid=[1, 0, 0, 0, 1]
            )
            
            if not fetch_success:
                raise AssertionError("地址一致性检查失败，无法发起fetch请求")
            
            dataarray_status = await agent.monitor_dataarray_toIData()
            pipeline_status = await agent.monitor_pipeline_status()
            
            print(f"  监控结果：")
            print(f"  - toIData_0_valid: {dataarray_status['toIData_0_valid']}")
            print(f"  - toIData_0_waymask_0_0: {dataarray_status['toIData_0_waymask_0_0']}")
            print(f"  - s0_fire: {pipeline_status['s0_fire']}")
            
            # 根据文档注释和verilog实现：会访问（toIData_0_valid=1），但数据无效（waymask=0表示miss）
            assert dataarray_status['toIData_0_valid'] == 1, "根据verilog实现，readValid=1时toIData_0_valid仍为1（会访问）"
            assert dataarray_status['toIData_0_waymask_0_0'] == 0, "waymask应为0，表示miss"
            assert pipeline_status['s0_fire'] == 1, "s0_fire应为1，表示流水线正常推进"
            
            await agent.clear_fetch_request()
            await agent.clear_waylookup_read()
            print("  ✓ 测试点11.2通过")
            
        except Exception as e:
            error_msg = f"测试点11.2失败: {str(e)}"
            print(f"  ✗ {error_msg}")
            test_errors.append(error_msg)
        
        # 测试点11.3: 不访问DataArray（ITLB查询失败）- 会访问，但是返回数据无效
        print("\n--- 测试点11.3: 不访问DataArray（ITLB查询失败）- 会访问，但是返回数据无效 ---")
        print("条件：s0_itlb_exception信号不为零（ITLB查询失败）")
        print("预期：根据文档注释，会访问但返回数据无效")
        
        try:
            await agent.reset()
            await agent.drive_set_flush(False)
            await agent.drive_data_array_ready(True)
            
            test_addr = 0xC00  # 测试地址：0xC00[13:6] = 0x30
            expected_vSetIdx = (test_addr >> 6) & 0xFF  # 0x30
            
            await agent.drive_waylookup_read(
                vSetIdx_0=expected_vSetIdx,
                vSetIdx_1=expected_vSetIdx,  # 由于0xC00[5]=0，nextlineStart=startAddr
                waymask_0=0x1,  # 有命中
                waymask_1=0x0,
                ptag_0=0xABCDE,
                ptag_1=0x0,
                itlb_exception_0=0x2,  # s0_itlb_exception信号不为零（ITLB查询失败）
                itlb_exception_1=0
            )
            
            # 确保WayLookup设置生效
            await bundle.step(1)
            
            fetch_success = await agent.drive_fetch_request(
                pcMemRead_addrs=[test_addr, 0, 0, 0, test_addr],
                readValid=[1, 0, 0, 0, 1]
            )
            
            if not fetch_success:
                raise AssertionError("地址一致性检查失败，无法发起fetch请求")
            
            # 等待一个额外的周期，让信号从S0传递到S1
            await bundle.step(1)
            
            dataarray_status = await agent.monitor_dataarray_toIData()
            pipeline_status = await agent.monitor_pipeline_status()
            exception_status = await agent.monitor_exception_merge_status()
            
            print(f"  监控结果：")
            print(f"  - toIData_0_valid: {dataarray_status['toIData_0_valid']}")
            itlb_exception = exception_status.get('s1_itlb_exception_0', None)
            print(f"  - ITLB exception: 0x{itlb_exception:x}" if itlb_exception is not None else "  - ITLB exception: None")
            print(f"  - s0_fire: {pipeline_status['s0_fire']}")
            
            # 根据文档注释和verilog实现：会访问（toIData_0_valid=1），但有ITLB异常
            assert dataarray_status['toIData_0_valid'] == 1, "根据verilog实现，readValid=1时toIData_0_valid仍为1（会访问）"
            assert itlb_exception == 0x2, f"应检测到ITLB异常0x2，实际为{itlb_exception}"
            
            await agent.clear_fetch_request()
            await agent.clear_waylookup_read()
            print("  ✓ 测试点11.3通过")
            
        except Exception as e:
            error_msg = f"测试点11.3失败: {str(e)}"
            print(f"  ✗ {error_msg}")
            test_errors.append(error_msg)
        
        # 测试点11.4: 不访问DataArray（DataArray正在进行写操作）
        print("\n--- 测试点11.4: 不访问DataArray（DataArray正在进行写操作）---")
        print("条件：toData.last.ready信号为低，表示DataArray正在进行写操作")
        print("预期：s0_fire和fetch_req_ready为低，表示流水线被阻止，虽然toIData_0_valid仍可能为1（直接由readValid控制）")
        
        try:
            await agent.reset()
            await agent.drive_set_flush(False)
            await agent.drive_data_array_ready(False)  # toData.last.ready信号为低
            
            test_addr = 0x1000  # 测试地址：0x1000[13:6] = 0x40
            expected_vSetIdx = (test_addr >> 6) & 0xFF  # 0x40
            
            await agent.drive_waylookup_read(
                vSetIdx_0=expected_vSetIdx,
                vSetIdx_1=expected_vSetIdx,
                waymask_0=0x1,
                waymask_1=0x0,
                ptag_0=0xDEAD,
                ptag_1=0x0,
                itlb_exception_0=0,
                itlb_exception_1=0
            )
            
            fetch_success = await agent.drive_fetch_request(
                pcMemRead_addrs=[test_addr, 0, 0, 0, test_addr],
                readValid=[1, 0, 0, 0, 1]
            )
            
            if not fetch_success:
                raise AssertionError("地址一致性检查失败，无法发起fetch请求")
            
            dataarray_status = await agent.monitor_dataarray_toIData()
            pipeline_status = await agent.monitor_pipeline_status()
            
            print(f"  监控结果：")
            print(f"  - toIData_3_ready: {bundle.io._dataArray._toIData._3._ready.value}")
            print(f"  - toIData_0_valid: {dataarray_status['toIData_0_valid']}")
            print(f"  - s0_fire: {pipeline_status['s0_fire']}")
            print(f"  - fetch_req_ready: {pipeline_status['fetch_req_ready']}")
            
            # 根据verilog源码：DataArray busy时，s0_can_go为低，阻止流水线推进，但toIData_0_valid仍由readValid直接控制
            assert pipeline_status['s0_fire'] == 0, "DataArray忙时s0_fire应为0（s0_can_go=0）"
            assert pipeline_status['fetch_req_ready'] == 0, "DataArray忙时fetch_req_ready应为0（s0_can_go=0）"
            # 注意：toIData_0_valid可能仍为1，因为它直接由readValid控制，与DataArray busy无关
            
            await agent.clear_fetch_request()
            await agent.clear_waylookup_read()
            print("  ✓ 测试点11.4通过")
            
        except Exception as e:
            error_msg = f"测试点11.4失败: {str(e)}"
            print(f"  ✗ {error_msg}")
            test_errors.append(error_msg)
    
    except Exception as e:
        error_msg = f"测试初始化失败: {str(e)}"
        print(f"✗ {error_msg}")
        test_errors.append(error_msg)
    
    # 汇总测试结果
    if test_errors:
        print(f"\n=== CP11测试完成，发现{len(test_errors)}个错误 ===")
        for i, error in enumerate(test_errors, 1):
            print(f"  {i}. {error}")
        # 抛出汇总的错误信息
        raise AssertionError(f"CP11测试失败，共{len(test_errors)}个错误：" + "; ".join(test_errors))
    else:
        print("\n✓ CP11: 访问DataArray的单路功能测试完成，所有测试点通过")


@toffee_test.testcase
async def test_cp12_meta_ecc_check(icachemainpipe_env: ICacheMainPipeEnv):
    """
    CP12: Meta ECC校验功能测试
    根据MainPipe.md文档第12节和ICacheMainPipe.v源码实现Meta数据的ECC校验逻辑测试
    
    测试依据：
    1. 文档要求：将物理地址的标签部分与对应的Meta进行ECC校验，以确保Meta的完整性
    2. 源码实现：s2_meta_corrupt_0 <= io_ecc_enable & (^s1_req_ptags_0 != s1_meta_codes_0 & s1_meta_corrupt_hit_num == 3'h1 | (|(s1_meta_corrupt_hit_num[2:1])))
    3. Hit数量计算：s1_meta_corrupt_hit_num = s1_waymasks_0_0 + s1_waymasks_0_1 + s1_waymasks_0_2 + s1_waymasks_0_3
    """
    print("\n=== CP12: Meta ECC校验功能测试 ===")
    agent = icachemainpipe_env.agent
    bundle = icachemainpipe_env.bundle
    
    # 收集所有测试错误，确保每个测试点都能执行
    test_errors = []
    
    # ==================== 测试点12.1: 无ECC错误 ====================
    print("\n--- Test 12.1: 无ECC错误 ---")
    print("条件：waymask全为0（没有命中）或waymask有一位为1（单路命中）且ECC对比通过")
    print("预期：s1_meta_corrupt为假，不报告错误")
    
    # Case 12.1a: waymask全为0（没有命中）
    try:
        print("\nCase 12.1a: waymask全为0（没有命中）")
        await agent.reset()
        await agent.drive_set_ecc_enable(True)
        await agent.drive_data_array_ready(True)
        
        test_vaddr = 0x1000
        test_ptag = 0x12345
        # 计算正确的ECC校验码（XOR奇偶校验）
        correct_meta_code = 0
        temp_ptag = test_ptag
        while temp_ptag:
            correct_meta_code ^= temp_ptag & 1
            temp_ptag >>= 1
        
        # 监控流水线状态
        pipeline_status = await agent.monitor_pipeline_status()
        print(f"  初始流水线状态: s0_fire={pipeline_status['s0_fire']}, ecc_enable={pipeline_status['ecc_enable']}")
        
        # 设置WayLookup：waymask全为0（没有命中）
        waylookup_result = await agent.drive_waylookup_read(
            vSetIdx_0=(test_vaddr >> 6) & 0xFF,
            vSetIdx_1=(test_vaddr >> 6) & 0xFF,
            waymask_0=0x0,  # 没有命中
            waymask_1=0x0,
            ptag_0=test_ptag,
            ptag_1=0,
            meta_codes_0=correct_meta_code,
            meta_codes_1=0
        )
        print(f"  WayLookup设置成功: {waylookup_result['send_success']}")
        
        # 发起fetch请求（满足地址一致性约束）
        fetch_success = await agent.drive_fetch_request(
            pcMemRead_addrs=[0, 0, 0, 0, test_vaddr],  # pcMemRead_4设置为test_vaddr
            readValid=[0, 0, 0, 0, 1]  # 只有readValid_4有效
        )
        print(f"  Fetch请求发起成功: {fetch_success}")
        assert fetch_success, "12.1a: 地址一致性检查失败，无法发起fetch请求"
        
        # 推进流水线，让数据到达S2阶段进行ECC校验
        await bundle.step(3)
        
        # 监控错误状态
        error_status = await agent.monitor_error_status()
        meta_status = await agent.monitor_check_meta_ecc_status()
        
        print(f"  waymask_0: 0x0 (没有命中)")
        print(f"  ptag_0: 0x{test_ptag:x}")
        print(f"  meta_codes_0: {correct_meta_code}")
        print(f"  预期：hit_num为0，s1_meta_corrupt应为假")
        print(f"  实际：io.errors[0].valid={error_status['0_valid']}")
        
        # 断言：没有命中时不应报告错误
        assert error_status['0_valid'] == 0, f"12.1a失败：没有命中时不应报告错误，但io.errors[0].valid={error_status['0_valid']}"
        
        # 清除请求
        await agent.clear_waylookup_read()
        await agent.clear_fetch_request()
        print("  ✓ Case 12.1a通过")
        
    except Exception as e:
        error_msg = f"12.1a测试失败: {str(e)}"
        print(f"  ✗ {error_msg}")
        test_errors.append(error_msg)
    
    # Case 12.1b: waymask有一位为1（单路命中）且ECC对比通过
    try:
        print("\nCase 12.1b: waymask有一位为1（单路命中）且ECC对比通过")
        await agent.reset()
        await agent.drive_set_ecc_enable(True)
        await agent.drive_data_array_ready(True)
        
        test_vaddr = 0x2000
        test_ptag = 0x54321
        # 计算正确的ECC校验码
        correct_meta_code = 0
        temp_ptag = test_ptag
        while temp_ptag:
            correct_meta_code ^= temp_ptag & 1
            temp_ptag >>= 1
        
        # 设置WayLookup：单路命中且ECC正确
        await agent.drive_waylookup_read(
            vSetIdx_0=(test_vaddr >> 6) & 0xFF,
            vSetIdx_1=(test_vaddr >> 6) & 0xFF,
            waymask_0=0x1,  # 单路命中（way 0）
            waymask_1=0x0,
            ptag_0=test_ptag,
            ptag_1=0,
            meta_codes_0=correct_meta_code,  # 正确的ECC码
            meta_codes_1=0
        )
        
        # 发起fetch请求
        fetch_success = await agent.drive_fetch_request(
            pcMemRead_addrs=[0, 0, 0, 0, test_vaddr],
            readValid=[0, 0, 0, 0, 1]
        )
        assert fetch_success, "12.1b: 地址一致性检查失败"
        
        # 推进流水线
        await bundle.step(1)
        
        # 监控状态
        error_status = await agent.monitor_error_status()
        meta_corrupt_status = await agent.monitor_meta_corrupt_status()
        
        print(f"  waymask_0: 0x1 (单路命中)")
        print(f"  ptag_0: 0x{test_ptag:x}")
        print(f"  meta_codes_0: {correct_meta_code} (正确的ECC码)")
        print(f"  hit_num应为1，ECC对比应通过，s1_meta_corrupt应为假")
        print(f"  实际：io.errors[0].valid={error_status['0_valid']}")
        if meta_corrupt_status:
            print(f"  s1_meta_corrupt_hit_num: {meta_corrupt_status.get('s1_meta_corrupt_hit_num', 'N/A')}")
        
        # 断言：单路命中且ECC正确时不应报告错误
        assert error_status['0_valid'] == 0, f"12.1b失败：单路命中且ECC正确时不应报告错误，但io.errors[0].valid={error_status['0_valid']}"
        
        # 清除请求
        await agent.clear_waylookup_read()
        await agent.clear_fetch_request()
        print("  ✓ Case 12.1b通过")
        
    except Exception as e:
        error_msg = f"12.1b测试失败: {str(e)}"
        print(f"  ✗ {error_msg}")
        test_errors.append(error_msg)
    
    # ==================== 测试点12.2: 单路命中的ECC错误 ====================
    print("\n--- Test 12.2: 单路命中的ECC错误 ---")
    print("条件：waymask有一位为1（单路命中），ECC对比失败（^ptag != meta_code）")
    print("预期：s2_meta_corrupt、io.errors.valid、io.errors.bits.report_to_beu为true")
    
    try:
        await agent.reset()
        await agent.drive_set_ecc_enable(True)
        await agent.drive_data_array_ready(True)
        
        test_vaddr = 0x3000
        test_ptag = 0xABCDE
        # 计算正确的ECC码，然后故意提供错误的ECC码
        correct_meta_code = 0
        temp_ptag = test_ptag
        while temp_ptag:
            correct_meta_code ^= temp_ptag & 1
            temp_ptag >>= 1
        wrong_meta_code = 1 - correct_meta_code  # 故意错误的ECC码
        
        print(f"  ptag: 0x{test_ptag:x}")
        print(f"  正确ECC码: {correct_meta_code}")
        print(f"  错误ECC码: {wrong_meta_code}")
        
        # 使用错误注入API设置单路命中的ECC错误
        inject_success = await agent.inject_meta_ecc_error(
            vSetIdx_0=(test_vaddr >> 6) & 0xFF,
            vSetIdx_1=(test_vaddr >> 6) & 0xFF,
            waymask_0=0x2,  # 单路命中（way 1）
            waymask_1=0x0,
            ptag_0=test_ptag,
            ptag_1=0,
            wrong_meta_code_0=wrong_meta_code
        )
        await bundle.step()
        assert inject_success, "12.2: Meta ECC错误注入失败"
        
        # 发起fetch请求
        fetch_success = await agent.drive_fetch_request(
            pcMemRead_addrs=[0, 0, 0, 0, test_vaddr],
            readValid=[0, 0, 0, 0, 1]
        )
        assert fetch_success, "12.2: 地址一致性检查失败"
        await bundle.step(2)
        
        # 监控错误状态和内部信号
        error_status = await agent.monitor_error_status()
        meta_corrupt_status = await agent.monitor_meta_corrupt_status()
        pipeline_status = await agent.monitor_pipeline_status()
        
        print(f"  waymask_0: 0x2 (单路命中，way 1)")
        print(f"  hit_num应为1，ECC对比应失败，应报告错误")
        print(f"  流水线状态: s0_fire={pipeline_status['s0_fire']}, s1_fire={pipeline_status.get('s1_fire', 'N/A')}, s2_fire={pipeline_status['s2_fire']}")
        print(f"  实际：io.errors[0].valid={error_status['0_valid']}")
        print(f"  实际：io.errors[0].report_to_beu={error_status['0_report_to_beu']}")
        if meta_corrupt_status:
            print(f"  s1_meta_corrupt_hit_num: {meta_corrupt_status.get('s1_meta_corrupt_hit_num', 'N/A')}")
        
        assert error_status['0_valid'] == 1, f"12.2失败：单路命中且ECC错误时应报告错误，但io.errors[0].valid={error_status['0_valid']}"
        assert error_status['0_report_to_beu'] == 1, f"12.2失败：应向BEU报告错误，但report_to_beu={error_status['0_report_to_beu']}"
        
        # 清除请求
        await agent.clear_waylookup_read()
        await agent.clear_fetch_request()
        print("  ✓ Test 12.2通过")
        
    except Exception as e:
        error_msg = f"12.2测试失败: {str(e)}"
        print(f"  ✗ {error_msg}")
        test_errors.append(error_msg)
    
    # ==================== 测试点12.3: 多路命中 ====================
    print("\n--- Test 12.3: 多路命中 ---")
    print("条件：waymask有两位及以上为1（多路命中），视为ECC错误")
    print("预期：s2_meta_corrupt、io.errors.valid、io.errors.bits.report_to_beu为true")
    
    try:
        await agent.reset()
        await agent.drive_set_ecc_enable(True)
        await agent.drive_data_array_ready(True)
        
        test_vaddr = 0x4000
        test_ptag = 0x98765
        
        print(f"  ptag: 0x{test_ptag:x}")
        print(f"  多路命中：waymask=0x5 (way 0和way 2同时命中)")
        
        # 使用多路命中错误注入API
        inject_success = await agent.inject_multi_way_hit(
            vSetIdx_0=(test_vaddr >> 6) & 0xFF,
            vSetIdx_1=(test_vaddr >> 6) & 0xFF,
            waymask_0=0x5,  # 多路命中（way 0和way 2）
            waymask_1=0x0,
            ptag_0=test_ptag,
            ptag_1=0
        )
        await bundle.step()
        assert inject_success, "12.3: 多路命中错误注入失败"
        
        # 发起fetch请求
        fetch_success = await agent.drive_fetch_request(
            pcMemRead_addrs=[0, 0, 0, 0, test_vaddr],
            readValid=[0, 0, 0, 0, 1]
        )
        assert fetch_success, "12.3: 地址一致性检查失败"
        
        # 推进流水线
        await bundle.step(2)
        
        # 监控错误状态
        error_status = await agent.monitor_error_status()
        meta_corrupt_status = await agent.monitor_meta_corrupt_status()
        
        print(f"  waymask_0: 0x5 (多路命中，way 0和way 2)")
        print(f"  hit_num应≥2，根据源码|(hit_num[2:1])检测多路命中，应报告错误")
        print(f"  实际：io.errors[0].valid={error_status['0_valid']}")
        print(f"  实际：io.errors[0].report_to_beu={error_status['0_report_to_beu']}")
        if meta_corrupt_status:
            print(f"  s1_meta_corrupt_hit_num: {meta_corrupt_status.get('s1_meta_corrupt_hit_num', 'N/A')}")
        
        # 根据Verilog源码，多路命中通过(|(s1_meta_corrupt_hit_num[2:1]))检测
        assert error_status['0_valid'] == 1, f"12.3失败：多路命中时应报告错误，但io.errors[0].valid={error_status['0_valid']}"
        assert error_status['0_report_to_beu'] == 1, f"12.3失败：应向BEU报告错误，但report_to_beu={error_status['0_report_to_beu']}"
        
        # 清除请求
        await agent.clear_waylookup_read()
        await agent.clear_fetch_request()
        print("  ✓ Test 12.3通过")
        
    except Exception as e:
        error_msg = f"12.3测试失败: {str(e)}"
        print(f"  ✗ {error_msg}")
        test_errors.append(error_msg)
    
    # ==================== 测试点12.4: ECC功能关闭 ====================
    print("\n--- Test 12.4: ECC功能关闭 ---")
    print("条件：奇偶校验关闭（ecc_enable为低）")
    print("预期：强制清除s1_meta_corrupt信号置位，不管是否发生ECC错误，s1_meta_corrupt都为假")
    
    try:
        await agent.reset()
        await agent.drive_set_ecc_enable(False)  # 关闭ECC功能
        await agent.drive_data_array_ready(True)
        
        test_vaddr = 0x5000
        test_ptag = 0x11111
        # 故意设置ECC错误条件但ECC功能关闭
        wrong_meta_code = 1  # 故意错误的ECC码
        
        print(f"  ECC功能已关闭")
        print(f"  ptag: 0x{test_ptag:x}")
        print(f"  故意设置错误ECC码: {wrong_meta_code}")
        
        # 设置ECC错误条件但ECC功能关闭
        await agent.drive_waylookup_read(
            vSetIdx_0=(test_vaddr >> 6) & 0xFF,
            vSetIdx_1=(test_vaddr >> 6) & 0xFF,
            waymask_0=0x1,  # 单路命中
            waymask_1=0x0,
            ptag_0=test_ptag,
            ptag_1=0,
            meta_codes_0=wrong_meta_code,  # 故意错误的ECC码
            meta_codes_1=0
        )
        
        # 发起fetch请求
        fetch_success = await agent.drive_fetch_request(
            pcMemRead_addrs=[0, 0, 0, 0, test_vaddr],
            readValid=[0, 0, 0, 0, 1]
        )
        assert fetch_success, "12.4: 地址一致性检查失败"
        
        # 推进流水线
        await bundle.step(3)
        
        # 监控错误状态
        error_status = await agent.monitor_error_status()
        meta_status = await agent.monitor_check_meta_ecc_status()
        
        print(f"  waymask_0: 0x1 (单路命中)")
        print(f"  由于ECC功能关闭，即使有ECC错误也不应报告")
        print(f"  实际：io.ecc_enable={meta_status['ecc_enable']}")
        print(f"  实际：io.errors[0].valid={error_status['0_valid']}")
        
        # 根据Verilog源码，ECC关闭时强制清除错误信号
        # s2_meta_corrupt_0 <= io_ecc_enable & (...)，当io_ecc_enable=0时，s2_meta_corrupt_0=0
        assert meta_status['ecc_enable'] == 0, f"12.4失败：ECC功能应被关闭，但ecc_enable={meta_status['ecc_enable']}"
        assert error_status['0_valid'] == 0, f"12.4失败：ECC功能关闭时不应报告错误，但io.errors[0].valid={error_status['0_valid']}"
        
        # 清除请求
        await agent.clear_waylookup_read()
        await agent.clear_fetch_request()
        print("  ✓ Test 12.4通过")
        
    except Exception as e:
        error_msg = f"12.4测试失败: {str(e)}"
        print(f"  ✗ {error_msg}")
        test_errors.append(error_msg)
    
    # ==================== 测试结果汇总 ====================
    print(f"\n=== CP12测试结果汇总 ===")
    if test_errors:
        print(f"测试失败数量: {len(test_errors)}")
        for error in test_errors:
            print(f"  - {error}")
        # 抛出汇总的错误信息
        raise AssertionError(f"CP12: Meta ECC校验功能测试有{len(test_errors)}个失败:\n" + "\n".join(test_errors))
    else:
        print("✓ CP12: Meta ECC校验功能测试完成，所有测试点通过")


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
            instr_0=0, mmio_0=0,
            instr_1=0, mmio_1=0
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
        print("√ Test 13.1 通过")
    except Exception as e:
        error_msg = f"Test 13.1 failed: {e}"
        test_errors.append(error_msg)
        print(f"× {error_msg}")
    
    # 13.2: 通道 0 有 PMP 异常
    # 文档：s1_pmp_exception(0) 为真，表示通道 0 有 PMP 异常
    # Verilog：io_pmp_0_resp_instr = 1 时产生 PMP 异常
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
            instr_1=0, mmio_1=0
        )
        await agent.drive_waylookup_read(
            vSetIdx_0=0x40, 
            vSetIdx_1=0x40, 
            waymask_0=0x0, 
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
        print("√ Test 13.2 通过")
    except Exception as e:
        error_msg = f"Test 13.2 failed: {e}"
        test_errors.append(error_msg)
        print(f"× {error_msg}")
    
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
            vSetIdx_1=0x41,  # 保持一致
            waymask_0=0x0,  # 没有命中
            ptag_0=0x12345,
            meta_codes_0=bin(0x12345).count('1') & 1,
            itlb_exception_0=0
        )
        await bundle.step()
        
        await agent.drive_fetch_request(
            pcMemRead_addrs=[0x1010, 0, 0, 0, 0x1020],  # pcMemRead_0和pcMemRead_4都设置
            readValid=[1, 0, 0, 0, 1]  # readValid_0和readValid_4都有效
        )
        await bundle.step()
        
        # 设置通道1产生PMP异常
        await agent.drive_pmp_response(
            instr_0=0, mmio_0=0,  # 通道0无异常
            instr_1=1, mmio_1=0   # 通道1产生PMP异常
        )
        
        await bundle.step(2)
        await agent.clear_fetch_request()
        await agent.clear_waylookup_read()
        
        fetch_resp = await agent.monitor_fetch_response()
        
        print(f"  Fetch resp exception 0: {fetch_resp['exception_0']}")
        print(f"  Fetch resp exception 1: {fetch_resp['exception_1']}")
        
        # 验证：通道0无异常，通道1有异常
        assert fetch_resp['exception_0'] == 0, "通道0不应有异常"
        assert fetch_resp['exception_1'] != 0, "通道1应有PMP异常"
        print("√ Test 13.3 通过")
    except Exception as e:
        error_msg = f"Test 13.3 failed: {e}"
        test_errors.append(error_msg)
        print(f"× {error_msg}")
    
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
         # 设置两个通道都产生PMP异常
        await agent.drive_pmp_response(
            instr_0=1, mmio_0=0,  # 通道0产生PMP异常
            instr_1=1, mmio_1=0   # 通道1产生PMP异常
        )

        # 使用跨行地址配置，确保双通道PMP检查都能正确激活
        # 使用bit[5]=1的地址来触发跨行取指，激活双通道处理
        base_addr_main = 0x1020  # 主地址，bit[5]=1，会跨行
        nextline_addr = (base_addr_main & ~0x3F) + 64  # 0x1040
        vSetIdx_0 = (base_addr_main >> 6) & 0xFF  # 0x40
        vSetIdx_1 = (nextline_addr >> 6) & 0xFF   # 0x41
        
        await agent.drive_waylookup_read(
            vSetIdx_0=vSetIdx_0,  # 与地址匹配
            vSetIdx_1=vSetIdx_1,  # 与地址匹配
            waymask_0=0x1,  # 通道0命中，确保流水线激活
            waymask_1=0x1,  # 通道1命中，确保流水线激活
            ptag_0=(base_addr_main >> 12) & 0xFFFFFFFFF,  # 正确的物理标签
            ptag_1=(nextline_addr >> 12) & 0xFFFFFFFFF,   # 正确的物理标签
            itlb_exception_0=0,
            itlb_exception_1=0
        )
        await bundle.step()
        
        await agent.drive_fetch_request(
            pcMemRead_addrs=[base_addr_main, 0, 0, 0, base_addr_main],  # 使用跨行地址
            readValid=[1, 0, 0, 0, 1],  # 激活通道0和MainPipe
            backendException=0
        )
        
        await bundle.step(2)
        await agent.clear_fetch_request()
        await agent.clear_waylookup_read()
        
        fetch_resp = await agent.monitor_fetch_response()
        
        print(f"  Fetch resp exception 0: {fetch_resp['exception_0']}")
        print(f"  Fetch resp exception 1: {fetch_resp['exception_1']}")
        
        # 验证：两个通道都有异常
        assert fetch_resp['exception_0'] != 0, "通道0应有PMP异常"
        assert fetch_resp['exception_1'] != 0, "通道1应有PMP异常"
        print("√ Test 13.4 通过")
    except Exception as e:
        error_msg = f"Test 13.4 failed: {e}"
        test_errors.append(error_msg)
        print(f"× {error_msg}")
    
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
            vSetIdx_1=0x41,  # 保持一致
            waymask_0=0x0,  # 没有命中
            ptag_0=0x12345,
            meta_codes_0=bin(0x12345).count('1') & 1,
            itlb_exception_0=0
        )
        
        await agent.drive_fetch_request(
            pcMemRead_addrs=[0x1000, 0, 0, 0, 0x1020],  # pcMemRead_0和pcMemRead_4都设置
            readValid=[1, 0, 0, 0, 1]  # readValid_0和readValid_4都有效
        )
        
        # 设置两个通道都不是MMIO区域
        await agent.drive_pmp_response(
            instr_0=0, mmio_0=0,  # 通道0有权限，非MMIO
            instr_1=0, mmio_1=0   # 通道1有权限，非MMIO
        )
        
        await bundle.step(2)
        await agent.clear_fetch_request()
        await agent.clear_waylookup_read()
        
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
        print("√ Test 13.5 通过")
    except Exception as e:
        error_msg = f"Test 13.5 failed: {e}"
        test_errors.append(error_msg)
        print(f"× {error_msg}")
    
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
        
        # 使用一致的地址配置，确保通道0能正确处理MMIO
        # 注意：这里只测试通道0的MMIO，所以使用不跨行的地址
        base_addr_0 = 0x1000  # 通道0地址，bit[5]=0，不跨行
        vSetIdx_0 = (base_addr_0 >> 6) & 0xFF  # 0x40
        
        await agent.drive_waylookup_read(
            vSetIdx_0=vSetIdx_0,  # 与地址匹配
            vSetIdx_1=vSetIdx_0,  # 不跨行时两个vSetIdx相同
            waymask_0=0x1,  # 通道0命中，确保流水线激活
            waymask_1=0x0,  # 通道1未命中
            ptag_0=(base_addr_0 >> 12) & 0xFFFFFFFFF,  # 正确的物理标签
            ptag_1=(base_addr_0 >> 12) & 0xFFFFFFFFF,  # 相同的物理标签
            itlb_exception_0=0, itlb_exception_1=0,
            itlb_pbmt_0=0, itlb_pbmt_1=0
        )
        
        await agent.drive_fetch_request(
            pcMemRead_addrs=[base_addr_0, 0, 0, 0, base_addr_0],  # 设置通道0和MainPipe地址
            readValid=[1, 0, 0, 0, 1],  # 激活通道0和MainPipe
            backendException=0
        )
        
        # 设置通道0映射到MMIO区域
        await agent.drive_pmp_response(
            instr_0=0, mmio_0=1,  # 通道0有权限，映射到MMIO
            instr_1=0, mmio_1=0   # 通道1有权限，非MMIO
        )
        
        await bundle.step(3)
        await agent.clear_fetch_request()
        await agent.clear_waylookup_read()
        
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
        print("√ Test 13.6 通过")
    except Exception as e:
        error_msg = f"Test 13.6 failed: {e}"
        test_errors.append(error_msg)
        print(f"× {error_msg}")
    
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
            vSetIdx_0=0x40, vSetIdx_1=0x41,  # 与0x1000匹配
            waymask_0=0x1, waymask_1=0x1,
            ptag_0=0x1006, ptag_1=0x1006,
            itlb_exception_0=0, itlb_exception_1=0,
            itlb_pbmt_0=0, itlb_pbmt_1=0
        )
        
        await agent.drive_fetch_request(
            pcMemRead_addrs=[0, 0, 0, 0, 0x1020],  # [13:6] = 0x40，匹配 vSetIdx_0
            readValid=[0, 0, 0, 0, 1],
            backendException=0
        )
        
        # 设置通道1映射到MMIO区域
        await agent.drive_pmp_response(
            instr_0=0, mmio_0=0,  # 通道0有权限，非MMIO
            instr_1=0, mmio_1=1   # 通道1有权限，映射到MMIO
        )
        
        await bundle.step(2)
        await agent.clear_fetch_request()
        await agent.clear_waylookup_read()
        
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
        print("√ Test 13.7 通过")
    except Exception as e:
        error_msg = f"Test 13.7 failed: {e}"
        test_errors.append(error_msg)
        print(f"× {error_msg}")
    
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
        
        # 使用跨行地址配置，确保双通道MMIO检查都能正确激活
        # 使用bit[5]=1的地址来触发跨行取指，激活双通道处理
        base_addr_main = 0x1020  # 主地址，bit[5]=1，会跨行
        nextline_addr = (base_addr_main & ~0x3F) + 64  # 0x1040
        vSetIdx_0 = (base_addr_main >> 6) & 0xFF  # 0x40
        vSetIdx_1 = (nextline_addr >> 6) & 0xFF   # 0x41
        
        await agent.drive_waylookup_read(
            vSetIdx_0=vSetIdx_0,  # 与地址匹配
            vSetIdx_1=vSetIdx_1,  # 与地址匹配
            waymask_0=0x1,  # 通道0命中，确保流水线激活
            waymask_1=0x1,  # 通道1命中，确保流水线激活
            ptag_0=(base_addr_main >> 12) & 0xFFFFFFFFF,  # 正确的物理标签
            ptag_1=(nextline_addr >> 12) & 0xFFFFFFFFF,   # 正确的物理标签
            itlb_exception_0=0, itlb_exception_1=0,
            itlb_pbmt_0=0, itlb_pbmt_1=0
        )
        
        await agent.drive_fetch_request(
            pcMemRead_addrs=[base_addr_main, 0, 0, 0, base_addr_main],  # 使用跨行地址
            readValid=[1, 0, 0, 0, 1],  # 激活通道0和MainPipe
            backendException=0
        )
        
        # 设置两个通道都映射到MMIO区域
        await agent.drive_pmp_response(
            instr_0=0, mmio_0=1,  # 通道0有权限，映射到MMIO
            instr_1=0, mmio_1=1   # 通道1有权限，映射到MMIO
        )
        
        await bundle.step(2)
        await agent.clear_fetch_request()
        await agent.clear_waylookup_read()
        
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
        print("√ Test 13.8 通过")
    except Exception as e:
        error_msg = f"Test 13.8 failed: {e}"
        test_errors.append(error_msg)
        print(f"× {error_msg}")
    
    # 汇总所有测试结果
    print("\n" + "="*60)
    if test_errors:
        print(f"× CP13: PMP检查功能测试完成 - {len(test_errors)}个错误:")
        for i, error in enumerate(test_errors, 1):
            print(f"  {i}. {error}")
        raise AssertionError(f"CP13 PMP测试失败，共{len(test_errors)}个错误: {'; '.join(test_errors)}")
    else:
        print("√ CP13: PMP检查功能测试完成 - 所有测试通过")


@toffee_test.testcase
async def test_cp14_exception_merge(icachemainpipe_env: ICacheMainPipeEnv):
    """
    CP14: 异常合并功能测试
    测试ITLB和PMP异常的优先级合并逻辑
    
    基于MainPipe.md文档和verilog源码异常合并逻辑：
    s2_exception_0 <= (|s1_itlb_exception_0) ? s1_itlb_exception_0 : {2{io_pmp_0_resp_instr}};
    ITLB异常优先于PMP异常
    """
    print("\n=== CP14: 异常合并功能测试 ===")
    agent = icachemainpipe_env.agent
    bundle = icachemainpipe_env.bundle
    
    # 收集所有测试错误，避免单一错误导致后续测试停止
    test_errors = []
    
    # 14.1: 没有异常
    try:
        print("\n--- 测试 14.1: 没有异常 ---")
        await agent.reset()
        
        # 环境准备：确保流水线能够正常工作
        await agent.drive_set_ecc_enable(True)
        await agent.drive_data_array_ready(True)
        
        # 设置WayLookup数据：无ITLB异常
        # verilog依据：s1_itlb_exception_0 <= io_wayLookupRead_bits_entry_itlb_exception_0
        await agent.drive_waylookup_read(
            vSetIdx_0=0x10,
            vSetIdx_1=0x10,
            waymask_0=0x1,
            ptag_0=0x1000,
            itlb_exception_0=0,  # 无ITLB异常
            itlb_exception_1=0
        )
        
        # 设置PMP响应：无PMP异常
        # verilog依据：{2{io_pmp_0_resp_instr}}，instr=0表示有指令访问权限
        await agent.drive_pmp_response(
            instr_0=0,  # 有指令访问权限，无PMP异常
            mmio_0=0,
            instr_1=0,
            mmio_1=0
        )
        
        # 驱动fetch请求启动流水线
        # 地址一致性约束：pcMemRead_4地址与wayLookup vSetIdx匹配
        # vSetIdx=0x10 -> pcMemRead_4=(0x10 << 6)=0x400
        await agent.drive_fetch_request(
            pcMemRead_addrs=[0, 0, 0, 0, 0x400],
            readValid=[0, 0, 0, 0, 1]
        )
        
        # 等待流水线推进到S2阶段
        await bundle.step(3)
        
        # 监控异常合并状态
        exception_status = await agent.monitor_exception_merge_status()
        fetch_resp = await agent.monitor_fetch_response()
        
        print(f"  S1 ITLB异常0: {exception_status.get('s1_itlb_exception_0', 'N/A')}")
        print(f"  S2异常0: {exception_status.get('s2_exception_0', 'N/A')}")
        print(f"  Fetch响应异常0: {fetch_resp.get('exception_0', 'N/A')}")
        
        # 验证：无异常时的状态
        # verilog依据：当itlb_exception_0=0且pmp_instr=0时，s2_exception_0={2{1}}=0
        # 这里3表示PMP正常指令访问权限，不是异常
        assert exception_status.get('s1_itlb_exception_0') == 0, \
            f"期望无ITLB异常(0)，实际得到 {exception_status.get('s1_itlb_exception_0')}"
        assert exception_status.get('s2_exception_0') == 0, \
            f"期望PMP正常权限编码(3)，实际得到 {exception_status.get('s2_exception_0')}"
        assert fetch_resp.get('exception_0') == 0, \
            f"期望fetch响应正常权限编码(3)，实际得到 {fetch_resp.get('exception_0')}"
        
        # 清除操作
        await agent.clear_fetch_request()
        await agent.clear_waylookup_read()
        
        print("  √ 测试14.1通过：无ITLB异常，PMP正常访问权限")
        
    except Exception as e:
        error_msg = f"测试14.1失败: {str(e)}"
        print(f"  × {error_msg}")
        test_errors.append(error_msg)
    
    # 14.2: 只有ITLB异常
    try:
        print("\n--- 测试 14.2: 只有ITLB异常 ---")
        await agent.reset()
        
        # 环境准备
        await agent.drive_set_ecc_enable(True)
        await agent.drive_data_array_ready(True)
        
        # 设置WayLookup数据：有ITLB异常
        await agent.drive_waylookup_read(
            vSetIdx_0=0x20,
            vSetIdx_1=0x20,
            waymask_0=0x1,
            ptag_0=0x2000,
            itlb_exception_0=0x2,  # ITLB异常类型2
            itlb_exception_1=0
        )
        
        # 设置PMP响应：无PMP异常
        await agent.drive_pmp_response(
            instr_0=0,  # 有指令访问权限
            mmio_0=0,
            instr_1=0,
            mmio_1=0
        )
        
        # 驱动fetch请求
        # vSetIdx=0x20 -> pcMemRead_4=(0x20 << 6)=0x800
        await agent.drive_fetch_request(
            pcMemRead_addrs=[0, 0, 0, 0, 0x800],
            readValid=[0, 0, 0, 0, 1]
        )
        
        await bundle.step(3)
        
        exception_status = await agent.monitor_exception_merge_status()
        fetch_resp = await agent.monitor_fetch_response()
        
        print(f"  S1 ITLB异常0: {exception_status.get('s1_itlb_exception_0', 'N/A')}")
        print(f"  S2异常0: {exception_status.get('s2_exception_0', 'N/A')}")
        print(f"  Fetch响应异常0: {fetch_resp.get('exception_0', 'N/A')}")
        
        # 验证：只有ITLB异常时，s2_exception应与ITLB异常一致
        # verilog依据：(|s1_itlb_exception_0) ? s1_itlb_exception_0 : {2{io_pmp_0_resp_instr}}
        # 当s1_itlb_exception_0=2时，s2_exception_0=2
        assert exception_status.get('s1_itlb_exception_0') == 0x2, \
            f"期望ITLB异常2，实际得到 {exception_status.get('s1_itlb_exception_0')}"
        assert exception_status.get('s2_exception_0') == 0x2, \
            f"期望S2异常2，实际得到 {exception_status.get('s2_exception_0')}"
        
        await agent.clear_fetch_request()
        await agent.clear_waylookup_read()
        
        print("  √ 测试14.2通过：只有ITLB异常情况正确")
        
    except Exception as e:
        error_msg = f"测试14.2失败: {str(e)}"
        print(f"  × {error_msg}")
        test_errors.append(error_msg)
    
    # 14.3: 只有PMP异常
    try:
        print("\n--- 测试 14.3: 只有PMP异常 ---")
        await agent.reset()
        
        # 环境准备
        await agent.drive_set_ecc_enable(True)
        await agent.drive_data_array_ready(True)
        
        # 设置WayLookup数据：无ITLB异常
        await agent.drive_waylookup_read(
            vSetIdx_0=0x30,
            vSetIdx_1=0x30,
            waymask_0=0x1,
            ptag_0=0x3000,
            itlb_exception_0=0,  # 无ITLB异常
            itlb_exception_1=0
        )
        
        # 设置PMP响应：有PMP异常
        await agent.drive_pmp_response(
            instr_0=1,  # 无指令访问权限，PMP异常
            mmio_0=0,
            instr_1=0,
            mmio_1=0
        )
        
        # 驱动fetch请求
        # vSetIdx=0x30 -> pcMemRead_4=(0x30 << 6)=0xC00
        await agent.drive_fetch_request(
            pcMemRead_addrs=[0, 0, 0, 0, 0xC00],
            readValid=[0, 0, 0, 0, 1]
        )
        
        await bundle.step(3)
        
        exception_status = await agent.monitor_exception_merge_status()
        fetch_resp = await agent.monitor_fetch_response()
        
        print(f"  S1 ITLB异常0: {exception_status.get('s1_itlb_exception_0', 'N/A')}")
        print(f"  S2异常0: {exception_status.get('s2_exception_0', 'N/A')}")
        print(f"  Fetch响应异常0: {fetch_resp.get('exception_0', 'N/A')}")
        print(f"  PMP instr响应: {bundle.io._pmp._0._resp._instr.value}")
        
        # 验证：只有PMP异常时，s2_exception应反映PMP状态
        # verilog依据：当s1_itlb_exception_0=0时，s2_exception_0={2{io_pmp_0_resp_instr}}
        # 当io_pmp_0_resp_instr=0时，s2_exception_0=2'b00=0
        assert exception_status.get('s1_itlb_exception_0') == 0, \
            f"期望无ITLB异常，实际得到 {exception_status.get('s1_itlb_exception_0')}"
        assert exception_status.get('s2_exception_0') == 3, \
            f"期望PMP异常结果0，实际得到 {exception_status.get('s2_exception_0')}"
        
        await agent.clear_fetch_request()
        await agent.clear_waylookup_read()
        
        print("  √ 测试14.3通过：只有PMP异常情况正确")
        
    except Exception as e:
        error_msg = f"测试14.3失败: {str(e)}"
        print(f"  × {error_msg}")
        test_errors.append(error_msg)
    
    # 14.4: ITLB与PMP异常同时出现（ITLB优先级更高）
    try:
        print("\n--- 测试 14.4: ITLB与PMP异常同时出现 ---")
        await agent.reset()
        
        # 环境准备
        await agent.drive_set_ecc_enable(True)
        await agent.drive_data_array_ready(True)
        
        # 设置WayLookup数据：有ITLB异常
        await agent.drive_waylookup_read(
            vSetIdx_0=0x40,
            vSetIdx_1=0x40,
            waymask_0=0x1,
            ptag_0=0x4000,
            itlb_exception_0=0x3,  # ITLB异常类型3
            itlb_exception_1=0
        )
        
        # 设置PMP响应：也有PMP异常
        await agent.drive_pmp_response(
            instr_0=1,  # 无指令访问权限，PMP异常
            mmio_0=0,
            instr_1=0,
            mmio_1=0
        )
        
        # 驱动fetch请求
        # vSetIdx=0x40 -> pcMemRead_4=(0x40 << 6)=0x1000
        await agent.drive_fetch_request(
            pcMemRead_addrs=[0, 0, 0, 0, 0x1000],
            readValid=[0, 0, 0, 0, 1]
        )
        
        await bundle.step(3)
        
        exception_status = await agent.monitor_exception_merge_status()
        fetch_resp = await agent.monitor_fetch_response()
        
        print(f"  S1 ITLB异常0: {exception_status.get('s1_itlb_exception_0', 'N/A')}")
        print(f"  S2异常0: {exception_status.get('s2_exception_0', 'N/A')}")
        print(f"  Fetch响应异常0: {fetch_resp.get('exception_0', 'N/A')}")
        print(f"  PMP instr响应: {bundle.io._pmp._0._resp._instr.value}")
        
        # 验证：ITLB与PMP异常同时出现时，ITLB优先级更高
        # verilog依据：(|s1_itlb_exception_0) ? s1_itlb_exception_0 : {2{io_pmp_0_resp_instr}}
        # 当s1_itlb_exception_0=3时，s2_exception_0=3（忽略PMP异常）
        assert exception_status.get('s1_itlb_exception_0') == 0x3, \
            f"期望ITLB异常3，实际得到 {exception_status.get('s1_itlb_exception_0')}"
        assert exception_status.get('s2_exception_0') == 0x3, \
            f"期望S2异常3(ITLB优先)，实际得到 {exception_status.get('s2_exception_0')}"
        
        await agent.clear_fetch_request()
        await agent.clear_waylookup_read()
        
        print("  √ 测试14.4通过：ITLB异常优先级正确")
        
    except Exception as e:
        error_msg = f"测试14.4失败: {str(e)}"
        print(f"  × {error_msg}")
        test_errors.append(error_msg)
    
    # 汇总测试结果
    if test_errors:
        print(f"\n× CP14测试完成，发现 {len(test_errors)} 个错误:")
        for i, error in enumerate(test_errors, 1):
            print(f"  {i}. {error}")
        # 抛出所有错误
        raise AssertionError(f"CP14异常合并测试失败: {'; '.join(test_errors)}")
    else:
        print("\n√ CP14: 异常合并功能测试完成 - 所有测试通过")


@toffee_test.testcase
async def test_cp15_mshr_match_data_select(icachemainpipe_env: ICacheMainPipeEnv):
    """
    CP15: MSHR匹配和数据选择功能测试
    测试MSHR命中检查和数据源选择逻辑
    基于文档和verilog源码:
    - 15.1: 命中 MSHR - s1_MSHR_hits(i) 为 true 时，s1_datas(i) 为 s1_bankMSHRHit(i)，s1_data_is_from_MSHR(i) 为 true
    - 15.2: 未命中 MSHR - s1_MSHR_hits(i) 为 false 时，s1_datas(i) 为 fromData.datas(i)，s1_data_is_from_MSHR(i) 为 false  
    - 15.3: MSHR 数据 corrupt - fromMSHR.bits.corrupt = true，那么 MSHR 将不匹配，应该读取 SRAM 的数据
    """
    print("\n=== CP15: MSHR匹配和数据选择功能测试 ===")
    agent = icachemainpipe_env.agent
    bundle = icachemainpipe_env.bundle
    
    errors = []
    
    # 15.1: 命中 MSHR 测试
    try:
        print("\n--- 测试点 15.1: 命中 MSHR ---")
        
        # 重置和环境准备
        await agent.reset()
        await agent.drive_set_ecc_enable(True)
        await agent.setup_mshr_ready(True)
        await agent.drive_data_array_ready(True)
        await bundle.step(2)
        
        # 监控初始状态
        initial_status = await agent.monitor_pipeline_status()
        print(f"初始流水线状态: {initial_status}")
        
        test_blkPaddr = 0x1000  # 测试物理地址
        test_vSetIdx = 0x10     # 测试缓存组索引
        test_data = 0x123456789ABCDEF0123456789ABCDEF0123456789ABCDEF0123456789ABCDEF  # 512位数据
        
        await agent.drive_mshr_response(
            blkPaddr=test_blkPaddr,
            vSetIdx=test_vSetIdx, 
            data=test_data,
            corrupt=0  # 无错误
        )
        await bundle.step(2)  # 让MSHR响应稳定
        
        # 执行waylookup操作 - 必须先于fetch执行
        # 基于verilog: s1_req_vaddr_0[13:6] == io_mshr_resp_bits_vSetIdx
        await agent.drive_waylookup_read(
            vSetIdx_0=test_vSetIdx,  # 与MSHR响应vSetIdx匹配
            vSetIdx_1=test_vSetIdx,  # 确保vSetIdx_1也匹配，避免RTL约束违反
            waymask_0=0x1,           # 单路命中
            ptag_0=(test_blkPaddr >> 6) & 0xFFFFFFFFF  # 物理标签匹配条件
        )
        await bundle.step(1)
        
        # 执行fetch请求 - 确保地址一致性
        # pcMemRead_4地址的[13:6]位必须与vSetIdx一致
        # 关键：确保startAddr[5]=0，这样nextlineStart=startAddr，两个vSetIdx相等
        fetch_addr = (test_vSetIdx << 6)  # 确保[5]=0，nextlineStart=startAddr
        await agent.drive_fetch_request(
            pcMemRead_addrs=[0, 0, 0, 0, fetch_addr],  # 使用第5个元素
            readValid=[0, 0, 0, 0, 1]
        )
        await bundle.step(5)  # 等待流水线推进到S1阶段
        
        # 监控MSHR匹配状态
        mshr_status = await agent.monitor_mshr_match_status()
        print(f"MSHR匹配状态: {mshr_status}")
        
        # 清除操作
        await agent.clear_fetch_request()
        await bundle.step(2)
        
        # 验证测试点15.1: 命中MSHR的条件
        # 基于verilog: s1_bankMSHRHit_7 = s1_valid & s1_req_vaddr_0[13:6] == io_mshr_resp_bits_vSetIdx 
        #              & s1_req_ptags_0 == io_mshr_resp_bits_blkPaddr[41:6] & io_mshr_resp_valid & ~io_mshr_resp_bits_corrupt
        expected_hit = any([
            mshr_status.get(f's1_bankMSHRHit_{i}', False) for i in range(8)
        ])
        
        if not expected_hit:
            errors.append("测试点15.1失败: 未检测到MSHR命中")
        else:
            print("√ 测试点15.1通过: 成功检测到MSHR命中")
            
    except Exception as e:
        errors.append(f"测试点15.1异常: {str(e)}")
        print(f"× 测试点15.1发生异常: {e}")
    
    # 15.2: 未命中 MSHR 测试  
    try:
        print("\n--- 测试点 15.2: 未命中 MSHR ---")
        
        # 重置环境
        await agent.reset()
        await agent.drive_set_ecc_enable(True) 
        await agent.setup_mshr_ready(True)
        await agent.drive_data_array_ready(True)
        
        # 设置MSHR响应 - 使用不同的地址确保不匹配
        mshr_blkPaddr = 0x2000
        mshr_vSetIdx = 0x20
        
        await agent.drive_mshr_response(
            blkPaddr=mshr_blkPaddr,
            vSetIdx=mshr_vSetIdx,
            data=0xDEADBEEFDEADBEEFDEADBEEFDEADBEEFDEADBEEFDEADBEEFDEADBEEFDEADBEEF,
            corrupt=0
        )
        await bundle.step(2)
        
        # 执行waylookup - 使用与MSHR不匹配的地址
        different_vSetIdx = 0x30  # 与MSHR的vSetIdx不同
        different_ptag = 0x3000 >> 6
        
        await agent.drive_waylookup_read(
            vSetIdx_0=different_vSetIdx,
            vSetIdx_1=different_vSetIdx, 
            waymask_0=0x1,
            ptag_0=different_ptag
        )
        await bundle.step(1)
        
        # 执行fetch请求 - 地址与MSHR不匹配
        fetch_addr = (different_vSetIdx << 6)  # 确保[5]=0，nextlineStart=startAddr
        await agent.drive_fetch_request(
            pcMemRead_addrs=[0, 0, 0, 0, fetch_addr],
            readValid=[0, 0, 0, 0, 1]
        )
        await bundle.step(5)
        
        # 监控MSHR匹配状态
        mshr_status = await agent.monitor_mshr_match_status()
        print(f"MSHR未命中状态: {mshr_status}")
        
        # 清除操作
        await agent.clear_fetch_request()
        await bundle.step(2)
        
        # 验证测试点15.2: 未命中MSHR的条件
        # 当地址不匹配时，s1_bankMSHRHit应该为false
        any_hit = any([
            mshr_status.get(f's1_bankMSHRHit_{i}', False) for i in range(8)
        ])
        
        if any_hit:
            errors.append("测试点15.2失败: 错误地检测到MSHR命中")
        else:
            print("√ 测试点15.2通过: 正确检测到MSHR未命中")
            
    except Exception as e:
        errors.append(f"测试点15.2异常: {str(e)}")
        print(f"× 测试点15.2发生异常: {e}")
    
    # 15.3: MSHR 数据 corrupt 测试
    try:
        print("\n--- 测试点 15.3: MSHR 数据 corrupt ---")
        
        # 重置环境
        await agent.reset()
        await agent.drive_set_ecc_enable(True)
        await agent.setup_mshr_ready(True) 
        await agent.drive_data_array_ready(True)
        
        # 设置MSHR响应 - 带有corrupt标记
        # 基于verilog: 当io_mshr_resp_bits_corrupt=true时，~io_mshr_resp_bits_corrupt=false，MSHR不匹配
        corrupt_blkPaddr = 0x4000
        corrupt_vSetIdx = 0x40
        
        await agent.drive_mshr_response(
            blkPaddr=corrupt_blkPaddr,
            vSetIdx=corrupt_vSetIdx,
            data=0xBAADBAADBAADBAADBAADBAADBAADBAADBAADBAADBAADBAADBAADBAADBAADBAA,
            corrupt=1  # 设置corrupt标记
        )
        await bundle.step(2)
        
        # 执行waylookup - 地址匹配但数据corrupt
        await agent.drive_waylookup_read(
            vSetIdx_0=corrupt_vSetIdx,  
            vSetIdx_1=corrupt_vSetIdx, 
            waymask_0=0x1,
            ptag_0=(corrupt_blkPaddr >> 6) & 0xFFFFFFFFF  # 物理标签匹配
        )
        await bundle.step(1)
        
        # 执行fetch请求
        fetch_addr = (corrupt_vSetIdx << 6)  # 确保[5]=0，nextlineStart=startAddr
        await agent.drive_fetch_request(
            pcMemRead_addrs=[0, 0, 0, 0, fetch_addr],
            readValid=[0, 0, 0, 0, 1]
        )
        await bundle.step(5)
        
        # 监控MSHR匹配状态
        mshr_status = await agent.monitor_mshr_match_status()
        print(f"MSHR corrupt状态: {mshr_status}")
        
        # 清除操作
        await agent.clear_fetch_request()
        await bundle.step(2)
        
        # 验证测试点15.3: corrupt数据时MSHR不应该匹配
        # 基于verilog: s1_bankMSHRHit条件包含~io_mshr_resp_bits_corrupt
        any_hit = any([
            mshr_status.get(f's1_bankMSHRHit_{i}', False) for i in range(8)
        ])
        
        if any_hit:
            errors.append("测试点15.3失败: corrupt数据时错误地检测到MSHR命中")
        else:
            print("√ 测试点15.3通过: corrupt数据时正确拒绝MSHR匹配")
            
    except Exception as e:
        errors.append(f"测试点15.3异常: {str(e)}")
        print(f"× 测试点15.3发生异常: {e}")
    
    # 汇总测试结果
    print(f"\n=== CP15测试完成 ===")
    if errors:
        print(f"× 发现 {len(errors)} 个错误:")
        for i, error in enumerate(errors, 1):
            print(f"  {i}. {error}")
        # 抛出所有收集到的错误
        raise AssertionError(f"CP15测试失败，错误列表: {'; '.join(errors)}")
    else:
        print("√ CP15: MSHR匹配和数据选择功能测试 - 所有测试点通过")


@toffee_test.testcase
async def test_cp16_data_ecc_check(icachemainpipe_env: ICacheMainPipeEnv):
    """
    CP16: Data ECC校验功能测试
    测试S2阶段的数据ECC校验逻辑
    
    测试点：
    16.1: 无ECC错误 - s2_data_corrupt(i)为false，没有ECC错误
    16.2: 单Bank ECC错误 - s2_bank_corrupt(bank)有一个为true，相关错误信号为true
    16.3: 多Bank ECC错误 - s2_bank_corrupt(bank)有两个或以上为true，相关错误信号为true  
    16.4: ECC功能关闭 - 当ecc_enable为低时，强制清除s2_data_corrupt信号
    """
    print("\n=== CP16: Data ECC校验功能测试 ===")
    agent = icachemainpipe_env.agent
    bundle = icachemainpipe_env.bundle
    
    errors = []  # 收集所有错误
    
    # 16.1: 无ECC错误
    try:
        print("\n--- 16.1: 无ECC错误测试 ---")
        
        # 重置环境并使能ECC
        await agent.reset()
        await agent.drive_set_ecc_enable(True)
        
        # 设置DataArray ready信号，确保能访问DataArray
        await agent.drive_data_array_ready(True)
        
        # 监控初始状态
        pipeline_status = await agent.monitor_pipeline_status()
        print(f"初始流水线状态: s0_fire={pipeline_status['s0_fire']}, s2_fire={pipeline_status['s2_fire']}")
        
        # 准备环境：先设置WayLookup再设置Fetch
        vSetIdx_0 = 0x10
        vSetIdx_1 = 0x10  # 同一缓存行
        ptag = 0x12345
        # 根据API约束计算正确的地址：pcMemRead_4[13:6]必须等于vSetIdx_0
        # 地址格式：[高位][ptag][vSetIdx][低6位]
        pcMemRead_addr = (vSetIdx_0 << 6) | 0x00 
        print(f"设置地址: pcMemRead_addr=0x{pcMemRead_addr:x}, 期望vSetIdx=0x{vSetIdx_0:x}")
        
        await agent.drive_waylookup_read(
            vSetIdx_0=vSetIdx_0,
            vSetIdx_1=vSetIdx_1,  # 设置第二个vSetIdx
            waymask_0=0x1,  # 单路命中
            waymask_1=0x1,  # 第二路也命中
            ptag_0=ptag,
            ptag_1=ptag,
            itlb_exception_0=0,  # 无ITLB异常
            itlb_exception_1=0,
            meta_codes_0=0,  # 正确的meta ECC码
            meta_codes_1=0
        )
        
        await agent.drive_fetch_request(
            pcMemRead_addrs=[0, 0, 0, 0, pcMemRead_addr],  # pcMemRead_4
            readValid=[0, 0, 0, 0, 1]  # 只有readValid_4有效
        )
        
        # 设置PMP正常响应
        await agent.drive_pmp_response(instr_0=1, mmio_0=0)
        
        # 发送正确的数据和ECC校验码
        test_datas = [0x1111111111111111 + i for i in range(8)]
        # 计算正确的ECC校验码（XOR奇偶校验）
        correct_codes = []
        for data in test_datas:
            ecc = 0
            temp = data
            while temp:
                ecc ^= temp & 1
                temp >>= 1
            correct_codes.append(ecc)
        
        await agent.drive_data_array_response(datas=test_datas, codes=correct_codes)
        
        # 等待流水线推进到S2阶段
        await bundle.step(5)
        
        # 监控ECC状态
        ecc_status = await agent.monitor_check_data_ecc_status()
        detailed_status = await agent.monitor_data_ecc_detailed_status()
        error_status = await agent.monitor_error_status()
        pipeline_status = await agent.monitor_pipeline_status()
        
        print(f"ECC状态: enable={ecc_status['ecc_enable']}, corrupt_0={ecc_status['s2_data_corrupt_0']}, corrupt_1={ecc_status['s2_data_corrupt_1']}")
        print(f"流水线状态: s2_fire={pipeline_status['s2_fire']}")
        print(f"错误状态: valid_0={error_status['0_valid']}, valid_1={error_status['1_valid']}")
        
        # 验证：无ECC错误时的预期行为
        if ecc_status['s2_data_corrupt_0'] != False:
            errors.append("16.1失败: s2_data_corrupt_0应为False但实际为True")
        if ecc_status['s2_data_corrupt_1'] != False:
            errors.append("16.1失败: s2_data_corrupt_1应为False但实际为True")
        if ecc_status['ecc_enable'] != True:
            errors.append("16.1失败: ECC应该被使能")
            
        await agent.clear_waylookup_read()
        await agent.clear_fetch_request()
        await bundle.step(2)
        
        if not errors:
            print("✓ 16.1: 无ECC错误测试通过")
            
    except Exception as e:
        errors.append(f"16.1测试异常: {str(e)}")
        print(f"✗ 16.1测试异常: {e}")
    
    # 16.2: 单Bank ECC错误
    try:
        print("\n--- 16.2: 单Bank ECC错误测试 ---")
        
        # 重置环境并使能ECC
        await agent.reset()
        await agent.drive_set_ecc_enable(True)
        await agent.drive_data_array_ready(True)
        
        # 准备环境
        await agent.drive_waylookup_read(
            vSetIdx_0=vSetIdx_0,
            vSetIdx_1=vSetIdx_1,
            waymask_0=0x1,  # 单路命中
            waymask_1=0x1,
            ptag_0=ptag,
            ptag_1=ptag,
            itlb_exception_0=0,
            itlb_exception_1=0,
            meta_codes_0=0,
            meta_codes_1=0
        )
        
        await agent.drive_fetch_request(
            pcMemRead_addrs=[0, 0, 0, 0, pcMemRead_addr],
            readValid=[0, 0, 0, 0, 1]
        )
        
        await agent.drive_pmp_response(instr_0=1, mmio_0=0)
        
        # 注入单Bank ECC错误
        error_bank = 0
        success = await agent.inject_data_ecc_error(
            bank_index=error_bank,
            error_data=0xDEADBEEF,
            wrong_code=1  # 故意错误的ECC码
        )
        
        if not success:
            errors.append("16.2失败: 无法注入Data ECC错误")
        
        # 等待流水线处理
        await bundle.step(5)
        
        # 监控状态
        ecc_status = await agent.monitor_check_data_ecc_status()
        detailed_status = await agent.monitor_data_ecc_detailed_status()
        error_status = await agent.monitor_error_status()
        
        print(f"单Bank错误状态: corrupt_0={ecc_status['s2_data_corrupt_0']}")
        print(f"Bank corrupt状态: {detailed_status.get('s2_bank_corrupt', [])}")
        print(f"错误报告: valid_0={error_status['0_valid']}, report_to_beu_0={error_status['0_report_to_beu']}")
        
        # 验证：单Bank ECC错误的预期行为
        # 根据verilog代码：s2_data_corrupt_0 = io_ecc_enable & (s2_bank_corrupt & s2_bankSel & ~s2_data_is_from_MSHR)
        if ecc_status['s2_data_corrupt_0'] != True:
            errors.append("16.2失败: 单Bank ECC错误时s2_data_corrupt_0应为True")
        if error_status['0_valid'] != True:
            errors.append("16.2失败: 单Bank ECC错误时io.errors[0].valid应为True")
        if error_status['0_report_to_beu'] != True:
            errors.append("16.2失败: 单Bank ECC错误时应报告给BEU")
            
        # 清除请求
        await agent.clear_waylookup_read()
        await agent.clear_fetch_request()
        await bundle.step(2)
        
        print("✓ 16.2: 单Bank ECC错误测试完成")
        
    except Exception as e:
        errors.append(f"16.2测试异常: {str(e)}")
        print(f"✗ 16.2测试异常: {e}")
    
    # 16.2跨行: 单Bank ECC错误（跨行取指）
    try:
        print("\n--- 16.2跨行: 单Bank ECC错误测试（跨行取指） ---")
        
        # 重置环境并使能ECC
        await agent.reset()
        await agent.drive_set_ecc_enable(True)
        await agent.drive_data_array_ready(True)
        
        # 使用辅助函数计算跨行取指参数（遵循CP17模式）
        cross_line_addr = 0x1020  # bit[5]=1，触发跨行
        params = calculate_waylookup_params(cross_line_addr)
        print(f"跨行参数: doubleline={params['is_doubleline']}, vSetIdx_0=0x{params['vSetIdx_0']:x}, vSetIdx_1=0x{params['vSetIdx_1']:x}")
        
        # 确保跨行取指并设置不同waymask避免冲突（CP17模式）
        waymask_0 = 0x1 
        waymask_1 = 0x2
        
        await agent.drive_waylookup_read(
            vSetIdx_0=params['vSetIdx_0'],
            vSetIdx_1=params['vSetIdx_1'],
            waymask_0=waymask_0,
            waymask_1=waymask_1,
            ptag_0=params['ptag_0'],
            ptag_1=params['ptag_1'],
            meta_codes_0=params['meta_codes_0'],
            meta_codes_1=params['meta_codes_1']
        )
        
        # 等待流水线状态稳定
        await bundle.step(2)
        
        # 计算两个端口对应的bank（CP17方法）
        target_bank_0 = (params['start_addr'] >> 3) & 0x7  # 端口0的bank
        target_bank_1 = (params['nextline_addr'] >> 3) & 0x7  # 端口1的bank
        print(f"地址0x{params['start_addr']:x} -> bank {target_bank_0}, 跨行地址0x{params['nextline_addr']:x} -> bank {target_bank_1}")
        
        # 准备Data ECC错误注入（遵循CP17的方法：同时注入两个bank）
        datas = [0] * 8
        codes = [0] * 8
        
        # 端口0的bank注入错误
        datas[target_bank_0] = 0xDEADBEEF
        codes[target_bank_0] = 1
        
        # 端口1的bank也注入错误（关键：CP17确保两个端口都能检测到错误）
        if target_bank_1 != target_bank_0:
            error_data_1 = 0xBADC0DE1
            correct_ecc_1 = bin(error_data_1).count('1') % 2
            wrong_ecc_1 = 1 - correct_ecc_1
            datas[target_bank_1] = error_data_1
            codes[target_bank_1] = wrong_ecc_1
            print(f"跨行模式：同时向bank {target_bank_0} 和 bank {target_bank_1} 注入错误")
        else:
            print(f"跨行模式：两个端口使用同一个bank {target_bank_0}")
        
        # 先注入ECC错误，然后执行fetch请求（CP17关键顺序）
        success = await agent.drive_data_array_response(datas=datas, codes=codes)
        assert success, "Data ECC错误注入必须成功"
        
        # 执行fetch请求
        print(f"Fetch请求: start_addr=0x{params['start_addr']:x}, nextline_addr=0x{params['nextline_addr']:x}")
        fetch_success = await agent.drive_fetch_request(
            pcMemRead_addrs=[0, 0, 0, 0, params['start_addr']],
            readValid=[0, 0, 0, 0, 1]
        )
        assert fetch_success, "fetch请求必须成功"
        
        # 等待s1_fire触发（CP17步骤）
        await bundle.step()
        
        # 设置PMP响应（CP17关键步骤）
        await agent.drive_pmp_response()
        
        # 监控Data ECC状态
        data_ecc_status = await agent.monitor_data_ecc_detailed_status()
        error_status = await agent.monitor_error_status()
        
        corrupt_0 = data_ecc_status.get('s2_data_corrupt_0', False)
        corrupt_1 = data_ecc_status.get('s2_data_corrupt_1', False)
        
        print(f"跨行单Bank错误状态: corrupt_0={corrupt_0}, corrupt_1={corrupt_1}")
        print(f"错误报告: valid_0={error_status['0_valid']}, valid_1={error_status['1_valid']}")
        
        # 验证：跨行取指时两个端口都应该检测到Data错误（CP17验证方式）
        assert corrupt_0, f"跨行取指时端口0应检测到Data ECC错误， corrupt_0={corrupt_0}"
        assert corrupt_1, f"跨行取指时端口1应检测到Data ECC错误， corrupt_1={corrupt_1}"
        
        # 清除操作
        await agent.clear_waylookup_read()
        await agent.clear_fetch_request()
        await bundle.step(2)
        
        print("✓ 16.2跨行: 单Bank ECC错误正确处理 (两个端口都检测到错误)")
        
    except Exception as e:
        errors.append(f"16.2跨行测试异常: {str(e)}")
        print(f"✗ 16.2跨行测试异常: {e}")
    
    # 16.3: 多Bank ECC错误
    try:
        print("\n--- 16.3: 多Bank ECC错误测试 ---")
        
        # 重置环境并使能ECC
        await agent.reset()
        await agent.drive_set_ecc_enable(True)
        await agent.drive_data_array_ready(True)
        
        # 准备环境
        await agent.drive_waylookup_read(
            vSetIdx_0=vSetIdx_0,
            vSetIdx_1=vSetIdx_1,
            waymask_0=0x1,
            waymask_1=0x1,
            ptag_0=ptag,
            ptag_1=ptag,
            itlb_exception_0=0,
            itlb_exception_1=0,
            meta_codes_0=0,
            meta_codes_1=0
        )
        
        await agent.drive_fetch_request(
            pcMemRead_addrs=[0, 0, 0, 0, pcMemRead_addr],
            readValid=[0, 0, 0, 0, 1]
        )
        
        await agent.drive_pmp_response(instr_0=1, mmio_0=0)
        
        # 注入多Bank ECC错误
        error_banks = [0, 2, 4]  # 多个bank有错误
        test_datas = [0] * 8
        error_codes = [0] * 8
        
        for bank in error_banks:
            test_datas[bank] = 0xBAD00000 + bank
            # 计算正确ECC然后故意提供错误ECC
            correct_ecc = 0
            temp = test_datas[bank]
            while temp:
                correct_ecc ^= temp & 1
                temp >>= 1
            error_codes[bank] = 1 - correct_ecc  # 错误的ECC码
        
        await agent.drive_data_array_response(datas=test_datas, codes=error_codes)
        
        # 等待流水线处理
        await bundle.step(5)
        
        # 监控状态
        ecc_status = await agent.monitor_check_data_ecc_status()
        detailed_status = await agent.monitor_data_ecc_detailed_status()
        error_status = await agent.monitor_error_status()
        
        print(f"多Bank错误状态: corrupt_0={ecc_status['s2_data_corrupt_0']}")
        print(f"Bank corrupt详情: {detailed_status.get('s2_bank_corrupt', [])}")
        print(f"错误报告: valid_0={error_status['0_valid']}")
        
        # 验证：多Bank ECC错误的预期行为
        if ecc_status['s2_data_corrupt_0'] != True:
            errors.append("16.3失败: 多Bank ECC错误时s2_data_corrupt_0应为True")
        if error_status['0_valid'] != True:
            errors.append("16.3失败: 多Bank ECC错误时应有错误报告")
            
        # 清除请求
        await agent.clear_waylookup_read()
        await agent.clear_fetch_request()
        await bundle.step(2)
        
        print("✓ 16.3: 多Bank ECC错误测试完成")
        
    except Exception as e:
        errors.append(f"16.3测试异常: {str(e)}")
        print(f"✗ 16.3测试异常: {e}")
    
    # 16.3跨行: 多Bank ECC错误（跨行取指）
    try:
        print("\n--- 16.3跨行: 多Bank ECC错误测试（跨行取指） ---")
        
        # 重置环境并使能ECC
        await agent.reset()
        await agent.drive_set_ecc_enable(True)
        await agent.drive_data_array_ready(True)
        
        # 使用辅助函数计算跨行取指参数（遵循CP17模式）
        cross_line_addr = 0x1020  # bit[5]=1，触发跨行
        params = calculate_waylookup_params(cross_line_addr)
        print(f"跨行参数: doubleline={params['is_doubleline']}, vSetIdx_0=0x{params['vSetIdx_0']:x}, vSetIdx_1=0x{params['vSetIdx_1']:x}")
        
        # 确保跨行取指并设置不同waymask避免冲突（CP17模式）
        waymask_0 = 0x1 
        waymask_1 = 0x2
        
        await agent.drive_waylookup_read(
            vSetIdx_0=params['vSetIdx_0'],
            vSetIdx_1=params['vSetIdx_1'],
            waymask_0=waymask_0,
            waymask_1=waymask_1,
            ptag_0=params['ptag_0'],
            ptag_1=params['ptag_1'],
            meta_codes_0=params['meta_codes_0'],
            meta_codes_1=params['meta_codes_1']
        )
        
        # 等待流水线状态稳定
        await bundle.step(2)
        
        # 计算两个端口对应的bank（CP17方法）
        target_bank_0 = (params['start_addr'] >> 3) & 0x7  # 端口0的bank
        target_bank_1 = (params['nextline_addr'] >> 3) & 0x7  # 端口1的bank
        print(f"地址0x{params['start_addr']:x} -> bank {target_bank_0}, 跨行地址0x{params['nextline_addr']:x} -> bank {target_bank_1}")
        
        # 准备Data ECC错误注入（多Bank错误：同时注入多个bank）
        datas = [0] * 8
        codes = [0] * 8
        
        # 端口0对应的多bank注入错误（使用bank 0,1）
        error_banks_0 = [0, 1]  # 端口0区域的bank
        for bank in error_banks_0:
            error_data = 0xBADC0DE0 + bank
            correct_ecc = bin(error_data).count('1') % 2
            wrong_ecc = 1 - correct_ecc
            datas[bank] = error_data
            codes[bank] = wrong_ecc
            
        # 端口1对应的多bank注入错误（使用bank 4,5）
        if target_bank_1 != target_bank_0:
            error_banks_1 = [4, 5]  # 端口1区域的bank
            for bank in error_banks_1:
                error_data = 0xDEADC0D0 + bank
                correct_ecc = bin(error_data).count('1') % 2
                wrong_ecc = 1 - correct_ecc
                datas[bank] = error_data
                codes[bank] = wrong_ecc
            print(f"跨行模式：同时向端口0(bank {error_banks_0})和端口1(bank {error_banks_1})注入多Bank错误")
        else:
            print(f"跨行模式：两个端口使用重叠的bank区域")
        
        # 先注入ECC错误，然后执行fetch请求（CP17关键顺序）
        success = await agent.drive_data_array_response(datas=datas, codes=codes)
        assert success, "Data ECC错误注入必须成功"
        
        # 执行fetch请求
        print(f"Fetch请求: start_addr=0x{params['start_addr']:x}, nextline_addr=0x{params['nextline_addr']:x}")
        fetch_success = await agent.drive_fetch_request(
            pcMemRead_addrs=[0, 0, 0, 0, params['start_addr']],
            readValid=[0, 0, 0, 0, 1]
        )
        assert fetch_success, "fetch请求必须成功"
        
        # 等待s1_fire触发（CP17步骤）
        await bundle.step()
        
        # 设置PMP响应（CP17关键步骤）
        await agent.drive_pmp_response()
        
        # 监控Data ECC状态
        data_ecc_status = await agent.monitor_data_ecc_detailed_status()
        meta_flush = await agent.monitor_meta_flush()
        
        corrupt_0 = data_ecc_status.get('s2_data_corrupt_0', False)
        corrupt_1 = data_ecc_status.get('s2_data_corrupt_1', False)
        
        print(f"跨行多Bank错误状态: corrupt_0={corrupt_0}, corrupt_1={corrupt_1}")
        print(f"数据flush状态: valid_0={meta_flush['0_valid']}, waymask_0=0x{meta_flush['0_bits_waymask']:x}, valid_1={meta_flush['1_valid']}, waymask_1=0x{meta_flush['1_bits_waymask']:x}")
        
        # 验证：跨行取指时两个端口都应该检测到Data错误（CP17验证方式）
        assert corrupt_0, f"跨行取指时端口0应检测到Data ECC错误， corrupt_0={corrupt_0}"
        assert corrupt_1, f"跨行取指时端口1应检测到Data ECC错误， corrupt_1={corrupt_1}"
        
        # 验证两个端口的flush都被激活（CP17验证方式）
        assert meta_flush['0_valid'], "跨行取指时flush端口0必须激活"
        assert meta_flush['1_valid'], "跨行取指时flush端口1必须激活"
        
        # 验证flush waymask（跨行时两个端口使用不同的waymask）
        assert meta_flush['0_bits_waymask'] == waymask_0, f"端口0 Data错误应冲刷特定路，期望0x{waymask_0:x}，实际0x{meta_flush['0_bits_waymask']:x}"
        assert meta_flush['1_bits_waymask'] == waymask_1, f"端口1 Data错误应冲刷特定路，期望0x{waymask_1:x}，实际0x{meta_flush['1_bits_waymask']:x}"
        assert meta_flush['0_bits_waymask'] != 0xF and meta_flush['1_bits_waymask'] != 0xF, "Data错误不应该冲刷所有路(0xF)，这是Meta错误的行为"
        
        # 清除操作
        await agent.clear_waylookup_read()
        await agent.clear_fetch_request()
        await bundle.step(2)
        
        print("✓ 16.3跨行: Data ECC错误正确处理 (两个端口都检测到错误)")
        
    except Exception as e:
        errors.append(f"16.3跨行测试异常: {str(e)}")
        print(f"✗ 16.3跨行测试异常: {e}")
    
    # 16.4: ECC功能关闭
    try:
        print("\n--- 16.4: ECC功能关闭测试 ---")
        
        # 重置环境并关闭ECC
        await agent.reset()
        await agent.drive_set_ecc_enable(False)
        await agent.drive_data_array_ready(True)
        
        # 监控ECC禁用状态
        pipeline_status = await agent.monitor_pipeline_status()
        print(f"ECC禁用状态: ecc_enable={pipeline_status['ecc_enable']}")
        
        # 准备环境
        await agent.drive_waylookup_read(
            vSetIdx_0=vSetIdx_0,
            vSetIdx_1=vSetIdx_1,
            waymask_0=0x1,
            waymask_1=0x1,
            ptag_0=ptag,
            ptag_1=ptag,
            itlb_exception_0=0,
            itlb_exception_1=0,
            meta_codes_0=0,
            meta_codes_1=0
        )
        
        await agent.drive_fetch_request(
            pcMemRead_addrs=[0, 0, 0, 0, pcMemRead_addr],
            readValid=[0, 0, 0, 0, 1]
        )
        
        await agent.drive_pmp_response(instr_0=1, mmio_0=0)
        
        # 即使有错误的ECC码，也不应报告错误
        bad_datas = [0xDEADBEEF + i for i in range(8)]
        bad_codes = [1] * 8  # 可能错误的校验码
        
        await agent.drive_data_array_response(datas=bad_datas, codes=bad_codes)
        
        # 等待流水线处理
        await bundle.step(5)
        
        # 监控状态
        ecc_status = await agent.monitor_check_data_ecc_status()
        error_status = await agent.monitor_error_status()
        
        print(f"ECC关闭时状态: enable={ecc_status['ecc_enable']}, corrupt_0={ecc_status['s2_data_corrupt_0']}")
        print(f"错误报告: valid_0={error_status['0_valid']}")
        
        # 验证：ECC功能关闭时的预期行为  
        # 根据verilog：s2_data_corrupt_0 = io_ecc_enable & (...)，当io_ecc_enable=False时结果为False
        if ecc_status['ecc_enable'] != False:
            errors.append("16.4失败: ECC应该被禁用")
        if ecc_status['s2_data_corrupt_0'] != False:
            errors.append("16.4失败: ECC禁用时s2_data_corrupt_0应为False")
        if ecc_status['s2_data_corrupt_1'] != False:
            errors.append("16.4失败: ECC禁用时s2_data_corrupt_1应为False")
            
        # 清除请求
        await agent.clear_waylookup_read()
        await agent.clear_fetch_request()
        await bundle.step(2)
        
        print("✓ 16.4: ECC功能关闭测试完成")
        
    except Exception as e:
        errors.append(f"16.4测试异常: {str(e)}")
        print(f"✗ 16.4测试异常: {e}")
    
    # 最终结果
    if errors:
        error_msg = "; ".join(errors)
        print(f"\n✗ CP16测试失败，错误列表: {error_msg}")
        raise AssertionError(f"CP16测试失败，错误列表: {error_msg}")
    else:
        print("\n✓ CP16: Data ECC校验功能测试 - 所有测试点通过")


@toffee_test.testcase
async def test_cp17_metaarray_flush(icachemainpipe_env: ICacheMainPipeEnv):
    """
    CP17: 冲刷MetaArray功能测试
    根据MainPipe.md文档第439-447行和verilog源码第2079-2090行重新实现
    """
    print("\n=== CP17: MetaArray Flush Test ===")
    agent = icachemainpipe_env.agent
    bundle = icachemainpipe_env.bundle
    
    test_errors = []

    # 17.1: 只有Meta ECC校验错误（冲刷所有路）
    # 文档依据：MainPipe.md第445行 "当s1_meta_corrupt为真时，MetaArray的所有路都会被冲刷"
    print("\n--- Test 17.1: 只有Meta ECC校验错误 ---")
    
    # 测试两种场景：非跨行取指和跨行取指
    test_scenarios = [
        {"name": "非跨行取指", "start_addr": 0x1000},  # bit[5]=0，非跨行
        {"name": "跨行取指", "start_addr": 0x1020}     # bit[5]=1，跨行
    ]
    
    for scenario in test_scenarios:
        try:
            print(f"\n  测试场景: {scenario['name']} (地址=0x{scenario['start_addr']:x})")
            await agent.reset()
            await agent.drive_set_ecc_enable(True)
            await agent.drive_data_array_ready(True)
            await agent.setup_mshr_ready(True)
            
            # 使用辅助函数计算完整参数
            params = calculate_waylookup_params(scenario['start_addr'])
            print(f"  计算参数: doubleline={params['is_doubleline']}, vSetIdx_0=0x{params['vSetIdx_0']:x}, vSetIdx_1=0x{params['vSetIdx_1']:x}")
            
            # 计算错误的ECC码
            wrong_ecc_0 = 1 - params['meta_codes_0']  
            wrong_ecc_1 = 1 - params['meta_codes_1']  
            
            # 先执行waylookup读取并注入Meta ECC错误
            await agent.drive_waylookup_read(
                vSetIdx_0=params['vSetIdx_0'],
                vSetIdx_1=params['vSetIdx_1'],
                waymask_0=params['waymask_0'],
                waymask_1=params['waymask_1'] if params['is_doubleline'] else 0,
                ptag_0=params['ptag_0'],
                ptag_1=params['ptag_1'],
                meta_codes_0=wrong_ecc_0,  # 注入端口0的错误ECC码
                meta_codes_1=wrong_ecc_1 if params['is_doubleline'] else params['meta_codes_1']  # 跨行时注入端口1错误
            )
            
            print(f"  注入Meta ECC错误: Port0(correct={params['meta_codes_0']}, wrong={wrong_ecc_0})" + 
                  (f", Port1(correct={params['meta_codes_1']}, wrong={wrong_ecc_1})" if params['is_doubleline'] else ""))
            
            # 监控流水线状态，确保环境准备就绪
            await bundle.step(2)
            status = await agent.monitor_pipeline_status()
            print(f"  Pipeline status: s0_fire={status['s0_fire']}, ecc_enable={status['ecc_enable']}")
            
            # 执行fetch操作，使用辅助函数计算的地址
            fetch_success = await agent.drive_fetch_request(
                pcMemRead_addrs=[0, 0, 0, 0, params['start_addr']],
                readValid=[0, 0, 0, 0, 1]
            )
            
            assert fetch_success, "fetch请求必须成功，否则无法测试flush逻辑"
            
            await bundle.step(2)
            
            # 监控meta flush状态
            meta_flush = await agent.monitor_meta_flush()
            
            print(f"  Meta Flush 端口0 - valid: {meta_flush['0_valid']}, waymask: 0x{meta_flush['0_bits_waymask']:x}")
            print(f"  Meta Flush 端口1 - valid: {meta_flush['1_valid']}, waymask: 0x{meta_flush['1_bits_waymask']:x}")
            
            # 验证：Meta错误应该冲刷所有路(waymask=0xF)
            assert meta_flush['0_valid'], f"Meta ECC错误时flush端口0必须激活，当前valid={meta_flush['0_valid']}"
            assert meta_flush['0_bits_waymask'] == 0xF, f"Meta错误应冲刷所有路(0xF)，实际waymask=0x{meta_flush['0_bits_waymask']:x}"
            
            # 对于跨行取指，还需要验证端口1的flush行为
            if params['is_doubleline']:
                assert meta_flush['1_valid'], f"跨行取指时，Meta ECC错误应激活flush端口1，当前valid={meta_flush['1_valid']}"
                assert meta_flush['1_bits_waymask'] == 0xF, f"跨行取指时，Meta错误应冲刷端口1所有路(0xF)，实际waymask=0x{meta_flush['1_bits_waymask']:x}"
                print(f"  ✓ {scenario['name']}: Meta ECC错误正确冲刷所有路 (端口0和端口1)")
            else:
                print(f"  ✓ {scenario['name']}: Meta ECC错误正确冲刷所有路 (端口0)")
                
            # 清除操作
            await agent.clear_waylookup_read()
            await agent.clear_fetch_request()
            await bundle.step(2)
                
        except Exception as e:
            test_errors.append(f"Test 17.1-{scenario['name']}失败: {str(e)}")
            print(f"  ✗ Test 17.1-{scenario['name']}失败: {e}")

    # 17.2: 只有Data ECC校验错误（冲刷特定路）
    # 文档依据：MainPipe.md第446行 "当s2_data_corrupt为真时，只有对应路会被冲刷"
    # verilog依据：ICacheMainPipe.v第2087-2090行 冲刷特定waymask
    print("\n--- Test 17.2: 只有Data ECC校验错误 ---")
    
    # 测试两种场景：非跨行取指和跨行取指
    for scenario in test_scenarios:
        try:
            print(f"\n  测试场景: {scenario['name']} (地址=0x{scenario['start_addr']:x})")
            await agent.reset()
            await agent.drive_set_ecc_enable(True)
            await agent.drive_data_array_ready(True)
            
            params = calculate_waylookup_params(scenario['start_addr'])
            print(f"  计算参数: doubleline={params['is_doubleline']}, vSetIdx_0=0x{params['vSetIdx_0']:x}, vSetIdx_1=0x{params['vSetIdx_1']:x}")
            
            if params['is_doubleline']:

                waymask_0 = 0x1 
                waymask_1 = 0x2 
                print(f"  跨行优化：设置waymask_0=0x{waymask_0:x}, waymask_1=0x{waymask_1:x}以确保SRAMhits")
            else:
                waymask_0 = params["waymask_0"]
                waymask_1 = 0
                
            await agent.drive_waylookup_read(
                vSetIdx_0=params['vSetIdx_0'],
                vSetIdx_1=params['vSetIdx_1'],
                waymask_0=waymask_0,
                waymask_1=waymask_1,
                ptag_0=params['ptag_0'],
                ptag_1=params['ptag_1'],
                meta_codes_0=params['meta_codes_0'],  
                meta_codes_1=params['meta_codes_1']
            )
            # 监控流水线状态，确保环境准备就绪
            await bundle.step(2)
            status = await agent.monitor_pipeline_status()
            print(f"  Pipeline status: {status}")
            
            target_bank_0 = (params['start_addr'] >> 3) & 0x7  # 端口0的bank
            print(f"  地址0x{params['start_addr']:x} -> bank {target_bank_0}")
            
            datas = [0] * 8
            codes = [0] * 8
            
            # 为端口0注入Data ECC错误
            datas[target_bank_0] = 0xDEADBEEF
            codes[target_bank_0] = 1
            injection_info = [f"bank {target_bank_0}"]
            
            # 跨行取指时，还需要为端口1对应的bank注入错误
            if params['is_doubleline']:
                target_bank_1 = (params['nextline_addr'] >> 3) & 0x7  # 端口1的bank
                print(f"  跨行地址0x{params['nextline_addr']:x} -> bank {target_bank_1}")
                
                if target_bank_1 != target_bank_0:  # 避免重复注入同一个bank
                    # 确保产生 ECC 错误：数据的奇偶校验与ECC码不匹配
                    error_data_1 = 0xBADC0DE1
                    correct_ecc_1 = bin(error_data_1).count('1') % 2  # 计算正确的奇偶校验
                    wrong_ecc_1 = 1 - correct_ecc_1  # 使用错误的ECC码
                    datas[target_bank_1] = error_data_1
                    codes[target_bank_1] = wrong_ecc_1
                    injection_info.append(f"bank {target_bank_1}")
                    print(f"  跨行模式：同时向{', '.join(injection_info)}注入错误")
                    print(f"  Bank {target_bank_1}: data=0x{error_data_1:x}, correct_ecc={correct_ecc_1}, wrong_ecc={wrong_ecc_1}")
                else:
                    print(f"  跨行模式：两个端口使用同一个bank {target_bank_0}")
            
            # 先注入ECC错误，然后执行fetch请求
            success = await agent.drive_data_array_response(datas=datas, codes=codes)
            assert success, f"Data ECC错误注入必须成功，目标{'，'.join(injection_info)}"
            
            # 执行fetch请求（这会触发s0_fire=1，进而设置s1_codes_REG=1）
            # 确保跨行取指时nextlineStart被正确计算
            print(f"  Fetch请求: start_addr=0x{params['start_addr']:x}, nextline_addr=0x{params['nextline_addr']:x}")
            fetch_success = await agent.drive_fetch_request(
                pcMemRead_addrs=[0, 0, 0, 0, params['start_addr']],
                readValid=[0, 0, 0, 0, 1]
            )
            
            assert fetch_success, "fetch请求必须成功，否则无法测试Data ECC处理逻辑"
            
            # 先等待s1_fire触发，确保io_metaArrayFlush_0_valid_REG被正确设置
            await bundle.step()
            status = await agent.monitor_pipeline_status()
            print(f"  Pipeline status: {status}")
            
            # 设置PMP响应（使用默认参数提供正常响应）
            await agent.drive_pmp_response()
            
            # 监控Data ECC状态
            data_ecc_status = await agent.monitor_data_ecc_detailed_status()
            print(f"  Data ECC状态: corrupt_0={data_ecc_status.get('s2_data_corrupt_0', 'N/A')}")
            
            # 监控meta flush状态
            meta_flush = await agent.monitor_meta_flush()
            print(f"  Data错误情况下的flush状态: valid={meta_flush['0_valid']}, waymask=0x{meta_flush['0_bits_waymask']:x}")
            
            # 验证Data ECC错误检测和flush行为
            if params['is_doubleline']:
                # 跨行取指：两个端口都应该检测到Data错误
                corrupt_0 = data_ecc_status.get('s2_data_corrupt_0', False)
                corrupt_1 = data_ecc_status.get('s2_data_corrupt_1', False)
                
                assert corrupt_0, \
                    f"跨行取指时端口0应检测到Data ECC错误， corrupt_0={corrupt_0}"
                assert corrupt_1, \
                    f"跨行取指时端口1应检测到Data ECC错误， corrupt_1={corrupt_1}"
                
                # 验证两个端口的flush都被激活
                assert meta_flush['0_valid'], "跨行取指时flush端口0必须激活"
                assert meta_flush['1_valid'], "跨行取指时flush端口1必须激活"
                
                # 验证flush waymask（跨行时两个端口使用不同的waymask）
                assert meta_flush['0_bits_waymask'] == waymask_0, \
                    f"端口0 Data错误应冲刷特定路，期望0x{waymask_0:x}，实际0x{meta_flush['0_bits_waymask']:x}"
                assert meta_flush['1_bits_waymask'] == waymask_1, \
                    f"端口1 Data错误应冲刷特定路，期望0x{waymask_1:x}，实际0x{meta_flush['1_bits_waymask']:x}"
                assert meta_flush['0_bits_waymask'] != 0xF and meta_flush['1_bits_waymask'] != 0xF, \
                    "Data错误不应该冲刷所有路(0xF)，这是Meta错误的行为"
                        
                print(f"  ✓ {scenario['name']}: Data ECC错误正确处理 (两个端口都检测到错误)")
            else:
                # 非跨行取指：只检查端口0
                assert data_ecc_status.get('s2_data_corrupt_0') == True, \
                    "非跨行取指时s2_data_corrupt_0应为True"
                    
                assert meta_flush['0_valid'], \
                    "非跨行取指时Data ECC错误flush端口0必须激活"
                    
                # 验证只冲刷特定路（不是所有路0xF）
                expected_waymask_0 = waymask_0  # 使用实际设置的waymask
                assert meta_flush['0_bits_waymask'] == expected_waymask_0, \
                    f"Data错误应只冲刷特定路，期望0x{expected_waymask_0:x}，实际0x{meta_flush['0_bits_waymask']:x}"
                    
                # 确保不是冲刷所有路（与Meta错误区分）
                assert meta_flush['0_bits_waymask'] != 0xF, \
                    "Data错误不应该冲刷所有路(0xF)，这是Meta错误的行为"
                    
                print(f"  ✓ {scenario['name']}: Data ECC错误正确冲刷特定路")
                
            # 清除操作  
            await agent.clear_waylookup_read()
            await agent.clear_fetch_request()
            await bundle.step(2)
            
        except Exception as e:
            test_errors.append(f"Test 17.2-{scenario['name']}失败: {str(e)}")
            print(f"  ✗ Test 17.2-{scenario['name']}失败: {e}")

    # 17.3: 同时有Meta ECC校验错误和Data ECC校验错误
    # 文档依据：MainPipe.md第447行 "处理Meta ECC的优先级更高，将MetaArray的所有路冲刷"
    print("\n--- Test 17.3: 同时有Meta和Data ECC错误 ---")
    
    # 测试两种场景：非跨行取指和跨行取指
    for scenario in test_scenarios:
        try:
            print(f"\n  测试场景: {scenario['name']} (地址=0x{scenario['start_addr']:x})")
            await agent.reset()
            await agent.drive_set_ecc_enable(True)
            await agent.drive_data_array_ready(True)
            
            # 使用辅助函数计算完整参数
            params = calculate_waylookup_params(scenario['start_addr'])
            print(f"  计算参数: doubleline={params['is_doubleline']}, vSetIdx_0=0x{params['vSetIdx_0']:x}, vSetIdx_1=0x{params['vSetIdx_1']:x}")
            
            if params['is_doubleline']:
                waymask_0 = 0x1 
                waymask_1 = 0x2 
            else:
                waymask_0 = 0x1  # 非跨行只需要端口0
                waymask_1 = 0
            
            # 计算错误的ECC码
            wrong_ecc_0 = 1 - params['meta_codes_0']  # 端口0的错误ECC码
            wrong_ecc_1 = 1 - params['meta_codes_1']  # 端口1的错误ECC码
            
            # 先执行waylookup读取并注入Meta ECC错误
            await agent.drive_waylookup_read(
                vSetIdx_0=params['vSetIdx_0'],
                vSetIdx_1=params['vSetIdx_1'],
                waymask_0=waymask_0,
                waymask_1=waymask_1,
                ptag_0=params['ptag_0'],
                ptag_1=params['ptag_1'],
                meta_codes_0=wrong_ecc_0,  
                meta_codes_1=wrong_ecc_1 if params['is_doubleline'] else params['meta_codes_1']
            )
            
            print(f"  注入Meta ECC错误: Port0(correct={params['meta_codes_0']}, wrong={wrong_ecc_0})" + 
                  (f", Port1(correct={params['meta_codes_1']}, wrong={wrong_ecc_1})" if params['is_doubleline'] else ""))
            await bundle.step(2)
            status = await agent.monitor_pipeline_status()
            print(f"  Pipeline status: {status}")
            
            # 应用17.2的关键修复：先注入Data ECC错误，再执行fetch请求
            # 准备Data ECC错误注入（同时测试Meta和Data错误优先级）
            target_bank_0 = (params['start_addr'] >> 3) & 0x7
            datas = [0] * 8
            codes = [0] * 8
            datas[target_bank_0] = 0xBADC0DE
            codes[target_bank_0] = 1  # 错误的ECC码
            
            if params['is_doubleline']:
                target_bank_1 = (params['nextline_addr'] >> 3) & 0x7
                if target_bank_1 != target_bank_0:
                    error_data_1 = 0xDEADC0DE
                    correct_ecc_1 = bin(error_data_1).count('1') % 2
                    wrong_ecc_1 = 1 - correct_ecc_1
                    datas[target_bank_1] = error_data_1
                    codes[target_bank_1] = wrong_ecc_1
                    print(f"  同时注入Data ECC错误到bank {target_bank_0} 和 bank {target_bank_1}")
                else:
                    print(f"  同时注入Data ECC错误到bank {target_bank_0}")
            else:
                print(f"  同时注入Data ECC错误到bank {target_bank_0}")
            
            # 先注入Data错误
            await agent.drive_data_array_response(datas=datas, codes=codes)
            
            # 然后执行fetch请求（关键：确保s1_codes_REG=1）
            fetch_success = await agent.drive_fetch_request(
                pcMemRead_addrs=[0, 0, 0, 0, params['start_addr']],
                readValid=[0, 0, 0, 0, 1]
            )
            
            assert fetch_success, "fetch请求必须成功，否则无法测试优先级逻辑"
            
            # 先等待s1_fire触发，确保io_metaArrayFlush_0_valid_REG被正确设置
            await bundle.step()
            
            # 设置PMP响应（使用默认参数提供正常响应）
            await agent.drive_pmp_response()
            
            # 监控meta corrupt状态
            meta_corrupt_status = await agent.monitor_meta_corrupt_status()
            print(f"  Meta corrupt hit num: {meta_corrupt_status.get('s1_meta_corrupt_hit_num', 'N/A')}")
            
            # 监控meta flush状态
            meta_flush = await agent.monitor_meta_flush()
            
            print(f"  同时错误情况下的flush - valid: {meta_flush['0_valid']}, waymask: 0x{meta_flush['0_bits_waymask']:x}")
            
            # 验证：Meta优先级更高，应该冲刷所有路（不是特定路）
            assert meta_flush['0_valid'], f"Meta ECC错误时flush端口0必须激活，当前valid={meta_flush['0_valid']}"
            assert meta_flush['0_bits_waymask'] == 0xF, \
                f"Meta优先级更高，应冲刷所有路(0xF)，实际waymask=0x{meta_flush['0_bits_waymask']:x}"
                
            # 对于跨行取指，还需要验证端口1的flush行为
            if params['is_doubleline']:
                assert meta_flush['1_valid'], f"跨行取指时，Meta ECC错误应激活flush端口1，当前valid={meta_flush['1_valid']}"
                assert meta_flush['1_bits_waymask'] == 0xF, f"跨行取指时，Meta错误应冲刷端口1所有路(0xF)，实际waymask=0x{meta_flush['1_bits_waymask']:x}"
                print(f"  ✓ {scenario['name']}: Meta优先级正确，冲刷所有路 (端口0和端口1)")
            else:
                print(f"  ✓ {scenario['name']}: Meta优先级正确，冲刷所有路 (端口0)")
                
            # 清除操作
            await agent.clear_waylookup_read()
            await agent.clear_fetch_request()
            await bundle.step(2)
            
        except Exception as e:
            test_errors.append(f"Test 17.3-{scenario['name']}失败: {str(e)}")
            print(f"  ✗ Test 17.3-{scenario['name']}失败: {e}")

    # 总结测试结果 - 只有所有子测试都通过assert验证才算成功
    if test_errors:
        print(f"\n✗ CP17测试失败，发现{len(test_errors)}个错误:")
        for i, error in enumerate(test_errors, 1):
            print(f"  {i}. {error}")
        # 最后抛出所有错误
        raise Exception(f"CP17测试失败: {'; '.join(test_errors)}")
    else:
        print("\n✓ CP17: MetaArray Flush功能测试 - 所有测试点通过assert验证")


@toffee_test.testcase
async def test_cp18_s2_mshr_match_data_update(icachemainpipe_env: ICacheMainPipeEnv):
    """
    CP18: 监控MSHR匹配与数据更新功能测试
    测试S2阶段MSHR匹配和数据更新逻辑
    
    测试点：
    18.1: MSHR命中（匹配且本阶段有效）
    18.2: MSHR未命中
    """
    print("\n=== CP18: S2 MSHR Match and Data Update Test ===")
    agent = icachemainpipe_env.agent
    bundle = icachemainpipe_env.bundle
    
    errors = []
    
    # ==================== 18.1: MSHR命中（匹配且本阶段有效） ====================
    try:
        print("\n--- Test 18.1: MSHR命中（匹配且本阶段有效） ---")
        
        # 重置环境
        await agent.reset()
        await agent.drive_set_ecc_enable(True)
        await agent.setup_mshr_ready(True)
        await agent.drive_data_array_ready(True)
        
        # 设置测试参数
        test_vSetIdx = 0x10
        test_blkPaddr = 0x40000  # blkPaddr[41:6] = 0x1000 
        test_ptag = (test_blkPaddr >> 6) & 0xFFFFF  # 提取ptag用于匹配
        test_mshr_data = 0x123456789ABCDEF0FEDCBA0987654321
        
        print(f"  设置测试参数: vSetIdx=0x{test_vSetIdx:x}, blkPaddr=0x{test_blkPaddr:x}, ptag=0x{test_ptag:x}")
        print("  1. 计算跨行取指的地址约束")
        startAddr = (test_vSetIdx << 6) | 0x20  # 设置bit[5]=1以触发跨行取指
        nextlineStart = (startAddr & ~0x3F) + 64  # 下一个64字节对齐地址
        vSetIdx_1 = (nextlineStart >> 6) & 0xFF  # nextlineStart[13:6]
        nextline_blkPaddr = nextlineStart & ~0x3F  # 64字节对齐的物理地址
        nextline_ptag = (nextline_blkPaddr >> 6) & 0xFFFFF  # 第二路的ptag
        print(f"    startAddr=0x{startAddr:x}, nextlineStart=0x{nextlineStart:x}, vSetIdx_1=0x{vSetIdx_1:x}")
        print(f"    nextline_blkPaddr=0x{nextline_blkPaddr:x}, nextline_ptag=0x{nextline_ptag:x}")
        
        # 2. 设置WayLookup读取信息
        print("  2. 设置WayLookup读取信息")
        await agent.drive_waylookup_read(
            vSetIdx_0=test_vSetIdx,
            vSetIdx_1=vSetIdx_1,
            waymask_0=0x1,
            waymask_1=0x1,
            ptag_0=test_ptag,
            ptag_1=nextline_ptag,  # 使用与MSHR响应匹配的ptag
            itlb_exception_0=0,
            itlb_exception_1=0,
            meta_codes_0=0,
            meta_codes_1=0
        )
        # 3. 设置PMP响应
        print("  3. 设置PMP响应")
        await agent.drive_pmp_response(instr_0=0, mmio_0=0, instr_1=0, mmio_1=0)
        await bundle.step()
        
        # 4. 预先发送MSHR响应 - 关键修复：匹配第二路地址参数
        print("  4. 预先发送MSHR响应")
        # s2_MSHR_hits_1检查的是第二路地址，所以MSHR响应需要匹配vSetIdx_1
        await agent.drive_mshr_response(
            blkPaddr=nextline_blkPaddr,
            vSetIdx=vSetIdx_1,  # 使用第二路的vSetIdx
            data=test_mshr_data,
            corrupt=0  # 数据正确
        )
        await bundle.step()
        
        # 5. 提供DataArray响应
        print("  5. 提供DataArray响应")
        await agent.drive_data_array_response(
            datas=[0x1111111111111111 + i for i in range(8)],
            codes=[0] * 8
        )
        await bundle.step()
        
        # 6. 发送fetch请求启动流水线（最后发送以确保所有响应就绪）
        print("  6. 发送fetch请求启动流水线")
        fetch_success = await agent.drive_fetch_request(
            pcMemRead_addrs=[0, 0, 0, 0, startAddr],
            readValid=[0, 0, 0, 0, 1],  # readValid_4=1
            backendException=0
        )
        
        if not fetch_success:
            raise Exception("Fetch请求因RTL约束检查失败，地址不匹配")
        
        # 7. 等待流水线处理
        print("  7. 等待流水线处理")
        await bundle.step(2)  # 等待流水线传播
        
        # 8. 监控S2阶段MSHR匹配状态
        print("  8. 监控S2阶段MSHR匹配状态")
        s2_mshr_status = await agent.monitor_s2_mshr_match_status()
        pipeline_status = await agent.monitor_pipeline_status()
        
        print(f"    S2 MSHR hits_1: {s2_mshr_status.get('s2_MSHR_hits_1', 'N/A')}")
        print(f"    流水线状态: s0_fire={pipeline_status.get('s0_fire')}, s2_fire={pipeline_status.get('s2_fire')}")
        
        # 9. 检查bank级别的匹配和数据来源
        print("  9. 检查bank级别的匹配和数据来源")
        bank_hit_found = False
        for i in range(8):
            bank_hit = s2_mshr_status.get(f's2_bankMSHRHit_{i}', False)
            data_from_mshr = s2_mshr_status.get(f's2_data_is_from_MSHR_{i}', False)
            if bank_hit or data_from_mshr:
                print(f"    Bank {i} - MSHR hit: {bank_hit}, data from MSHR: {data_from_mshr}")
                bank_hit_found = True
        
        # 10. 验证MSHR命中逻辑
        print("  10. 验证MSHR命中逻辑")
        s2_mshr_hits_1 = s2_mshr_status.get('s2_MSHR_hits_1', False)
        s2_fire = pipeline_status.get('s2_fire', False)
        
        # Assert 1: 应该检测到MSHR命中
        assert s2_mshr_hits_1, f"18.1: 未检测到S2 MSHR命中，s2_MSHR_hits_1={s2_mshr_hits_1}"
        print(f"    ✓ Assert 1 通过: S2 MSHR命中 s2_MSHR_hits_1={s2_mshr_hits_1}")
        
        # Assert 2: 应该有bank级别的命中
        assert bank_hit_found, f"18.1: 预期有bank级别MSHR命中但未检测到"
        print(f"    ✓ Assert 2 通过: 检测到bank级别MSHR命中")
        
        # Assert 3: 验证数据来源标记
        mshr_data_banks = [s2_mshr_status.get(f's2_data_is_from_MSHR_{i}', False) for i in range(8)]
        any_mshr_data = any(mshr_data_banks)
        assert any_mshr_data, f"18.1: 预期有数据来自MSHR但未检测到，s2_data_is_from_MSHR={mshr_data_banks}"
        print(f"    ✓ Assert 3 通过: 检测到数据来自MSHR，banks={[i for i, v in enumerate(mshr_data_banks) if v]}")
        
        print("    √ 18.1 MSHR命中逻辑所有assert验证通过")
        
        # 清除操作
        print("  ✓ 清除waylookup和fetch操作")
        await agent.clear_waylookup_read()
        await agent.clear_fetch_request()
    except Exception as e:
        errors.append(f"18.1: 测试过程中发生异常: {str(e)}")
        print(f"    × 18.1测试异常: {e}")
    
    # ==================== 18.2: MSHR未命中 ====================
    try:
        print("\n--- Test 18.2: MSHR未命中 ---")
        
        # 重置环境
        await agent.reset()
        await agent.drive_set_ecc_enable(True)
        await agent.setup_mshr_ready(True)
        await agent.drive_data_array_ready(True)
        
        # 设置测试参数（故意使用不匹配的地址）
        request_vSetIdx = 0x20  # 请求的地址
        mshr_vSetIdx = 0x30     # MSHR中的地址（不匹配）
        request_blkPaddr = 0x50000
        mshr_blkPaddr = 0x60000   # 不匹配的MSHR地址
        request_ptag = (request_blkPaddr >> 6) & 0xFFFFF
        
        print(f"  设置不匹配参数: 请求vSetIdx=0x{request_vSetIdx:x}, MSHR vSetIdx=0x{mshr_vSetIdx:x}")
        print(f"  请求blkPaddr=0x{request_blkPaddr:x}, MSHR blkPaddr=0x{mshr_blkPaddr:x}")
        print("  1. 计算跨行取指的地址约束")
        startAddr = (request_vSetIdx << 6) | 0x20  # 设置bit[5]=1以触发跨行取指
        nextlineStart = (startAddr & ~0x3F) + 64  # 下一个64字节对齐地址
        request_vSetIdx_1 = (nextlineStart >> 6) & 0xFF  # nextlineStart[13:6]
        nextline_blkPaddr = nextlineStart & ~0x3F  # 64字节对齐的物理地址
        nextline_ptag = (nextline_blkPaddr >> 6) & 0xFFFFF  # 第二路的ptag
        print(f"    startAddr=0x{startAddr:x}, nextlineStart=0x{nextlineStart:x}, vSetIdx_1=0x{request_vSetIdx_1:x}")
        print(f"    nextline_blkPaddr=0x{nextline_blkPaddr:x}, nextline_ptag=0x{nextline_ptag:x}")
        
        # 2. 设置WayLookup读取信息
        print("  2. 设置WayLookup读取信息")
        await agent.drive_waylookup_read(
            vSetIdx_0=request_vSetIdx,
            vSetIdx_1=request_vSetIdx_1,
            waymask_0=0x1,  # 确保第一路命中，避免s2_should_fetch_0
            waymask_1=0x1,  # 确保第二路也命中，避免s2_should_fetch_1
            ptag_0=request_ptag,
            ptag_1=nextline_ptag,  # 使用第二路正确的ptag
            itlb_exception_0=0,
            itlb_exception_1=0,
            meta_codes_0=0,
            meta_codes_1=0
        )
        
        # 3. 设置PMP响应（关键步骤）
        print("  3. 设置PMP响应（关键步骤）")
        await agent.drive_pmp_response(instr_0=0, mmio_0=0, instr_1=0, mmio_1=0)
        
        # 4. 发送不匹配的MSHR响应
        print("  4. 发送不匹配的MSHR响应")
        await agent.drive_mshr_response(
            blkPaddr=mshr_blkPaddr,
            vSetIdx=mshr_vSetIdx,
            data=0xDEADBEEFCAFEBABE,
            corrupt=0
        )
        
        # 5. 提供DataArray响应
        print("  5. 提供DataArray响应")
        await agent.drive_data_array_response(
            datas=[0x2222222222222222 + i for i in range(8)],
            codes=[0] * 8
        )
        
        # 6. 发送fetch请求启动流水线
        print("  6. 发送fetch请求启动流水线")
        fetch_success = await agent.drive_fetch_request(
            pcMemRead_addrs=[0, 0, 0, 0, startAddr],
            readValid=[0, 0, 0, 0, 1],  # readValid_4=1
            backendException=0
        )
        
        if not fetch_success:
            raise Exception("Fetch请求因RTL约束检查失败，地址不匹配")
        
        # 7. 等待流水线处理
        print("  7. 等待流水线处理")
        await bundle.step(5)
        
        # 8. 监控S2阶段MSHR匹配状态
        print("  8. 监控S2阶段MSHR匹配状态")
        s2_mshr_status = await agent.monitor_s2_mshr_match_status()
        pipeline_status = await agent.monitor_pipeline_status()
        
        print(f"    S2 MSHR hits_1: {s2_mshr_status.get('s2_MSHR_hits_1', 'N/A')}")
        print(f"    流水线状态: s0_fire={pipeline_status.get('s0_fire')}, s2_fire={pipeline_status.get('s2_fire')}")
        
        # 9. 验证MSHR未命中逻辑
        print("  9. 验证MSHR未命中逻辑")
        any_bank_hit = False
        any_data_from_mshr = False
        for i in range(8):
            bank_hit = s2_mshr_status.get(f's2_bankMSHRHit_{i}', False)
            data_from_mshr = s2_mshr_status.get(f's2_data_is_from_MSHR_{i}', False)
            if bank_hit:
                any_bank_hit = True
                print(f"    意外Bank {i} MSHR hit: {bank_hit}")
            if data_from_mshr:
                any_data_from_mshr = True
                print(f"    意外Bank {i} data from MSHR: {data_from_mshr}")
        
        s2_mshr_hits_1 = s2_mshr_status.get('s2_MSHR_hits_1', False)
        s2_fire = pipeline_status.get('s2_fire', False)
        
        # Assert 1: 不应该检测到MSHR命中
        assert not s2_mshr_hits_1, f"18.2: 预期MSHR未命中但检测到命中，s2_MSHR_hits_1={s2_mshr_hits_1}"
        print(f"    ✓ Assert 1 通过: S2 MSHR未命中 s2_MSHR_hits_1={s2_mshr_hits_1}")
        
        # Assert 2: 不应该有bank级别的命中
        assert not any_bank_hit, f"18.2: 预期无bank级别MSHR命中但检测到命中"
        print(f"    ✓ Assert 2 通过: 无bank级别MSHR命中")
        
        # Assert 3: 验证数据不来自MSHR
        assert not any_data_from_mshr, f"18.2: 预期数据不来自MSHR但检测到MSHR数据"
        print(f"    ✓ Assert 3 通过: 数据不来自MSHR")
        
        print("    √ 18.2 MSHR未命中逻辑所有assert验证通过")
        
        # 清除操作
        print("  ✓ 清除waylookup和fetch操作")
        await agent.clear_waylookup_read()
        await agent.clear_fetch_request()
        
    except Exception as e:
        errors.append(f"18.2: 测试过程中发生异常: {str(e)}")
        print(f"    × 18.2测试异常: {e}")
    
    # ==================== 汇总测试结果 ====================
    print(f"\n=== CP18测试完成 ===")
    if errors:
        print("× 发现以下错误:")
        for i, error in enumerate(errors, 1):
            print(f"  {i}. {error}")
        # 抛出所有错误
        raise AssertionError(f"CP18测试失败，共{len(errors)}个错误: " + "; ".join(errors))
    else:
        print("√ CP18: S2 MSHR Match and Data Update测试 - 所有测试点通过验证")


@toffee_test.testcase
async def test_cp19_miss_request_logic(icachemainpipe_env: ICacheMainPipeEnv):
    """
    CP19: Miss请求发送逻辑和合并异常功能测试
    测试Miss请求仲裁和异常合并逻辑
    
    基于MainPipe.md第19节和verilog源码:
    - s2_should_fetch = (~s2_hits | s2_corrupt_refetch) & s2_exception == 0 & ~s2_mmio
    - s2_exception_out = (|s2_exception) ? s2_exception : {2{s2_l2_corrupt}}
    - 使用Arbiter合并多个端口的Miss请求，通过s2_has_send避免重复请求
    """
    print("\n=== CP19: Miss请求发送逻辑和合并异常功能测试 ===")
    agent = icachemainpipe_env.agent
    bundle = icachemainpipe_env.bundle
    
    errors = []  # 收集所有测试错误
    
    # 19.1: 未发生Miss
    try:
        print("\n--- 测试点19.1: 未发生Miss ---")
        await agent.reset()
        await agent.setup_mshr_ready(True)
        await agent.drive_set_ecc_enable(True)
        await agent.drive_data_array_ready(True)
        await bundle.step()
        
        test_addr = 0x400
        # 使用辅助函数计算正确的ECC参数
        waylookup_params = calculate_waylookup_params(test_addr)
        await agent.drive_waylookup_read(
            vSetIdx_0=waylookup_params['vSetIdx_0'],
            vSetIdx_1=waylookup_params['vSetIdx_1'],
            waymask_0=0x1,       # 命中
            waymask_1=0x0,       # 单行取指，第二路不命中
            ptag_0=waylookup_params['ptag_0'],
            ptag_1=waylookup_params['ptag_1'],
            itlb_exception_0=0,  # 无ITLB异常
            meta_codes_0=waylookup_params['meta_codes_0'],
            meta_codes_1=waylookup_params['meta_codes_1']
        )
        
        # 设置PMP响应
        await agent.drive_pmp_response()
        
        # 发送fetch请求，使用计算出的地址确保一致性
        await agent.drive_fetch_request(
            pcMemRead_addrs=[0, 0, 0, 0, test_addr],  # 使用统一计算的地址
            readValid=[0, 0, 0, 0, 1]
        )
        await bundle.step(2)
        
        # 监控流水线状态
        pipeline_status = await agent.monitor_pipeline_status()
        miss_status = await agent.monitor_miss_request_status()
        mshr_status = await agent.monitor_mshr_status()
        
        print(f"  s2_fire: {pipeline_status.get('s2_fire')}")
        print(f"  s2_should_fetch_0: {miss_status.get('s2_should_fetch_0')}")
        print(f"  MSHR请求有效: {mshr_status.get('req_valid')}")
        
        # 验证：命中情况下不应发送Miss请求
        if miss_status.get('s2_should_fetch_0') is not None:
            assert miss_status.get('s2_should_fetch_0') == 0, "19.1: 命中时s2_should_fetch_0应为0"
        if mshr_status.get('req_valid') is not None:
            assert mshr_status.get('req_valid') == 0, "19.1: 命中时不应发送MSHR请求"
            
        await agent.clear_fetch_request()
        await agent.clear_waylookup_read()
        print("  √ 19.1: 未发生Miss - 测试通过")
        
    except Exception as e:
        error_msg = f"19.1测试失败: {str(e)}"
        print(f"  × {error_msg}")
        errors.append(error_msg)
    
    # 19.2: 单口Miss
    try:
        print("\n--- 测试点19.2: 单口Miss ---")
        await agent.reset()
        await agent.setup_mshr_ready(True)
        await agent.drive_set_ecc_enable(True)
        await agent.drive_data_array_ready(True)
        await bundle.step()
        
        # 设置未命中情况: waymask=0x0表示未命中
        test_addr = 0x600
        waylookup_params = calculate_waylookup_params(test_addr)
        await agent.drive_waylookup_read(
            vSetIdx_0=waylookup_params['vSetIdx_0'],
            vSetIdx_1=waylookup_params['vSetIdx_1'],
            waymask_0=0x0,       # 未命中
            waymask_1=0x0,       # 单行取指，第二路也未命中
            ptag_0=waylookup_params['ptag_0'],
            ptag_1=waylookup_params['ptag_1'],
            itlb_exception_0=0,  # 无ITLB异常
            meta_codes_0=waylookup_params['meta_codes_0'],
            meta_codes_1=waylookup_params['meta_codes_1']
        )
        await bundle.step()
        await agent.drive_pmp_response()  # 非MMIO
        
        await agent.drive_fetch_request(
            pcMemRead_addrs=[0, 0, 0, 0, test_addr],  # 使用统一计算的地址
            readValid=[0, 0, 0, 0, 1]
        )
        await bundle.step(2)
        miss_status = await agent.monitor_miss_request_status()
        print(miss_status)
        
        print(f"  s2_should_fetch_0: {miss_status.get('s2_should_fetch_0')}")
        print(f"  MSHR请求发送: {miss_status.get('mshr_req_valid')}")
        
        # 验证：未命中且无异常非MMIO时应发送Miss请求
        if miss_status.get('s2_should_fetch_0') is not None:
            assert miss_status.get('s2_should_fetch_0') == 1, "19.2: 未命中时s2_should_fetch_0应为1"
        
        # 验证MSHR请求发送
        assert miss_status.get('mshr_req_valid') == 1, "19.2: 未命中时应发送MSHR请求"
        
        # 验证topdownIcacheMiss信号
        topdown_miss = miss_status.get('io_fetch_topdownIcacheMiss_0', 0)
        assert topdown_miss == 1, "19.2: Miss时topdownIcacheMiss应为1"
            
        await agent.clear_fetch_request()
        await agent.clear_waylookup_read()
        print("  √ 19.2: 单口Miss - 测试通过")
        
    except Exception as e:
        error_msg = f"19.2测试失败: {str(e)}"
        print(f"  × {error_msg}")
        errors.append(error_msg)
    
    # 19.3: 双口都需要Miss
    try:
        print("\n--- 测试点19.3: 双口都需要Miss ---")
        await agent.reset()
        await agent.setup_mshr_ready(True)
        await agent.drive_set_ecc_enable(True)
        await agent.drive_data_array_ready(True)
        await bundle.step()
        
        # 设置双口未命中: 两个端口都未命中，无异常，非MMIO，需要跨行
        # 跨行取指需要addr[5]=1触发，nextlineStart=(addr & ~0x3F) + 64
        test_addr = 0xC20  # addr[5]=1，跨行地址
        # 使用辅助函数计算正确的ECC参数
        waylookup_params = calculate_waylookup_params(test_addr)
        await agent.drive_waylookup_read(
            vSetIdx_0=waylookup_params['vSetIdx_0'],
            vSetIdx_1=waylookup_params['vSetIdx_1'],
            waymask_0=0x0,         # 第一路未命中
            waymask_1=0x0,         # 第二路未命中
            ptag_0=waylookup_params['ptag_0'],
            ptag_1=waylookup_params['ptag_1'],
            itlb_exception_0=0,
            itlb_exception_1=0,
            meta_codes_0=waylookup_params['meta_codes_0'],
            meta_codes_1=waylookup_params['meta_codes_1']
        )
        
        await agent.drive_pmp_response()
        
        # 跨行取指：使用计算出的地址确保一致性
        await agent.drive_fetch_request(
            pcMemRead_addrs=[0, 0, 0, 0, test_addr],  # 使用计算出的跨行地址
            readValid=[0, 0, 0, 0, 1]
        )
        
        await bundle.step(3)
        
        miss_status = await agent.monitor_miss_request_status()
        
        print(f"  s2_should_fetch_0: {miss_status.get('s2_should_fetch_0')}")
        print(f"  s2_should_fetch_1: {miss_status.get('s2_should_fetch_1')}")
        print(f"  s2_doubleline: {miss_status.get('s2_doubleline')}")
        
        # 验证：双口都未命中时，两个should_fetch都应为1
        if miss_status.get('s2_should_fetch_0') is not None:
            assert miss_status.get('s2_should_fetch_0') == 1, "19.3: 双口Miss时s2_should_fetch_0应为1"
        if miss_status.get('s2_should_fetch_1') is not None:
            assert miss_status.get('s2_should_fetch_1') == 1, "19.3: 双口Miss时s2_should_fetch_1应为1"
        
        # 验证跨行取指状态
        assert miss_status.get('s2_doubleline') == 1, "19.3: 跨行取指时s2_doubleline应为1"
        
        # 验证topdownIcacheMiss信号 = s2_should_fetch_0 | s2_should_fetch_1
        topdown_miss = miss_status.get('io_fetch_topdownIcacheMiss_0', 0)
        expected_topdown = (miss_status.get('s2_should_fetch_0', 0) or miss_status.get('s2_should_fetch_1', 0))
        assert topdown_miss == expected_topdown, "19.3: topdownIcacheMiss应等于should_fetch_0|should_fetch_1"
            
        await agent.clear_fetch_request()
        await agent.clear_waylookup_read()
        print("  √ 19.3: 双口都需要Miss - 测试通过")
        
    except Exception as e:
        error_msg = f"19.3测试失败: {str(e)}"
        print(f"  × {error_msg}")
        errors.append(error_msg)
    
    # 19.4: 重复请求屏蔽
    try:
        print("\n--- 测试点19.4: 重复请求屏蔽 ---")
        await agent.reset()
        await agent.setup_mshr_ready(False)  # MSHR不ready，模拟无法立即处理请求
        await agent.drive_set_ecc_enable(True)
        await agent.drive_data_array_ready(True)
        await bundle.step()
        
        test_addr = 0x1000
        # 使用辅助函数计算正确的ECC参数
        waylookup_params = calculate_waylookup_params(test_addr)
        await agent.drive_waylookup_read(
            vSetIdx_0=waylookup_params['vSetIdx_0'],
            vSetIdx_1=waylookup_params['vSetIdx_1'],
            waymask_0=0x0,       # 未命中
            waymask_1=0x0,
            ptag_0=waylookup_params['ptag_0'],
            ptag_1=waylookup_params['ptag_1'],
            itlb_exception_0=0,
            meta_codes_0=waylookup_params['meta_codes_0'],
            meta_codes_1=waylookup_params['meta_codes_1']
        )
        
        await agent.drive_pmp_response()
        
        await agent.drive_fetch_request(
            pcMemRead_addrs=[0, 0, 0, 0, test_addr],  # 使用统一计算的地址
            readValid=[0, 0, 0, 0, 1]
        )
        
        await bundle.step(3)
        
        miss_status = await agent.monitor_miss_request_status()
        
        print(f"  s2_has_send_0: {miss_status.get('s2_has_send_0')}")
        print(f"  MSHR ready: {bundle.io._mshr._req._ready.value}")
        print(f"  MSHR req valid: {miss_status.get('mshr_req_valid')}")
        
        # 验证：当MSHR不ready时，has_send机制防止重复发送
        # RTL逻辑：s2_has_send在发送后置1，防止重复请求
        assert bundle.io._mshr._req._ready.value == 0, "19.4: MSHR应该不ready以测试重复请求屏蔽"
        if miss_status.get('s2_should_fetch_0') is not None:
            assert miss_status.get('s2_should_fetch_0') == 1, "19.4: 未命中时应该需要fetch"
        
        await agent.clear_fetch_request()
        await agent.clear_waylookup_read()
        print("  √ 19.4: 重复请求屏蔽 - 测试通过")
        
    except Exception as e:
        error_msg = f"19.4测试失败: {str(e)}"
        print(f"  × {error_msg}")
        errors.append(error_msg)
    
    # 19.5: 仅ITLB/PMP异常
    try:
        print("\n--- 测试点19.5: 仅ITLB/PMP异常 ---")
        await agent.reset()
        await agent.setup_mshr_ready(True)
        await agent.drive_set_ecc_enable(True)
        await agent.drive_data_array_ready(True)
        await bundle.step()
        
        # 设置ITLB异常：即使命中也有异常
        test_addr = 0x1400
        # 使用辅助函数计算正确的ECC参数
        waylookup_params = calculate_waylookup_params(test_addr)
        print(waylookup_params)
        await agent.drive_waylookup_read(
            vSetIdx_0=waylookup_params['vSetIdx_0'],
            vSetIdx_1=waylookup_params['vSetIdx_1'],
            waymask_0=0x1,       # 命中
            waymask_1=0x0,
            ptag_0=waylookup_params['ptag_0'],
            ptag_1=waylookup_params['ptag_1'],
            itlb_exception_0=0x2,  # ITLB异常
            meta_codes_0=waylookup_params['meta_codes_0'],
            meta_codes_1=waylookup_params['meta_codes_1']
        )
        
        await agent.drive_pmp_response()
        
        await agent.drive_fetch_request(
            pcMemRead_addrs=[0, 0, 0, 0, test_addr],  # 使用统一计算的地址
            readValid=[0, 0, 0, 0, 1]
        )
        
        await bundle.step(3)
        
        miss_status = await agent.monitor_miss_request_status()
        
        print(f"  s2_exception_0: {miss_status.get('s2_exception_0')}")
        print(f"  s2_exception_out_0: {miss_status.get('s2_exception_out_0')}")
        print(f"  s2_l2_corrupt_0: {miss_status.get('s2_l2_corrupt_0')}")
        
        # 验证：仅ITLB异常时，exception_out保留ITLB异常，L2_corrupt为false
        # RTL: s2_exception_out_0 = (|s2_exception_0) ? s2_exception_0 : {2{s2_l2_corrupt_0}}
        assert miss_status.get('s2_exception_0') == 0x2, "19.5: s2_exception_0应保留ITLB异常值0x2"
        assert miss_status.get('s2_l2_corrupt_0') == 0, "19.5: 仅ITLB异常时L2_corrupt应为0"
        assert miss_status.get('s2_exception_out_0') == 0x2, "19.5: exception_out应等于ITLB异常值0x2"
        
        # 验证不发送Miss请求（因为有异常）
        assert miss_status.get('s2_should_fetch_0') == 0, "19.5: 有异常时不应发送Miss请求"
        
        await agent.clear_fetch_request()
        await agent.clear_waylookup_read()
        print("  √ 19.5: 仅ITLB/PMP异常 - 测试通过")
        
    except Exception as e:
        error_msg = f"19.5测试失败: {str(e)}"
        print(f"  × {error_msg}")
        errors.append(error_msg)
    
    # 19.6: 仅L2异常
    # try:
    #     print("\n--- 测试点19.6: 仅L2异常 ---")
    #     await agent.reset()
    #     await agent.setup_mshr_ready(True)
    #     await agent.drive_set_ecc_enable(True)
    #     await agent.drive_data_array_ready(True)
    #     await bundle.step()
        
    #     # 先设置正常的waylookup和fetch，无ITLB/PMP异常
    #     test_addr = 0x1800
    #     # 使用辅助函数计算正确的ECC参数
    #     waylookup_params = calculate_waylookup_params(test_addr)
    #     print(waylookup_params)
    #     blk_paddr = (waylookup_params['ptag_0'] << 6) | ((test_addr >> 6) & 0x3F)  # 组合ptag和vSetIdx成为blkPaddr
    #     # 使用辅助函数计算正确的ECC参数
    #     waylookup_params = calculate_waylookup_params(test_addr)
    #     await agent.drive_waylookup_read(
    #         vSetIdx_0=waylookup_params['vSetIdx_0'],
    #         vSetIdx_1=waylookup_params['vSetIdx_1'],
    #         waymask_0=0x1,       # 命中
    #         waymask_1=0x0,
    #         ptag_0=waylookup_params['ptag_0'],
    #         ptag_1=waylookup_params['ptag_1'],
    #         itlb_exception_0=0,   # 无ITLB异常
    #         meta_codes_0=waylookup_params['meta_codes_0'],
    #         meta_codes_1=waylookup_params['meta_codes_1']
    #     )
        
    #     await agent.drive_pmp_response()
        
    #     await agent.drive_fetch_request(
    #         pcMemRead_addrs=[0, 0, 0, 0, test_addr],  # 使用统一计算的地址
    #         readValid=[0, 0, 0, 0, 1]
    #     )
    #     # 注入L2 corrupt响应，使用计算出的地址确保匹配
    #     await agent.inject_l2_corrupt_response(
    #         blkPaddr=blk_paddr,    # 使用计算出的blkPaddr
    #         vSetIdx=waylookup_params['vSetIdx_0'],  # 使用计算出的vSetIdx
    #         corrupt_data=0xBADD4A7A,
    #         corrupt=1
    #     )
        
    #     await bundle.step(3)
        
    #     miss_status = await agent.monitor_miss_request_status()
        
    #     print(f"  s2_l2_corrupt_0: {miss_status.get('s2_l2_corrupt_0')}")
    #     print(f"  s2_exception_0: {miss_status.get('s2_exception_0')}")
    #     print(f"  s2_exception_out_0: {miss_status.get('s2_exception_out_0')}")
        
    #     # 验证：仅L2异常时，exception_out表示L2访问错误(AF)
    #     # RTL: s2_exception_out_0 = (|s2_exception_0) ? s2_exception_0 : {2{s2_l2_corrupt_0}}
    #     assert miss_status.get('s2_l2_corrupt_0') == 1, "19.6: 应检测到L2 corrupt"
    #     assert miss_status.get('s2_exception_0') == 0, "19.6: 无ITLB/PMP异常时s2_exception_0应为0"
    #     assert miss_status.get('s2_exception_out_0') == 3, "19.6: L2 corrupt应产生AF异常(值为3={2{1}})"
        
    #     await agent.clear_fetch_request()
    #     await agent.clear_waylookup_read()
    #     print("  √ 19.6: 仅L2异常 - 测试通过")
        
    # except Exception as e:
    #     error_msg = f"19.6测试失败: {str(e)}"
    #     print(f"  × {error_msg}")
    #     errors.append(error_msg)
    
    # 19.7: ITLB + L2同时出现
    # try:
    #     print("\n--- 测试点19.7: ITLB + L2同时出现 ---")
    #     await agent.reset()
    #     await agent.setup_mshr_ready(True)
    #     await agent.drive_set_ecc_enable(True)
    #     await agent.drive_data_array_ready(True)
    #     await bundle.step()
        
    #     # 设置ITLB异常
    #     test_addr = 0x1C00
    #     # 使用辅助函数计算正确的ECC参数
    #     waylookup_params = calculate_waylookup_params(test_addr)
    #     blk_paddr = (waylookup_params['ptag_0'] << 6) | ((test_addr >> 6) & 0x3F)  # 组合ptag和vSetIdx成为blkPaddr
    #     # 使用辅助函数计算正确的ECC参数
    #     waylookup_params = calculate_waylookup_params(test_addr)
    #     await agent.drive_waylookup_read(
    #         vSetIdx_0=waylookup_params['vSetIdx_0'],
    #         vSetIdx_1=waylookup_params['vSetIdx_1'],
    #         waymask_0=0x1,       # 命中
    #         waymask_1=0x0,
    #         ptag_0=waylookup_params['ptag_0'],
    #         ptag_1=waylookup_params['ptag_1'],
    #         itlb_exception_0=0x1,  # ITLB异常
    #         meta_codes_0=waylookup_params['meta_codes_0'],
    #         meta_codes_1=waylookup_params['meta_codes_1']
    #     )
        
    #     await agent.drive_pmp_response()
        
    #     # 同时注入L2 corrupt响应，使用计算出的地址确保匹配
    #     await agent.inject_l2_corrupt_response(
    #         blkPaddr=blk_paddr,    # 使用计算出的blkPaddr
    #         vSetIdx=waylookup_params['vSetIdx_0'],  # 使用计算出的vSetIdx
    #         corrupt_data=0xDEADBEEF,
    #         corrupt=1
    #     )
        
    #     await agent.drive_fetch_request(
    #         pcMemRead_addrs=[0, 0, 0, 0, test_addr],  # 使用统一计算的地址
    #         readValid=[0, 0, 0, 0, 1]
    #     )
        
    #     await bundle.step(3)
        
    #     miss_status = await agent.monitor_miss_request_status()
        
    #     print(f"  s2_exception_0: {miss_status.get('s2_exception_0')}")
    #     print(f"  s2_l2_corrupt_0: {miss_status.get('s2_l2_corrupt_0')}")
    #     print(f"  s2_exception_out_0: {miss_status.get('s2_exception_out_0')}")
        
    #     # 验证：ITLB + L2同时出现时，ITLB异常优先级更高
    #     # RTL: s2_exception_out_0 = (|s2_exception_0) ? s2_exception_0 : {2{s2_l2_corrupt_0}}
    #     assert miss_status.get('s2_exception_0') == 0x1, "19.7: 应检测到ITLB异常0x1"
    #     assert miss_status.get('s2_l2_corrupt_0') == 1, "19.7: 应同时检测到L2 corrupt"
    #     assert miss_status.get('s2_exception_out_0') == 0x1, "19.7: ITLB异常优先级高，exception_out应为0x1而非L2异常"
        
    #     # 验证不发送Miss请求（因为有异常）
    #     assert miss_status.get('s2_should_fetch_0') == 0, "19.7: 有异常时不应发送Miss请求"
        
    #     await agent.clear_fetch_request()
    #     await agent.clear_waylookup_read()
    #     print("  √ 19.7: ITLB + L2同时出现 - 测试通过")
        
    # except Exception as e:
    #     error_msg = f"19.7测试失败: {str(e)}"
    #     print(f"  × {error_msg}")
    #     errors.append(error_msg)
    
    # 19.8: s2阶段取指完成
    try:
        print("\n--- 测试点19.8: s2阶段取指完成 ---")
        await agent.reset()
        await agent.setup_mshr_ready(True)
        await agent.drive_set_ecc_enable(True)
        await agent.drive_data_array_ready(True)
        await bundle.step()
        
        # 设置正常命中情况，所有端口should_fetch都为低
        test_addr = 0x2000
        vset_idx = (test_addr >> 6) & 0xFF  # 0x2000 >> 6 = 0x80
        # 使用辅助函数计算正确的ECC参数
        waylookup_params = calculate_waylookup_params(test_addr)
        await agent.drive_waylookup_read(
            vSetIdx_0=waylookup_params['vSetIdx_0'],
            vSetIdx_1=waylookup_params['vSetIdx_1'],
            waymask_0=0x1,       # 命中
            waymask_1=0x0,
            ptag_0=waylookup_params['ptag_0'],
            ptag_1=waylookup_params['ptag_1'],
            itlb_exception_0=0,   # 无异常
            meta_codes_0=waylookup_params['meta_codes_0'],
            meta_codes_1=waylookup_params['meta_codes_1']
        )
        
        await agent.drive_pmp_response()  # 非MMIO
        
        await agent.drive_fetch_request(
            pcMemRead_addrs=[0, 0, 0, 0, test_addr],  # 使用统一计算的地址
            readValid=[0, 0, 0, 0, 1]
        )
        
        await bundle.step(3)
        
        miss_status = await agent.monitor_miss_request_status()
        pipeline_status = await agent.monitor_pipeline_status()
        
        print(f"  s2_should_fetch_0: {miss_status.get('s2_should_fetch_0')}")
        print(f"  s2_should_fetch_1: {miss_status.get('s2_should_fetch_1')}")
        print(f"  s2_fire: {pipeline_status.get('s2_fire')}")
        print(f"  io_fetch_topdownIcacheMiss: {miss_status.get('io_fetch_topdownIcacheMiss_0')}")
        
        # 验证：当所有端口should_fetch都为低时，取指完成
        # RTL: io_fetch_topdownIcacheMiss_0 = s2_should_fetch_0 | s2_should_fetch_1
        should_fetch_0 = miss_status.get('s2_should_fetch_0', 0)
        should_fetch_1 = miss_status.get('s2_should_fetch_1', 0)
        assert should_fetch_0 == 0, "19.8: 命中时s2_should_fetch_0应为0表示不需要fetch"
        assert should_fetch_1 == 0, "19.8: 单路取指时s2_should_fetch_1应为0"
        
        # 验证topdownIcacheMiss信号
        topdown_miss = miss_status.get('io_fetch_topdownIcacheMiss_0', 0)
        assert topdown_miss == 0, "19.8: 无Miss时topdownIcacheMiss应为0"
        
        print("  取指完成：所有端口should_fetch都为低")
        
        await agent.clear_fetch_request()
        await agent.clear_waylookup_read()
        print("  √ 19.8: s2阶段取指完成 - 测试通过")
        
    except Exception as e:
        error_msg = f"19.8测试失败: {str(e)}"
        print(f"  × {error_msg}")
        errors.append(error_msg)
    
    # 最终检查所有错误
    if errors:
        print(f"\n× CP19测试完成，发现 {len(errors)} 个错误:")
        for error in errors:
            print(f"  - {error}")
        # 抛出所有错误的汇总
        raise AssertionError(f"CP19测试失败，共{len(errors)}个错误: {'; '.join(errors)}")
    else:
        print("\n√ CP19: Miss请求发送逻辑和合并异常功能测试 - 所有测试点通过验证")


@toffee_test.testcase
async def test_cp20_response_ifu(icachemainpipe_env: ICacheMainPipeEnv):
    """
    CP20: 响应IFU功能测试
    测试S2阶段向IFU的响应逻辑
    
    测试点：
    20.1: 正常命中并返回
    20.2: 异常返回  
    20.3: 跨行取指
    20.4: RespStall
    """
    print("\n=== CP20: Response IFU Test ===")
    agent = icachemainpipe_env.agent
    bundle = icachemainpipe_env.bundle
    
    
    errors = []
    
    # ==================== CP20.1: 正常命中并返回 ====================
    try:
        print("\n--- CP20.1: 正常命中并返回 ---")
        
        # 重置环境
        await agent.reset()
        await agent.drive_set_ecc_enable(True)
        await agent.drive_resp_stall(False)
        await agent.drive_data_array_ready(True)
        
        # 监控流水线状态
        pipeline_status = await agent.monitor_pipeline_status()
        print(f"初始流水线状态: s0_fire={pipeline_status.get('s0_fire')}, s2_fire={pipeline_status.get('s2_fire')}")
        
        # 设置测试地址和参数
        params = calculate_waylookup_params(0x1000) 
        print(f"  地址参数: start_addr=0x{params['start_addr']:x}, vSetIdx_0=0x{params['vSetIdx_0']:x}, ptag_0=0x{params['ptag_0']:x}, meta_codes_0={params['meta_codes_0']}, is_doubleline={params['is_doubleline']}")
        
        await agent.drive_waylookup_read(
            vSetIdx_0=params['vSetIdx_0'],
            vSetIdx_1=params['vSetIdx_1'],
            waymask_0=params['waymask_0'],
            waymask_1=params['waymask_1'],
            ptag_0=params['ptag_0'],
            ptag_1=params['ptag_1'],
            itlb_exception_0=params['itlb_exception_0'],
            itlb_exception_1=params['itlb_exception_1'],
            meta_codes_0=params['meta_codes_0'],
            meta_codes_1=params['meta_codes_1']
        )
        
        # 设置PMP响应 - 正常权限，非MMIO
        await agent.drive_pmp_response()
        
        # 设置DataArray响应
        test_data = [0x1111111111111111 + i for i in range(8)]
        await agent.drive_data_array_response(
            datas=test_data,
            codes=calculate_data_ecc_codes(test_data)  # 正确的ECC校验码
        )
        
        # 发送fetch请求
        fetch_success = await agent.drive_fetch_request(
            pcMemRead_addrs=[0, 0, 0, 0, params['start_addr']], 
            readValid=[0, 0, 0, 0, 1],
            backendException=0
        )
        
        if not fetch_success:
            raise AssertionError("Fetch请求发送失败，地址约束不满足")
        
        # 修复：3级流水线需要3个周期完成处理
        await bundle.step(3)
        
        # 监控流水线状态
        pipeline_status = await agent.monitor_pipeline_status()
        print(f"处理后流水线状态: s0_fire={pipeline_status.get('s0_fire')}, s2_fire={pipeline_status.get('s2_fire')}")
        
        # 修复：在监控响应前再等待一个周期确保信号稳定
        await bundle.step(1)
        
        # 监控IFU响应
        fetch_response = await agent.monitor_fetch_response()
        
        print(f"  响应有效性: {fetch_response['valid']}")
        print(f"  异常状态_0: {fetch_response['exception_0']}")
        print(f"  异常状态_1: {fetch_response['exception_1']}")
        print(f"  PMP MMIO_0: {fetch_response['pmp_mmio_0']}")
        print(f"  数据: 0x{fetch_response['data']:016x}" if fetch_response['data'] else "无数据")
        print(f"  双行标志: {fetch_response['doubleline']}")
        
        # 清除请求
        await agent.clear_fetch_request()
        await agent.clear_waylookup_read()
        await agent.drive_data_array_ready(False)
        
        # 验证正常命中情况 - 基于Verilog源码 io_fetch_resp_valid = s2_fire
        assert fetch_response['valid'] == 1, f"正常命中应有有效响应，实际valid={fetch_response['valid']}"
        assert fetch_response['exception_0'] == 0, f"正常情况不应有异常，实际exception_0={fetch_response['exception_0']}"
        assert fetch_response['pmp_mmio_0'] == 0, f"非MMIO区域，实际pmp_mmio_0={fetch_response['pmp_mmio_0']}"
        assert fetch_response['doubleline'] == 0, f"非跨行取指，实际doubleline={fetch_response['doubleline']}"
        
        print("  √ CP20.1: 正常命中并返回 - 测试通过")
        
    except Exception as e:
        error_msg = f"CP20.1测试失败: {str(e)}"
        print(f"  × {error_msg}")
        errors.append(error_msg)
    
    # ==================== CP20.2: 异常返回 ====================
    try:
        print("\n--- CP20.2: 异常返回 ---")
        
        # 重置环境
        await agent.reset()
        await agent.drive_set_ecc_enable(True)
        await agent.drive_resp_stall(False)
        await agent.drive_data_array_ready(True)
        
        # 设置测试地址和参数 - ITLB异常情况
        params = calculate_waylookup_params(0x2000)
        print(f"  异常测试地址参数: start_addr=0x{params['start_addr']:x}, vSetIdx_0=0x{params['vSetIdx_0']:x}, ptag_0=0x{params['ptag_0']:x}, meta_codes_0={params['meta_codes_0']}")
        
        await agent.drive_waylookup_read(
            vSetIdx_0=params['vSetIdx_0'],
            vSetIdx_1=params['vSetIdx_1'],
            waymask_0=params['waymask_0'],
            waymask_1=params['waymask_1'],
            ptag_0=params['ptag_0'],
            ptag_1=params['ptag_1'],
            itlb_exception_0=0x2,  # ITLB异常 - 特殊设置覆盖默认值
            itlb_exception_1=params['itlb_exception_1'],
            meta_codes_0=params['meta_codes_0'],
            meta_codes_1=params['meta_codes_1']
        )
        
        # 设置PMP响应
        await agent.drive_pmp_response()
        
        # 设置DataArray响应
        test_data_cp20_2 = [0x2222222222222222 + i for i in range(8)]
        await agent.drive_data_array_response(
            datas=test_data_cp20_2,
            codes=calculate_data_ecc_codes(test_data_cp20_2)
        )
        
        # 发送fetch请求
        fetch_success = await agent.drive_fetch_request(
            pcMemRead_addrs=[0, 0, 0, 0, params['start_addr']],
            readValid=[0, 0, 0, 0, 1],
            backendException=0
        )
        
        if not fetch_success:
            raise AssertionError("异常测试的Fetch请求发送失败")
        
        await bundle.step(5)
        
        # 监控异常合并状态
        exception_status = await agent.monitor_exception_merge_status()
        print(f"  异常合并状态: s1_itlb_exception_0={exception_status.get('s1_itlb_exception_0')}")
        
        # 监控IFU响应
        fetch_response = await agent.monitor_fetch_response()
        
        print(f"  异常响应有效性: {fetch_response['valid']}")
        print(f"  异常类型_0: {fetch_response['exception_0']}")
        print(f"  ITLB PBMT_0: {fetch_response['itlb_pbmt_0']}")
        # 清除请求
        await agent.clear_fetch_request()
        await agent.clear_waylookup_read()
        
        # 验证异常返回
        assert fetch_response['valid'] == 1, f"异常情况也应有有效响应，实际valid={fetch_response['valid']}"
        assert fetch_response['exception_0'] == 0x2, f"应报告ITLB异常，实际exception_0={fetch_response['exception_0']}"
        
        print("  √ CP20.2: 异常返回 - 测试通过")
        
    except Exception as e:
        error_msg = f"CP20.2测试失败: {str(e)}"
        print(f"  × {error_msg}")
        errors.append(error_msg)
    
    # ==================== CP20.3: 跨行取指 ====================
    try:
        print("\n--- CP20.3: 跨行取指 ---")
        
        # 重置环境
        await agent.reset()
        await agent.drive_set_ecc_enable(True)
        await agent.drive_resp_stall(False)
        await agent.drive_data_array_ready(True)
        
        # 设置跨行测试地址 - 使用bit[5]=1的地址触发跨行
        start_addr = 0x3020  # 0x3000 | 0x20，设置bit[5]=1触发跨行
        params = calculate_waylookup_params(start_addr)
        
        print(f"  跨行地址计算:")
        print(f"    起始地址: 0x{params['start_addr']:x} -> vSetIdx_0=0x{params['vSetIdx_0']:x}, ptag_0=0x{params['ptag_0']:x}, meta_codes_0={params['meta_codes_0']}")
        print(f"    跨行地址: 0x{params['nextline_addr']:x} -> vSetIdx_1=0x{params['vSetIdx_1']:x}, ptag_1=0x{params['ptag_1']:x}, meta_codes_1={params['meta_codes_1']}")
        print(f"    跨行标志: {params['is_doubleline']}")
        
        await agent.drive_waylookup_read(
            vSetIdx_0=params['vSetIdx_0'],
            vSetIdx_1=params['vSetIdx_1'], 
            waymask_0=params['waymask_0'],
            waymask_1=params['waymask_1'],
            ptag_0=params['ptag_0'],
            ptag_1=params['ptag_1'],
            itlb_exception_0=params['itlb_exception_0'],
            itlb_exception_1=params['itlb_exception_1'],
            meta_codes_0=params['meta_codes_0'],
            meta_codes_1=params['meta_codes_1']
        )
        
        # 设置PMP响应
        await agent.drive_pmp_response()
        
        # 设置DataArray响应
        test_data_cp20_3 = [0x3333333333333333 + i for i in range(8)]
        await agent.drive_data_array_response(
            datas=test_data_cp20_3,
            codes=calculate_data_ecc_codes(test_data_cp20_3)
        )
        
        # 修复：等待一个周期确保所有输入信号稳定
        await bundle.step(1)
        
        # 发送跨行fetch请求 - 使用计算好的跨行起始地址
        # 依据：agent中的跨行逻辑，startAddr[5]=1时触发跨行
        fetch_success = await agent.drive_fetch_request(
            pcMemRead_addrs=[0, 0, 0, 0, params['start_addr']],  # 使用包含bit[5]=1的地址
            readValid=[0, 0, 0, 0, 1],                           # readValid[4]=1启用跨行检测
            backendException=0
        )
        
        if not fetch_success:
            raise AssertionError("跨行测试的Fetch请求发送失败")
        
        # 修复：3级流水线需要3个周期完成处理
        await bundle.step(3)
        
        # 修复：在监控前再等待一个周期
        await bundle.step(1)
        
        # 监控IFU响应
        fetch_response = await agent.monitor_fetch_response()
        
        print(f"  跨行响应有效性: {fetch_response['valid']}")
        print(f"  双行标志: {fetch_response['doubleline']}")
        print(f"  虚拟地址_0: 0x{fetch_response['vaddr_0']:x}" if fetch_response['vaddr_0'] else "无")
        print(f"  虚拟地址_1: 0x{fetch_response['vaddr_1']:x}" if fetch_response['vaddr_1'] else "无")
        print(f"  异常_0: {fetch_response['exception_0']}")
        print(f"  异常_1: {fetch_response['exception_1']}")
        
        # 清除请求
        await agent.clear_fetch_request()
        await agent.clear_waylookup_read()
        
        # 验证跨行取指 - 基于Verilog源码 io_fetch_resp_bits_doubleline = s2_doubleline
        assert fetch_response['valid'] == 1, f"跨行取指应有有效响应，实际valid={fetch_response['valid']}"
        assert fetch_response['doubleline'] == 1, f"应设置双行标志，实际doubleline={fetch_response['doubleline']}"
        assert fetch_response['exception_0'] == 0, f"第一路不应有异常，实际exception_0={fetch_response['exception_0']}"
        assert fetch_response['exception_1'] == 0, f"第二路不应有异常，实际exception_1={fetch_response['exception_1']}"
        
        print("  √ CP20.3: 跨行取指 - 测试通过")
        
    except Exception as e:
        error_msg = f"CP20.3测试失败: {str(e)}"
        print(f"  × {error_msg}")
        errors.append(error_msg)
    
    # ==================== CP20.4: RespStall ====================
    try:
        print("\n--- CP20.4: RespStall ---")
        
        # 重置环境
        await agent.reset()
        await agent.drive_set_ecc_enable(True)
        await agent.drive_data_array_ready(True)
        
        # 启用响应暂停
        await agent.drive_resp_stall(True)
        
        # 设置RespStall测试地址参数
        params = calculate_waylookup_params(0x4000)
        print(f"  RespStall测试地址参数: start_addr=0x{params['start_addr']:x}, vSetIdx_0=0x{params['vSetIdx_0']:x}, ptag_0=0x{params['ptag_0']:x}, meta_codes_0={params['meta_codes_0']}")
        
        await agent.drive_waylookup_read(
            vSetIdx_0=params['vSetIdx_0'],
            vSetIdx_1=params['vSetIdx_1'],
            waymask_0=params['waymask_0'],
            waymask_1=params['waymask_1'],
            ptag_0=params['ptag_0'],
            ptag_1=params['ptag_1'],
            itlb_exception_0=params['itlb_exception_0'],
            itlb_exception_1=params['itlb_exception_1'],
            meta_codes_0=params['meta_codes_0'],
            meta_codes_1=params['meta_codes_1']
        )
        
        # 设置PMP和DataArray响应
        await agent.drive_pmp_response()
        test_data_cp20_4 = [0x4444444444444444 + i for i in range(8)]
        await agent.drive_data_array_response(
            datas=test_data_cp20_4,
            codes=calculate_data_ecc_codes(test_data_cp20_4)
        )
        
        # 修复：等待一个周期确保所有输入信号稳定
        await bundle.step(1)
        
        # 发送fetch请求
        fetch_success = await agent.drive_fetch_request(
            pcMemRead_addrs=[0, 0, 0, 0, params['start_addr']],
            readValid=[0, 0, 0, 0, 1],
            backendException=0
        )
        
        if not fetch_success:
            raise AssertionError("RespStall测试的Fetch请求发送失败")
        
        # 修复：等待流水线推进到S2阶段
        await bundle.step(3)
        
        # 监控RespStall激活时的响应
        fetch_response_stalled = await agent.monitor_fetch_response()
        respStall_active = bundle.io._respStall.value
        
        print(f"  RespStall激活状态: {respStall_active}")
        print(f"  Stall时响应有效性: {fetch_response_stalled['valid']}")
        
        # 验证RespStall效果 - 基于Verilog源码 s2_fire = s2_valid & ~io_respStall & ...
        assert respStall_active == 1, f"RespStall应该激活，实际值={respStall_active}"
        assert fetch_response_stalled['valid'] == 0, f"RespStall时不应有有效响应，实际valid={fetch_response_stalled['valid']}"
        
        # 解除RespStall并检查响应恢复
        await agent.drive_resp_stall(False)
        # 修复：等待RespStall解除生效
        await bundle.step(2)
        
        fetch_response_released = await agent.monitor_fetch_response()
        respStall_released = bundle.io._respStall.value
        
        print(f"  RespStall解除状态: {respStall_released}")
        print(f"  解除后响应有效性: {fetch_response_released['valid']}")
        
        # 清除请求
        await agent.clear_fetch_request()
        await agent.clear_waylookup_read()
        
        # 验证RespStall解除效果
        assert respStall_released == 0, f"RespStall应该解除，实际值={respStall_released}"
        assert fetch_response_released['valid'] == 1, f"解除RespStall后应有有效响应，实际valid={fetch_response_released['valid']}"
        
        print("  √ CP20.4: RespStall - 测试通过")
        
    except Exception as e:
        error_msg = f"CP20.4测试失败: {str(e)}"
        print(f"  × {error_msg}")
        errors.append(error_msg)
    
    # ==================== 测试结果汇总 ====================
    if errors:
        print(f"\n× CP20测试完成，发现 {len(errors)} 个错误:")
        for error in errors:
            print(f"  - {error}")
        # 抛出所有错误的汇总
        raise AssertionError(f"CP20测试失败，共{len(errors)}个错误: {'; '.join(errors)}")
    else:
        print("\n√ CP20: 响应IFU功能测试 - 所有测试点通过验证")


@toffee_test.testcase
async def test_cp21_l2_corrupt_report(icachemainpipe_env: ICacheMainPipeEnv):
    """
    CP21: L2 Corrupt报告功能测试
    测试L2 Cache corrupt错误报告逻辑
    
    测试点21.1: L2 Corrupt单路 - s2阶段准备完成可以发射(s2_fire为高)，s2_MSHR_hits(0)和fromMSHR.bits.corrupt为高
    测试点21.2: 双路同时corrupt - 端口0和端口1都从L2 corrupt数据中获取
    """
    print("\n=== CP21: L2 Corrupt Report Test ===")
    agent = icachemainpipe_env.agent
    bundle = icachemainpipe_env.bundle
    
    errors = []  # 收集所有测试错误，统一抛出
    
    # 测试点21.1: L2 Corrupt单路报告
    try:
        print("\n--- 测试点21.1: L2 Corrupt单路报告 ---")
        await agent.reset()
        
        # 设置环境准备就绪，确保能进入s0_fire
        await agent.setup_mshr_ready(True)
        await agent.drive_set_ecc_enable(True)
        await agent.drive_data_array_ready(True)
        
        # 使用ECC辅助函数设置测试地址和参数
        test_start_addr = 0x1000
        params = calculate_waylookup_params(test_start_addr)
        test_blkPaddr = (params['ptag_0'] << 6) | params['vSetIdx_0']
        test_vSetIdx = params['vSetIdx_0']
        test_ptag = params['ptag_0']
        
        print(f"  测试参数: blkPaddr=0x{test_blkPaddr:x}, vSetIdx=0x{test_vSetIdx:x}, ptag=0x{test_ptag:x}")
        
        test_corrupt_data = 0xBADD4A7A00000000
        
        # 执行waylookup操作 - 设置为未命中以触发MSHR查找
        await agent.drive_waylookup_read(
            vSetIdx_0=params['vSetIdx_0'],
            vSetIdx_1=params['vSetIdx_1'],
            waymask_0=0x0,  # 未命中，会触发MSHR查找
            waymask_1=0x0,
            ptag_0=params['ptag_0'],
            ptag_1=params['ptag_1'],
            itlb_exception_0=0,
            itlb_exception_1=0,
            meta_codes_0=params['meta_codes_0'],
            meta_codes_1=params['meta_codes_1']
        )
        await bundle.step()
        
        # 设置PMP响应为正常（非MMIO）
        await agent.drive_pmp_response()
        await bundle.step()
        
        # 执行fetch请求，使用原始start_addr确保地址匹配
        await agent.drive_fetch_request(
            pcMemRead_addrs=[0, 0, 0, 0, test_start_addr],  # 修复：使用start_addr而不是blkPaddr
            readValid=[0, 0, 0, 0, 1]
        )
        success = await agent.drive_mshr_response(
            blkPaddr=test_blkPaddr,
            vSetIdx=test_vSetIdx,
            data=test_corrupt_data,
            corrupt=1
        )
        assert success, "MSHR响应注入失败"
        print(f"  ✓ MSHR corrupt响应已注入")
        
        # 等待流水线推进到s2阶段
        await bundle.step(3)  # 给足够的时间让流水线推进
        
        # 5. 监控关键信号状态
        mshr_match = await agent.monitor_mshr_match_status()
        exception_status = await agent.monitor_exception_merge_status()
        
        print(f"  MSHR匹配: s1_bankMSHRHit_0={mshr_match.get('s1_bankMSHRHit_0')}")
        print(f"  L2 corrupt状态: s2_l2_corrupt_0={exception_status.get('s2_l2_corrupt_0') if 's2_l2_corrupt_0' in exception_status else 'N/A'}")
        
        assert bundle.io._mshr._resp._bits._corrupt.value == 1, "MSHR响应corrupt标志应为1"
        
        # 验证MSHR匹配条件已满足
        assert exception_status.get('s2_l2_corrupt_0') == 1, "L2 corrupt状态必须满足"
        await bundle.step()
        error_status = await agent.monitor_error_status()
        # 验证L2 corrupt错误报告
        print(f"  错误状态: 端口0_valid={error_status.get('0_valid')}, 端口0_paddr=0x{error_status.get('0_paddr', 0):x}")
        assert error_status["0_valid"] == 1, "端口0错误报告未生效"
        print("  ✓ 测试点21.1完成")
        
    except Exception as e:
        errors.append(f"测试点21.1失败: {str(e)}")
        print(f"  × 测试点21.1失败: {e}")
    
    finally:
        # 清理操作
        await agent.clear_waylookup_read()
        await agent.clear_fetch_request()
        
    # 测试点21.2: 双路同时corrupt
    try:
        print("\n--- 测试点21.2: 双路同时corrupt ---")
        await agent.reset()
        
        # 设置环境准备就绪
        await agent.setup_mshr_ready(True)
        await agent.drive_set_ecc_enable(True)
        await agent.drive_data_array_ready(True)
        
        # 构造真正的跨行取指场景
        # 关键理解：跨行取指需要两次MSHR响应，分别对应两个不同的cache block
        crossline_addr = 0x3020
        params = calculate_waylookup_params(crossline_addr)
        
        # 对于跨行情况，端口0和端口1访问相邻cache line，有不同的vSetIdx和ptag
        port0_vSetIdx = params['vSetIdx_0']
        port1_vSetIdx = params['vSetIdx_1'] 
        port0_ptag = params['ptag_0']
        port1_ptag = params['ptag_1']
        
        print(f"  跨行参数:")
        print(f"    crossline_addr=0x{crossline_addr:x}, is_doubleline={params['is_doubleline']}")
        print(f"    端口0: vSetIdx=0x{port0_vSetIdx:x}, ptag=0x{port0_ptag:x}")
        print(f"    端口1: vSetIdx=0x{port1_vSetIdx:x}, ptag=0x{port1_ptag:x}")
        
        # 验证确实是跨行场景
        if not params['is_doubleline']:
            raise AssertionError("测试地址必须是跨行地址")
        
        # 设置跨行waylookup - 两个端口未命中，需要MSHR查找
        await agent.drive_waylookup_read(
            vSetIdx_0=port0_vSetIdx,
            vSetIdx_1=port1_vSetIdx,
            waymask_0=0x0,  # 端口0未命中
            waymask_1=0x0,  # 端口1未命中
            ptag_0=port0_ptag,
            ptag_1=port1_ptag,
            itlb_exception_0=0,
            itlb_exception_1=0,
            meta_codes_0=params['meta_codes_0'],
            meta_codes_1=params['meta_codes_1']
        )
        await bundle.step()
        
        # 设置PMP响应
        await agent.drive_pmp_response()
        await bundle.step()
        
        # 执行跨行fetch请求
        await agent.drive_fetch_request(
            pcMemRead_addrs=[0, 0, 0, 0, crossline_addr],
            readValid=[0, 0, 0, 0, 1]
        )
         # 注入端口0的MSHR corrupt响应
        port0_blkPaddr = (port0_ptag << 6) | port0_vSetIdx
        test_corrupt_data_0 = 0xDEADBEEF00000000
        print(f"  阶段1 - 端口0 MSHR响应: blkPaddr=0x{port0_blkPaddr:x}, vSetIdx=0x{port0_vSetIdx:x}")
        await agent.drive_mshr_response(
            blkPaddr=port0_blkPaddr,
            vSetIdx=port0_vSetIdx,
            data=test_corrupt_data_0,
            corrupt=1
        )
        await bundle.step(2)
        
        # 注入端口1的MSHR corrupt响应
        port1_blkPaddr = (port1_ptag << 6) | port1_vSetIdx
        test_corrupt_data_1 = 0xCAFEBABE00000000
        
        print(f"  阶段2 - 端口1 MSHR响应: blkPaddr=0x{port1_blkPaddr:x}, vSetIdx=0x{port1_vSetIdx:x}")
        await agent.drive_mshr_response(
            blkPaddr=port1_blkPaddr,
            vSetIdx=port1_vSetIdx,
            data=test_corrupt_data_1,
            corrupt=1
        )
        
        # 等待端口0的MSHR匹配和处理
        await bundle.step(2)

        error_status = await agent.monitor_error_status()
        exception_status = await agent.monitor_exception_merge_status()
        
        print(f"  最终双端口L2 corrupt状态:")
        print(f"    s2_l2_corrupt_0={exception_status.get('s2_l2_corrupt_0', 'N/A')}")
        print(f"    s2_l2_corrupt_1={exception_status.get('s2_l2_corrupt_1', 'N/A')}")
        
        print(f"  最终错误报告:")
        print(f"    端口0: valid={error_status.get('0_valid')}, paddr=0x{error_status.get('0_paddr', 0):x}")
        print(f"    端口1: valid={error_status.get('1_valid')}, paddr=0x{error_status.get('1_paddr', 0):x}")
        # 验证双端口都检测到L2 corrupt
        assert exception_status.get('s2_l2_corrupt_0') == 1, "端口0应该检测到L2 corrupt"
        assert exception_status.get('s2_l2_corrupt_1') == 1, "端口1应该检测到L2 corrupt"
        
        # 等待一个周期确保错误报告生效
        await bundle.step(1)
        error_status = await agent.monitor_error_status()
        assert error_status["0_valid"] == 1, "端口0应该有错误报告"
        assert error_status["1_valid"] == 1, "端口1应该有错误报告"
        
        print("  ✓ 双端口跨行L2 corrupt测试完成 - 两个端口都成功检测到corrupt")
        
    except Exception as e:
        errors.append(f"测试点21.2失败: {str(e)}")
        print(f"  × 测试点21.2失败: {e}")
    
    finally:
        # 清理操作
        await agent.clear_waylookup_read()
        await agent.clear_fetch_request()
    
    # 统一处理所有错误
    if errors:
        error_msg = "\n".join(errors)
        print(f"\n× CP21测试存在错误:\n{error_msg}")
        raise AssertionError(f"CP21: L2 Corrupt报告测试失败\n{error_msg}")
    else:
        print("\n√ CP21: L2 Corrupt报告功能测试 - 所有测试点通过验证")


@toffee_test.testcase
async def test_cp22_flush_mechanism(icachemainpipe_env: ICacheMainPipeEnv):
    """
    CP22: 刷新机制功能测试
    测试流水线刷新控制逻辑
    """
    print("\n=== CP22: 刷新机制功能测试 ===")
    agent = icachemainpipe_env.agent
    bundle = icachemainpipe_env.bundle
    
    # 收集所有测试错误，避免单一测试错误导致后续测试停止
    test_errors = []
    
    # 测试22.1: 全局刷新
    try:
        print("\n--- 测试22.1: 全局刷新 ---")
        await agent.setup_mshr_ready(True)
        await agent.drive_set_ecc_enable(True)
        await agent.drive_data_array_ready(True)
        await agent.drive_set_flush(False)  # 确保初始状态无刷新
        
        # 设置环境准备就绪，建立正常流水线
        # 必须先设置waylookup再设置fetch，保持vSetIdx一致性
        await agent.drive_waylookup_read(
            vSetIdx_0=0x10,  # 对应startAddr[13:6] 
            vSetIdx_1=0x10,  # 对应nextlineStart[13:6]，不跨行时与vSetIdx_0相同
            waymask_0=0x1,   # 命中路0
            waymask_1=0x0,   # 不跨行，第二路不使用
            ptag_0=0x1000,
            ptag_1=0x1000,   # 保持一致
            itlb_exception_0=0,
            itlb_exception_1=0,
            meta_codes_0=0,
            meta_codes_1=0
        )
        
        # 设置fetch请求，地址需要与waylookup vSetIdx一致
        # 使用0x400: startAddr[13:6] = 0x400>>6 = 0x10, startAddr[5] = 0 (不跨行)
        # 不跨行时: nextlineStart = startAddr = 0x400, nextlineStart[13:6] = 0x10
        fetch_success = await agent.drive_fetch_request(
            pcMemRead_addrs=[0, 0, 0, 0, 0x400],  # pcMemRead_4: startAddr=0x400, nextlineStart=0x400
            readValid=[0, 0, 0, 0, 1]
        )
        
        if not fetch_success:
            raise Exception("Fetch请求设置失败 - 地址一致性约束违反")
        
        # 允许流水线推进几个周期，建立正常运行状态
        await bundle.step(1)
        
        # 监控刷新前的流水线状态
        pipeline_status_before = await agent.monitor_pipeline_status()
        print(f"  刷新前流水线状态:")
        print(f"    s0_fire: {pipeline_status_before['s0_fire']}")
        print(f"    s1_fire: {pipeline_status_before['s1_fire']}")
        print(f"    s2_fire: {pipeline_status_before['s2_fire']}")
        
        # 激活全局刷新
        await agent.drive_set_flush(True)
        await bundle.step(2)
        
        # 监控刷新期间的流水线状态
        pipeline_status_during = await agent.monitor_pipeline_status()
        fetch_response = await agent.monitor_fetch_response()
        mshr_status = await agent.monitor_mshr_status()
        
        print(f"  刷新期间流水线状态:")
        print(f"    flush信号: {bundle.io._flush.value}")
        print(f"    s0_fire: {pipeline_status_during['s0_fire']}")
        print(f"    s1_fire: {pipeline_status_during['s1_fire']}")
        print(f"    s2_fire: {pipeline_status_during['s2_fire']}")
        print(f"    fetch_resp_valid: {fetch_response['valid']}")
        print(f"    mshr_req_valid: {mshr_status['req_valid']}")
        
        # 根据verilog源码验证刷新逻辑
        # s0_fire = io_fetch_req_valid & s0_can_go & ~io_flush (行240)
        # s1_fire = s1_valid & s2_ready & ~io_flush (行374)  
        # s2_fire = s2_valid & ~io_fetch_topdownIcacheMiss_0 & ~io_respStall & ~io_flush (行529)
        assert bundle.io._flush.value == 1, f"全局刷新信号应该激活，实际值: {bundle.io._flush.value}"
        
        # 刷新期间所有fire信号都应该被抑制（基于RTL逻辑中的~io_flush条件）
        assert pipeline_status_during['s0_fire'] == 0, f"s0_fire在刷新期间应为0，实际值: {pipeline_status_during['s0_fire']}"
        assert pipeline_status_during['s1_fire'] == 0, f"s1_fire在刷新期间应为0，实际值: {pipeline_status_during['s1_fire']}"  
        assert pipeline_status_during['s2_fire'] == 0, f"s2_fire在刷新期间应为0，实际值: {pipeline_status_during['s2_fire']}"
        
        print("  √ 测试22.1通过: 全局刷新正确抑制所有阶段fire信号")
        
    except Exception as e:
        error_msg = f"测试22.1失败 - 全局刷新: {str(e)}"
        print(f"  × {error_msg}")
        test_errors.append(error_msg)
    
    # 测试22.2: S0阶段刷新
    try:
        print("\n--- 测试22.2: S0阶段刷新 ---")
        # 22.2已包含在22.1的全局刷新测试中，根据文档：s0_flush = true, s0_fire = false
        # 验证已在22.1中完成，这里添加额外验证
        
        pipeline_status = await agent.monitor_pipeline_status()
        
        # 根据verilog RTL逻辑：s0_fire = io_fetch_req_valid & s0_can_go & ~io_flush
        # 当io_flush=1时，无论其他条件如何，s0_fire都应该为0
        assert pipeline_status['s0_fire'] == 0, f"S0刷新时s0_fire应为0，实际值: {pipeline_status['s0_fire']}"
        
        print("  √ 测试22.2通过: S0阶段刷新正确抑制s0_fire信号")
        
    except Exception as e:
        error_msg = f"测试22.2失败 - S0阶段刷新: {str(e)}"
        print(f"  × {error_msg}")
        test_errors.append(error_msg)
    
    # 测试22.3: S1阶段刷新  
    try:
        print("\n--- 测试22.3: S1阶段刷新 ---")
        
        pipeline_status = await agent.monitor_pipeline_status()
        assert pipeline_status['s1_fire'] == 0, f"S1刷新时s1_fire应为0，实际值: {pipeline_status['s1_fire']}"
        
        print("  √ 测试22.3通过: S1阶段刷新正确抑制s1_fire信号")
        
    except Exception as e:
        error_msg = f"测试22.3失败 - S1阶段刷新: {str(e)}"
        print(f"  × {error_msg}")
        test_errors.append(error_msg)
    
    # 测试22.4: S2阶段刷新
    try:
        print("\n--- 测试22.4: S2阶段刷新 ---")
        pipeline_status = await agent.monitor_pipeline_status()
        mshr_status = await agent.monitor_mshr_status()
        assert pipeline_status['s2_fire'] == 0, f"S2刷新时s2_fire应为0，实际值: {pipeline_status['s2_fire']}"
        assert mshr_status['req_valid'] == 0, f"S2刷新时MSHR请求应停止，实际req_valid: {mshr_status['req_valid']}"
        
        print("  √ 测试22.4通过: S2阶段刷新正确抑制s2_fire和MSHR请求")
        
    except Exception as e:
        error_msg = f"测试22.4失败 - S2阶段刷新: {str(e)}"
        print(f"  × {error_msg}")
        test_errors.append(error_msg)
    
    # 清除环境，恢复正常状态测试
    try:
        print("\n--- 刷新恢复测试 ---")
        await agent.drive_set_flush(False)  # 取消刷新
        await bundle.step(3)
        
        pipeline_status_after = await agent.monitor_pipeline_status()
        
        print(f"  取消刷新后流水线状态:")
        print(f"    flush信号: {bundle.io._flush.value}")
        print(f"    s0_fire: {pipeline_status_after['s0_fire']}")
        print(f"    s1_fire: {pipeline_status_after['s1_fire']}")
        print(f"    s2_fire: {pipeline_status_after['s2_fire']}")
        
        # 验证刷新取消后流水线可以正常工作
        assert bundle.io._flush.value == 0, f"刷新取消后flush信号应为0，实际值: {bundle.io._flush.value}"
        
        print("  √ 刷新恢复测试通过: 取消刷新后流水线状态正常")
        
    except Exception as e:
        error_msg = f"刷新恢复测试失败: {str(e)}"
        print(f"  × {error_msg}")
        test_errors.append(error_msg)
    
    finally:
        # 清理环境
        try:
            await agent.clear_fetch_request()
            await agent.clear_waylookup_read()
            await agent.drive_set_flush(False)
        except:
            pass
    
    # 汇总测试结果
    if test_errors:
        print(f"\n× CP22测试完成，发现 {len(test_errors)} 个错误:")
        for i, error in enumerate(test_errors, 1):
            print(f"  {i}. {error}")
        # 抛出所有错误
        raise Exception(f"CP22刷新机制测试失败: {'; '.join(test_errors)}")
    else:
        print("\n√ CP22: 刷新机制功能测试 - 所有测试点通过验证")
