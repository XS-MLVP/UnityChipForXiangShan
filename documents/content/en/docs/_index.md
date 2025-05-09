---
title: Progress Overview
linkTitle: Progress Overview
#menu: {main: {weight: 20}}
weight: 10
---

<script src="../../js/echarts.min.js"></script>
<script src="../../js/chart_meta.js"></script>
<script>
function update_charts(data_url){
    show_meta_chart("meta_chart", data_url)
    updateDUTestStatus(data_url)
}
</script>

This project aims to perform unit testing (Unit Test, UT) verification of the [XiangShan Processor](https://github.com/OpenXiangShan/XiangShan) Kunming Lake architecture through open-source crowdsourcing. The chart below shows the verification status of each module in the XiangShan Kunming Lake architecture.

<div id="meta_chart" style="width: 100%;height:400px;"></div>
<div style="text-align: center; width: 100%;">
{{<list-report  baseurl="../../data/reports" label="Current Version:" detail="View Test Report" id="index" onchange="update_charts">}}
</div>
<br>

Overall statistics are as follows:

<table>
    <ol>
    <tr>
        <td>Total Cases:</td>
        <td  style="text-align: left; font-weight: bold;"><em id="em_id_report_cases_toal">-</em></td>
        <td>Passed Cases:</td>
        <td  style="text-align: left; font-weight: bold;"><em id="em_id_report_cases_pass">-</em></td>
        <td>Passed Rate:</td>
        <td  style="text-align: left; font-weight: bold;"><em id="em_id_report_cases_prate">-</em></td>
    </tr>
    <tr>
        <td>Failed Cases:</td>
        <td  style="text-align: left; font-weight: bold;"><em id="em_id_report_cases_fail">-</em></td>
        <td>Skipped Cases:</td>
        <td  style="text-align: left; font-weight: bold;"><em id="em_id_report_cases_skip">-</em></td>
        <td>Skip Rate:</td>
        <td  style="text-align: left; font-weight: bold;"><em id="em_id_report_cases_srate">-</em></td>
    </tr>
    <tr>
        <td>Function Coverage:</td>
        <td  style="text-align: left; font-weight: bold;"><em id="em_id_report_function_total">-</em></td>
        <td>Covered Functions:</td>
        <td  style="text-align: left; font-weight: bold;"><em id="em_id_report_function_cover">-</em></td>
        <td>Covered Rate:</td>
        <td  style="text-align: left; font-weight: bold;"><em id="em_id_report_function_rate">-</em></td>
    </tr>
    <tr>
        <td>Total Lines:</td>
        <td  style="text-align: left; font-weight: bold;"><em id="em_id_report_line_total">-</em></td>
        <td>Covered Lines:</td>
        <td  style="text-align: left; font-weight: bold;"><em id="em_id_report_line_cover">-</em></td>
        <td>Covered Rate:</td>
        <td  style="text-align: left; font-weight: bold;"><em id="em_id_report_line_rate">-</em></td>
    </tr>
    </ol>
</table>

*The total number of lines will continue to increase as DUTs are added, so: the total line coverage is not the final coverage.

Other quick links:

- **[DUT Documentation & Functions](https://open-verify.cc/UnityChipForXiangShan/docs/98_ut/)**
- **[Pending Bug List](https://github.com/XS-MLVP/UnityChipForXiangShan/labels/bug%20need%20to%20confirm)**
- **[Confirmed Bug List](https://github.com/XS-MLVP/UnityChipForXiangShan/labels/bug%20confirmed)**
- **[Fixed Bug List](https://github.com/XS-MLVP/UnityChipForXiangShan/labels/bug%20fixed)**
- **[Ongoing Task List](https://open-verify.cc/crowdsourcing/kunming_lake)**
- **[Completed Task List](https://open-verify.cc/crowdsourcing/kunming_lake)**

<br>
<div style="text-align: center; width: 100%;">
<h4 id="testmap">XiangShan Kunming Lake DUT Verification Progress</h4>
</div>
<br>

{{<list-dut-test-status>}}

<div style="text-align: center; width: 100%;">
<br>
Note: The statistics in this document are automatically generated based on test results.<br>
Data auto-update date: <em id="em_id_report_date">1970-01-01 00:00:00</em>
</div>
