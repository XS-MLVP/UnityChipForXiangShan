from comm import UT_FCOV, module_name_with
import toffee.funcov as fc
def init_virtual_funcov(virtualqueue):
    g = fc.CovGroup(UT_FCOV("../../UT_LSQ_virtual"))
    g.add_watch_point(virtualqueue.agent.bundle.io._enq_req._0._valid, 
                      {
                        "can receive enqueue query": lambda x: x.value > 0,
                        #"can't receive violation query": lambda x: x.value == 0,
                      }, name = "VIRTUAL_ENQUEUE_0")
    g.add_watch_point(virtualqueue.agent.bundle.io._enq_req._1._valid, 
                      {
                        "can receive enqueue query": lambda x: x.value > 0,
                        #"can't receive violation query": lambda x: x.value == 0,
                      }, name = "VIRTUAL_ENQUEUE_1")
    g.add_watch_point(virtualqueue.agent.bundle.io._enq_req._2._valid, 
                      {
                        "can receive enqueue query": lambda x: x.value > 0,
                        #"can't receive violation query": lambda x: x.value == 0,
                      }, name = "VIRTUAL_ENQUEUE_2")
    g.add_watch_point(virtualqueue.agent.bundle.io._enq_req._3._valid, 
                      {
                        "can receive enqueue query": lambda x: x.value > 0,
                        #"can't receive violation query": lambda x: x.value == 0,
                      }, name = "VIRTUAL_ENQUEUE_3")
    g.add_watch_point(virtualqueue.agent.bundle.io._enq_req._4._valid, 
                      {
                        "can receive enqueue query": lambda x: x.value > 0,
                        #"can't receive violation query": lambda x: x.value == 0,
                      }, name = "VIRTUAL_ENQUEUE_4")
    g.add_watch_point(virtualqueue.agent.bundle.io._enq_req._5._valid, 
                      {
                        "can receive enqueue query": lambda x: x.value > 0,
                        #"can't receive violation query": lambda x: x.value == 0,
                      }, name = "VIRTUAL_ENQUEUE_5")
    g.add_watch_point(virtualqueue.agent.bundle.VirtualLoadQueue._committed._0, 
                      {
                        "can commited": lambda x: x.value > 0,
                        #"can't receive violation query": lambda x: x.value == 0,
                      }, name = "VIRTUAL_COMMIT")
    g.add_watch_point(virtualqueue.agent.bundle.io._ldin._0._valid, 
                      {
                        "can writeback": lambda x: x.value > 0,
                        #"can't receive violation query": lambda x: x.value == 0,
                      }, name = "VIRTUAL_WRITEBACK_0")
    g.add_watch_point(virtualqueue.agent.bundle.io._ldin._1._valid, 
                      {
                        "can writeback": lambda x: x.value > 0,
                        #"can't receive violation query": lambda x: x.value == 0,
                      }, name = "VIRTUAL_WRITEBACK_1")
    g.add_watch_point(virtualqueue.agent.bundle.io._ldin._2._valid, 
                      {
                        "can writeback": lambda x: x.value > 0,
                        #"can't receive violation query": lambda x: x.value == 0,
                      }, name = "VIRTUAL_WRITEBACK_2")
    g.add_watch_point(virtualqueue.agent.bundle.io._lqEmpty, 
                      {
                        "judge full": lambda x: x.value > 0,
                        #"can't receive violation query": lambda x: x.value == 0,
                      }, name = "VIRTUAL_FULL")
    def _M(name):
        # get the module name
        return module_name_with(name, "./test_spec_case")
    g.mark_function("VIRTUAL_ENQUEUE_0", _M("test_ctl_update"), bin_name=["can receive enqueue query"])
    g.mark_function("VIRTUAL_ENQUEUE_1", _M("test_ctl_update"), bin_name=["can receive enqueue query"])
    g.mark_function("VIRTUAL_ENQUEUE_2", _M("test_ctl_update"), bin_name=["can receive enqueue query"])
    g.mark_function("VIRTUAL_ENQUEUE_3", _M("test_ctl_update"), bin_name=["can receive enqueue query"])
    g.mark_function("VIRTUAL_ENQUEUE_4", _M("test_ctl_update"), bin_name=["can receive enqueue query"])
    g.mark_function("VIRTUAL_ENQUEUE_5", _M("test_ctl_update"), bin_name=["can receive enqueue query"])
    g.mark_function("VIRTUAL_COMMIT", _M("test_ctl_commit"), bin_name=["can commited"])
    g.mark_function("VIRTUAL_WRITEBACK_0", _M("test_ctl_writeback"), bin_name=["can writeback"])
    g.mark_function("VIRTUAL_WRITEBACK_1", _M("test_ctl_writeback"), bin_name=["can writeback"])
    g.mark_function("VIRTUAL_WRITEBACK_2", _M("test_ctl_writeback"), bin_name=["can writeback"])
    g.mark_function("VIRTUAL_FULL", _M("test_queue_full"), bin_name=["judge full"])
    return g