---
title: 模板-UT-README
linkTitle: 模板-UT-README
#menu: {main: {weight: 20}}
weight: 21
---

```markdown
# 模块名称

## 测试目标

<测试目标、测试方法描述>


## 测试环境

<测试环境描述，依赖描述>

## 功能检测

<给出目标待测功能与对应的检测方法>

|序号|所属模块|功能描述|检查点描述|检查标识|检查项|
|-|-|-|-|-|-|
|-|-|-|-|-|-|


## 验证接口

<接口的描述>


## 用例说明

#### 测试用例1

|步骤|操作内容|预期结果|覆盖功能点|
|-|-|-|-|
|-|-|-|-|

#### 测试用例2

|步骤|操作内容|预期结果|覆盖功能点|
|-|-|-|-|
|-|-|-|-|


## 目录结构

<对本模块的目录结构进行描述>


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
- [ ] 所有DUT或对应wrapper都是通过fixture创建
- [ ] 在上述fixture中对RTL版本进行了检查
- [ ] 创建DUT或对应wrapper的fixture进行了功能和代码行覆盖率统计
- [ ] 设置代码行覆盖率时对过滤需求进行了检查
```

展示效果如下：

# 模块名称

## 测试目标

<测试目标、测试方法描述>


## 测试环境

<测试环境描述，依赖描述>

## 功能检测

<给出目标待测功能与对应的检测方法>

|序号|所属模块|功能描述|检查点描述|检查标识|检查项|
|-|-|-|-|-|-|
|-|-|-|-|-|-|


## 验证接口

<接口的描述>


## 用例说明

#### 测试用例1

|步骤|操作内容|预期结果|覆盖功能点|
|-|-|-|-|
|-|-|-|-|

#### 测试用例2

|步骤|操作内容|预期结果|覆盖功能点|
|-|-|-|-|
|-|-|-|-|


## 目录结构

<对本模块的目录结构进行描述>


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
- [ ] 所有DUT或对应wrapper都是通过fixture创建
- [ ] 在上述fixture中对RTL版本进行了检查
- [ ] 创建DUT或对应wrapper的fixture进行了功能和代码行覆盖率统计
- [ ] 设置代码行覆盖率时对过滤需求进行了检查