from comm import UT_FCOV, module_name_with
import toffee.funcov as fc
def init_store_funcov(storequeue):
    g = fc.CovGroup(UT_FCOV("../../UT_LSQ_store"))
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
    return g