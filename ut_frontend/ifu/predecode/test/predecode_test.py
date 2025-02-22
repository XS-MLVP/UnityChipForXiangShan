import toffee_test
from .predecode_fixture import predecode_env
from ..env import PreDecodeEnv
from .predecode_instr_gen import PreDecodeInstrGen

instrGen = PreDecodeInstrGen()
@toffee_test.testcase
async def test_smoke(predecode_env : PreDecodeEnv):
    fake_instrs = [19212 for i in range(17)]

    res = await predecode_env.agent.predecode(fake_instrs)
    #print(res)
    
@toffee_test.testcase
async def test_splice_checker(predecode_env : PreDecodeEnv):
    #指令拼接测试
    print(' ')
    print('test_splice_checker')
    for _ in range(50):
        instrGen.clear()
        instrs, new_instrs = instrGen.random_instrs()
        res = await predecode_env.agent.predecode(instrs)
        assert res.new_instrs == new_instrs
@toffee_test.testcase
async def test_precoding_checker_2_1_1(predecode_env : PreDecodeEnv):
    ##RVC判定
    print(' ')
    print('test_precoding_checker_2_1_1')
    for _ in range(50):
        instrGen.clear()
        instrs, rvcs = instrGen.precoding_checker(task = '2.1.1')
        res = await predecode_env.agent.predecode(instrs)
        assert res.rvcs == rvcs 

@toffee_test.testcase
async def test_precoding_checker_2_1_2(predecode_env : PreDecodeEnv):
    #RVI判定
    print(' ')
    print('test_precoding_checker_2_1_2')
    for _ in range(50):
        instrGen.clear()
        instrs, rvcs = instrGen.precoding_checker(task = '2.1.2')
        res = await predecode_env.agent.predecode(instrs)
        assert res.rvcs == rvcs

@toffee_test.testcase
async def test_precoding_checker_2_2_1(predecode_env : PreDecodeEnv):
    ##RVC.J计算 offset
    print(' ')
    print('test_precoding_checker_2_2_1')
    for _ in range(50):
        instrGen.clear()
        instrs, jmp_offsets = instrGen.precoding_checker(task = '2.2.1')
        res = await predecode_env.agent.predecode(instrs)
        assert [i & 0xFFFF for i in res.jmp_offsets] == jmp_offsets
        
@toffee_test.testcase
async def test_precoding_checker_2_2_2(predecode_env : PreDecodeEnv):
    ##RVI.J计算 offset
    print(' ')
    print('test_precoding_checker_2_2_2')
    ##TODO
    for _ in range(50):
        instrGen.clear()
        instrs, jmp_offsets = instrGen.precoding_checker(task = '2.2.2')
        res = await predecode_env.agent.predecode(instrs)
        assert [i & 0xFFFFFFFF for i in res.jmp_offsets] == jmp_offsets
        
@toffee_test.testcase
async def test_precoding_checker_2_2_3(predecode_env : PreDecodeEnv):
    #RVC.BR计算 offset
    print(' ')
    print('test_precoding_checker_2_2_3')
    for _ in range(50):
        instrGen.clear()
        instrs, jmp_offsets = instrGen.precoding_checker(task = '2.2.3')
        res = await predecode_env.agent.predecode(instrs)
        assert [i & 0xFFFF for i in res.jmp_offsets] == jmp_offsets
        
    
@toffee_test.testcase
async def test_precoding_checker_2_2_4(predecode_env : PreDecodeEnv):
    #RVI.BR计算 offset
    #TODO
    print(' ')
    print('test_precoding_checker_2_2_4')
    for _ in range(50):
        instrGen.clear()
        instrs, jmp_offsets = instrGen.precoding_checker(task = '2.2.4')
        res = await predecode_env.agent.predecode(instrs)
        assert [i & 0xFFFFFFFF for i in res.jmp_offsets] == jmp_offsets

@toffee_test.testcase
async def test_precoding_checker_2_3_1(predecode_env : PreDecodeEnv):
    #有效指令开始向量计算1
    print(' ')
    print('test_precoding_checker_2_3_1')
    for _ in range(50):
        instrGen.clear()
        instrs, valid_starts = instrGen.precoding_checker(task = '2.3.1')
        res = await predecode_env.agent.predecode(instrs)
        assert res.valid_starts == valid_starts
        
@toffee_test.testcase
async def test_precoding_checker_2_3_2(predecode_env : PreDecodeEnv):
    #有效指令开始向量计算2
    print(' ')
    print('test_precoding_checker_2_3_2')
    for _ in range(50):
        instrGen.clear()
        instrs, half_valid_starts = instrGen.precoding_checker(task = '2.3.2')
        res = await predecode_env.agent.predecode(instrs)
        assert res.half_valid_starts ==half_valid_starts
        