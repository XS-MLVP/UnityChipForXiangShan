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
import argparse
import pytest
import json
from comm import init_cfg, cfg_as_str, get_rtl_lnk_version, error, build_dut, replace_default_vars_in_dict, remove_version_tag
from comm import download_rtl, get_rtl_dir, init_log, init, new_report_name, process_doc_result, base64_encode


def main():
    parser = argparse.ArgumentParser(description="Run pytest")
    parser.add_argument("--config", type=str, help="config file", default=None)
    parser.add_argument("-b", "--build", type=str, help="duts to buld, eg: -b dut1,dut2; -b dut*", default="")
    parser.add_argument("--download-rtl", action="store_true", help="only download rtl")
    parser.add_argument("--allure-json", action="store_true", help="generate allure-report json data")
    args, append_args = parser.parse_known_args()
    cfg_value = []
    for a in append_args.copy():
        key = append_args.pop(0)
        if "=" in key:
            cfg_value.append(key)
        if a.startswith("--"):
            break
    if args.config:
        if not os.path.exists(args.config):
            error("config file not found: %s", args.config)
            return
    cfg = init_cfg(args.config, cfg_value)
    init(cfg)
    if args.download_rtl:
        init_log(cfg)
        download_rtl(cfg.rtl.base_url, get_rtl_dir(cfg=cfg), cfg.rtl.version)
        return
    cfg.unfreeze()
    link_verison = get_rtl_lnk_version(cfg)
    if cfg.rtl.version != "latest":
        assert link_verison == cfg.rtl.version, f"RTL link version ({link_verison}) not equal to config version ({cfg.rtl.version})"
    else:
        cfg.rtl.version = link_verison # set current rtl version
    cfg.rtl.version = remove_version_tag(cfg.rtl.version)
    report_dir, report_name = new_report_name(cfg)
    cfg.report.report_name = report_name
    cfg.freeze()
    cfg_value = cfg_as_str(cfg)
    if args.build:
        init_log(cfg)
        build_dut(args.build, cfg)
        return
    # set report args
    toffee_key_value = {
        "toffee_tags_current_version" : cfg.rtl.version,
        "toffee_tags_skip_tags"       : cfg.test.skip_tags,
        "toffee_tags_run_tags"        : cfg.test.run_tags,
        "toffee_tags_skip_cases"      : cfg.test.skip_cases,
        "toffee_tags_run_cases"       : cfg.test.run_cases,
        "toffee_ignore_exceptions"    : cfg.test.skip_exceptions,
        "toffee_report_information"   : replace_default_vars_in_dict(cfg.report.information.as_dict(), cfg=cfg),
        "global_unitychip_cfg"        : cfg_value,
    }
    append_args.extend(["--report-dir", report_dir, "--report-name", report_name,
                        "--report-dump-json", "--custom-key-value", base64_encode(json.dumps(toffee_key_value))])
    if args.allure_json:
        def _allure_dir(pdir, pname):
            return os.path.join(os.path.dirname(os.path.join(pdir, pname)), "allure")
        append_args.extend(["--alluredir", _allure_dir(report_dir, report_name)])
    pytest.main(append_args, plugins=[__import__(__name__)])
    process_doc_result(report_dir, report_name, cfg)


if __name__ == "__main__":
    main()
