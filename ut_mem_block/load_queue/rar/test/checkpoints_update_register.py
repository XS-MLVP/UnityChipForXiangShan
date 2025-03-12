from comm import UT_FCOV
from toffee.funcov import CovGroup
from ..env.LoadQueueRAREnv import LoadQueueRAREnv

def is_dequeue(index: int):
    def dequeue(loadqueue_rar_env: LoadQueueRAREnv) -> bool:
        io_ldWbPtr_flag = loadqueue_rar_env.agent.bundle.io._ldWbPtr._flag.value
        uop_i_lqIdx_flag = getattr(loadqueue_rar_env.agent.bundle.LoadQueueRAR._uop, f'_{index}')._lqIdx._flag.value
        io_ldWbPtr_value = loadqueue_rar_env.agent.bundle.io._ldWbPtr._value.value
        uop_i_lqIdx_value = getattr(loadqueue_rar_env.agent.bundle.LoadQueueRAR._uop, f'_{index}')._lqIdx._value.value
        io_redirect_valid = loadqueue_rar_env.agent.bundle.io._redirect._valid.value
        io_redirect_bits_level = loadqueue_rar_env.agent.bundle.io._redirect._bits._level.value
        uop_i_robIdx_flag = getattr(loadqueue_rar_env.agent.bundle.LoadQueueRAR._uop, f'_{index}')._robIdx._flag.value
        uop_i_robIdx_value = getattr(loadqueue_rar_env.agent.bundle.LoadQueueRAR._uop, f'_{index}')._robIdx._value.value
        needFlush = loadqueue_rar_env.agent.bundle.LoadQueueRAR_._needFlush_flushItself_T._286.value
        io_redirect_bits_robIdx_flag = loadqueue_rar_env.agent.bundle.io._redirect._bits._robIdx._flag.value
        io_redirect_bits_robIdx_value = loadqueue_rar_env.agent.bundle.io._redirect._bits._robIdx._value.value
        judge = (io_ldWbPtr_flag ^ uop_i_lqIdx_flag ^ (io_ldWbPtr_value >= uop_i_lqIdx_value)) or \
                (io_redirect_valid and (
                    (io_redirect_bits_level and 
                    (uop_i_robIdx_flag, uop_i_robIdx_value) == needFlush) or \
                    (uop_i_robIdx_flag ^ io_redirect_bits_robIdx_flag) or \
                    (uop_i_robIdx_value > io_redirect_bits_robIdx_value)
                ))
        return judge

    return dequeue
  
def is_release(index: int):
    def release(loadqueue_rar_env: LoadQueueRAREnv) -> bool:
      released = []
      for i in range(72):
          released.append(getattr(loadqueue_rar_env.agent.bundle.LoadQueueRAR._released, f'_{i}').value)
      release = released.count(1)
      return release > 0

    return release
  
def get_coverage_group_of_update_register(loadqueue_rar_env: LoadQueueRAREnv) -> CovGroup:
    g = CovGroup(UT_FCOV("../LoadQueueRAR"))

    g.add_watch_point(loadqueue_rar_env, {"release": is_release},
                      name="RAR_REALEASE")
    
    g.add_watch_point(loadqueue_rar_env, {f"dequeue_{i}": is_dequeue(i) for i in range(72)}, name=f"RAR_DEQUEUE")
        
    return g