import random
from typing import Callable, Generator, List, Literal, Tuple
from hypothesis import strategies as st
from hypothesis.strategies import composite

from ut_frontend.ifu.frontend_trigger.agent.frontend_trigger_agent import (
    BreakpointFlags,
    BreakpointUpdateInfo,
)


def get_mask_one(length: int) -> int:
    # 生成一个长度为 length 的全 1 的二进制数，用来进行数据截断
    return (1 << length) - 1


@composite
def bp_update_strategy(draw, pc_width=50):
    # Generate a random pc value
    max_pc = get_mask_one(pc_width)
    pc = draw(st.integers(min_value=0, max_value=max_pc))
    action = draw(st.integers(min_value=0, max_value=1))
    tselect = draw(st.booleans())
    match_type = draw(st.sampled_from([0, 2, 3]))
    chain = draw(st.booleans())

    bp_update = BreakpointUpdateInfo(
        action=action, tdata2=pc, select=tselect, matchType=match_type, chain=chain
    )

    return bp_update


@composite
def bp_flags_strategy(draw):
    tEnableVec = draw(st.lists(st.booleans(), min_size=4, max_size=4))
    debugMode = draw(st.booleans())
    triggerCanRaiseBpExp = draw(st.booleans())

    return BreakpointFlags(
        tEnableVec=tEnableVec,
        debugMode=debugMode,
        triggerCanRaiseBpExp=triggerCanRaiseBpExp,
    )


def bp_update_generator(
    pc_width: int = 50,
    condition: Callable[[BreakpointUpdateInfo], bool] = lambda x: True,
):
    """生成器版本的断点更新信息生成器"""
    max_pc = get_mask_one(pc_width - 1)
    while True:
        # 生成随机pc值
        pc = random.randint(0, max_pc) << 1
        action = random.randint(0, 1)
        tselect = random.choice([True, False])
        match_type = random.choice([0, 2, 3])
        chain = random.choice([True, False])

        bp_update = BreakpointUpdateInfo(
            action=action, tdata2=pc, select=tselect, matchType=match_type, chain=chain
        )

        if condition(bp_update):
            yield bp_update


def bp_flags_generator(
    condition: Callable[[BreakpointFlags], bool] = lambda x: True
) -> Generator[BreakpointFlags, None, None]:
    while True:
        tEnableVec = [random.choice([True, False]) for _ in range(4)]
        debugMode = random.choice([True, False])
        triggerCanRaiseBpExp = random.choice([True, False])

        flags = BreakpointFlags(
            tEnableVec=tEnableVec,
            debugMode=debugMode,
            triggerCanRaiseBpExp=triggerCanRaiseBpExp,
        )

        if condition(flags):
            yield flags


def int_generator(
    min_value: int = 0,
    max_value: int = 0xFFFFFFFF,
    condition: Callable[[int], bool] = lambda x: True,
) -> Generator[int, None, None]:
    while True:
        value = random.randint(0, max_value)
        if condition(value):
            yield value


def gen_pcs(include_pc_list):
    # 确保 include_pc_list 中的每一项都是偶数，且不为负数
    if any(pc % 2 != 0 or pc < 0 for pc in include_pc_list):
        assert False, "include_pc_list 中的每一项必须是偶数且不为负数"

    # 确保最大值和最小值的差不超过 30
    if max(include_pc_list) - min(include_pc_list) > 30:
        assert False, "include_pc_list 中的最大项和最小项的差不能超过 30"

    # 计算所有可能的 start 值，使得 rand_pcs 包含 include_pc_list 中的每一项
    min_pc = min(include_pc_list)
    max_pc = max(include_pc_list)

    # 计算 start 的范围
    start_min = max(0, max_pc - 2 * 15)
    start_max = min_pc

    # 确保为偶数
    start = random.randint(start_min // 2, start_max // 2) * 2

    # 生成包含 16 项的列表，每项递增 2
    rand_pcs = [start + 2 * i for i in range(16)]

    # 验证 include_pc_list 中的每一项是否在列表中
    for pc in include_pc_list:
        assert (
            pc in rand_pcs
        ), "生成的列表中未包含 include_pc_list 中的某一项，逻辑错误！"

    return rand_pcs


def int_with_condition_generator(
    cond_list: List[Tuple[Literal[">", "<", "=", ">=", "<="], int]],
    lower_spec: int = 0,
    upper_spec: int = int(1e9),
) -> Generator[int, None, None]:
    """
    生成满足所有条件的随机数。

    Args:
        cond_list: 条件列表，每个条件是一个元组 (条件类型, 值)。
                      条件类型可以是 ">", "<", "=", ">=", "<=" 中的一种。
        lower_spec: 指定的下界，在条件列表无解时使用，默认为 0。
        upper_spec: 指定的上界，在条件列表无解时使用，默认为 1e9。

    Yields:
        生成器，产生满足所有条件的随机整数。
        如果条件列表无解，则 Yield None 一次，然后停止生成。
    """
    lower_bound = -(10**9)  # 初始下界设为负无穷大
    upper_bound = 10**9  # 初始上界设为正无穷大

    for condition_type, value in cond_list:
        if condition_type == ">":
            lower_bound = max(lower_bound, value + 1)
        elif condition_type == "<":
            upper_bound = min(upper_bound, value - 1)
        elif condition_type == ">=":
            lower_bound = max(lower_bound, value)
        elif condition_type == "<=":
            upper_bound = min(upper_bound, value)
        elif condition_type == "=":
            lower_bound = max(lower_bound, value)
            upper_bound = min(upper_bound, value)
        else:
            raise ValueError(f"未知的条件类型: {condition_type}")

        if lower_bound > upper_bound:
            print(
                "警告: 条件列表互相矛盾，无法找到满足所有条件的数字。将使用指定的上下界范围。"
            )  # 增加警告信息
            lower_bound = lower_spec  # 使用指定的上下界
            upper_bound = upper_spec
            if lower_bound > upper_bound:  # 再次检查指定上下界是否有效
                print("警告: 指定的上下界也无效。无法生成随机数。")
                yield None  # Yield None 表示无法生成
                return  # 提前结束生成器

    if lower_bound > upper_bound:  # 最终再次检查，虽然理论上在循环内已经检查过
        print(
            "最终检查：条件列表互相矛盾，无法找到满足所有条件的数字。"
        )  # 增加最终检查的警告
        yield None  # Yield None 表示无法生成
        return  # 提前结束生成器

    while True:
        yield random.randint(int(lower_bound), int(upper_bound))


def bound_pair_generator(input_int: int, bound_types: List[Literal[">=", "==", "<"]]):
    """
    生成一个生成器，输出两个 bound，输入的 int 满足该 bound。
    bound 的类型有 >=, ==, < 这三种。

    Args:
        input_int: 输入的整数，生成的 bound 需要满足这个整数。

    Yields:
        生成器，每次 yield 一对 Bound (Tuple[BoundType, int])，
        其中 BoundType 是 '>=', '==', '<' 中的一种，int 是 bound 的值。
    """

    def _generate_bound_value(input_int: int, bound_type) -> int:
        """
        根据 bound 类型生成合适的 bound 值，确保 input_int 满足该 bound。
        """
        if bound_type == ">=":
            # bound 值应该小于等于 input_int，这样 input_int 才能满足 >= bound_value
            return random.randint(
                0, input_int
            )  # 范围可以调整，这里使用 input_int - 5 到 input_int
        elif bound_type == "==":
            # bound 值必须等于 input_int
            return input_int
        elif bound_type == "<":
            # bound 值应该大于 input_int，这样 input_int 才能满足 < bound_value
            return random.randint(input_int + 1, input_int * 2)  # 范围可以调整
        else:
            raise ValueError(f"未知的 bound 类型: {bound_type}")

    while True:
        bound1_type = random.choice(bound_types)
        bound2_type = random.choice(bound_types)

        bound1_value = _generate_bound_value(input_int, bound1_type)
        bound2_value = _generate_bound_value(input_int, bound2_type)

        bound1 = (bound1_type, bound1_value)
        bound2 = (bound2_type, bound2_value)
        yield (bound1, bound2)


def to_odd(x: int) -> int:
    """
    将一个整数转换为奇数。
    """
    return x | 1


def to_even(x: int) -> int:
    """
    将一个整数转换为偶数。
    """
    return x & ~1
