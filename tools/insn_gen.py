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


import random


def generate_rvc_instructions():
    rvc_instructions = []
    for i in range(65536):  # 2^16
        if (i & 0b11) != 0b11:
            rvc_instructions.append(i)
    return rvc_instructions

def generate_32bit_insn(count, opcode):
    insn_list = []
    for i in range(count):
        rand_insn = (random.randint(0, 2**25-1) << 7) | opcode
        insn_list.append(rand_insn)
    return insn_list

def generate_LOAD_insn(count):
    return generate_32bit_insn(count, 0b0000011)

def generate_STORE_insn(count):
    return generate_32bit_insn(count, 0b0100011)

def generate_LOAD_FP_insn(count):
    return generate_32bit_insn(count, 0b0000111)

def generate_STORE_FP_insn(count):
    return generate_32bit_insn(count, 0b0100111)

def generate_MISC_MEM_insn(count):
    return generate_32bit_insn(count, 0b0001111)

def generate_AMO_insn(count):
    return generate_32bit_insn(count, 0b0101111)

def generate_OP_IMM_insn(count):
    return generate_32bit_insn(count, 0b0010011)

def generate_OP_insn(count):
    return generate_32bit_insn(count, 0b0110011)

def generate_AUIPC_insn(count):
    return generate_32bit_insn(count, 0b0010111)

def generate_LUI_insn(count):
    return generate_32bit_insn(count, 0b0110111)

def generate_OP_IMM_32_insn(count):
    return generate_32bit_insn(count, 0b0011011)

def generate_OP_32_insn(count):
    return generate_32bit_insn(count, 0b0111011)

def generate_MADD_insn(count):
    return generate_32bit_insn(count, 0b1000011)

def generate_MSUB_insn(count):
    return generate_32bit_insn(count, 0b1000111)

def generate_NMSUB_insn(count):
    return generate_32bit_insn(count, 0b1001011)

def generate_NMADD_insn(count):
    return generate_32bit_insn(count, 0b1001111)

def generate_OP_FP_insn(count):
    return generate_32bit_insn(count, 0b1010011)

def generate_BRANCH_insn(count):
    return generate_32bit_insn(count, 0b1100011)

def generate_JALR_insn(count):
    return generate_32bit_insn(count, 0b1100111)

def generate_JAL_insn(count):
    return generate_32bit_insn(count, 0b1101111)

def generate_SYSTEM_insn(count):
    return generate_32bit_insn(count, 0b1110011)

def generate_OP_V_insn(count):
    return generate_32bit_insn(count, 0b1010111)

def generate_all_OP_V_insn():
    insn = []
    for i in range(2**25 - 1):
        insn.append((i << 7) | 0b1010111)
    return insn

def generate_random_32bits(count):
    insn = []
    for i in range(count):
        insn.append(random.randint(0, 2**32-1))
    return insn

def generate_random_32bits_rvi(count):
    insn = []
    for i in range(count):
        num = random.randint(0, 2**30 - 1) << 2 | 0b11
        insn.append(num)
    return insn

def generate_all_rvi():
    insn = []
    for i in range(2**30 - 1):
        insn.append(i << 2 | 0b11)
    return insn
