#coding=utf8

from logging import getLogger, DEBUG, INFO, WARNING, ERROR, basicConfig

FORMAT = '[%(asctime)s,%(pathname)s,%(lineno)s,%(levelname)s] %(message)s'
basicConfig(format=FORMAT)


log = getLogger("UnityChip")


def init_log(cfg):
    level = cfg.log.level
    log.setLevel({
        "debug": DEBUG,
        "info": INFO,
        "warning": WARNING,
        "error": ERROR
    }.get(str(level).lower(), INFO))


debug = log.debug
info = log.info
warning = log.warning
error = log.error
