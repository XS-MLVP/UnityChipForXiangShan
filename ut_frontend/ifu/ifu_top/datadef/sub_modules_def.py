class PreDecodeDataDef():
    def __init__(self):
        
        self.new_instrs = []
        self.jmp_offsets = []
        self.rvcs = []
        self.valid_starts = []
        self.half_valid_starts = []

    def __str__(self):
        res = f"new instrs: {self.new_instrs}\njump offsets: {self.jmp_offsets}\nrvcs: {self.rvcs}\nvalid_starts: {self.valid_starts}\nhalf_valid_starts: {self.half_valid_starts}\n"
        return res
    
    def __eq__(self, value):
        if type(self) != type(value):
            return False
        return self.new_instrs == value.new_instrs and self.jmp_offsets == value.jmp_offsets and self.rvcs == value.rvcs \
                and self.valid_starts == value.valid_starts and self.half_valid_starts == value.half_valid_starts
    

class F3PreDecodeData():
    
    def __init__(self):
        self.brTypes = [] 
        self.isCalls = [] 
        self.isRets = []

    def __str__(self):
        return f"brTypes: {self.brTypes}\nisCalls: {self.isCalls}\nisRets: {self.isRets}"
    
    def __eq__(self, value):
        if type(value) != F3PreDecodeData:
            return False
        return self.brTypes == value.brTypes and self.isCalls == value.isCalls and self.isRets == value.isRets

class PredCheckerRetData():
    def __init__(self):
        self.ranges = [0] * 16
        self.takens = [True] * 16
        self.fixed_tgts = [0] * 16
        self.jmp_tgts = [0] * 16
        self.faults = [0] * 16

        # assistant vars 
        self.miss_pred = [False] * 16
        self.fixed_length = 0
        self.taken_occurs = False

    def __str__(self):
        return f"fixed_ranges: {self.ranges}\nfixed_takens: {self.takens}\nfixed_targets: {self.fixed_tgts}\njump_targets: {self.jmp_tgts}\nfault_type: {self.faults}"
    
    def __eq__(self, value):
        if type(value) != PredCheckerRetData:
            return False

        return self.ranges == value.ranges and self.takens == value.takens and self.fixed_tgts == value.fixed_tgts and self.jmp_tgts == value.jmp_tgts and self.faults == value.faults
    
class PredCheckerStage1RetData():

    def __init__(self):
        self.ranges = [0] * 16
        self.takens = [True] * 16

        # assistant vars 
        self.fixed_length = 0
        self.taken_occurs = False

    def __str__(self):
        return f"fixed_ranges: {self.ranges}\nfixed_takens: {self.takens}\n"
    
    def __eq__(self, value):
        if type(value) != PredCheckerStage1RetData:
            return False

        return self.ranges == value.ranges and self.takens == value.takens 
    
class PredCheckerStage2RetData():
    def __init__(self):
        self.fixed_tgts = [0] * 16
        self.jmp_tgts = [0] * 16
        self.faults = [0] * 16

        # assistant vars 
        self.miss_pred = [False] * 16


    def __str__(self):
        return f"fixed_targets: {self.fixed_tgts}\njump_targets: {self.jmp_tgts}\nfault_type: {self.faults}"
    
    def __eq__(self, value):
        if type(value) != PredCheckerStage2RetData:
            return False

        return self.fixed_tgts == value.fixed_tgts and self.jmp_tgts == value.jmp_tgts and self.faults == value.faults