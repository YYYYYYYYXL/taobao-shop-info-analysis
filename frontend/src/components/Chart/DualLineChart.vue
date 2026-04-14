<template>
  <BaseChart
    :title="title"
    :height="height"
    :options="chartOptions"
    :theme="theme"
  />
</template>

<script>
import BaseChart from './BaseChart.vue'

export default {
  name: 'DualLineChart',
  components: {
    BaseChart
  },
  props: {
    data: {
      type: Array,
      default: () => []
    },
    title: {
      type: String,
      default: '双折线图'
    },
    height: {
      type: Number,
      default: 300
    },
    theme: {
      type: String,
      default: 'default'
    },
    series1Color: {
      type: String,
      default: '#5470c6'
    },
    series2Color: {
      type: String,
      default: '#91cc75'
    },
    xAxisName: {
      type: String,
      default: ''
    },
    yAxisName: {
      type: String,
      default: ''
    },
    yAxis2Name: {
      type: String,
      default: ''
    }
  },
  computed: {
    xAxisData() {
      return this.data.map(item => item.name)
    },
    series1Values() {
      return this.data.map(item => item.value1)
    },
    series2Values() {
      return this.data.map(item => item.value2)
    },
    chartOptions() {
      return {
        tooltip: {
          trigger: 'axis',
          axisPointer: {
            type: 'cross'
          },
          formatter: function(params) {
            let result = params[0].name + '<br/>'
            params.forEach(param => {
              result += param.marker + param.seriesName + ': ' + param.value + '<br/>'
            })
            return result
          }
        },
        legend: {
          data: [this.yAxisName || '数据1', this.yAxis2Name || '数据2'],
          top: '5%'
        },
        grid: {
          left: '5%',
          right: '10%',
          bottom: '1%',
          top: '10%',
          containLabel: true,
          show: false
        },
        xAxis: {
          type: 'category',
          data: this.xAxisData,
          axisTick: {
            alignWithLabel: true
          },
          name: this.xAxisName,
          nameLocation: 'end',
          nameGap: 10,
        },
        yAxis: {
          type: 'value',
          nameLocation: 'end',
          nameGap: 10,
          axisLabel: {
            formatter: function(value) {
              if (value >= 1000) {
                return (value / 1000).toFixed(1) + 'k'
              }
              return value.toLocaleString()
            }
          },
          splitLine: {
            show: true,
            lineStyle: {
              color: '#f3f4f6',
              type: 'dashed'
            }
          }
        },
        series: [
          {
            name: this.yAxisName || '数据1',
            type: 'line',
            data: this.series1Values,
            smooth: true,
            symbol: 'circle',
            symbolSize: 6,
            itemStyle: {
              color: this.series1Color
            },
            label: {
              show: true,
              position: 'top',
              color: '#333',
              fontSize: 12
            },
            areaStyle: {
              color: {
                type: 'linear',
                x: 0,
                y: 0,
                x2: 0,
                y2: 1,
                colorStops: [
                  {
                    offset: 0,
                    color: this.series1Color
                  },
                  {
                    offset: 1,
                    color: this.series1Color + '10'
                  }
                ]
              }
            }
          },
          {
            name: this.yAxis2Name || '数据2',
            type: 'line',
            data: this.series2Values,
            smooth: true,
            symbol: 'circle',
            symbolSize: 6,
            itemStyle: {
              color: this.series2Color
            },
            label: {
              show: true,
              position: 'top',
              color: '#333',
              fontSize: 12
            },
            areaStyle: {
              color: {
                type: 'linear',
                x: 0,
                y: 0,
                x2: 0,
                y2: 1,
                colorStops: [
                  {
                    offset: 0,
                    color: this.series2Color
                  },
                  {
                    offset: 1,
                    color: this.series2Color + '10'
                  }
                ]
              }
            }
          }
        ]
      }
    }
  }
}
</script>
