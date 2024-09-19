
// UTs Meta Chart
function show_meta_chart(chart_id, data_url){
  var chartDom = document.getElementById(chart_id);
  var utChart = echarts.init(chartDom);
  var option;

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
        data: ['BPU', 'ICache', 'Decoder', 'ITLB', 'ROB', 'CSR', 'IFU']
      }
    ],
    yAxis: [
      {
        type: 'value'
      }
    ],
    series: [
      {
        name: 'Funtions',
        type: 'bar',
        emphasis: {
          focus: 'series'
        },
        data: [320, 332, 301, 334, 390, 330, 320]
      },
      {
        name: 'Cover Points',
        type: 'bar',
        stack: 'Ad',
        emphasis: {
          focus: 'series'
        },
        data: [120, 132, 101, 134, 90, 230, 210]
      },
      {
        name: 'Line Coverage',
        type: 'bar',
        stack: 'Ad',
        emphasis: {
          focus: 'series'
        },
        data: [220, 182, 191, 234, 290, 330, 310]
      },
      {
        name: 'Test Cases',
        type: 'bar',
        stack: 'Ad',
        emphasis: {
          focus: 'series'
        },
        data: [150, 232, 201, 154, 190, 330, 410]
      },
      {
        name: 'Total Bugs',
        type: 'bar',
        data: [862, 1018, 964, 1026, 1679, 1600, 1570],
        emphasis: {
          focus: 'series'
        },
        //markLine: {
        //  lineStyle: {
        //    type: 'dashed'
        // },
        //  data: [[{ type: 'min' }, { type: 'max' }]]
        //}
      },
      {
        name: 'Bugs of Functions',
        type: 'bar',
        barWidth: 5,
        stack: 'Total Bugs',
        emphasis: {
          focus: 'series'
        },
        data: [620, 732, 701, 734, 1090, 1130, 1120]
      },
      {
        name: 'Bugs of Performance',
        type: 'bar',
        stack: 'Total Bugs',
        emphasis: {
          focus: 'series'
        },
        data: [120, 132, 101, 134, 290, 230, 220]
      },
      {
        name: 'Bugs of Typos',
        type: 'bar',
        stack: 'Total Bugs',
        emphasis: {
          focus: 'series'
        },
        data: [60, 72, 71, 74, 190, 130, 110]
      },
      {
        name: 'Others Bugs',
        type: 'bar',
        stack: 'Total Bugs',
        emphasis: {
          focus: 'series'
        },
        data: [62, 82, 91, 84, 109, 110, 120]
      }
    ]
  };
  
  option && utChart.setOption(option);
  window.addEventListener('resize', function () {utChart.resize();});
}
