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
    
    return g