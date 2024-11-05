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
import atexit
from logging import getLogger, DEBUG, INFO, WARNING, ERROR, basicConfig


FORMAT = '[%(asctime)s,%(pathname)s:%(lineno)s,%(levelname)s] %(message)s'
basicConfig(format=FORMAT)

log = getLogger()

debug = log.debug
info = log.info
warning = log.warning
error = log.error

def init_log(cfg):
    if not cfg:
        return
    global debug, info, warning, error
    level_map = {
        "debug": DEBUG,
        "info": INFO,
        "warning": WARNING,
        "error": ERROR
    }
    log.setLevel(level_map.get(cfg.log.root_level, INFO))
    from .functions import get_log_dir
    log_path = get_log_dir(cfg=cfg)
    os.makedirs(log_path, exist_ok=True)
    from .functions import time_format
    log_file = cfg.log.file_name.replace("%{time}", time_format()).replace("%{pid}",
                                                                           str(os.getpid())).replace("%{host}",
                                                                                                     os.uname().nodename)
    log_file = os.path.join(log_path, log_file)
    from logging import FileHandler, Formatter, StreamHandler
    ch = StreamHandler()
    ch.setLevel(level_map.get(str(cfg.log.term_level).lower(), INFO))
    ch.setFormatter(Formatter(FORMAT))
    fh = FileHandler(log_file)
    fh.setLevel(level_map.get(str(cfg.log.file_level).lower(), INFO))
    fh.setFormatter(Formatter(FORMAT))
    for handler in log.handlers:
        log.removeHandler(handler)
    log.addHandler(ch)
    log.addHandler(fh)
    def close_fh():
        fh.close()
        log.removeHandler(fh)
    atexit.register(lambda: close_fh())
    debug = log.debug
    info = log.info
    warning = log.warning
    error = log.error
    return log
