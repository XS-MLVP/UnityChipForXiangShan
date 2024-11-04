#coding=utf8

import os
import argparse
import pytest
from comm import init_cfg, cfg_as_str, get_rtl_lnk_version, error
from comm import download_rtl, get_rtl_dir, init_log, init, new_report_name


def main():
    parser = argparse.ArgumentParser(description="Run pytest")
    parser.add_argument("--config", type=str, help="config file", default=None)
    parser.add_argument("--download-rtl", action="store_true", help="only download rtl")
    agrs, append_args = parser.parse_known_args()
    cfg_value = []
    for a in append_args.copy():
        key = append_args.pop(0)
        if "=" in key:
            cfg_value.append(key)
        if a.startswith("--"):
            break
    if agrs.config:
        if not os.path.exists(agrs.config):
            error("config file not found: %s", agrs.config)
            return
    cfg = init_cfg(agrs.config, cfg_value)
    init(cfg)
    if agrs.download_rtl:
        init_log(cfg)
        download_rtl(cfg.rtl.base_url, get_rtl_dir(cfg=cfg), cfg.rtl.version)
        return
    cfg.unfreeze()
    link_verison = get_rtl_lnk_version(cfg)
    if cfg.rtl.version != "latest":
        assert link_verison == cfg.rtl.version, f"RTL link version ({link_verison}) not equal to config version ({cfg.rtl.version})"
    else:
        cfg.rtl.version = link_verison # set current rtl version
    cfg.freeze()
    cfg_value = cfg_as_str(cfg)
    # set report args
    report_dir, report_name = new_report_name(cfg)
    append_args.extend(["--report-dir", report_dir, "--report-name", report_name])
    # cache global config in pytest
    pytest.global_unitychip_cfg = cfg_value
    # set toffee config
    pytest.toffee_tags_current_version = cfg.rtl.version
    pytest.toffee_tags_skip_tags = cfg.test.skip_tags
    pytest.toffee_tags_run_tags = cfg.test.run_tags
    pytest.toffee_tags_skip_cases = cfg.test.skip_cases
    pytest.toffee_tags_run_cases = cfg.test.run_cases
    pytest.toffee_ignore_exceptions = cfg.test.skip_exceptions
    pytest.toffee_report_information = cfg.report.information.as_dict()
    pytest.main(append_args, plugins=[__import__(__name__)])


if __name__ == "__main__":
    main()
