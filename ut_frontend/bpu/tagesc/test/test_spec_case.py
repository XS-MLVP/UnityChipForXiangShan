import toffee
import toffee_test

from dut.Tage_SC import DUTTage_SC
from .checkpoints_sc_predict import get_coverage_group_of_sc_predict
from .checkpoints_sc_train import get_coverage_group_of_sc_train
from .checkpoints_tage_predict import get_coverage_group_of_tage_predict
from .checkpoints_tage_train import get_coverage_group_of_tage_train
from ..env.tage_sc_env import TageSCEnv
from ..util.meta_parser import MetaParser


@toffee_test.testcase
async def test_tage_tn_saturing_ctr_update(tage_sc_dut: DUTTage_SC):
    env = TageSCEnv(tage_sc_dut)
    await env.reset_dut()
    await tage_sc_dut.AStep(1)
    pc = 0x80000002
    with MetaParser(0) as parser:
        for x in parser.providers_valid:
            x.value = 1
        for x in parser.providerResps_ctr:
            x.value = 0

        # ctr down saturing
        for ti in range(4):
            for x in parser.providers:
                x.value = ti
            await env.train_agent.exec_update(pc, 1, 1, 1, parser.value, 0, 0, 0, 1, 1, 0, 0)
            for w in range(2):
                assert getattr(tage_sc_dut, f"Tage_SC_tables_{ti}_per_bank_update_wdata_0_{w}_ctr").value == 0, \
                    f"TageTable{ti} down saturation-update failed!"

        # ctr up saturing
        pc += 32
        for x in parser.providerResps_ctr:
            x.value = 0b111
        for w in range(2):
            for ti in range(4):
                for x in parser.providers:
                    x.value = ti
                await env.train_agent.exec_update(pc, w, 1, 1, parser.value, 0, w, 1, 1, 1, 0, 0)
                assert getattr(tage_sc_dut, f"Tage_SC_tables_{ti}_per_bank_update_wdata_0_{w}_ctr").value == 0b111, \
                    f"TageTable{ti} up saturation-update failed!"


@toffee_test.testcase
async def test_bank_tick_ctrs(tage_sc_dut: DUTTage_SC):
    env = TageSCEnv(tage_sc_dut)

    async def expect_reset_u(way: int):
        await tage_sc_dut.AStep(1)
        assert getattr(tage_sc_dut, f"Tage_SC_updateResetU_{way}").value == 1, "ResetU should be high!"

    ##### Test Code Start  #####
    await env.reset_dut()
    await tage_sc_dut.AStep(1)
    pc = 0x80000002
    with MetaParser(0) as parser:
        for x in parser.allocates:
            x.value = 0

        for w in range(2):
            for i in range(32):
                await env.train_agent.exec_update(pc, w, 1, 1, parser.value, 2, w, 1, 1, 1, 0, 0)
            async with toffee.Executor() as _exec:
                _exec(env.train_agent.exec_update(pc, w, 1, 1, parser.value, 2, w, 1, 1, 1, 0, 0))
                _exec(expect_reset_u(1 - w))

        for x in parser.allocates:
            x.value = 7
        await env.train_agent.exec_update(pc, w, 1, 1, parser.value, 2, w, 1, 1, 1, 0, 0)

        for x in parser.allocates:
            x.value = 0xf
        for w in range(2):
            await env.train_agent.exec_update(pc, w, 1, 1, parser.value, 2, w, 1, 1, 1, 0, 0)
    bank_tick_ctrs = [getattr(tage_sc_dut, f"Tage_SC_bankTickCtrs_{w}").value for w in range(2)]
    assert sum(bank_tick_ctrs) == 0, "BankTickCtrs is not down saturation update"


@toffee_test.testcase
async def test_tage_alt_predict_keep_true_and_false(tage_sc_dut: DUTTage_SC):
    env = TageSCEnv(tage_sc_dut)
    await env.reset_dut()
    # Alt prediction is false, provider is true
    with MetaParser(0) as parser:
        for x in parser.allocates:
            x.value = 0xf
        for x in parser.altUsed:
            x.value = 1
        for x in parser.basecnts:
            x.value = 0
        for x in parser.providers_valid:
            x.value = 1
        for x in parser.providerResps_ctr:
            x.value = 0b100
        for i in range(128):
            for _ in range(18):
                await env.train_agent.exec_update(i * 2, 1, 1, 1, parser.value, 0, 0, 0, 1, 1, 0, 0)
        for w in range(2):
            for i in range(128):
                ctr_val = getattr(tage_sc_dut, f"Tage_SC_useAltOnNaCtrs_{w}_{i}").value
                assert ctr_val == 0xf, f"useAltOnNaCtrs_{w}_{i} should be 0xf!"
        # Alt prediction is true, provider is false
        for x in parser.basecnts:
            x.value = 2
        for x in parser.providerResps_ctr:
            x.value = 0b011
        for i in range(128):
            for _ in range(18):
                await env.train_agent.exec_update(i * 2, 1, 1, 1, parser.value, 0, 0, 0, 1, 1, 0, 0)
    for w in range(2):
        for i in range(128):
            ctr_val = getattr(tage_sc_dut, f"Tage_SC_useAltOnNaCtrs_{w}_{i}").value
            assert ctr_val == 0, f"useAltOnNaCtrs_{w}_{i} should be 0!"


@toffee_test.testcase
async def test_sc_threshold_saturation_update(tage_sc_dut: DUTTage_SC):
    env = TageSCEnv(tage_sc_dut)
    await env.reset_dut()
    pc = 0x80000004
    ctrs = [getattr(tage_sc_dut, f"Tage_SC_scThresholds_{i}_ctr") for i in range(2)]
    thresholds = [getattr(tage_sc_dut, f"Tage_SC_scThresholds_{i}_thres") for i in range(2)]
    with MetaParser(0) as parser:
        for x in parser.sc_ctrs:
            for y in x[1:]:
                y.value = 9
        for x in parser.providers_valid:
            x.value = 1
        for x in parser.providerResps_ctr:
            x.value = 0
        for x in parser.sc_preds:
            x.value = 1

        # Threshold.threshold up saturation & ctr up saturation
        for i in range(14):
            for x in parser.sc_ctrs:
                x[0].value = i
            for _ in range(15):
                await env.train_agent.exec_update(pc, 1, 1, 1, parser.value, 3, 0, 0, 1, 1, 0, 0)
            for x in ctrs:
                assert x.value == 0x10, "SC Threshold.ctr should back to neutral value"
    for x in thresholds:
        assert x.value == 0x20, "SC Threshold.thres should execute limit up saturation update"

    # Threshold.threshold down saturation & ctr down saturation
    with MetaParser(0) as parser:
        for x in parser.sc_ctrs:
            for y in x[1:3]:
                y.value = 0
            x[3].value = 10
        for x in parser.providers_valid:
            x.value = 1
        for x in parser.providerResps_ctr:
            x.value = 0
        for x in parser.sc_preds:
            x.value = 1
        for i in range(15):
            for x in parser.sc_ctrs:
                x[0].value = 31 - i
            for w in range(2):
                for _ in range(16):
                    await env.train_agent.exec_update(pc, w, 1, 1, parser.value, 3, w, 1, 1, 1, 0, 0)
            for x in ctrs:
                assert x.value == 0x10, "SC Threshold.ctr should back to neutral value"
    for x in thresholds:
        assert x.value == 0x4, "SC Threshold.thres should execute limit down saturation update"


@toffee_test.testcase
async def test_sc_table_saturation(tage_sc_dut: DUTTage_SC):
    env = TageSCEnv(tage_sc_dut)
    await env.reset_dut()
    pc = 0x1919810
    # SC Table down saturation update
    with MetaParser(0) as parser:
        parser.sc_ctrs[1][1].value = 0x20
        for i in [0, 2, 3]:
            parser.sc_ctrs[1][i].value = 0x20
        for x in parser.sc_ctrs[0]:
            x.value = 0x20

        for x in parser.sc_preds:
            x.value = 1
        for x in parser.providers_valid:
            x.value = 1
        for x in parser.providerResps_ctr:
            x.value = 0
        await env.train_agent.exec_update(pc, 1, 1, 1, parser.value, 2, 0, 0, 1, 1, 0, 0)
    for i in range(4):
        for w in range(2):
            update_write_val = getattr(tage_sc_dut, f"Tage_SC_scTables_{i}_update_wdata_{w}").S()  # read as signed
            assert update_write_val == -32, f"Slot{w} of SC Table{i} is not signed down saturation update"

    # SC Table up saturation update
    with MetaParser(0) as parser:
        parser.sc_ctrs[1][1].value = 31
        for i in [0, 2, 3]:
            parser.sc_ctrs[1][i].value = 31
        for x in parser.sc_ctrs[0]:
            x.value = 31
        for x in parser.sc_preds:
            x.value = 0
        for x in parser.providers_valid:
            x.value = 1
        for x in parser.providerResps_ctr:
            x.value = 0b110

        for w in range(2):
            await env.train_agent.exec_update(pc, w, 1, 1, parser.value, 2, w, 1, 1, 1, 0, 0)

    for i in range(4):
        for w in range(2):
            update_write_val = getattr(tage_sc_dut, f"Tage_SC_scTables_{i}_update_wdata_{w}").S()  # read as signed
            assert update_write_val == 31, f"Slot{w} of SC Table{i} is not signed up saturation update"


@toffee_test.testcase
async def test_sc_total_sum_correctness(tage_sc_dut: DUTTage_SC):
    def get_total_sum(sc_sum: int, tage_ctr: int):
        sc_ctr_sum = sc_sum * 2 + 4
        tage_ctr_centered = ((tage_ctr - 4) * 2 + 1) * 8
        return sc_ctr_sum + tage_ctr_centered

    env = TageSCEnv(tage_sc_dut)
    ##### Test Code Start  #####
    await env.reset_dut()
    pc = 0x80000000
    with MetaParser(0) as parser:
        for w in range(2):
            parser.sc_ctrs[w][0].value = 19

        for x in parser.providers_valid:
            x.value = 1
        for x in parser.providerResps_ctr:
            x.value = 5

        # Test total sum of train
        async def assert_train_total_sum(w: int):
            update_tage_ctr = parser.providerResps_ctr
            sc_table_sum = sum([parser.sc_ctrs[w][i].S() for i in range(4)])
            total_sum_attr = "Tage_SC_sumAboveThreshold_totalSum" + ("_1" if w else "")
            real_val_xdata = getattr(tage_sc_dut, total_sum_attr)
            expect_val = get_total_sum(sc_table_sum, update_tage_ctr[w].value)
            await tage_sc_dut.AStep(1)
            assert expect_val == real_val_xdata.S(), "TotalSum in train is not correct"

        async with toffee.Executor() as _exec:
            _exec(env.train_agent.exec_update(pc, 1, 1, 1, parser.value, 2, 0, 0, 1, 1, 0, 0))
            _exec(assert_train_total_sum(0), sche_group="train_total_sum_assertion1")
            _exec(assert_train_total_sum(1), sche_group="train_total_sum_assertion2")

    # Test total sum of predict
    async def assert_predict_total_sum(w: int):
        _suffix = "_1" if w else ""
        tage = getattr(tage_sc_dut, f"Tage_SC_s2_tagePrvdCtrCentered_r" + _suffix).value
        tage_centered = ((tage - 4) * 2 + 1) * 8
        high_sc_sum = getattr(tage_sc_dut, f"Tage_SC_s2_scTableSums{_suffix}_1").S()
        low_sc_sum = getattr(tage_sc_dut, f"Tage_SC_s2_scTableSums{_suffix}_0").S()
        expect_high = high_sc_sum + tage_centered
        expect_low = low_sc_sum + tage_centered
        real_high = getattr(tage_sc_dut, "Tage_SC_s2_totalSums_1" + _suffix)
        real_low = getattr(tage_sc_dut, "Tage_SC_s2_totalSums_0" + _suffix)
        await tage_sc_dut.AStep(1)
        assert expect_high == real_high.S() and expect_low == real_low.S(), "TotalSum in predict is not correct"

    async with toffee.Executor() as _exec:
        _exec(env.ctrl_agent.exec_activate())
        _exec(env.predict_agent.exec_predict(pc, 2))
        _exec(assert_predict_total_sum(1))


@toffee_test.testcase
async def test_update_when_predict(tage_sc_dut: DUTTage_SC):
    env = TageSCEnv(tage_sc_dut)
    await env.reset_dut()
    async with toffee.Executor() as _exec:
        _exec(env.predict_agent.exec_predict(0x114514, 1))
        _exec(env.ctrl_agent.exec_activate())

    prev = env.predict_agent.io_out.as_dict()
    async with toffee.Executor() as _exec:
        _exec(env.predict_agent.exec_predict(0x114514, 1))
        _exec(env.ctrl_agent.exec_activate())
        _exec(env.train_agent.exec_update(0x114514, 1, 1, 1, prev["last_stage_meta"], 1, 0, 0, 1, 1, 0, 0))
    assert prev == env.predict_agent.io_out.as_dict()


@toffee_test.testcase
async def test_always_taken(tage_sc_dut: DUTTage_SC):
    env = TageSCEnv(tage_sc_dut)

    pc = 0x800013
    await env.reset_dut()
    for w in range(2):
        await env.train_agent.exec_update(pc, w, 1, 1, 1, 0, 1, 0, 0, 0, w, 1)

    async with toffee.Executor() as _exec:
        _exec(env.ctrl_agent.exec_activate())
        _exec(env.predict_agent.exec_predict(pc, 1))
    await tage_sc_dut.AStep(1)
    s3 = env.predict_agent.io_out.s3
    assert (s3.br_taken_mask_1.value, s3.br_taken_mask_0.value) == (1, 1), "Predict result should be true"


@toffee_test.fixture
async def tage_sc_dut(toffee_request: toffee_test.ToffeeRequest):
    import asyncio
    dut = toffee_request.create_dut(DUTTage_SC, "clock")

    toffee_request.add_cov_groups([
        get_coverage_group_of_tage_predict(dut),
        get_coverage_group_of_tage_train(dut),
        get_coverage_group_of_sc_predict(dut),
        get_coverage_group_of_sc_train(dut),
    ])
    toffee.start_clock(dut)
    yield dut

    cur_loop = asyncio.get_event_loop()
    for task in asyncio.all_tasks(cur_loop):
        if task.get_name() == "__clock_loop":
            task.cancel()
            try:
                await task
            except asyncio.CancelledError:
                break
