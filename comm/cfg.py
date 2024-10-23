#coding=utf8

from comm.functions import *
import yaml
import os


cfg = None
def init_cfg(cfg_file=None, args=[], cfg_str_data=None):
    global cfg
    if cfg_str_data:
        cfg = cfg_from_str(cfg_str_data)
        return cfg
    default_cfg = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../configs/_default.yaml")
    with open(default_cfg, 'r') as f:
        cfg = yaml.safe_load(f)
    if cfg_file:
        with open(cfg_file, 'r') as f:
            cfg = merge_dict(cfg, yaml.safe_load(f))
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
    return cfg


def cfg_as_str(cfg):
    return base64_encode(yaml.dump(cfg, default_flow_style=False))


def cfg_from_str(cfg_str):
    return yaml.safe_load(base64_decode(cfg_str))


def dump_cfg(cfg_file=None):
    if not cfg_file:
        cfg_file = os.path.join(get_out_dir(), "config-%s.yaml" % time_format())
        debug(f"Dump config to {cfg_file}")
    with open(cfg_file, 'w') as f:
        f.write(yaml.dump(cfg, default_flow_style=False))
