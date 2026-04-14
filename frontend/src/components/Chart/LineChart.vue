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
  name: 'LineChart',
  components: {
    BaseChart
  },
  props: {
    title: {
      type: String,
      default: '折线图'
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
      default: '#67c23a'
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
    xAxisData() {
      return this.data.map(item => item.name)
    },
    values() {
      return this.data.map(item => item.value)
    },
    chartOptions() {
      return {
        tooltip: {
          trigger: 'axis'
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
          type: 'category',
          boundaryGap: false,
          data: this.xAxisData,
          name: this.xAxisName,
          nameLocation: 'end',
          nameGap: 10
        },
        yAxis: {
          type: 'value',
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
            type: 'line',
            data: this.values,
            smooth: true,
            lineStyle: {
              color: this.color
            },
            itemStyle: {
              color: this.color
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
                    color: this.color + '40'
                  },
                  {
                    offset: 1,
                    color: this.color + '10'
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
