from comm import UT_FCOV, module_name_with
import toffee.funcov as fc
def init_replay_funcov(replayqueue):
    g = fc.CovGroup(UT_FCOV("../../../mem_block/lsq/replay_queue"))
    g.add_watch_point(replayqueue.agent.bundle.io._enq._0._valid, 
                      {
                        "can receive violation query": lambda x: x.value > 0,
                        #"can't receive violation query": lambda x: x.value == 0,
                      }, name = "REPLAY_ENQUEUE_0")
    g.add_watch_point(replayqueue.agent.bundle.io._enq._1._valid, 
                      {
                        "can receive violation query": lambda x: x.value > 0,
                        #"can't receive violation query": lambda x: x.value == 0,
                      }, name = "REPLAY_ENQUEUE_1")
    g.add_watch_point(replayqueue.agent.bundle.io._enq._2._valid, 
                      {
                        "can receive violation query": lambda x: x.value > 0,
                        #"can't receive violation query": lambda x: x.value == 0,
                      }, name = "REPLAY_ENQUEUE_2")
    g.add_watch_point(replayqueue.agent.bundle.LoadQueueReplay._blocking._0, 
                      {
                        "can update blocking register": lambda x: x.value > 0,
                        #"can't receive violation query": lambda x: x.value == 0,
                      }, name = "REPLAY_BLOCK_0")
    g.add_watch_point(replayqueue.agent.bundle.LoadQueueReplay._blocking._1, 
                      {
                        "can update blocking register": lambda x: x.value > 0,
                        #"can't receive violation query": lambda x: x.value == 0,
                      }, name = "REPLAY_BLOCK_1")
    g.add_watch_point(replayqueue.agent.bundle.LoadQueueReplay._blocking._2, 
                      {
                        "can update blocking register": lambda x: x.value > 0,
                        #"can't receive violation query": lambda x: x.value == 0,
                      }, name = "REPLAY_BLOCK_2")
    g.add_watch_point(replayqueue.agent.bundle.io._lqFull, 
                      {
                        "judge full": lambda x: x.value > 0,
                        #"can't receive violation query": lambda x: x.value == 0,
                      }, name = "REPLAY_FULL")
    g.add_watch_point(replayqueue.agent.bundle.io._replay._0._valid, 
                      {
                        "can replay": lambda x: x.value > 0,
                        #"can't receive violation query": lambda x: x.value == 0,
                      }, name = "REPLAY_0")
    g.add_watch_point(replayqueue.agent.bundle.io._replay._1._valid, 
                      {
                        "can replay": lambda x: x.value > 0,
                        #"can't receive violation query": lambda x: x.value == 0,
                      }, name = "REPLAY_1")
    g.add_watch_point(replayqueue.agent.bundle.io._replay._2._valid, 
                      {
                        "can replay": lambda x: x.value > 0,
                        #"can't receive violation query": lambda x: x.value == 0,
                      }, name = "REPLAY_2")
    g.add_watch_point(replayqueue.agent.bundle.LoadQueueReplay._coldCounter._0, 
                      {
                        "can cold": lambda x: x.value > 0,
                        #"can't receive violation query": lambda x: x.value == 0,
                      }, name = "COLDCOUNT_0")
    g.add_watch_point(replayqueue.agent.bundle.LoadQueueReplay._coldCounter._1, 
                      {
                        "can cold": lambda x: x.value > 0,
                        #"can't receive violation query": lambda x: x.value == 0,
                      }, name = "COLDCOUNT_1")
    g.add_watch_point(replayqueue.agent.bundle.LoadQueueReplay._coldCounter._2, 
                      {
                        "can cold": lambda x: x.value > 0,
                        #"can't receive violation query": lambda x: x.value == 0,
                      }, name = "COLDCOUNT_2")
    
    def _M(name):
        # get the module name
        return module_name_with(name, "./test_spec_case")
    g.mark_function("REPLAY_ENQUEUE_0", _M("test_ctl_update"), bin_name=["can receive violation query"])
    g.mark_function("REPLAY_ENQUEUE_1", _M("test_ctl_update"), bin_name=["can receive violation query"])
    g.mark_function("REPLAY_ENQUEUE_2", _M("test_ctl_update"), bin_name=["can receive violation query"])
    g.mark_function("REPLAY_BLOCK_0", _M("test_ctl_blocking"), bin_name=["can update blocking register"])
    g.mark_function("REPLAY_BLOCK_1", _M("test_ctl_blocking"), bin_name=["can update blocking register"])
    g.mark_function("REPLAY_BLOCK_2", _M("test_ctl_blocking"), bin_name=["can update blocking register"])
    g.mark_function("REPLAY_0", _M("test_ctl_replay"), bin_name=["can replay"])
    g.mark_function("REPLAY_1", _M("test_ctl_replay"), bin_name=["can replay"])
    g.mark_function("REPLAY_2", _M("test_ctl_replay"), bin_name=["can replay"])
    g.mark_function("COLDCOUNT_0", _M("test_cold_queue"), bin_name=["can cold"])
    g.mark_function("COLDCOUNT_1", _M("test_cold_queue"), bin_name=["can cold"])
    g.mark_function("COLDCOUNT_2", _M("test_cold_queue"), bin_name=["can cold"])
    g.mark_function("REPLAY_FULL", _M("test_queue_full"), bin_name=["judge full"])

    return g