#coding=utf8
#***************************************************************************************
# This project is licensed under Mulan PSL v2.
# You can use this software according to the terms and conditions of the Mulan PSL v2.
# You may obtain a copy of Mulan PSL v2 at:
#          http://license.coscl.org.cn/MulanPSL2
#
# THIS SOFTWARE IS PROVIDED ON AN "AS IS" BASIS, WITHOUT WARRANTIES OF ANY KIND,
# EITHER EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO NON-INFRINGEMENT,
# MERCHANTABILITY OR FIT FOR A PARTICULAR PURPOSE.
#
# See the Mulan PSL v2 for more details.
#**************************************************************************************/

from dut_tree import *

kmh_dut_heriarchy = {
    "name": "kmh_dut",
    "children": [
        {
            "name": "frontend",
            "children": [
                {
                    "name": "bpu",
                    "children": [
                        {
                            "name": "ftb"
                        },
                        {
                            "name": "uftb"
                        },
                        {
                            "name": "ittage"
                        },
                        {
                            "name": "tagesc"
                        },
                        {
                            "name": "ras"
                        }
                    ]
                },
                {
                    **dut_priority_critical,
                    "name": "ftq",
                },
                {
                    **dut_priority_high,
                    "name": "ibuffer",
                },
                {
                    **dut_priority_high,
                    "name": "icache",
                },
                {
                    "name": "ifu",
                },
                {
                    **dut_priority_high,
                    "name": "instr_uncache",
                },
                {
                    "name": "itlb",
                },
                {
                    "name": "pmp",
                }
            ]
        },
        {
            "name": "backend",
            "children": [
                {
                    "name": "ctrl_block",
                    "children": [
                        {
                            "name": "decode"
                        },
                        {
                            "name": "rename",
                            "children": [
                                {
                                    "name": "rename_table"
                                },
                                {
                                    "name": "freelist",
                                    "children": [
                                        {
                                            "name": "int"
                                        },
                                        {
                                            "name": "float"
                                        },
                                        {
                                            "name": "vtype"
                                        }
                                    ]
                                }
                            ]
                        },
                        {
                            "name": "dispatch"
                        },
                        {
                            "name": "dispatch_queue",
                            "children": [
                                {
                                    "name": "int"
                                },
                                {
                                    "name": "float"
                                },
                                {
                                    "name": "mem"
                                },
                                {
                                    "name": "vector_float"
                                }
                            ]
                        },
                        {
                            "name": "mem_ctrl"
                        },
                        {
                            **dut_priority_high,
                            "name": "redirect_gen"
                        },
                        {
                            **dut_priority_critical,
                            "name": "rob"
                        },
                        {
                            "name": "pc_gpa_mem"
                        }
                    ]
                },
                {
                    **dut_priority_high,
                    "name": "data_path"
                },
                {
                    **dut_priority_high,
                    "name": "scheduler",
                    "children": [
                        {
                            "name": "int"
                        },
                        {
                            "name": "float"
                        },
                        {
                            "name": "mem"
                        },
                        {
                            "name": "vector_float"
                        }
                    ]
                },
                {
                    "name": "exu_block",
                    "children": [
                        {
                            "name": "float"
                        },
                        {
                            "name": "int",
                            "children": [
                                {
                                    **dut_priority_critical,
                                    "name": "csr"
                                },
                                {
                                    "name": "other"
                                }
                            ]
                        },
                        {
                            **dut_priority_critical,
                            "name": "vector_float"
                        }
                    ]
                },
                {
                    **dut_priority_critical,
                    "name": "og2_for_vector"
                },
                {
                    "name": "pc_target_mem"
                },
                {
                    **dut_priority_high,
                    "name": "wb_data_path"
                },
                {
                    **dut_priority_high,
                    "name": "wb_fu_busy_table"
                },
                {
                    **dut_priority_high,
                    "name": "bypass_network"
                }
            ]
        },
        {
            "name": "mem_block",
            "children": [
                {
                    "name": "lsq",
                    "children": [
                        {
                            **dut_priority_critical,
                            "name": "load_queue",
                            "children": [
                                {
                                    "name": "virtual_load_queue",                                    
                                },
                                {
                                    "name": "raw_rar_queue",
                                },
                                {
                                    "name": "uncache_queue",
                                },
                                {
                                    "name": "exception_queue",
                                }
                            ]
                        },
                        {
                            "name": "store_queue"
                        }
                    ]
                },
                {
                    **dut_priority_critical,
                    "name": "dtlb"
                },
                {
                    **dut_priority_critical,
                    "name": "load_store_unit"
                },
                {
                    **dut_priority_critical,
                    "name": "dcache"
                },
                {
                    "name": "pmp"
                },
                {
                    "name": "prefetcher"
                },
                {
                    "name": "v_mem",
                    **dut_priority_critical,
                    "children": [
                        {
                            "name": "vl_split"
                        },
                        {
                            "name": "v_segment_unit"
                        },
                        {
                            "name": "vl_merger_buffer"
                        },
                        {
                            "name": "vs_merge_buffer"
                        }
                    ]
                },
                {
                    "name": "ptw"
                },
                {
                    "name": "uncache"
                },
                {
                    "name": "sbuffer"
                }
            ]
        },
        {
            "name": "misc",
            "children": [
                {
                    **dut_priority_critical,
                    "name": "l2_cache",
                },
                {
                    **dut_priority_high,
                    "name": "mmio"
                }
            ]
        }
    ]
}

if __name__ == "__main__":
    dut_tree = DutTree(kmh_dut_heriarchy)
    dut_tree.update_leaf_meta({"/kmh_dut/misc/mmio": {"cases": {"total": 10, "pass": 12, "fail": 0, "skip": 0}},
                               "/kmh_dut/mem_block/ptw": {"cases": {"total": 10, "pass": 6, "fail": 2, "skip": 2}},
                               })
    print(dut_tree.as_json())
