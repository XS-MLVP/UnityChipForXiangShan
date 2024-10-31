#coding=utf8

from .logger import debug
import yaml
import os
import pytest

global_cfg = None

class CfgObject:
    freeze = False
    def __init__(self, data: dict) -> None:
        if data:
            for key, value in data.items():
                key = key.replace("-", "_")
                if isinstance(value, dict):
                    super().__setattr__(key, CfgObject(value))
                else:
                    super().__setattr__(key, value)

    def freeze(self):
        self.freeze = True
        for _, value in self.__dict__.items():
            if isinstance(value, CfgObject):
                value.freeze()

    def unfreeze(self):
        self.freeze = False
        for _, value in self.__dict__.items():
            if isinstance(value, CfgObject):
                value.unfreeze()

    def __setattr__(self, name, value):
        if self.freeze and name != "freeze":
            raise AttributeError("Cannot set attribute %s in freeze mode" % name)
        super().__setattr__(name, value)

    def as_dict(self):
        data = {}
        for key, value in self.__dict__.items():
            if isinstance(value, CfgObject):
                data[key] = value.as_dict()
            else:
                data[key] = value
        return data

    def __str__(self):
        return str(self.as_dict())


def get_config(cfg=None):
    if cfg is not None:
        return cfg
    global global_cfg
    if global_cfg is not None:
        return global_cfg
    cfg_str = pytest.global_unitychip_cfg
    global_cfg = cfg_from_str(cfg_str)
    global_cfg.freeze()
    return global_cfg


@pytest.fixture(scope="session")
def config():
    return get_config()


def init_cfg(cfg_file=None, args=[], cfg_str_data=None):
    from .functions import merge_dict
    if cfg_str_data:
        return cfg_from_str(cfg_str_data)
    default_cfg = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                               "../configs/_default.yaml")
    default_cfg = os.path.abspath(default_cfg)
    debug("load default config from %s", default_cfg)
    with open(default_cfg, 'r') as f:
        cfg = yaml.safe_load(f)
        cfg["__file__"] = default_cfg
    if cfg_file:
        with open(cfg_file, 'r') as f:
            cfg = merge_dict(cfg, yaml.safe_load(f))
            cfg["__file__"] = os.path.abspath(cfg_file)
    for arg in args:
        tmp_cfg = cfg
        if "=" in arg:
            key, value = arg.split("=")
            keys = key.split(".")
            for k in keys[:-1]:
                if k not in tmp_cfg:
                    tmp_cfg = None
                    break
                tmp_cfg = tmp_cfg[k]
            if tmp_cfg:
                k = keys[-1]
                if k not in tmp_cfg:
                    debug(f"Key {key} not found in config, ignore")
                else:
                    tmp_cfg[k] = type(tmp_cfg[k])(value)
    return CfgObject(cfg)


def cfg_as_str(cfg: CfgObject):
    from .functions import base64_encode
    return base64_encode(yaml.dump(cfg.as_dict(), default_flow_style=False))


def cfg_from_str(cfg_str):
    from .functions import base64_decode
    return CfgObject(yaml.safe_load(base64_decode(cfg_str)))


def dump_cfg(cfg: CfgObject = None, cfg_file=None):
    from .functions import time_format, get_out_dir
    if not cfg_file:
        cfg_file = os.path.join(get_out_dir(), "config-%s.yaml" % time_format())
        debug(f"Dump config to {cfg_file}")
    if cfg is None:
        cfg = get_config()
    assert cfg is not None, "cfg is not initialized"
    with open(cfg_file, 'w') as f:
        f.write(yaml.dump(cfg.as_dict(), default_flow_style=False))
