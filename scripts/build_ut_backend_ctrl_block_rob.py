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


import os


def build(cfg):
    return False


def get_metadata():
    return {
        "dut_name": "backend_ctrl_block_rob",
        "dut_dir": "Rob",
        "test_targets": [
            "ut_backend/ctrl_block/rob",
            "ut_backend/ctrl_block",
            "ut_backend"
        ]
    }


def line_coverage_files(cfg):
    return []
