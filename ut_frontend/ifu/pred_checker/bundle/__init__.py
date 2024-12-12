from toffee import Bundle, Signal, Signals
from dut.PredChecker import DUTPredChecker
from ... import PREDICT_WIDTH
from .auto_bundle import _13Bundle

class PreDecodeInfoBundle(Bundle):
    isRVC, brType, isRet = Signals(3)
    # ret = Signal()

class IfuToPredCheckerBundle(Bundle):
    target, fire_in, ftqOffset_valid, ftqOffset_bits = Signals(4)
    for i in range(PREDICT_WIDTH):
        locals()[f'instrRange_{i}'] = Signal()

        locals()[f'instrValid_{i}'] = Signal()

        locals()[f'jumpOffset_{i}'] = Signal()

        locals()[f'pc_{i}'] = Signal()

        locals()[f'pds_{i}_'] = PreDecodeInfoBundle.from_prefix(f'pds_{i}_')
    
class Stage1OutBundle(Bundle):
    for i in range(PREDICT_WIDTH):
        locals()[f'fixedRange_{i}'] = Signal()
        locals()[f'fixedTaken_{i}'] = Signal()

class Stage2OutBundle(Bundle):
    for i in range(PREDICT_WIDTH):
        locals()[f'fixedTarget_{i}'] = Signal()
        locals()[f'jalTarget_{i}'] = Signal()
        locals()[f'fixedMissPred_{i}'] = Signal()

class PredCheckerRespBundle(Bundle):
    stage1Out = Stage1OutBundle.from_prefix('stage1Out_')
    stage2Out = Stage2OutBundle.from_prefix('stage2Out_')

class PredCheckerIOBundle(Bundle):
    sig_in = IfuToPredCheckerBundle.from_prefix('in_')
    sig_out = PredCheckerRespBundle.from_prefix('out_')

class InternalBundle(Bundle):
    fixedRange = Signal()

class PredCheckerBundle(Bundle):
    def __init__(self, dut: DUTPredChecker):
        super().__init__()
        self.sig_io = PredCheckerIOBundle.from_prefix('io')
        self.sig_self = Bundle.new_class_from_xport(dut.PredChecker).from_prefix("PredChecker_")
