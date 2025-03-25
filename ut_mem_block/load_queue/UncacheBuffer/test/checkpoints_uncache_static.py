from comm import UT_FCOV, module_name_with
import toffee.funcov as fc
def init_uncache_funcov(uncachequeue):
    g = fc.CovGroup(UT_FCOV("../../UT_LSQ_uncache"))
    return g