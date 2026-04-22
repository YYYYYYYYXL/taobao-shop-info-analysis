<template>
  <BaseChart
    :title="title"
    :height="height"
    :options="chartOptions"
    :theme="theme"
    @chart-click="handleChartClick"
  />
</template>

<script>
import BaseChart from './BaseChart.vue'

export default {
  name: 'HorizontalBarChart',
  components: {
    BaseChart
  },
  props: {
    title: {
      type: String,
      default: '条形图'
    },
    height: {
      type: Number,
      default: 300
    },
    data: {
      type: Array,
      required: true
    },
    theme: {
      type: String,
      default: 'default'
    },
    color: {
      type: String,
      default: '#409eff'
    },
    xAxisName: {
      type: String,
      default: ''
    },
    yAxisName: {
      type: String,
      default: ''
    }
  },
  computed: {
    yAxisData() {
      return this.data.map(item => item.name)
    },
    values() {
      return this.data.map(item => item.value)
    },
    chartOptions() {
      return {
        tooltip: {
          trigger: 'axis',
          axisPointer: {
            type: 'shadow'
          }
        },
        grid: {
          left: '3%',
          right: '10%',
          bottom: '1%',
          top: '10%',
          containLabel: true,
          show: false
        },
        xAxis: {
          type: 'value',
          name: this.xAxisName,
          nameLocation: 'end',
          nameGap: 10
        },
        yAxis: {
          type: 'category',
          data: this.yAxisData,
          axisTick: {
            alignWithLabel: true
          },
          name: this.yAxisName,
          nameLocation: 'end',
          nameGap: 10,
          splitLine: {
            show: false
          }
        },
        series: [
          {
            name: this.title,
            type: 'bar',
            data: this.values,
            itemStyle: {
              color: {
                type: 'linear',
                x: 0,
                y: 0,
                x2: 1,
                y2: 0,
                colorStops: [
                  {
                    offset: 0,
                    color: this.color
                  },
                  {
                    offset: 1,
                    color: this.color + '80'
                  }
                ]
              }
            },
            label: {
              show: true,
              position: 'right',
              color: '#333',
              fontSize: 12
            },
            emphasis: {
              itemStyle: {
                color: this.color,
                shadowBlur: 10,
                shadowOffsetX: 0,
                shadowColor: 'rgba(0, 0, 0, 0.5)'
              }
            }
          }
        ]
      }
    }
  },
  methods: {
    handleChartClick(params) {
      this.$emit('chart-click', params)
    }
  }
}
</script>
