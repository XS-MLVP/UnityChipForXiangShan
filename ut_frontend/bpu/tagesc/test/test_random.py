import os
import random

import pytest
import toffee
import toffee_test

from dut.Tage_SC import DUTTage_SC
from .checkpoints_sc_predict import get_coverage_group_of_sc_predict
from .checkpoints_tage_predict import get_coverage_group_of_tage_predict
from .checkpoints_tage_train import get_coverage_group_of_tage_train
from ..env.fake_global_history import FakeGlobalHistory
from ..env.tage_sc_env import TageSCEnv


@pytest.mark.parametrize("pc_bound", list(range(8)))
@toffee_test.testcase
async def test_random(tage_sc_env: TageSCEnv, pc_bound: int):
    random.seed(os.urandom(128))
    fgh = FakeGlobalHistory()
    env = tage_sc_env
    await env.reset_dut()
    for _ in range(3500):
        taken = (random.randint(0, 1), random.randint(0, 1)) if _ > 0 else (0, 0)
        pc = 0x80000003 + random.randint(0, pc_bound)
        await env.predict_agent.exec_predict(pc, fgh.value)

        tage_predict = await env.predict_agent.get_tage_prediction()
        sc_predict = await env.predict_agent.get_sc_prediction()
        meta = await env.predict_agent.get_meta_value()
        miss = sc_predict[0] != taken[0], sc_predict[1] != taken[1]
        await env.update_agent.exec_update(pc, 1, 1, 1, meta, fgh.value, *taken, *miss, 0, 0)
        for t in taken:
            fgh.update(t > 0)


@toffee_test.fixture
async def tage_sc_env(toffee_request: toffee_test.ToffeeRequest):
    import asyncio
    dut = toffee_request.create_dut(DUTTage_SC, "clock")
    env = TageSCEnv(dut)
    toffee_request.add_cov_groups([
        get_coverage_group_of_tage_predict(env),
        get_coverage_group_of_tage_train(env),
        get_coverage_group_of_sc_predict(env),
    ])
    toffee.start_clock(dut)
    yield env

    cur_loop = asyncio.get_event_loop()
    for task in asyncio.all_tasks(cur_loop):
        if task.get_name() == "__clock_loop":
            task.cancel()
            try:
                await task
            except asyncio.CancelledError:
                break
