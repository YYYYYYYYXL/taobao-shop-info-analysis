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
  name: 'BarLineChart',
  components: {
    BaseChart
  },
  props: {
    title: {
      type: String,
      default: '柱状图+折线图'
    },
    height: {
      type: Number,
      default: 300
    },
    data: {
      type: Array,
      required: true
    },
    barName: {
      type: String,
      default: '柱状图'
    },
    lineName: {
      type: String,
      default: '折线图'
    },
    theme: {
      type: String,
      default: 'default'
    },
    barColor: {
      type: String,
      default: '#409eff'
    },
    lineColor: {
      type: String,
      default: '#67c23a'
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
    barValues() {
      return this.data.map(item => item.value1)
    },
    lineValues() {
      return this.data.map(item => item.value2)
    },
    chartOptions() {
      return {
        tooltip: {
          trigger: 'axis',
          axisPointer: {
            type: 'cross',
            crossStyle: {
              color: '#999'
            }
          }
        },
        legend: {
          data: [this.yAxisName, this.yAxis2Name],
          top: '5%',
          textStyle: {
            fontSize: 12
          }
        },
        grid: {
          left: '5%',
          right: '10%',
          bottom: '1%',
          top: '13%',
          containLabel: true,
          show: false
        },
        xAxis: [
          {
            type: 'category',
            data: this.xAxisData,
            axisPointer: {
              type: 'shadow'
            },
            name: this.xAxisName,
            nameLocation: 'end',
            nameGap: 30
          }
        ],
        yAxis: [
          {
            type: 'value',
            name: this.yAxisName || this.barName,
            position: 'left',
            axisLine: {
              lineStyle: {
                color: '#999'
              }
            },
            axisTick: {
              lineStyle: {
                color: '#999'
              }
            },
            axisLabel: {
              formatter: '{value}'
            },
            nameLocation: 'end',
            nameGap: 10,
            splitLine: {
              show: false
            }
          },
          {
            type: 'value',
            name: this.yAxis2Name || this.lineName,
            position: 'right',
            max: 100,
            axisLine: {
              lineStyle: {
                color: '#999'
              }
            },
            axisTick: {
              lineStyle: {
                color: '#999'
              }
            },
            axisLabel: {
              formatter: '{value}'
            },
            splitLine: {
              show: false
            }
          }
        ],
        series: [
          {
            name: this.yAxisName,
            type: 'bar',
            data: this.barValues,
            itemStyle: {
              color: {
                type: 'linear',
                x: 0,
                y: 0,
                x2: 0,
                y2: 1,
                colorStops: [
                  {
                    offset: 0,
                    color: this.barColor
                  },
                  {
                    offset: 1,
                    color: this.barColor + '80'
                  }
                ]
              }
            },
            label: {
              show: true,
              position: 'top',
              color: '#333',
              fontSize: 12
            }
          },
          {
            name: this.yAxis2Name,
            type: 'line',
            yAxisIndex: 1,
            data: this.lineValues,
            smooth: true,
            lineStyle: {
              color: this.lineColor
            },
            itemStyle: {
              color: this.lineColor
            },
            label: {
              show: true,
              position: 'top',
              color: '#333',
              fontSize: 12
            }
          }
        ]
      }
    }
  }
}
</script>
