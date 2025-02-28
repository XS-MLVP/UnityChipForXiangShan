from comm import UT_FCOV, module_name_with
import toffee.funcov as fc
def init_rar_funcov(rarqueue):
    g = fc.CovGroup(UT_FCOV("../../UT_LSQ_RAR"))
    g.add_watch_point(rarqueue.agent.bundle.io._query._0._req._ready, 
                      {
                        "can receive violation query": lambda x: x.value > 0,
                        #"can't receive violation query": lambda x: x.value == 0,
                      }, name = "RAR_ENQUEUE_0")
    g.add_watch_point(rarqueue.agent.bundle.io._query._1._req._ready, 
                      {
                        "can receive violation query": lambda x: x.value > 0,
                        #"can't receive violation query": lambda x: x.value == 0,
                      }, name = "RAR_ENQUEUE_1")
    g.add_watch_point(rarqueue.agent.bundle.io._query._2._req._ready, 
                      {
                        "can receive violation query": lambda x: x.value > 0,
                        #"can't receive violation query": lambda x: x.value == 0,
                      }, name = "RAR_ENQUEUE_2")
    def _M(name):
        # get the module name
        return module_name_with(name, "../../test_queueupdate")
    g.mark_function("RAR_ENQUEUE_0", _M("test_can_enqueue_smoke"), bin_name=["can receive violation query"])
    g.mark_function("RAR_ENQUEUE_1", _M("test_can_enqueue_smoke"), bin_name=["can receive violation query"])
    g.mark_function("RAR_ENQUEUE_2", _M("test_can_enqueue_smoke"), bin_name=["can receive violation query"])
    return g