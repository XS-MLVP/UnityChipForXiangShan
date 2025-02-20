from .f3predecoder_fixture import f3predecoder_env
from ..env import F3PreDecoderEnv
import toffee_test
from .f3predecoder_instr_gen import F3PredecodeInstrGen

instrGen = F3PredecodeInstrGen()

@toffee_test.testcase
async def test_cfi_checker_1_1(f3predecoder_env : F3PreDecoderEnv):
    print(' ')
    print("test_cfi_checker_1_1")
    for _ in range(50):
        instrGen.clear()
        instrs, brTypes = instrGen.inst_gen(type='not_cfi', isa='rvc')
        res = await f3predecoder_env.agent.f3_predecode(instrs)
        assert res.brTypes == brTypes
        
        instrGen.clear()
        instrs, brTypes = instrGen.inst_gen(type='not_cfi', isa='rvi')
        res = await f3predecoder_env.agent.f3_predecode(instrs)
        assert res.brTypes == brTypes


@toffee_test.testcase
async def test_cfi_checker_1_2(f3predecoder_env : F3PreDecoderEnv):
    print(' ')
    print("test_cfi_checker_1_2")
    for _ in range(50):
        instrGen.clear()
        instrs, brTypes = instrGen.inst_gen(type='br', isa='rvi')
        res = await f3predecoder_env.agent.f3_predecode(instrs)
        assert res.brTypes == brTypes
        
        instrGen.clear()
        instrs, brTypes = instrGen.inst_gen(type='br', isa='rvc')
        res = await f3predecoder_env.agent.f3_predecode(instrs)
        assert res.brTypes == brTypes
    
@toffee_test.testcase
async def test_cfi_checker_1_3(f3predecoder_env : F3PreDecoderEnv):
    print(' ')
    print("test_cfi_checker_1_3")
    for _ in range(50):
        instrGen.clear()
        instrs, brTypes = instrGen.inst_gen(type='jal', isa='rvi')
        res = await f3predecoder_env.agent.f3_predecode(instrs)
        assert res.brTypes == brTypes
        
        instrGen.clear()
        instrs, brTypes = instrGen.inst_gen(type='jal', isa='rvc')
        res = await f3predecoder_env.agent.f3_predecode(instrs)
        assert res.brTypes == brTypes

@toffee_test.testcase
async def test_cfi_checker_1_4(f3predecoder_env : F3PreDecoderEnv):
    print(' ')
    print("test_cfi_checker_1_4")
    for _ in range(50):
        instrGen.clear()
        instrs, brTypes = instrGen.inst_gen(type='jalr', isa='rvi')
        res = await f3predecoder_env.agent.f3_predecode(instrs)
        assert res.brTypes == brTypes
        
        instrGen.clear()
        instrs, brTypes = instrGen.inst_gen(type='jalr', isa='rvc')
        res = await f3predecoder_env.agent.f3_predecode(instrs)
        assert res.brTypes == brTypes
    
@toffee_test.testcase
async def test_ret_call_checker_2_1_1(f3predecoder_env : F3PreDecoderEnv):
    #check not cfi
    print(' ')
    print("test_ret_call_checker_2_1_1")
    for _ in range(50):
        instrGen.clear()
        instrs, isCalls, isRets = instrGen.ret_call_checker(task = '2.1.1')
        res = await f3predecoder_env.agent.f3_predecode(instrs)
        assert res.isCalls == isCalls
        assert res.isRets == isRets

@toffee_test.testcase
async def test_ret_call_checker_2_1_2(f3predecoder_env : F3PreDecoderEnv):
    #check br
    print(' ')
    print("test_ret_call_checker_2_1_2")
    for _ in range(50):
        instrGen.clear()
        instrs, isCalls, isRets = instrGen.ret_call_checker(task = '2.1.2')
        res = await f3predecoder_env.agent.f3_predecode(instrs)
        assert res.isCalls == isCalls
        assert res.isRets == isRets

@toffee_test.testcase
async def test_ret_call_checker_2_2_1_1(f3predecoder_env : F3PreDecoderEnv):
    #check RVI.JAL call
    print(' ')
    print("test_ret_call_checker_2_2_1_1")
    for _ in range(50):
        instrGen.clear()
        instrs, isCalls, isRets = instrGen.ret_call_checker(task = '2.2.1.1')
        res = await f3predecoder_env.agent.f3_predecode(instrs)
        assert res.isCalls == isCalls
        assert res.isRets == isRets
    
@toffee_test.testcase   
async def test_ret_call_checker_2_2_1_2(f3predecoder_env : F3PreDecoderEnv):
    #check RVI.JAL not call and ret
    print(' ')
    print("test_ret_call_checker_2_2_1_2")
    for _ in range(50):
        instrGen.clear()
        instrs, isCalls, isRets = instrGen.ret_call_checker(task = '2.2.1.2')
        res = await f3predecoder_env.agent.f3_predecode(instrs)
        assert res.isCalls == isCalls
        assert res.isRets == isRets
    
@toffee_test.testcase
async def test_ret_call_checker_2_2_2(f3predecoder_env : F3PreDecoderEnv):
    #check RVC.JAL not call and ret
    print(' ')
    print("test_ret_call_checker_2_2_2")
    for _ in range(50):
        instrGen.clear()
        instrs, isCalls, isRets = instrGen.ret_call_checker(task = '2.2.2')
        res = await f3predecoder_env.agent.f3_predecode(instrs)
        assert res.isCalls == isCalls
        assert res.isRets == isRets

@toffee_test.testcase
async def test_ret_call_checker_2_3_1_1(f3predecoder_env : F3PreDecoderEnv):
    #check RVI.JALR call
    print(' ')
    print("test_ret_call_checker_2_3_1_1")
    for _ in range(50):
        instrGen.clear()
        instrs, isCalls, isRets = instrGen.ret_call_checker(task = '2.3.1.1')
        res = await f3predecoder_env.agent.f3_predecode(instrs)
        assert res.isCalls == isCalls
        assert res.isRets == isRets
    
@toffee_test.testcase
async def test_ret_call_checker_2_3_1_2(f3predecoder_env : F3PreDecoderEnv):
    #check RVI.JALR ret
    print(' ')
    print("test_ret_call_checker_2_3_1_2")
    for _ in range(50):
        instrGen.clear()
        instrs, isCalls, isRets = instrGen.ret_call_checker(task = '2.3.1.2')
        res = await f3predecoder_env.agent.f3_predecode(instrs)
        assert res.isCalls == isCalls
        assert res.isRets == isRets
    
@toffee_test.testcase
async def test_ret_call_checker_2_3_1_3(f3predecoder_env : F3PreDecoderEnv):
    #check RVI.JALR not call and ret
    print(' ')
    print("test_ret_call_checker_2_3_1_3")
    for _ in range(50):
        instrGen.clear()
        instrs, isCalls, isRets = instrGen.ret_call_checker(task = '2.3.1.3')
        res = await f3predecoder_env.agent.f3_predecode(instrs)
        assert res.isCalls == isCalls
        assert res.isRets == isRets
    
@toffee_test.testcase
async def test_ret_call_checker_2_3_2_1(f3predecoder_env: F3PreDecoderEnv):
    #check RVC.JALR call
    print(' ')
    print("test_ret_call_checker_2_3_2_1")
    for _ in range(50):
        instrGen.clear()
        instrs, isCalls, isRets = instrGen.ret_call_checker(task = '2.3.2.1')
        res = await f3predecoder_env.agent.f3_predecode(instrs)
        assert res.isCalls == isCalls
        assert res.isRets == isRets
        
@toffee_test.testcase
async def test_ret_call_checker_2_3_2_2_1(f3predecoder_env: F3PreDecoderEnv):
    #check RVC.JR ret
    print(' ')
    print("test_ret_call_checker_2_3_2_2_1")
    for _ in range(50):
        instrGen.clear()
        instrs, isCalls, isRets = instrGen.ret_call_checker(task = '2.3.2.2.1')
        res = await f3predecoder_env.agent.f3_predecode(instrs)
        assert res.isCalls == isCalls
        assert res.isRets == isRets
        
@toffee_test.testcase
async def test_ret_call_checker_2_3_2_2_2(f3predecoder_env: F3PreDecoderEnv):
    #check RVC.JR not ret
    print(' ')
    print("test_ret_call_checker_2_3_2_2_2")
    for _ in range(50):
        instrGen.clear()
        instrs, isCalls, isRets = instrGen.ret_call_checker(task = '2.3.2.2.2')
        res = await f3predecoder_env.agent.f3_predecode(instrs)
        assert res.isCalls == isCalls
        assert res.isRets == isRets