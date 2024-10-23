#coding=utf8

import os
import argparse
import pytest
from comm import init_cfg, cfg_as_str


def pytest_addoption(parser):
    parser.addoption("--xs-cfg-values", action="store", default="", help="Configuration values")


@pytest.fixture(scope="session", autouse=True)
def apply_cfg_values(request):
    cfg_values = request.config.getoption("--xs-cfg-values")
    if cfg_values:
        init_cfg(cfg_str_data=cfg_values)


def main():
    parser = argparse.ArgumentParser(description="Run pytest")
    parser.add_argument("--config", type=str, help="config file", default=None)
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
            print("config file not found:", agrs.config)
            return
    cfg_value = cfg_as_str(init_cfg(agrs.config, cfg_value))
    append_args.extend(["--xs-cfg-values", cfg_value])
    pytest.main(append_args, plugins=[__import__(__name__)])


if __name__ == "__main__":
    main()
