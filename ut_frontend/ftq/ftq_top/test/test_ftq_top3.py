# ut_frontend/ftq/ftq_top/test/test_ftq_top3.py
import random
import toffee_test
import pytest
from collections import namedtuple
from ..ref.ftq_ref import FtqAccurateRef, BpuPacket, FtqPointer, get_random_ptr_before_bpu
from .top_test_fixture import ftq_env
from .test_configs import BPU_REDIRECT_EVENT_TYPES, BPU_REDIRECT_EVENT_WEIGHTS 

@toffee_test.testcase
async def test_example_integration(ftq_env):
    dut = ftq_env.dut
    ref = FtqAccurateRef()
    await ftq_env.ftq_agent.reset5(ftq_env.dut)
    await ftq_env.ftq_agent.set_write_mode_as_rise()
    for cycle in range(300):
        event_type = random.choices(BPU_REDIRECT_EVENT_TYPES, 
                                 weights=BPU_REDIRECT_EVENT_WEIGHTS)[0]                         
        s1_valid = s2_valid = s2_hasRedirect = s3_valid = s3_hasRedirect = False
        if event_type == 'S1':
            s1_valid = True
        elif event_type == 'S2_REDIRECT':
            s2_valid = s2_hasRedirect = True
        elif event_type == 'S3_REDIRECT':
            s3_valid = s3_hasRedirect = True
        s1_packet = BpuPacket(pc=0x8000_0000 | (cycle << 4), fallThruError=(random.random() < 0.05))
        s2_redirect_ptr = get_random_ptr_before_bpu(ref.bpu_ptr)
        s2_redirect_idx = s2_redirect_ptr.value
        s2_redirect_flag = s2_redirect_ptr.flag
        s2_packet = BpuPacket(pc=0x9000_0000 | (s2_redirect_idx << 4), fallThruError=(random.random() < 0.05))
        s3_redirect_ptr = get_random_ptr_before_bpu(ref.bpu_ptr)
        s3_redirect_idx = s3_redirect_ptr.value
        s3_redirect_flag = s3_redirect_ptr.flag
        s3_packet = BpuPacket(pc=0xA000_0000 | (s3_redirect_idx << 4), fallThruError=(random.random() < 0.05))
        to_ifu_ready = random.choice([True, True, False])
        await ftq_env.ftq_agent.drive_toifu_ready(to_ifu_ready)
        await ftq_env.ftq_agent.drive_s1_signals(
            valid=s1_valid,
            pc=s1_packet.pc,
            fallThruError=s1_packet.fallThruError
        )
        await ftq_env.ftq_agent.drive_s2_signals(
            valid=s2_valid,
            hasRedirect=s2_hasRedirect,
            pc=s2_packet.pc,
            redirect_idx=s2_redirect_ptr.value,
            redirect_flag=s2_redirect_ptr.flag,
            fallThruError=s2_packet.fallThruError
        )
        await ftq_env.ftq_agent.drive_s3_signals(
            valid=s3_valid,
            hasRedirect=s3_hasRedirect,
            pc=s3_packet.pc,
            redirect_idx=s3_redirect_ptr.value,
            redirect_flag=s3_redirect_ptr.flag,
            fallThruError=s3_packet.fallThruError
        )
        await ftq_env.ftq_agent.bundle.step(1)
        s3_redirect_fire = s3_valid and s3_hasRedirect
        s2_redirect_fire = s2_valid and s2_hasRedirect
        s1_enqueue_fire = s1_valid and await ftq_env.ftq_agent.get_fromBpu_resp_ready()
        toicache_outputs = await ftq_env.ftq_agent.get_toicache_outputs()    
        toprefetch_outputs = await ftq_env.ftq_agent.get_toprefetch_outputs()
        if toicache_outputs['req_valid'] and to_ifu_ready :
            expected_packet = ref.dequeue()
            assert toicache_outputs['startAddr']['0'] == expected_packet.pc, f"PC mismatch! Expected {hex(expected_packet.pc)}, got {hex(actual_pc)}"
            for i in range(5):
                str_i = str(i)
                assert toicache_outputs['readValid'][str_i] == 1, f"ICache readValid[{i}] should be 1, but got {read_valid}"
                assert toicache_outputs['startAddr'][str_i] == expected_packet.pc, f"ICache startAddr[{i}] mismatch! Expected {hex(expected_packet.pc)}, got {hex(start_addr)}"
                assert toicache_outputs['nextlineStart'][str_i] == expected_packet.pc + 64, f"ICache nextlineStart[{i}] mismatch! Expected {hex(expected_packet.pc + 64)}, got {hex(nextline_start)}"
        if s3_valid and s3_hasRedirect:
            assert toprefetch_outputs['flushFromBpu']['s3']['valid'] == 1, f"S3 redirect valid should be 1 when s3_redirect_fire=True"
            assert toprefetch_outputs['flushFromBpu']['s3']['flag'] == s3_redirect_flag, f"S3 redirect flag mismatch! Expected {s3_redirect_flag}, got {dut_s3_flag}"
            assert toprefetch_outputs['flushFromBpu']['s3']['value'] == s3_redirect_idx, f"S3 redirect value mismatch! Expected {s3_redirect_idx}, got {dut_s3_value}"
        for condition, action, *args in [
            (s3_redirect_fire, 'redirect', s3_redirect_ptr.value, s3_redirect_ptr.flag, s3_packet),
            (s2_redirect_fire, 'redirect', s2_redirect_ptr.value, s2_redirect_ptr.flag, s2_packet),
            (s1_enqueue_fire, 'enqueue', s1_packet)
        ]:
            if condition:
                if action == 'redirect':
                    ref.redirect(args[0], args[1], args[2])
                elif action == 'enqueue':
                    ref.enqueue(args[0])
                break        
