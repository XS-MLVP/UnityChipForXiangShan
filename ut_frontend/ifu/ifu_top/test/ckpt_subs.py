from ..env import IFUTopEnv
from ..commons import PREDICT_WIDTH
from toffee.funcov import CovGroup

from comm import UT_FCOV

def is_provider_instr_concat(pos):
    assert 0 <= pos < PREDICT_WIDTH
    def provider_instr_concat(env: IFUTopEnv):
        return env.top_agent.top.internal_wires.pre_decoder.out_instrs[pos].value != 0
    return provider_instr_concat

def is_provider_rvc(pos, rvc_val):
    assert 0 <= pos < PREDICT_WIDTH
    def provider_instr_concat(env: IFUTopEnv):
        return env.top_agent.top.internal_wires.pre_decoder.out_pd_isRVCs[pos].value == rvc_val
    return provider_instr_concat

def is_provider_jmp_off_type(pos, rvc_val, j_type):
    assert 0 <= pos < PREDICT_WIDTH
    assert 1 <=j_type< 3
    def provider_jmp_off_type(env: IFUTopEnv):
        return env.top_agent.top.internal_wires.pre_decoder.out_pd_isRVCs[pos].value == rvc_val \
            and env.top_agent.top.internal_wires.pre_decoder.out_pd_brTypes[pos].value == j_type
    return provider_jmp_off_type

def is_provider_cfi_type(pos, cfi_type):
    assert 0 <= pos < PREDICT_WIDTH
    assert 0 <=cfi_type <= 3
    def provider_jmp_off_type(env: IFUTopEnv):
        return env.top_agent.top.internal_wires.pre_decoder.out_pd_brTypes[pos].value == cfi_type
    return provider_jmp_off_type

def is_provider_jal_ret(pos, rvc, jal_ret_type):
    assert 0 <= pos < PREDICT_WIDTH
    def provider_jal_ret(env: IFUTopEnv) -> bool:
        is_ret = env.top_agent.top.internal_wires.pre_decoder.out_pd_isRets[pos].value
        is_call = env.top_agent.top.internal_wires.pre_decoder.out_pd_isCalls[pos].value
        if rvc != env.top_agent.top.internal_wires.pre_decoder.out_pd_isRVCs[pos].value:
            return False
        if jal_ret_type == 0:
            return (not is_ret) and (not is_call)
        elif jal_ret_type == 1:
            return is_ret
        else:
            return is_call
    return provider_jal_ret


def is_provider_valids_selection(choice):
    def provider_valids_selection(env: IFUTopEnv):
        return env.top_agent.toIbufferAll._toIbuffer._bits._valids[0].value == choice
    return provider_valids_selection


def is_provider_err_check(pos, err_type):
    assert 0 <= pos < PREDICT_WIDTH
    assert 0 <= err_type <= 6
    def provider_err_check(env: IFUTopEnv) -> bool:
        return env.top_agent.top.internal_wires.pred_checker.fault_types[pos].value == err_type
    return provider_err_check

def is_provider_rvc_expand(rvc, ill):
    def provider_rvc_expand(env:IFUTopEnv) ->bool:
        if not rvc:
            for i in range(PREDICT_WIDTH):
                if  env.top_agent.top.to_ibuffer_all._toIbuffer._bits._pd[i]._isRVC.value == rvc:
                    return True
            return False
        for i in range(PREDICT_WIDTH):
            if env.top_agent.top.to_ibuffer_all._toIbuffer._bits._pd[0]._isRVC.value == rvc \
            and env.top_agent.toIbufferAll._toIbuffer._bits._illegalInstr[0].value == ill:
                return True
        return False
        # return env.top_agent.top.to_ibuffer_all._toIbuffer._bits._pd[0]._isRVC.value == rvc \
        #     and env.top_agent.toIbufferAll._toIbuffer._bits._illegalInstr[0].value == ill
    return provider_rvc_expand

def get_coverage_group_sub_modules(env: IFUTopEnv):
    group = CovGroup(UT_FCOV("../UT_IFU_TOP"))
    
    group.add_watch_point(env, {
        f"_instr_{i}": is_provider_instr_concat(i) for i in range(PREDICT_WIDTH)
    }, name="predecode_concat")
    
    group.add_watch_point(env, {
        f"_{i}_{bool(j)}": is_provider_rvc(i, bool(j)) for i in range(PREDICT_WIDTH) for j in range(2)
    }, name="predecode_rvc")

    group.add_watch_point(env, {
        f"_{i}_{'br' if j == 1 else 'j'}_{'c' if bool(k) else 'i'}": is_provider_jmp_off_type(i, bool(k), j) for i in range(PREDICT_WIDTH) for j in range(1, 3) for k in range(2)
    }, name="predecode_jmpoff")
    
    group.add_watch_point(env, {
        f"_{i}_{'non_cfi' if j == 0 else 'br' if j == 1 else 'jal' if j == 2 else 'jalr'}": \
            is_provider_cfi_type(i, j) for i in range(PREDICT_WIDTH) for j in range(4)
    }, name="predecode_brtype")
    
    group.add_watch_point(env,{
        f"_{i}_rv{'c' if bool(j) else 'i'}_{'nop' if k==0 else 'ret' if k == 1 else 'jal'}": \
            is_provider_jal_ret(i, j, k) for i in range(PREDICT_WIDTH) for j in range(2) for k in range(3)
    }, name="predecode_jal_ret")
    
    group.add_watch_point(env, {
        "_normal": is_provider_valids_selection(True),
        "_last_half": is_provider_valids_selection(False)
    }, name="starts")
    
    errs = ["no", "jal", "ret", "target", "not_cfi", "invalid", "jalr"]
    
    group.add_watch_point(env, {
        f"_{i}_fault_{errs[j]}": is_provider_err_check(i, j) for i in range(PREDICT_WIDTH) for j in range(7)
    }, name="check_errs")
    
    group.add_watch_point(env,{
        f"_rvi": is_provider_rvc_expand(False, False),
        f"_rvc_ill": is_provider_rvc_expand(True, True),
        f"_rvc_normal": is_provider_rvc_expand(True, False)
    }, name="rvc_expand")
    
    return group
    