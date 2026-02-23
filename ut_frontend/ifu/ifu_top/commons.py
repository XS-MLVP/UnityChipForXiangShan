PREDICT_WIDTH = 16
# BLOCK_BYTES=64
BLOCK_OFF_BITS=6
PRED_ERR = 1
LAST_HALF_ERR = 2
from random import randint

def randbool(rate=50):
    return randint(0, 99) < rate

def is_next_line(addr1, addr2):
    return bool(((addr1 >> BLOCK_OFF_BITS) & 1) ^ ((addr2 >> BLOCK_OFF_BITS) & 1))

def is_last_in_line(pc):
    return (pc & 0x3F) == 0b111110

def calc_double_line(start_addr):
    return (start_addr >> (BLOCK_OFF_BITS -1 )) & 1

def calc_blk_length(start, next_start):
    block_length = (next_start - start) // 2
    return max(0, min(block_length, PREDICT_WIDTH))

def calc_cut_ptr(startAddr):
    idx_pos = (startAddr >> 1) & 0x1F
    cuts = [idx_pos + i for i in range(PREDICT_WIDTH + 1)]
    return cuts

def check_icache_resp_all_valid(icache_resp_valid, vaddrs, icache_doubleline, req_doubleline, start, next_start):
    if not icache_resp_valid:
        return False
    if vaddrs[0] != start:
        return False
            
    if not req_doubleline:
        return True
    return icache_resp_valid and (icache_doubleline and vaddrs[1] == next_start)