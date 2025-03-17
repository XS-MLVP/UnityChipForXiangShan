---
title: 维护者
linkTitle: 维护者
#menu: {main: {weight: 99}}
weight: 99
---


在提交 issue、pull request、discussion 时，如果指定对应模块的 maintainer 能更及时的得到响应。目前已有的维护人员如下（首字母排名）：

**验证工具：**
- picker：[Makiras](https://github.com/Makiras), [SFangYy](https://github.com/SFangYy), [yaozhicheng](https://github.com/yaozhicheng)
- toffee/toffe-test：[Miical](https://github.com/Miical), [yaozhicheng](https://github.com/yaozhicheng)

<!-- <script src="../../js/echarts.min.js"></script> -->

<script>
function update_maintainers(data_url){
    updateMaintainers(data_url)
}
</script>

<div style="text-align: center; width: 100%;">
{{<list-report  baseurl="../../data/reports" label="当前版本：" id="maintainers" onchange="update_maintainers">}}
</div>
<br>

{{<maintainers>}}

*其他维护者陆续更新中

如果您对本项目感兴趣，欢迎申请成为本项目中的维护者。
