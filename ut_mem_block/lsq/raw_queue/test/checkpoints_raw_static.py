from comm import UT_FCOV, module_name_with
import toffee.funcov as fc
def init_raw_funcov(rawqueue):
    g = fc.CovGroup(UT_FCOV("../../../mem_block/lsq/raw_queue"))
    g.add_watch_point(rawqueue.agent.bundle.io._query._0._req._ready, 
                      {
                        "can receive violation query": lambda x: x.value > 0,
                        #"can't receive violation query": lambda x: x.value == 0,
                      }, name = "RAW_ENQUEUE_0")
    g.add_watch_point(rawqueue.agent.bundle.io._query._1._req._ready, 
                      {
                        "can receive violation query": lambda x: x.value > 0,
                        #"can't receive violation query": lambda x: x.value == 0,
                      }, name = "RAW_ENQUEUE_1")
    g.add_watch_point(rawqueue.agent.bundle.io._query._2._req._ready, 
                      {
                        "can receive violation query": lambda x: x.value > 0,
                        #"can't receive violation query": lambda x: x.value == 0,
                      }, name = "RAW_ENQUEUE_2")
    g.add_watch_point(rawqueue.agent.bundle.io._query._0._revoke, 
                      {
                        "can cancel violation query": lambda x: x.value > 0,
                        #"can't receive violation query": lambda x: x.value == 0,
                      }, name = "RAW_REVOKE_0")
    g.add_watch_point(rawqueue.agent.bundle.io._query._1._revoke, 
                      {
                        "can cancel violation query": lambda x: x.value > 0,
                        #"can't receive violation query": lambda x: x.value == 0,
                      }, name = "RAW_REVOKE_1")
    g.add_watch_point(rawqueue.agent.bundle.io._query._2._revoke, 
                      {
                        "can cancel violation query": lambda x: x.value > 0,
                        #"can't receive violation query": lambda x: x.value == 0,
                      }, name = "RAW_REVOKE_2")
    g.add_watch_point(rawqueue.agent.bundle.io._rollback._0._valid, 
                      {
                        "can replay violation query": lambda x: x.value > 0,
                        #"can't receive violation query": lambda x: x.value == 0,
                      }, name = "RAW_ROLLBACK_0")
    g.add_watch_point(rawqueue.agent.bundle.io._rollback._1._valid, 
                      {
                        "can replay violation query": lambda x: x.value > 0,
                        #"can't receive violation query": lambda x: x.value == 0,
                      }, name = "RAW_ROLLBACK_1")
    g.add_watch_point(rawqueue.agent.bundle.io._lqFull, 
                      {
                        "judge queue full": lambda x: x.value > 0,
                        #"can't receive violation query": lambda x: x.value == 0,
                      }, name = "RAW_FULL")
    def _M(name):
        # get the module name
        return module_name_with(name, "./test_spec_case")
    g.mark_function("RAW_ENQUEUE_0", _M("test_ctl_enqueue"), bin_name=["can receive violation query"])
    g.mark_function("RAW_ENQUEUE_1", _M("test_ctl_enqueue"), bin_name=["can receive violation query"])
    g.mark_function("RAW_ENQUEUE_2", _M("test_ctl_enqueue"), bin_name=["can receive violation query"])
    g.mark_function("RAW_REVOKE_0", _M("test_ctl_revoke"), bin_name=["can cancel violation query"])
    g.mark_function("RAW_REVOKE_1", _M("test_ctl_revoke"), bin_name=["can cancel violation query"])
    g.mark_function("RAW_REVOKE_2", _M("test_ctl_revoke"), bin_name=["can cancel violation query"])
    g.mark_function("RAW_ROLLBACK_0", _M("test_ctl_raw_violation"), bin_name=["can replay violation query"])
    g.mark_function("RAW_ROLLBACK_1", _M("test_ctl_raw_violation"), bin_name=["can replay violation query"])
    g.mark_function("RAW_FULL", _M("test_freelist_full"), bin_name=["judge queue full"])
    return g