


test_scenarios = [
    "br_true_hit", "br_false_hit",
    "jal_true_hit", "jal_false_hit",
    "jalr_true_hit", "jalr_false_hit",
    "call_true_hit", "call_false_hit",
    "ret_true_hit", "ret_false_hit",
    "shared_br_true_hit", "shared_br_false_hit",
    "pd_mispred_hit",
]

BACKEND_REDIRECT_LOGIC_GOALS = [
    'VERIFY_BR_HIT',
    'VERIFY_JR_HIT',
    'HIT_SHIFT_1_ADDHIST_1',
    'MISS_SHIFT_1_ADDHIST_1'
]

BACKEND_REDIRECT_PATHS = ['AHEAD_REDIRECT', 'NORMAL_REDIRECT']

BPU_REDIRECT_EVENT_TYPES = ['S1', 'S2_REDIRECT', 'S3_REDIRECT', 'IDLE']
BPU_REDIRECT_EVENT_WEIGHTS = [0.6, 0.05, 0.05, 0.3]


FTQ_BACKEND_UPDATE_SCENARIOS = ['s1', 's2', 's3', 'ifu_redirect', 'backend_redirect']


FTQ_REDIRECT_SCENARIOS = ["backend_redirect", "ifu_redirect"]


CFI_INDEX_UPDATE_STRATEGIES = ["cfiindex_bits_wen", "cfiindex_valid_wen"]

FTQ_FLUSH_REDIRECT_TYPES = ["backend_only", "ifu_only", "both"]



PREDICT_WIDTH = 16
FTQ_SIZE = 64
C_EMPTY = 0
C_FLUSHED = 3
C_COMMITTED = 2
COMMIT_WIDTH = 8