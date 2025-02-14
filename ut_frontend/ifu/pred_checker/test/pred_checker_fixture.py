import toffee_test
from comm import get_version_checker
from ... import PREDICT_WIDTH, RET_LABEL, RVC_LABEL, BRTYPE_LABEL

from dut.PredChecker import DUTPredChecker
from comm.functions import UT_FCOV, module_name_with
import toffee.funcov as fc
from toffee import *

version_check = get_version_checker("openxiangshan-kmh-*")

gr = fc.CovGroup(UT_FCOV("../../../TOFFEE"))

from ..env import PredCheckerEnv


    
