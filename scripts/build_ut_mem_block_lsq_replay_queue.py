# coding=utf8
# ***************************************************************************************
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
# **************************************************************************************/


from comm.export_dut import picker_export

TARGET_NAME = "LoadQueueReplay"


def build(cfg):
    # import base modules
    from comm import get_rtl_dir, extract_signals
    from tempfile import NamedTemporaryFile

    with NamedTemporaryFile("w+", prefix=TARGET_NAME, suffix=".yaml") as internal:
        internal_signals_path = internal.name
        extract_signals(get_rtl_dir(f"{TARGET_NAME}.sv", cfg=cfg), internal_signals_path)
        return picker_export(TARGET_NAME, cfg, internal_file=internal_signals_path)


def line_coverage_files(cfg):
    return ["LoadQueueReplay.v"]
