# import random
# import toffee_test
# from .top_test_fixture import ftq_env
# from .test_configs import FTQ_BACKEND_UPDATE_SCENARIOS

# @toffee_test.testcase
# async def test_example7_integration_with_agent(ftq_env):
#     dut = ftq_env.dut
#     await ftq_env.ftq_agent.reset5(ftq_env.dut)
#     await ftq_env.ftq_agent.set_write_mode_as_imme()
#     bpu_value = 0
#     bpu_flag = 0
#     for test_iter in range(300):
#         selected = random.choice(FTQ_BACKEND_UPDATE_SCENARIOS)
#         random_pc            = random.randint(0, 0xFFFFFFFF)
#         random_target        = random.randint(0, 0xFFFFFFFF)
#         random_ftq_idx_value = random.randint(0, 63)
#         random_ftq_idx_flag  = random.randint(0, 1)
#         random_mis_offset    = random.randint(0, 7)
#         random_cfi_offset    = random.randint(0, 7)
#         selected_configs = {
#             "s1": {"method": "drive_s1_signals", "params": {"valid": True, "pc": random_pc}, "check_ready": True},
#             "s2": {"method": "drive_s2_signals", "params": {"pc": random_pc, "valid": True, "hasRedirect": True, "redirect_idx": random_ftq_idx_value, "redirect_flag": random_ftq_idx_flag}, "check_ready": False},
#             "s3": {"method": "drive_s3_signals", "params": {"pc": random_pc, "valid": True, "hasRedirect": True, "redirect_idx": random_ftq_idx_value, "redirect_flag": random_ftq_idx_flag}, "check_ready": False},
#             "ifu_redirect": {"method": "drive_ifu_inputs", "params": {"valid": True, "misOffset_valid": True, "target": random_target, "ftqIdx_value": random_ftq_idx_value, "ftqIdx_flag": random_ftq_idx_flag}, "check_ready": False},
#             "backend_redirect": {"method": "drive_backend_inputs", "params": {"valid": True, "cfiUpdate_target": random_target, "ftqIdx_value": random_ftq_idx_value, "ftqIdx_flag": random_ftq_idx_flag}, "check_ready": False}
#         }
#         config = selected_configs.get(selected)
#         if config:
#             if config["check_ready"] and dut.io_fromBpu_resp_ready.value != 1:
#                 continue
#             await getattr(ftq_env.ftq_agent, config["method"])(**config["params"])    
#         await ftq_env.ftq_agent.bundle.step(1)
#         await ftq_env.ftq_agent.drive_s1_signals(valid=False)
#         await ftq_env.ftq_agent.bundle.step(1)
#         if selected == 's1':
#             assert dut.tobackend_pc_mem_wen.value == 1
#             assert dut.tobackend_pc_mem_waddr.value == bpu_value
#             assert dut.tobackend_pc_mem_wdata_start.value == random_pc
#         elif selected in ['s2', 's3']:
#             assert dut.tobackend_pc_mem_wen.value == 1
#             assert dut.tobackend_pc_mem_waddr.value == random_ftq_idx_value
#             assert dut.tobackend_pc_mem_wdata_start.value == random_pc
#         if selected in ['s2', 's3', 'ifu_redirect', 'backend_redirect']:
#             await ftq_env.ftq_agent.bundle.step(2)
#         else:
#             await ftq_env.ftq_agent.bundle.step(1)
#         config = {
#             's1': (bpu_value, random_pc + 32, bpu_value + 1),
#             's2': (random_ftq_idx_value, random_pc + 32, random_ftq_idx_value + 1),
#             's3': (random_ftq_idx_value, random_pc + 32, random_ftq_idx_value + 1),
#             'ifu_redirect': (random_ftq_idx_value, random_target, random_ftq_idx_value + 1),
#             'backend_redirect': (random_ftq_idx_value, random_target, random_ftq_idx_value + 1)
#         }
#         entry_ptr, target, new_bpu_value = config[selected]
#         assert dut.tobackend_newest_entry_en.value == 1
#         assert dut.tobackend_newest_entry_ptr.value == entry_ptr
#         assert dut.tobackend_newest_target.value == target
#         bpu_value = new_bpu_value
#         if bpu_value == 64:
#             bpu_flag = 1 - bpu_flag
#             bpu_value = 0
#         await ftq_env.ftq_agent.reset_inputs()
#         await ftq_env.ftq_agent.bundle.step(1)
    
 