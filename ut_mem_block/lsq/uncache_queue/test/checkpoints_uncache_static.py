from comm import UT_FCOV, module_name_with
import toffee.funcov as fc
def init_uncache_funcov(uncachequeue):
    g = fc.CovGroup(UT_FCOV("../../../mem_block/lsq/uncache_queue"))
    g.add_watch_point(uncachequeue.agent.bundle.io._req._0._valid, 
                      {
                        "can receive violation query": lambda x: x.value > 0,
                        #"can't receive violation query": lambda x: x.value == 0,
                      }, name = "UNCACHE_ENQUEUE_0")
    g.add_watch_point(uncachequeue.agent.bundle.io._req._1._valid, 
                      {
                        "can receive violation query": lambda x: x.value > 0,
                        #"can't receive violation query": lambda x: x.value == 0,
                      }, name = "UNCACHE_ENQUEUE_1")
    g.add_watch_point(uncachequeue.agent.bundle.io._req._2._valid, 
                      {
                        "can receive violation query": lambda x: x.value > 0,
                        #"can't receive violation query": lambda x: x.value == 0,
                      }, name = "UNCACHE_ENQUEUE_2")
    g.add_watch_point(uncachequeue.agent.bundle.LoadQueueUncache_._entries._0._io._mmioSelect, 
                      {
                        "can make uncache": lambda x: x.value > 0,
                        #"can't receive violation query": lambda x: x.value == 0,
                      }, name = "UNCACHE_REQ_RESP")
    g.add_watch_point(uncachequeue.agent.bundle.LoadQueueUncache_._entries._0._io._flush, 
                      {
                        "can make uncache": lambda x: x.value > 0,
                        #"can't receive violation query": lambda x: x.value == 0,
                      }, name = "UNCACHE_FLUSH")
    g.add_watch_point(uncachequeue.agent.bundle.LoadQueueUncache_._entries._0._io._ncOut._valid, 
                      {
                        "can make uncache": lambda x: x.value > 0,
                        #"can't receive violation query": lambda x: x.value == 0,
                      }, name = "UNCACHE_NC")
    g.add_watch_point(uncachequeue.agent.bundle.io._rollback._valid, 
                      {
                        "can rollback": lambda x: x.value > 0,
                        #"can't receive violation query": lambda x: x.value == 0,
                      }, name = "UNCACHE_ROLLBACK")
    
    def _M(name):
        # get the module name
        return module_name_with(name, "./test_spec_case")
    g.mark_function("UNCACHE_ENQUEUE_0", _M("test_ctl_update"), bin_name=["can receive violation query"])
    g.mark_function("UNCACHE_ENQUEUE_1", _M("test_ctl_update"), bin_name=["can receive violation query"])
    g.mark_function("UNCACHE_ENQUEUE_2", _M("test_ctl_update"), bin_name=["can receive violation query"])
    g.mark_function("UNCACHE_REQ_RESP", _M("test_ctl_uncache"), bin_name=["can make uncache"])
    g.mark_function("UNCACHE_FLUSH", _M("test_ctl_uncache"), bin_name=["can make uncache"])
    g.mark_function("UNCACHE_NC", _M("test_ctl_uncache"), bin_name=["can make uncache"])
    g.mark_function("UNCACHE_ROLLBACK", _M("test_full_rollback"), bin_name=["can rollback"])
    return g