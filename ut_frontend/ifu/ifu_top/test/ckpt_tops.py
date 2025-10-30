from ..env import IFUTopEnv
from ..commons import PREDICT_WIDTH
from toffee.funcov import CovGroup
from ..bundle import StageFlushBundle

from comm import UT_FCOV

def is_provider_cut_ptr_start(num):
    assert 0 <= num < 32
    def provider_cut_ptr_start(env: IFUTopEnv):
        return env.top_agent.top.internal_wires.f2_cut_ptrs[0].value == num
    return provider_cut_ptr_start

def is_provider_exception_vec(exception_type, pos):
    assert 0 <= pos < PREDICT_WIDTH
    assert 0 <= exception_type <= 3
    def provider_exception_vec(env: IFUTopEnv):
        return env.top_agent.get_exception_vecs()[pos] == exception_type
    return provider_exception_vec

def is_provider_cross_blk(val):
    def provider_cross_blk(env: IFUTopEnv):
        return env.top_agent.top.internal_wires._f3_lastHalf_valid.value == val
    return provider_cross_blk

def is_provider_gpaddr_fault(val):
    def provider_gpaddr_fault(env: IFUTopEnv):
        return env.top_agent.toIbufferAll._toBackend_gpaddrMem._wen.value == val
    return provider_gpaddr_fault

def is_provider_from_bpu_flush(val):
    def provider_from_bpu_flush(env: IFUTopEnv):
        return env.top_agent.top.internal_wires._f0_flush_from_bpu_probe.value == val
    return provider_from_bpu_flush

# def is_provider_from_bpu_flush(stg, cycled):
#     assert 0 <= stg <= 1
#     def provider_from_bpu_flush(env: IFUTopEnv):
#         stgs:list[StageFlushBundle] = [env.top_agent.ftqFlushStgsBundle._s2, env.top_agent.ftqFlushStgsBundle._s3]
#         stg_flag = stgs[stg]._bits._flag.value
#         stg_value = stgs[stg]._bits._value.value
#     return provider_from_bpu_flush

def get_coverage_group_tops(env: IFUTopEnv):
    group = CovGroup(UT_FCOV("../UT_IFU_TOP"))
    
    group.add_watch_point(env, {
        f"_start_{i}": is_provider_cut_ptr_start(i) for i in range(32)
    }, name="cut_ptr")
    
    group.add_watch_point(env, {
        f"_{i}_type{j}": is_provider_exception_vec(j, i) for i in range(PREDICT_WIDTH) for j in range(4)
    }, name="exception")
    
    group.add_watch_point(env, {
        f"_{bool(i)}": is_provider_cross_blk(i) for i in range(2)
    }, name="cross_blk")
    
    group.add_watch_point(env, {
        f"_{bool(i)}": is_provider_gpaddr_fault(i) for i in range(2)
    }, name="gpaddr_fault")
    
    group.add_watch_point(env, {
        f"_{bool(i)}": is_provider_from_bpu_flush(i) for i in range(2)
    }, name="bpu_flush")
    
    return group
    