#coding=utf8

import os
import ctypes

current_dir = os.path.dirname(os.path.abspath(__file__))
lib_path = os.path.join(current_dir, 'build', 'libdisasm.so')
assert os.path.isfile(lib_path), f"File not found: {lib_path}, please build the library first, eg: cd {current_dir} && make."

libdisasm = ctypes.CDLL(lib_path)
libdisasm.disasm.argtypes = [ctypes.c_uint64]
libdisasm.disasm.restype = ctypes.c_void_p
libdisasm.disasm_custom_insn.argtypes = [ctypes.c_uint64, ctypes.c_uint64]
libdisasm.disasm_custom_insn.restype = ctypes.c_void_p
libdisasm.disasm_free_mem.argtypes = [ctypes.c_void_p]
libdisasm.disasm_free_mem.restype = None
