from .functions import *
from .cfg import *
from .logger import *
from .constants import *

def init(cfg=None):
    if not cfg:
        cfg = get_config()
    init_log(cfg)

init()