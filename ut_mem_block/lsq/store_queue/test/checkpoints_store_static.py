from comm import UT_FCOV, module_name_with
import toffee.funcov as fc
def init_store_funcov(storequeue):
    g = fc.CovGroup(UT_FCOV("../../../mem_block/lsq/store_queue"))
    g.add_watch_point(storequeue.agent.bundle.io._enq_req._0._valid, 
                      {
                        "can receive store query": lambda x: x.value > 0,
                        #"can't receive violation query": lambda x: x.value == 0,
                      }, name = "STORE_ENQUEUE_0")
    g.add_watch_point(storequeue.agent.bundle.io._enq_req._1._valid, 
                      {
                        "can receive store query": lambda x: x.value > 0,
                        #"can't receive violation query": lambda x: x.value == 0,
                      }, name = "STORE_ENQUEUE_1")
    g.add_watch_point(storequeue.agent.bundle.io._enq_req._2._valid, 
                      {
                        "can receive store query": lambda x: x.value > 0,
                        #"can't receive violation query": lambda x: x.value == 0,
                      }, name = "STORE_ENQUEUE_2")
    g.add_watch_point(storequeue.agent.bundle.io._enq_req._3._valid, 
                      {
                        "can receive store query": lambda x: x.value > 0,
                        #"can't receive violation query": lambda x: x.value == 0,
                      }, name = "STORE_ENQUEUE_3")
    g.add_watch_point(storequeue.agent.bundle.io._enq_req._4._valid, 
                      {
                        "can receive store query": lambda x: x.value > 0,
                        #"can't receive violation query": lambda x: x.value == 0,
                      }, name = "STORE_ENQUEUE_4")
    g.add_watch_point(storequeue.agent.bundle.io._enq_req._5._valid, 
                      {
                        "can receive store query": lambda x: x.value > 0,
                        #"can't receive violation query": lambda x: x.value == 0,
                      }, name = "STORE_ENQUEUE_5")
    g.add_watch_point(storequeue.agent.bundle.StoreQueue._forwardMask2, 
                      {
                        "can forward data": lambda x: x.value > 0,
                        #"can't receive violation query": lambda x: x.value == 0,
                      }, name = "STORE_FORWARD")
    g.add_watch_point(storequeue.agent.bundle.StoreQueue._mmioState, 
                      {
                        "can do mmio": lambda x: x.value > 0,
                        #"can't receive violation query": lambda x: x.value == 0,
                      }, name = "STORE_MMIO")
    
    def _M(name):
        # get the module name
        return module_name_with(name, "./test_spec_case")
    g.mark_function("STORE_ENQUEUE_0", _M("test_ctl_update"), bin_name=["can receive store query"])
    g.mark_function("STORE_ENQUEUE_1", _M("test_ctl_update"), bin_name=["can receive store query"])
    g.mark_function("STORE_ENQUEUE_2", _M("test_ctl_update"), bin_name=["can receive store query"])
    g.mark_function("STORE_ENQUEUE_3", _M("test_ctl_update"), bin_name=["can receive store query"])
    g.mark_function("STORE_ENQUEUE_4", _M("test_ctl_update"), bin_name=["can receive store query"])
    g.mark_function("STORE_FORWARD", _M("test_ctl_forward"), bin_name=["can forward data"])
    g.mark_function("STORE_MMIO", _M("test_mmio"), bin_name=["can do mmio"])

    return g