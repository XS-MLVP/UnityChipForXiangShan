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
import ast
import functools
import os

import pytest
import yaml

from comm.cfg.model import UnityChipConfig
from comm.functions.base64 import base64_encode, base64_decode
from comm.functions.utils import get_root_dir, get_abs_path, time_format
from comm.logger import debug

__all__ = [
    "get_config",
    "get_log_dir",
    "get_out_dir",
    "get_rtl_dir",
    "get_rtl_lnk_version",
    "get_report_dir",
    "get_version_checker",
    "new_report_name",
    "init_cfg",
    "cfg_as_str",
    "cfg_from_str",
    "dump_cfg",
]

global_cfg = None


def get_config(cfg=None):
    if cfg is not None:
        return cfg
    global global_cfg
    if global_cfg is not None:
        return global_cfg
    import pytest
    cfg_dict = getattr(pytest, "toffee_custom_key_value", None).get("global_unitychip_cfg")
    global_cfg = UnityChipConfig.model_validate(cfg_dict, by_alias=True)
    return global_cfg


def get_log_dir(subdir: str = "", cfg=None) -> str:
    """Gets the absolute path to the log directory from the configuration.

    Args:
        subdir (str, optional): A subdirectory to append to the log path.
            Defaults to "".
        cfg (optional): The configuration object. Loaded automatically if None.

    Returns:
        str: The absolute path to the log directory.
    """
    cfg = get_config(cfg)
    return get_abs_path(cfg.output.out_dir, os.path.join(cfg.log.file_dir, subdir), cfg)


def get_out_dir(subdir: str = "", cfg=None) -> str:
    """Gets the absolute path to the output directory from the configuration.

    Args:
        subdir (str, optional): A subdirectory to append to the output path.
            Defaults to "".
        cfg (optional): The configuration object. Loaded automatically if None.

    Returns:
        str: The absolute path to the output directory.
    """
    cfg = get_config(cfg)
    return get_abs_path(cfg.output.out_dir, subdir, cfg)


def get_rtl_dir(subdir: str = "", cfg=None) -> str:
    """Gets the absolute path to the RTL cache directory from the configuration.

    Args:
        subdir (str, optional): A subdirectory to append to the RTL path.
            Defaults to "".
        cfg (optional): The configuration object. Loaded automatically if None.

    Returns:
        str: The absolute path to the RTL cache directory.
    """
    cfg = get_config(cfg)
    return get_abs_path(cfg.rtl.cache_dir, subdir, cfg)


def get_rtl_lnk_version(cfg=None) -> str:
    """Reads the RTL version from the 'rtl' symlink in the cache directory.

    This function parses the target of the 'rtl' symlink to extract the
    version string.

    Args:
        cfg (optional): The configuration object. Loaded automatically if None.

    Returns:
        str: The extracted RTL version string.

    Raises:
        AssertionError: If the 'rtl' symlink does not exist or is not a symlink.
    """
    lnk = os.path.join(get_rtl_dir(cfg=cfg), "rtl")
    assert os.path.exists(lnk), f"rtl link {lnk} not found"
    assert os.path.islink(lnk), f"{lnk} is not a link, please check"
    version = os.readlink(lnk).replace("/rtl", "").split("/")[-1].strip()
    return version


def get_report_dir(cfg=None) -> str:
    """Gets the absolute path to the report directory from the configuration.

    Args:
        cfg (optional): The configuration object. Loaded automatically if None.

    Returns:
        str: The absolute path to the report directory.
    """
    cfg = get_config(cfg)
    return os.path.join(get_out_dir(cfg=cfg), cfg.report.report_dir)


def get_version_checker(target_version: str):
    """Returns a function to check RTL version compatibility for pytest.

    This factory returns a checker function. If the project's RTL version
    does not match `target_version`, the checker calls `pytest.skip`.
    Otherwise, it does nothing.

    Args:
        target_version (str): The target version string to match against.

    Returns:
        Callable[[], None]: A function that performs the version check.
    """
    from toffee_test.markers import match_version
    version = get_config().rtl.version
    if not match_version(version, target_version):
        def _fail():
            import pytest
            return pytest.skip(f"Unsupported RTL version {version}, need: {target_version}")

        return _fail
    return lambda: None


def new_report_name(cfg=None) -> tuple[str, str]:
    """Generates a new report name and ensures the report directory exists.

    It creates the report directory if needed and resolves placeholders in the
    report name template from the configuration.

    Args:
        cfg (optional): The configuration object. Loaded automatically if None.

    Returns:
        tuple[str, str]: A tuple containing the report directory path and the
            generated report name.
    """
    cfg = get_config(cfg)
    report_dir = get_report_dir(cfg=cfg)
    report_name = cfg.report.report_name
    os.makedirs(report_dir, exist_ok=True)
    return report_dir, report_name


def init_cfg(cfg_file=None, args: list[str] = (), cfg_str_data=None) -> UnityChipConfig:
    if args is None:
        args = list()
    if cfg_str_data:
        return cfg_from_str(cfg_str_data)
    default_cfg = os.path.join(get_root_dir(), "configs/_default.yaml")
    debug("load default config from %s", default_cfg)
    with open(default_cfg, 'r') as f:
        cfg = yaml.safe_load(f)
        cfg["load_path"] = default_cfg
    if cfg_file:
        with open(cfg_file, 'r') as f:
            cfg.update(yaml.safe_load(f))
            cfg["load_path"] = os.path.abspath(cfg_file)
    config = UnityChipConfig.model_validate(cfg)
    for arg in args:
        if "=" in arg:
            key, value = arg.split("=")
            key = key.strip().replace("-", "_")
            try:
                value = ast.literal_eval(value)
                last_attr = key.split(".")[-1]
                attr = functools.reduce(getattr, key.split(".")[:-1], config)
                setattr(attr, last_attr, value)
            except AttributeError as e:
                debug(f"Key {key} not found in config, ignore")
    return config


def cfg_as_str(cfg: UnityChipConfig):
    return base64_encode(yaml.dump(cfg.model_dump(by_alias=True), default_flow_style=False))


def cfg_from_str(cfg_str):
    return UnityChipConfig.model_validate(yaml.safe_load(base64_decode(cfg_str)))


def dump_cfg(cfg: UnityChipConfig = None, cfg_file=None):
    if not cfg_file:
        cfg_file = os.path.join(get_out_dir(), "config-%s.yaml" % time_format())
        debug(f"Dump config to {cfg_file}")
    if cfg is None:
        cfg = get_config()
    assert cfg is not None, "cfg is not initialized"
    with open(cfg_file, 'w') as f:
        f.write(yaml.dump(cfg.model_dump(by_alias=True), default_flow_style=False))


@pytest.fixture(scope="session")
def config():
    return get_config()
