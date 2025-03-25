from comm import UT_FCOV, module_name_with
import toffee.funcov as fc
def init_virtual_funcov(virtualqueue):
    g = fc.CovGroup(UT_FCOV("../../UT_LSQ_virtual"))
    return g