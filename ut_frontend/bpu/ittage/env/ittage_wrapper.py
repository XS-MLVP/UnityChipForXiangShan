import os.path
import random
from datetime import datetime


import toffee
from toffee import ClockCycles
from dut.ITTage import DUTITTage
from ..util.common import get_folded_hist
from .bundle import *

__all__ = ['ITTageWrapper']


class ITTageWrapper:
    def __init__(self, dut: DUTITTage):
        # Create DUT
        self.dut = dut
        self.dut.InitClock("clock")
        self.xclock = self.dut.xclock  # for callback function

        # Connect Bundle
        self.update_bundle = UpdateBundle.from_prefix("io_update_").set_name("ittage_update").bind(self.dut)
        self.in_bundle = InBundle.from_prefix("io_in_").set_name("ittage_in").bind(self.dut)
        self.out_bundle = OutBundle.from_prefix("io_out_").set_name("ittage_out").bind(self.dut)
        self.pipeline_ctrl = PipelineCtrl.from_prefix("io_").set_name("ittage_pipeline_ctrl").bind(self.dut)

        # Reset
        self.reset()

    def finalize(self):
        self.dut.Finish()

    async def __rst_async__(self):
        self.dut.reset.value = 1
        await ClockCycles(self.dut, 10)
        self.dut.reset.value = 0

    def __set_fire__(self, stage):
        for i in range(0, 4):
            getattr(self.pipeline_ctrl, f"s{stage}_fire_{i}").value = 1


    def __unset_fire__(self, stage):
        for i in range(0, 4):
            getattr(self.pipeline_ctrl, f"s{stage}_fire_{i}").value = 0

    async def __predict_async__(self, fh, pc, use_dummy_fh=False):
        # stage0
        self.__set_fire__(0)
        self.in_bundle.bits_s0_pc_3.value = pc
        if use_dummy_fh:
            self.in_bundle.folded_hist.set_all(0)
        else:
            self.in_bundle.folded_hist.assign(get_folded_hist(fh))
        await ClockCycles(self.dut, 1)
        self.__unset_fire__(0)

        # stage1
        self.__set_fire__(1)
        await ClockCycles(self.dut, 1)
        self.__unset_fire__(1)

        # stage2
        self.__set_fire__(2)
        await ClockCycles(self.dut, 1)
        self.__unset_fire__(2)

        # stage3
        await ClockCycles(self.dut, 1)

        return self.out_bundle.as_dict()

    async def __update_async__(self, update_req):
        self.update_bundle.assign(update_req)
        self.update_bundle.valid.value = 1
        await ClockCycles(self.dut, 1)
        self.update_bundle.valid.value = 0

        await ClockCycles(self.dut, 3)

        return None

    def predict(self, fh, pc, use_dummy_fh=False):
        # stage0
        self.__set_fire__(0)
        self.in_bundle.bits_s0_pc_3.value = pc
        if use_dummy_fh:
            self.in_bundle.folded_hist.set_all(0)
        else:
            self.in_bundle.folded_hist.assign(get_folded_hist(fh))
        self.xclock.Step(1)
        self.__unset_fire__(0)

        # stage1
        self.__set_fire__(1)
        self.xclock.Step(1)
        self.__unset_fire__(1)

        # stage2
        self.__set_fire__(2)
        self.xclock.Step(1)
        self.__unset_fire__(2)

        # stage3
        self.xclock.Step(1)

        return self.out_bundle.as_dict()

    def predict_async(self, fh, pc, use_dummy_fh=False):
        return toffee.create_task(self.__predict_async__(fh, pc, use_dummy_fh))

    def update(self, update_req):
        self.update_bundle.assign(update_req)
        self.update_bundle.valid.value = 1
        self.xclock.Step(1)
        self.update_bundle.valid.value = 0

        self.xclock.Step(1)
        pass

    def update_async(self, update_req):
        return toffee.create_task(self.__update_async__(update_req))

    def reset(self):
        self.dut.reset.value = 1
        self.xclock.Step(1)
        self.dut.reset.value = 0
        while self.dut.io_s1_ready.value == 0:
            self.xclock.Step(1)
        self.xclock.Step(10)

    def reset_async(self):
        return toffee.create_task(self.__rst_async__())