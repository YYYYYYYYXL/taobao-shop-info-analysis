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
  name: 'GaugeChart',
  components: {
    BaseChart
  },
  props: {
    title: {
      type: String,
      default: '仪表盘'
    },
    height: {
      type: Number,
      default: 300
    },
    value: {
      type: Number,
      default: 0
    },
    max: {
      type: Number,
      default: 100
    },
    theme: {
      type: String,
      default: 'default'
    },
    color: {
      type: String,
      default: '#409eff'
    }
  },
  computed: {
    chartOptions() {
      return {
        series: [
          {
            name: this.title,
            type: 'gauge',
            progress: {
              show: true
            },
            detail: {
              valueAnimation: true,
              formatter: '{value}%'
            },
            data: [
              {
                value: this.value,
                name: this.title
              }
            ],
            axisLine: {
              lineStyle: {
                width: 20,
                color: [
                  [0.3, '#67c23a'],
                  [0.7, '#e6a23c'],
                  [1, '#f56c6c']
                ]
              }
            },
            pointer: {
              itemStyle: {
                color: 'auto'
              }
            },
            axisTick: {
              distance: -30,
              splitNumber: 5,
              lineStyle: {
                width: 2,
                color: '#999'
              }
            },
            splitLine: {
              distance: -30,
              length: 30,
              lineStyle: {
                width: 4,
                color: '#999'
              }
            },
            axisLabel: {
              color: 'auto',
              distance: 40,
              fontSize: 12
            }
          }
        ]
      }
    }
  }
}
</script>
