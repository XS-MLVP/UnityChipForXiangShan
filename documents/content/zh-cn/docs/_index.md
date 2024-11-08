---
title: 进度概述
linkTitle: 进度概述
#menu: {main: {weight: 20}}
weight: 10
---

<script src="../js/echarts.min.js"></script>
<script src="../js/chart_meta.js"></script>
<script>
function update_charts(data_url){
    show_meta_chart("meta_chart", data_url)
    updateDUTestStatus(data_url)
}
</script>

<div id="meta_chart" style="width: 100%;height:400px;"></div>
<div style="text-align: center; width: 100%;">
{{<list-report  baseurl="../data/reports" label="当前版本：" detail="查看测试报告" id="index" onchange="update_charts">}}
</div>
<br>


香山昆明湖架构各个模块验证情况如上图中所示。总统计数据如下：
<table>
    <ol>
    <tr>
        <td>总测试用例数（Total Cases）：</td>
        <td  style="text-align: left; font-weight: bold;"><em id="em_id_report_cases_toal">-</em></td>
        <td>测试用例通过数（Passed Cases）：</td>
        <td  style="text-align: left; font-weight: bold;"><em id="em_id_report_cases_pass">-</em></td>
        <td>测试用例通过率（Passed Rate）：</td>
        <td  style="text-align: left; font-weight: bold;"><em id="em_id_report_cases_prate">-</em></td>
    </tr>
    <tr>
        <td>测试用例未过数（Failed Cases）：</td>
        <td  style="text-align: left; font-weight: bold;"><em id="em_id_report_cases_fail">-</em></td>
        <td>测试用例跳过数（Skipped Cases）：</td>
        <td  style="text-align: left; font-weight: bold;"><em id="em_id_report_cases_skip">-</em></td>
        <td>测试用例调过率（Skip Rate）：</td>
        <td  style="text-align: left; font-weight: bold;"><em id="em_id_report_cases_srate">-</em></td>
    </tr>
    <tr>
        <td>总功能覆盖点数（Function Coverage）：</td>
        <td  style="text-align: left; font-weight: bold;"><em id="em_id_report_function_total">-</em></td>
        <td>覆盖点已覆盖数（Covered Functions）：</td>
        <td  style="text-align: left; font-weight: bold;"><em id="em_id_report_function_cover">-</em></td>
        <td>覆盖点已覆盖率（Covered Rate）：</td>
        <td  style="text-align: left; font-weight: bold;"><em id="em_id_report_function_rate">-</em></td>
    </tr>
    <tr>
        <td>总代码行覆盖率（Total Lines）：</td>
        <td  style="text-align: left; font-weight: bold;"><em id="em_id_report_line_total">-</em></td>
        <td>总代码行覆盖数（Covered Lines）：</td>
        <td  style="text-align: left; font-weight: bold;"><em id="em_id_report_line_cover">-</em></td>
        <td>总代码行覆盖率（Covered Rate）：</td>
        <td  style="text-align: left; font-weight: bold;"><em id="em_id_report_line_rate">-</em></td>
    </tr>
    </ol>
</table>

*总代码行会随着DUT的增加而不断增加，因此：总代码行覆盖率不是最终覆盖率


其他内容快捷连接：

- **[DUT文档与功能](https://open-verify.cc/UnityChipForXiangShan/)**
- **[待确认bug列表](https://github.com/XS-MLVP/UnityChipForXiangShan/labels/bugc)**
- **[已发现bug列表](https://github.com/XS-MLVP/UnityChipForXiangShan/labels/bug)**
- **[已修复bug列表](https://github.com/XS-MLVP/UnityChipForXiangShan/labels/bugfixed)**
- **[正在进行的任务列表](https://github.com/XS-MLVP/UnityChipForXiangShan/labels/task)**
- **[已完成的任务列表](https://github.com/XS-MLVP/UnityChipForXiangShan/labels/taskdone)**

<br>
<div style="text-align: center; width: 100%;">
<h4>香山昆明湖DUT验证进展</h4>
</div>
<br>

{{<list-dut-test-status>}}

<div style="text-align: center; width: 100%;">
<br>
注：本项目中的统计信息根据commit等数据自动更新，参与者可以提交issue（写明任务内容，预计完成时间等）同步正在进行的任务。<br>
数据自动更新日期：<em id="em_id_report_date">1970-01-01 00:00:00</em>
</div>
