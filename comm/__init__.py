from .functions import *
from .cfg import *
from .logger import *

def init():
    cfg = get_config()
    init_log(cfg)
