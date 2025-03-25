from comm import UT_FCOV, module_name_with
import toffee.funcov as fc
def init_replay_funcov(replayqueue):
    g = fc.CovGroup(UT_FCOV("../../UT_LSQ_replay"))
    return g