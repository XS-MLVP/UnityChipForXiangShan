#coding=utf8

import os
import argparse
import pytest
from comm import init_cfg, cfg_as_str, error, download_rtl, get_rtl_dir, init_log


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
            error("config file not found:", agrs.config)
            return
    cfg = init_cfg(agrs.config, cfg_value)
    if agrs.download_rtl:
        init_log(cfg)
        download_rtl(cfg.rtl.base_url, get_rtl_dir(cfg=cfg), cfg.rtl.version)
        return
    cfg_value = cfg_as_str(cfg)
    pytest.global_unitychip_cfg = cfg_value
    pytest.main(append_args, plugins=[__import__(__name__)])


if __name__ == "__main__":
    main()
