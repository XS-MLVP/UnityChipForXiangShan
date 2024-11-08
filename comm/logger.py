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


level_map = {
    "debug": DEBUG,
    "info": INFO,
    "warning": WARNING,
    "error": ERROR
}


def init_log(cfg):
    if not cfg:
        return
    global debug, info, warning, error
    log.setLevel(level_map.get(str(cfg.log.root_level).lower(), INFO))
    from .functions import get_log_dir
    log_path = get_log_dir(cfg=cfg)
    os.makedirs(log_path, exist_ok=True)
    from .functions import replace_default_vars
    log_file = replace_default_vars(cfg.log.file_name, cfg=cfg)
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


__cached_loggers__ = {}
def get_file_logger(file_name=None, name=None, level="debug", format=FORMAT, cfg=None, propagate=False):
    assert file_name, "file_name must be specified"
    from .functions import get_log_dir, replace_default_vars
    file_name = replace_default_vars(file_name, cfg=cfg)
    # Cache the logger to avoid creating multiple loggers for the same file
    global __cached_loggers__
    if not file_name.startswith("/"):
        file_name = os.path.abspath(os.path.join(get_log_dir(cfg=cfg), file_name))
    if file_name in __cached_loggers__:
        warning(f"logger for file {file_name} already exists, ignore create new one")
        return __cached_loggers__[file_name]
    # Create a new logger
    logger = getLogger(name if name else file_name)
    # Set propagate to False to avoid duplicate logs (default no need to propagate to root logger)
    logger.propagate = propagate
    __cached_loggers__[file_name] = logger
    logger.setLevel(level_map.get(level.lower(), INFO))
    # Create a file handler
    from logging import FileHandler, Formatter
    fh = FileHandler(file_name)
    fh.setLevel(level_map.get(level.lower(), INFO))
    if format:
        fh.setFormatter(Formatter(format))
    # Remove all handlers and add the new file handler
    for handler in logger.handlers:
        logger.removeHandler(handler)
    logger.addHandler(fh)
    # Close the file handler when the program exits
    def close_fh():
        fh.close()
        logger.removeHandler(fh)
    atexit.register(lambda: close_fh())
    return logger
