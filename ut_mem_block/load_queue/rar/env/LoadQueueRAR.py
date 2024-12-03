import toffee
import os
import pytest
import ctypes
import datetime
import toffee.funcov as fc

from comm import get_out_dir, get_root_dir, debug, UT_FCOV, get_file_logger, get_version_checker, module_name_with

from toffee_test.reporter import set_func_coverage
from toffee_test.reporter import set_line_coverage

class LoadQueueRAR(toffee.Bundle):
    def __init__(self, dut: DUTLoadQueueRAR):
        super().__init__()
        self.dut = dut
        for i in range(6):
            setattr(self, f"in_data_{i}", toffee.Bundle.from_prefix(f"io_in_{i}_", dut))
            setattr(self, f"out_data_{i}", toffee.Bundle.from_prefix(f"io_out_{i}_", dut))
        self.input_inst = [getattr(self, f"in_data_{i}") for i in range(6)]
        self.output_instrution = [getattr(self, f"out_data_{i}") for i in range(6)]
        self.io = toffee.Bundle.from_prefix(f"io_", dut)
        self.bind(dut)