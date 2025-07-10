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
    g.add_watch_point(rarqueue.agent.bundle.io._query._2._resp._bits_rep_frm_fetch, 
                      {
                        "have violation": lambda x: x.value > 0,
                        #"can't receive violation query": lambda x: x.value == 0,
                      }, name = "RAR_DETECT_2")
    g.add_watch_point(rarqueue.agent.bundle.io._query._1._resp._bits_rep_frm_fetch, 
                      {
                        "have violation": lambda x: x.value > 0,
                        #"can't receive violation query": lambda x: x.value == 0,
                      }, name = "RAR_DETECT_1")
    g.add_watch_point(rarqueue.agent.bundle.io._query._0._resp._bits_rep_frm_fetch, 
                      {
                        "have violation": lambda x: x.value > 0,
                        #"can't receive violation query": lambda x: x.value == 0,
                      }, name = "RAR_DETECT_0")
    g.add_watch_point(rarqueue.agent.bundle.io._query._0._revoke, 
                      {
                        "revoke": lambda x: x.value > 0,
                        #"can't receive violation query": lambda x: x.value == 0,
                      }, name = "RAR_REVOKE_0")
    g.add_watch_point(rarqueue.agent.bundle.io._query._1._revoke, 
                      {
                        "revoke": lambda x: x.value > 0,
                        #"can't receive violation query": lambda x: x.value == 0,
                      }, name = "RAR_REVOKE_1")
    g.add_watch_point(rarqueue.agent.bundle.io._query._2._revoke, 
                      {
                        "revoke": lambda x: x.value > 0,
                        #"can't receive violation query": lambda x: x.value == 0,
                      }, name = "RAR_REVOKE_2")
    def _M(name):
        # get the module name
        return module_name_with(name, "./test_spec_case")
    g.mark_function("RAR_ENQUEUE_0", _M("test_ctl_enqueue"), bin_name=["can receive violation query"])
    g.mark_function("RAR_ENQUEUE_1", _M("test_ctl_enqueue"), bin_name=["can receive violation query"])
    g.mark_function("RAR_ENQUEUE_2", _M("test_ctl_enqueue"), bin_name=["can receive violation query"])
    g.mark_function("RAR_DETECT_2", _M("test_ctl_releasedupdate"), bin_name=["have violation"])
    g.mark_function("RAR_DETECT_1", _M("test_ctl_releasedupdate"), bin_name=["have violation"])
    g.mark_function("RAR_DETECT_0", _M("test_ctl_releasedupdate"), bin_name=["have violation"])
    g.mark_function("RAR_REVOKE_2", _M("test_ctl_dequeue"), bin_name=["revoke"])
    g.mark_function("RAR_REVOKE_1", _M("test_ctl_dequeue"), bin_name=["revoke"])
    g.mark_function("RAR_REVOKE_0", _M("test_ctl_dequeue"), bin_name=["revoke"])
    return g