
// UTs Progress Chart
function show_progress_chart(chart_id, data_url){
  var chartDom = document.getElementById(chart_id);
  var utChart = echarts.init(chartDom);
  var option;
  utChart.showLoading();
  $.getJSON(data_url, function (graph) {
    utChart.hideLoading();
    option = {
      tooltip: {},
      legend: [
        {
          data: graph.categories.map(function (a) {
            return a.name;
          })
        }
      ],
      series: [
        {
          name: 'XiangShan UTs',
          type: 'graph',
          layout: 'force',
          data: graph.nodes,
          links: graph.links,
          categories: graph.categories,
          roam: true,
          force: {
            repulsion: 300
          },
          label: {
            show: true,
            position: 'right',
            formatter: '{b}'
          },
          labelLayout: {
            hideOverlap: true
          },
          scaleLimit: {
            min: 0.4,
            max: 2
          },
          lineStyle: {
            color: 'source',
            curveness: 0.3
          }
        }
      ]
    };
    utChart.setOption(option);
    window.addEventListener('resize', function () {
      utChart.resize();
  });
  });
  option && utChart.setOption(option);
}
