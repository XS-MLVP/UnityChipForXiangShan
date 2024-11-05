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
from comm import warning, info


def build(cfg):
	# import base modules
	from toffee_test.markers import match_version
	from comm import is_all_file_exist, get_rtl_dir, exe_cmd, get_root_dir
	# check version
	if not match_version(cfg.rtl.version, []):
		warning("backend_ctrlblock_decode: %s" % f"Unsupported RTL version {cfg.rtl.version}")
		return False
	# check files
	f = is_all_file_exist(["rtl/RVCExpander.sv", "rtl/PreDecode.sv", "rtl/DecodeStage.sv"], get_rtl_dir(cfg=cfg))
	assert f is True, f"File {f} not found"
	# build
	# export RVCExpander.sv
	if not os.path.exists(get_root_dir("dut/rvcexpander")):
		info("Exporting RVCExpander.sv")
		s, out, err = exe_cmd(f'picker export --cp_lib false {get_rtl_dir("rtl/RVCExpander.sv", cfg=cfg)} --lang python --tdir {get_root_dir("dut/rvcexpander")}')
		assert s, "Failed to export RVCExpander.sv: %s\n%s" % (out, err)
	# export PreDecode.sv
	if not os.path.exists(get_root_dir("dut/predecode")):
		info("Exporting PreDecode.sv")
		s, _, _ = exe_cmd(f'picker export --cp_lib false {get_rtl_dir("rtl/PreDecode.sv", cfg=cfg)} --lang python --tdir {get_root_dir("dut/predecode")} -w predecode.fst -c')
		assert s, "Failed to export PreDecode.sv"
	# export DecodeStage.sv
	if not os.path.exists(get_root_dir("dut/decodestage")):
		info("Exporting DecodeStage.sv")
		s, _, _ = exe_cmd(f'picker export --cp_lib false {get_rtl_dir("rtl/DecodeStage.sv", cfg=cfg)} --fs {get_root_dir("scripts/backend_ctrlblock_decode/rtl_files.f")} --lang python --tdir {get_root_dir("dut/decodestage")}  -w decode.fst -c')
		assert s, "Failed to export DecodeStage.sv"
	# build disasm
	if not os.path.exists(get_root_dir("tools/disasm/build")):
		info("Building disasm")
		s, _, _ = exe_cmd("make -C %s" % get_root_dir("tools/disasm"))
		assert s, "Failed to build disasm"
	info("Build backend_ctrlblock_decode done")
	return True


def line_coverage_files(cfg):
	return ["rtl/PreDecode.sv", "rtl/DecodeStage.sv"]
