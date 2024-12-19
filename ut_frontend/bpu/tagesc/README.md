# TAGE-SC单元验证

## 测试目标

TAGE-SC是香山前端BPU中的一个子预测器，主要的功能是预测指令块中的条件分支指令是“跳转”还是“不跳转”，具体分为TAGE和SC两个子模块。

本单元测试的主要目标：

1. 确认相关逻辑是否正确实现，例如，检查 SC 的 `totalSum` 计算是否准确。
2. 在特定状态下，验证是否能够通过给定输入获得预期的输出结果。

测试基本流程：

1. 随机生成指令块PC和指令跳转情况
2. 把预测相关的信息输入DUT，得到预测结果
3. 再根据正确结果，把更新信息输入DUT
4. 根据测试目标判断DUT的端口/内部信号状态是否符合预期

本测试分为两类，一种是给予特定的输入后检查输出预期结果，另一种是随机测试，未来会接入参考模型进行比对[TBD]。

## 测试环境 

本测试环境对预测、更新和控制相关的行为进行了封装，即`TageSCEnv`类。

除了对DUT进行封装外，本测试环境还实现了工具和模拟外围设备的函数：

+ `TageSCFakeGlobalHistory`：维护分支历史并生成折叠历史
+ `MetaParser`：用于解析Meta信息。但不推荐使用，因为实现所用到的`SubDataRef`函数存在问题。

## 功能检测

> 约定说明：
> 1. `way`代表第`way`路
> 2. `ti`代表历史表序号
> 3. `PC`代表更新输入的预测块地址
> 4. `UpdateMeta`代表更新输入的Meta信息

| 序号 | 所述模块 | 功能描述   | 检查点描述                               | 检查标识                                              | 检查项                                                                                                                                                                                                                                                                                     |
|----|------|--------|-------------------------------------|-------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 1  | TAGE | TAGE预测 | 历史表Tn(1≤n≤4)提供主预测                   | Tn is provider                                              | `status.s2_valid(1) && s2_internal.provided(way) && s2_internal.provider(way) == ti`                                                                                                                                                                                                    |
| 2  | TAGE | TAGE预测 | 没有命中的历史表                            | All Tn Miss                                                 | status.s2_valid(1) && status.internal.s2.provided(way)                                                                                                                                                                                                                                  |
| 3  | TAGE | TAGE预测 | 多个历史表同时命中                           | Multi Tables Hit                                            | status.s2_valid(1) && status.internal.s2.provided(way) && status.internal.tage_table.hit_count(way) > 1                                                                                                                                                                                 |
| 4  | TAGE | TAGE预测 | 预测块中的所有分支指令由同一个历史表提供主预测             | All Slots use the Same Provider                             | status.s2_valid(1) && (status.internal.s2.provided(0) && status.internal.s2.provided(1))&& (status.internal.s2.provider(0) == status.internal.s2.provider(1))                                                                                                                           |
| 5  | TAGE | TAGE预测 | Tn(1 ≤ n ≤ 4) 提供弱预测，最终没有使用替代预测      | Tn is Unconfident Provider and NOT use_alt                  | status.s2_valid(1) && status.internal.s2.provided(way) && status.internal.s2.provider_weak(way) && status.internal.s2.provider(way) == ti && !status.internal.s2.alt_used(way)                                                                                                          |
| 6  | TAGE | TAGE预测 | Tn(1 ≤ n ≤ 4) 提供弱预测，最终使用替代预测        | Tn is Unconfident Provider and use_alt                      | status.s2_valid(1) && status.internal.s2.provided(way) && status.internal.s2.provider_weak(way) && status.internal.s2.provider(way) == ti && status.internal.s2.alt_used(way)                                                                                                           |
| 7  | TAGE | TAGE预测 | 多个历史表命中且主预测置信度低，最终没有使用替代预测          | Multiple Tables Hit&Provider is Unconf and NOT use _alt     | status.s2_valid(1) && status.internal.s2.provided(way) && status.internal.s2.provider_weak(way) && status.internal.tage_table.hit_count(way) > 1 && !status.internal.s2.alt_used(way)                                                                                                   |
| 8  | TAGE | TAGE预测 | 多个历史表命中且主预测置信度低，最终使用替代预测            | Multiple Tables Hit&Provider is Unconf and use _alt         | status.s2_valid(1) && status.internal.s2.provided(way) && status.internal.s2.provider_weak(way) && status.internal.tage_table.hit_count(way) > 1 && status.internal.s2.alt_used(way)                                                                                                    |
| 9  | TAGE | TAGE预测 | 预测块中的所有分支指令由同一个历史表提供弱预测，最终没有 使用替代预测 | All Slots Use the Same Unconfident Provider and NOT use_alt | status.s2_valid(1) && status.internal.s2.provided(0) && status.internal.s2.provided(1) &&  status.internal.s2.provided(1) && <br />!status.internal.s2.alt_used(0) && !status.internal.s2.alt_used(1) && (status.internal.s2.provider(0) == status.internal.s2.provider(1))             |
| 10 | TAGE | TAGE预测 | 预测块中的所有分支指令由同一个历史表提供弱预测，最终使用 替代预测   | All Slots Use the Same Unconfident Provider and  use_alt    | status.s2_valid(1) && status.internal.s2.provided(0) && status.internal.s2.provided(1) &&  status.internal.s2.provided(1) && <br />status.internal.s2.alt_used(0) && status.internal.s2.alt_used(1) && (status.internal.s2.provider(0) == status.internal.s2.provider(1))               |
| 11 | TAGE | TAGE训练 | T0下饱和更新                             | TO Down saturing                                            | status.pipline.s1_ready.value && status.internal.base_table.write_valid() && status.internal.base_table.write_mask(pc, way) &&  status.internal.base_table.old_ctr(way) == 0 && status.internal.base_table.new_ctr == 0 && status.internal.base_table.update_taken(pc, way)             |
| 12 | TAGE | TAGE训练 | T0上饱和更新                             | TO Up saturing                                              | status.pipline.s1_ready.value && status.internal.base_table.write_valid() && status.internal.base_table.write_mask(pc, way) &&  status.internal.base_table.old_ctr(way) == 3 && status.internal.base_table.new_ctr == 3 && status.internal.base_table.update_taken(pc, way)             |                                                                                                                                                                                                                                                                               |
| 13 | TAGE | TAGE训练 | Tn(1 ≤ n ≤ 4) 下饱和更新                 | Tn Down saturing                                            | status.pipline.s1_ready.value && status.internal.tage_table.has_silent(ti, way) && status.internal.tage_table.get_table(ti).update_mask(pc, way) && !status.internal.tage_table.get_table(ti).update_taken(pc, way)                                                                     |
| 14 | TAGE | TAGE训练 | Tn(1 ≤ n ≤ 4) 上饱和更新                 | Tn Up saturing                                              | status.pipline.s1_ready.value && status.internal.tage_table.has_silent(ti, way) && status.internal.tage_table.get_table(ti).update_mask(pc, way) && status.internal.tage_table.get_table(ti).update_taken(pc, way)                                                                      |
| 15 | TAGE | TAGE训练 | 历史表申请新表项成功                          | Tn Allocate Success                                         | status.internal.update.valid(way) && status.update.valid.value && status.pipline.s1_ready.value && status.internal.need_to_allocate(way) && sum(UpdateMeta.allocates) > 1                                                                                                               |
| 16 | TAGE | TAGE训练 | 历史表申请新表项失败                          | Tn Allocate Failure                                         | status.internal.update.valid(way) && status.update.valid.value && status.pipline.s1_ready.value && status.internal.need_to_allocate(way) && sum(UpdateMeta.allocates) == 0                                                                                                              |
| 17 | TAGE | TAGE训练 | 主预测错误，在更长历史表中申请新表项成功                | Tn Allocate As Provider MisPredict Success                  | status.pipline.s1_ready.value && status.update.valid.value && status.internal.update.provider_correct(way) && UpdateMeta.providers_valid(way)                                                                                                                                           |
| 18 | TAGE | TAGE训练 | 主预测错误，在更长历史表中申请新表项失败                | Tn Allocate As Provider MisPredict Failure                  | status.pipline.s1_ready.value && status.update.valid.value && !status.internal.update.provider_correct(way) && UpdateMeta.providers_valid(way)                                                                                                                                          |
| 18 | TAGE | TAGE训练 | useAltOnNaCtrs 寄存器组更新               | Update useAltOnNaCtrs                                       | status.internal.update.valid(way) && status.update.valid.value && UpdateMeta.providers_valid(way) && (UpdateMeta.basecnts(way) >= 0b10) != (UpdateMeta.providerResps_ctr(way) >= 0b100) && UpdateMeta.providerResps_ctr(way) in {0b100, 0b011}                                          |
| 19 | TAGE | TAGE训练 | 重置us计数器                             | Reset us                                                    | status.pipline.s1_ready.value && status.internal.bank_tick_ctr(way) == 0x7f && status.internal.update.reset_u(way)                                                                                                                                                                      |
| 20 | TAGE | TAGE训练 | 输入的训练信息中 always_taken 位为 1          | Always Taken is True                                        | status.pipline.s1_ready.value && status.update.bits.ftb_entry.always_taken(way) && status.update.valid.value                                                                                                                                                                            |
| 21 | TAGE | TAGG训练 | 训练与预测同时进行                           | Update When Predict                                         | status.internal.update.valid(way) && status.pipline.s0_fire_1.value                                                                                                                                                                                                                     |
| 22 | SC   | SC预测   | 预测时 TotalSum 计算正确                   | SC Predict Calculate TotalSum                               | status.s2_valid(3)                                                                                                                                                                                                                                                                      |
| 23 | SC   | SC预测   | 不使用 SC 的预测因为 TAGE 预测来自替代预测          | SC is Not Used and TAGE Use TO, Tn Miss                     | status.s2_valid(3) && !status.internal.s2.alt_used(way) && status.internal.s2.provided(way) && (status.internal.s2.total_sum(way, status.internal.s2.tage_taken(way)) > status.internal.s2.sc_threshold(way))                                                                           |
| 24 | SC   | SC预测   | 不使用 SC 的预测因为 TAGE 没有命中的历史表          | SC is Not Used and TAGE Use TO, Tn Hit                      | status.s2_valid(3) && !status.internal.s2.alt_used(way) && !status.internal.s2.provided(way) && (status.internal.s2.total_sum(way, status.internal.s2.tage_taken(way)) > status.internal.s2.sc_threshold(way))                                                                          |
| 25 | SC   | SC训练   | 训练时 TotalSum 计算正确                   | SC Train Calculate TotalSum                                 | status.pipline.s1_ready.value && status.internal.update.valid(way) && UpdateMeta.providers_valid(way)                                                                                                                                                                                   |
| 26 | SC   | SC训练   | Tn(1≤n≤4)上饱和更新                      | SC Table is Up Saturing                                     | status.pipline.s1_ready.value && status.internal.sc.get_table(ti).update_mask(pc, way) && status.internal.sc.get_table(ti).old_ctr(pc, way) == 31 && status.internal.sc.get_table(ti).update_taken(way)                                                                                 |
| 27 | SC   | SC训练   | Tn(1≤n≤4)下饱和更新                      | SC Table is Down Saturing                                   | status.pipline.s1_ready.value && status.internal.sc.get_table(ti).update_mask(pc, way) && status.internal.sc.get_table(ti).old_ctr(pc, way) == -32 && !status.internal.sc.get_table(ti).update_taken(way)                                                                               |
| 28 | SC   | SC训练   | SC Threshold 中的 ctr 训练后的值为最小值       | SC Threshold Counter is Down Saturing                       | status.pipline.s1_ready.value && status.update.valid.value && status.internal.update.valid(way) && (status.internal.sc_threshold(way) - 4 <= status.internal.above_threshold_total_sum(way) <= status.internal.sc_threshold(way) - 2) && status.internal.new_threshold_ctr(way) == 0    |
| 29 | SC   | SC训练   | SC Threshold 中的 ctr 训练后的值为最大值       | SC Threshold Counter is Up Saturing                         | status.pipline.s1_ready.value && status.update.valid.value && status.internal.update.valid(way) && (status.internal.sc_threshold(way) - 4 <= status.internal.above_threshold_total_sum(way) <= status.internal.sc_threshold(way) - 2) && status.internal.new_threshold_ctr(way) == 0x1f |
| 30 | SC   | SC训练   | SC Threshold 中的 thres 有限地下饱和更新      | SC Threshold Threshold is Down Saturing                     | status.pipline.s1_ready.value &&  status.internal.sc_threshold(way) == 4                                                                                                                                                                                                                |
| 31 | SC   | SC训练   | SC Threshold 中的 thres 有限地上饱和更新      | SC Threshold Threshold is Down Saturing                     | status.pipline.s1_ready.value &&  status.internal.sc_threshold(way) == 32                                                                                                                                                                                                               |


## 验证接口

### TrainAgent.exec_update

参数: 
1. pc: 预测块的地址
2. br_slot_valid: 条件分支指令槽中的指令是否有效
3. tail_slot_valid: 无条件跳转指令槽是否有效
4. tail_slot_sharing: 无条件跳转指令放的是否是条件分支指令
5. meta: Meta信息
6. fgh：全局分支历史
7. br_taken_mask_0：第一个指令(brSlot的)是否跳转
8. br_taken_mask_1：第二个指令(tailSlot的)是否跳转
9. mispred_mask_0: 第一个指令(brSlot的)的结果是否错误
10. mispred_mask_1: 第二个指令(tailSlot的)的结果是否错误
11. always_taken_0: 第一个指令(brSlot的)是否是强偏向性的
12. always_taken_1: 第二个指令(tailSlot的)是否是强偏向性的

## 用例说明[TBD]

#### Random Test

| 步骤 | 操作内容                            | 预期结果        | 功能覆盖点 |
|----|---------------------------------|-------------|-------|
| 1  | 创建 GlobalHistory 实例维护全局分支历史     |             |       |
| 2  | 随机生成预测块的 PC 和块中分支的跳转情况(块中分支均有效) |             |       |
| 3  | 输入 PC 和折叠历史                     | DUT根据输入进行预测 |       |
| 4  | 输入预测结果和分支的跳转情况;同时更新全局分支历史       | DUT根据输入进行训练 |       |
| 5  | 将2-5步重复2.5万次                    |             |       |

#### 饱和更新测试

该用例会触发计数器的饱和更新，验证计数器的饱和更新是否符合预期。

| 步骤 | 操作内容                                                                 | 预期结果                                  | 功能覆盖点 |
|----|----------------------------------------------------------------------|---------------------------------------|-------|
| 1  | 令预测块 PC=0x80000002                                                   |                                       |       |
| 2  | 构建Meta信息：2 条分支均有效且提供的ctr为0                                           |                                       |       |
| 3  | 对每个历史表依次执行:把 Meta 信息中提供主预测的历史表修 改为 Tn，在块中分支均有效、均预测错误且执行结果均为不跳转的情况下训练 | TAGE 中每个历史表均下饱和更新，更新后结果为最小值           |       |
| 4  | 修改刚刚的 Meta 信息:2 条分支的主预测提供的 ctr 均为 0b111                              |                                       |       |
| 5  | 对每个历史表依次执行:把 Meta 信息中提供主预测的历史表修 改为 Tn，在块中第二个分支有效、预测错误且执行结果为跳转的情况下训练  | TAGE 中每个历史表，对应第二个分支的表项上饱和更新，更新后结果为最大值 |       |
| 6  | 对每个历史表依次执行:把 Meta 信息中提供主预测的历史表修 改为 Tn，在块中第一个分支有效、预测错误且执行结果为跳转的情况下训练  | TAGE 中每个历史表，对应第一个分支的表项上饱和更新，更新后结果为最大值 |       |

#### 申请新表项一直失败测试

该用例会让 TAGE 历史表申请新表项多次失败，触发重置所有历史表的 us 计数器。

| 步骤 | 操作内容                                                     | 预期结果                          | 功能覆盖点 |
|----|----------------------------------------------------------|-------------------------------|-------|
| 1  | 令预测块 PC=0x80000002，全局分支历史为0x2                            |                               |       |
| 2  | 构建Meta信息：2 条分支均有效且表项读取结果为0                               |                               |       |
| 3  | 以“PC，刚刚修改的 Meta 信息，预测块中第二条指令有效、跳 转情况为跳转且预测错误”为输入，训练 33 次 | TAGE 中所有历史表重置对应第 二条分支的 us 计数器 |       |
| 4  | 以“PC，刚刚修改的 Meta 信息，预测块中第一条指令有效、跳 转情况为跳转且预测错误”为输入，训练 33 次 | TAGE 中所有历史表重置对应第 一条分支的 us 计数器 |       |


#### 替代预测一直预测成功/ 失败测试

该用例首先会不断输入替代预测一直成功的训练信息，之后再不断输入替代预测一直失败的训练信息，期间不断变化预测块的 PC，从而更新 useAltOnNaCtrs 寄存器中的所有计数器。

| 步骤 | 操作内容                                                                            | 预期结果                                   | 功能覆盖点 |
|----|---------------------------------------------------------------------------------|----------------------------------------|-------|
| 1  | 构造 Meta 信息:两条分支 T0 提供的 ctr 均为 0，预测结果均为跳转，主预测均提供有效的弱预测 3'b100，使用替代预测             |                                        |       |
| 2  | 执行循环 128 次，对于第 i 次循环:用“PC=i*2，块中分支均有效，1 中构造的 Meta 信息，分支均不跳转且分支均预测错误”为输入，训练 18 次 | useAltOnNaCtrs 中的所有计数器增加到最大值，且完成过上饱和更新 |       |
| 3  | 修改 Meta 信息:T0 的 ctr 均为 2'b10，主预测的 ctr 均为 3'b011                                 |                                        |       |
| 4  | 执行循环 128 次，对于第 i 次循环:用“PC=i*2，块中分支均有效，1 中构造的 Meta 信息，分支均不跳转且分支均预测错误”为输入，训练 18 次 | useAltOnNaCtrs 中的所有计数器增加到最大值，且完成过下饱和更新 |       |

#### always_taken置1测试

该用例会测试训练输入中指令的 always_taken 为 1 时，模块是否会将其对应表项的预测信息更新为跳转。

| 步骤 | 操作内容                                                             | 预期结果          | 功能覆盖点 |
|----|------------------------------------------------------------------|---------------|-------|
| 1  | 以“PC=0x800013，全局分支历史为 1，第二条分支有效、预测错误且 always_taken 位置 1”为输入，进行训练 |               |       |
| 2  | 以“PC=0x800013，全局分支历史为 1，第一条分支有效、预测错误且 always_taken 位置 1”为输入，进行训练 |               |       |
| 3  | 以“PC=0x800013，全局分支历史为 1”为输入，进行预测                                 | 块中两条分支的预测均为跳转 |       |


#### 预测和更新同时进行测试

该用例会在固定预测块 PC 的情况下，先进行一次预测得到结果 A，之后在同样的预测输入下让预测和更新同时进行，得到结果 B，最终判断 A 和 B 是否一致，从而验证预测和训练同时进行时，不会对预测产生干扰。

| 步骤 | 操作内容                                                                                               | 预期结果           | 功能覆盖点 |
|----|----------------------------------------------------------------------------------------------------|----------------|-------|
| 1  | 以“PC=0x800013，全局分支历史为 0”为输入，进行预测                                                                   | 得到预测结果，保存      |       |
| 2  | 以“PC=0x800013，全局分支历史为 0”为输入；同时，PC=0x114514、全局分支历史为 0、Meta 信息为先前预测的 Meta、预测块中分支均有效、均不跳转且均预测错误”为更新输入 | 预测结果与先前的预测结果相同 |       |

#### SC 历史表饱和更新测试

| 步骤 | 操作内容                                                                                                 | 预期结果                   | 功能覆盖点 |
|----|------------------------------------------------------------------------------------------------------|------------------------|-------|
| 1  | 构造 Meta 信息:两条分支的主预测有效且 ctr 为 3'b111，SC预测均为跳转，TAGE-SC 均使用 SC 的结果，TAGE 的预测均为不跳转，且 SC 中的历史表 ctr 均为 0x20 |                        |       |
| 2  | 以“构造的 Meta 信息，PC=0x1919810，块中分支均有效且预测错 误”做为输入，进行训练                                                   | 历史表所有分支的 ctr 下饱和更新     |       |
| 3  | 修改 Meta 信息:两条分支的主预测有效且 ctr 为 3'b110，SC 预测均为不跳转且 SC 中的历史表 ctr 均为  0x10                                |                        |       |
| 4  | 以“构造的 Meta 信息，PC=0x919810，块中第二条分支有效、预测错误且跳转情况为跳转”做为输入，进行训练                                           | 历史表对应第二条分支的 ctr 上饱 和更新 |       |
| 5  | 以“构造的 Meta 信息，PC=0x919810，块中第一条分支有效、预测错误且跳转情况为跳转”做为输入，进行训练                                           | 历史表对应第一条分支的 ctr 上饱 和更新 |       |


#### SCThreshold 饱和更新测试

SCThreshold 包含两个计数器:ctr 和 thres。该用例会让 ctr 和 thres 不断更新。

| 步骤 | 操作内容                                                                                           | 预期结果                                                                                         | 功能覆盖点 |
|----|------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------|-------|
| 1  | 构造Meta信息:两条分支的主预测均有效且ctr均为 3'b0，TAGE 预测结果均为不跳转，两条分支的 SC 预测均为跳转、均使用 SC 的预测、SC的ctr结果均为9, 9, 9, i |                                                                                              |       |
| 2  | 让 i 从 0 开始依次增加 1，执行 13 次:以“PC=0x80000004，构造的 Meta 信息，块中分支均有效、均不跳转、均预测错误”为输入，进行 15 次训练          | SCThreshold 中的 ctr 不断增加， 当更新后的值达到最大值时恢 复到 6’b100000;SCThreshold 中的 thres 不断增加，进行有限的上饱和更新     |       |
| 3  | 修改 Meta 信息:两条分支的 SC 预测均为不跳转、均使用 SC 的预测、TAGE 预测结果均为跳转、SC的 ctr 均为 31-i, 0, 0, 10                 |                                                                                              |       |
| 4  | 让 i 从 0 开始依次增加 1，执行 14 次:以“PC=0x80000004，构造的 Meta 信息，块中分支均有效、均不跳转、均预测错误”为输入，进行 16 次训练          | SCThreshold 中的 ctr 不断减少， 当更新后的值达到最小值时随后 恢复到 6’b100000;SCThreshold 中 的 thres 不断减少，进行有限的 下饱和更新 |       |


#### TotalSum 计算正确测试

该用例会检查 SC 在预测和训练过程中 TotalSum 计算是否正确。

| 步骤 | 操作内容                                                                                                 | 预期结果                                                   | 功能覆盖点 |
|----|------------------------------------------------------------------------------------------------------|--------------------------------------------------------|-------|
| 1  | 以“PC = 0x80000000，全局分支历史为 2，Meta 中每路 scCtrs 之和为 19、TAGE 预测结果有效且 ctr=5”作为训练输入，update_valid 拉高后的一个周期检测 | SC 训练时的 TotalSum 符合公式 `TotalSum = ScCtrSum + tagePvdr` |       |
| 2  | 以“PC = 0x80000000，全局分支历史为 2”作为预测输入，在开始预测后的一个周期检测                                                     | SC 预测时的 TotalSum 符合公式 `TotalSum = ScCtrSum + tagePvdr` |       |


## 目录结构

```
tagesc
├── agent # DUT操作封装
│   ├── ctrl_agent.py
│   ├── __init__.py
│   ├── predict_agent.py
│   └── train_agent.py
├── bundle # 引脚相关
│   ├── __init__.py
│   ├── internal.py
│   └── port.py
├── env # 封装的测试环境
│   ├── fake_global_history.py 
│   ├── __init__.py
│   └── tage_sc_env.py
├── __init__.py
├── internal.yaml
├── README.md
├── test # 功能点和testcase
│   ├── checkpoints_sc_predict.py
│   ├── checkpoints_sc_train.py
│   ├── checkpoints_tage_predict.py
│   ├── checkpoints_tage_train.py
│   ├── __init__.py
│   ├── test_random.py
│   └── test_spec_case.py
└── util
    ├── __init__.py
    └── meta_parser.py
```



## 检测列表


- [ ] 本文档符合指定[模板]()要求
- [ ] Env提供的API不包含任何DUT引脚和时序信息
- [ ] Env的API保持稳定（共有[ X ]个）
- [ ] Env中对所支持的RTL版本（支持版本[ X ]）进行了检查
- [ ] 功能点（共有[ X ]个）与[设计文档]()一致
- [ ] 检查点（共有[ X ]个）覆盖所有功能点
- [ ] 检查点的输入不依赖任何DUT引脚，仅依赖Env的标准API
- [ ] 所有测试用例（共有[ X ]个）都对功能检查点进行了反标
- [ ] 所有测试用例都是通过 assert 进行的结果判断
- [x] 所有DUT或对应wrapper都是通过fixture创建
- [x] 在上述fixture中对RTL版本进行了检查
- [x] 创建DUT或对应wrapper的fixture进行了功能和代码行覆盖率统计
- [ ] 设置代码行覆盖率时对过滤需求进行了检查

## TODO

+ 重命名检查表示
+ 完善用例说明的功能覆盖点部分
+ 适配新的RTL
+ 接入参考模型