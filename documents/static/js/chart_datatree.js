
// UTs datatree chart
function show_datatree_chart(chart_id, data_url) {
  var chartDom = document.getElementById(chart_id);
  var utChart = echarts.init(chartDom);
  var option;
  utChart.showLoading();
  $.getJSON(data_url, function (graph_data) {
    utChart.hideLoading();
    const formatUtil = echarts.format;
    function getLevelOption() {
      return [
        {
          itemStyle: {
            borderColor: '#777',
            borderWidth: 0,
            gapWidth: 1
          },
          upperLabel: {
            show: false
          }
        },
        {
          itemStyle: {
            borderColor: '#555',
            borderWidth: 5,
            gapWidth: 1
          },
          emphasis: {
            itemStyle: {
              borderColor: '#ddd'
            }
          }
        },
        {
          colorSaturation: [0.35, 0.5],
          itemStyle: {
            borderWidth: 5,
            gapWidth: 1,
            borderColorSaturation: 0.6
          }
        }
      ];
    }
    option = {
      title: {
        text: 'XiangShan-KMH Unit Verifaction Flatten Map',
        left: 'center'
      },
      tooltip: {
        formatter: function (info) {
          var meta = info.data.meta;
          var treePathInfo = info.treePathInfo;
          var treePath = [];
          for (var i = 1; i < treePathInfo.length; i++) {
            treePath.push(treePathInfo[i].name);
          }
          return [
            '<div class="tooltip-title">' +
            formatUtil.encodeHTML(treePath.join('/')) +
            '</div>',
            'Test Cases: ' + formatUtil.addCommas(meta.cases.pass) + '/' +
            formatUtil.addCommas(meta.cases.total) + '&nbsp(' +
            formatUtil.addCommas(meta.cases.skip)  + '&nbsp;skiped,&nbsp;&nbsp;' +
            formatUtil.addCommas(meta.cases.fail)  + '&nbsp;fail ) <br>',
            'Line coverage: ' + formatUtil.addCommas(meta.cases.pass) + '<br>',
            'Func coverage: ' + formatUtil.addCommas(meta.cases.pass) + '<br>',
          ].join('');
        }
      },
      series: [
        {
          name: graph_data["tree"]["name"],
          type: 'treemap', // sunburst treemap
          visibleMin: 300,
          label: {
            show: true,
            position: 'insideTopLeft',
            formatter: function (params) { //formatter: '{b}'
              if (params.data.children) {
                return params.name;
              }
              let arr = [
                '{name|' + params.name + '}'
              ]
              if (params.data.meta.cases.fail > 0) {
                arr.push(
                  '{fail|' + echarts.format.addCommas(params.data.meta.cases.fail) + '} {label|fail}'
                );
              }
              if (params.data.meta.cases.pass > 0) {
                let font_type = "pass";
                if (params.data.meta.cases.pass >= params.data.meta.cases.total) {
                  font_type = "complete";
                }
                arr.push(
                  '{'+ font_type + '|' + echarts.format.addCommas(params.data.meta.cases.pass) + '/'+
                             echarts.format.addCommas(params.data.meta.cases.total) + '} {label|pass}'
                )
              }
              return arr.join('\n');
            },
            rich: {
              fail: {
                fontSize: 22,
                lineHeight: 30,
                color: 'yellow'
              },
              complete: {
                fontSize: 15,
                color: 'green',
              },
              label: {
                fontSize: 9,
                backgroundColor: 'rgba(0,0,0,0.3)',
                color: '#fff',
                borderRadius: 2,
                padding: [2, 4],
                lineHeight: 25,
                align: 'right'
              },
              name: {
                fontSize: 12,
                color: '#fff'
              }
            }
          },
          upperLabel: {
            show: true,
            height: 30
          },
          itemStyle: {
            borderColor: '#fff'
          },
          levels: getLevelOption(),
          data: graph_data["tree"]["children"],
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


document.addEventListener('DOMContentLoaded', function() {
  show_datatree_chart("datatree_chart", "../../data/ut_data_progress.json");
});
