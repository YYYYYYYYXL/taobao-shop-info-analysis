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
  name: 'RadarChart',
  components: {
    BaseChart
  },
  props: {
    title: {
      type: String,
      default: '雷达图'
    },
    height: {
      type: Number,
      default: 300
    },
    data: {
      type: Array,
      required: true
    },
    indicators: {
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
    }
  },
  computed: {
    chartOptions() {
      return {
        tooltip: {},
        radar: {
          indicator: this.indicators,
          radius: '70%',
          center: ['50%', '50%']
        },
        series: [
          {
            name: this.title,
            type: 'radar',
            data: this.data.map(item => ({
              ...item,
              itemStyle: {
                color: this.color
              },
              areaStyle: {
                color: this.color + '20'
              },
              label: {
                show: true,
                formatter: function(params) {
                  return params.value;
                },
                fontSize: 12
              }
            }))
          }
        ]
      }
    }
  }
}
</script>
