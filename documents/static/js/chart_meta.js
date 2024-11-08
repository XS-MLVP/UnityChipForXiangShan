
function setEmRate(item, b, a, config){
  if (a == 0) {
    $(item).removeClass();
    $(item).text("0");
    return;
  }
  var rate = (b / a * 100).toFixed(2);
  if(rate < config.rate_low){
    $(item).css("color", "red");
  }else if(rate < config.rate_middle){
    $(item).css("color", "orange");
  }else if(rate > config.rate_high){
    $(item).css("color", "green");
  }
  $(item).text(rate + " %");
}


// UTs Meta Chart
function show_meta_chart(chart_id, data_url) {
  var utChart = echarts.init(document.getElementById(chart_id), null, { renderer: 'canvas' });
  var option;
  utChart.showLoading();
  $.getJSON(data_url, function (graph_data) {
    utChart.hideLoading();
    option = {
      tooltip: {
        trigger: 'axis',
        axisPointer: {
          type: 'shadow'
        }
      },
      legend: {},
      grid: {
        left: '3%',
        right: '4%',
        bottom: '3%',
        containLabel: true
      },
      xAxis: [
        {
          type: 'category',
          data: graph_data["list"]["names"],
          axisLabel: {
            rotate: 90,
            verticalAlign: 'middle',
            align: 'right',
            fontSize: 18,
            color: '#0000ff',
            formatter: function (value, index) {
              return value + '. ' + (index + 1);
            }
          }
        }
      ],
      yAxis: [
        {
          type: 'value'
        }
      ],
      series: graph_data["list"]["series"]
    };

    option && utChart.setOption(option);
    window.addEventListener('resize', function () { utChart.resize(); });

    // set em data
    $("#em_id_report_cases_toal").text(graph_data["tree"]["meta"]["cases"]["total"]);
    $("#em_id_report_cases_pass").text(graph_data["tree"]["meta"]["cases"]["pass"]);
    $("#em_id_report_cases_fail").text(graph_data["tree"]["meta"]["cases"]["fail"]);
    $("#em_id_report_cases_skip").text(graph_data["tree"]["meta"]["cases"]["skip"]);
    $("#em_id_report_function_total").text(graph_data["tree"]["meta"]["functions"]["total"]);
    $("#em_id_report_function_cover").text(graph_data["tree"]["meta"]["functions"]["cover"]);
    $("#em_id_report_line_total").text(graph_data["tree"]["meta"]["lines"]["total"]);
    $("#em_id_report_line_cover").text(graph_data["tree"]["meta"]["lines"]["cover"]);
    $("#em_id_report_date").text(graph_data["extend"]["time"]);
    // calc rate
    setEmRate($("#em_id_report_cases_prate"),
      graph_data["tree"]["meta"]["cases"]["pass"], graph_data["tree"]["meta"]["cases"]["total"], graph_data["config"]);
    setEmRate($("#em_id_report_cases_srate"),
      graph_data["tree"]["meta"]["cases"]["skip"], graph_data["tree"]["meta"]["cases"]["total"], graph_data["config"]);
    setEmRate($("#em_id_report_function_rate"),
      graph_data["tree"]["meta"]["functions"]["cover"], graph_data["tree"]["meta"]["functions"]["total"], graph_data["config"]);
    setEmRate($("#em_id_report_line_rate"),
      graph_data["tree"]["meta"]["lines"]["cover"], graph_data["tree"]["meta"]["lines"]["total"], graph_data["config"]);
  });
}
