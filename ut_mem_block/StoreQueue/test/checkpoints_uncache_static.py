from comm import UT_FCOV, module_name_with
import toffee.funcov as fc
def init_store_funcov(uncachequeue):
    g = fc.CovGroup(UT_FCOV("../../UT_LSQ_store"))
    return g