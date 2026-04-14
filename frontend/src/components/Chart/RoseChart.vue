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
  name: 'RoseChart',
  components: {
    BaseChart
  },
  props: {
    title: {
      type: String,
      default: '玫瑰图'
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
    colors: {
      type: Array,
      default: () => ['#409eff', '#67c23a', '#e6a23c', '#f56c6c', '#909399', '#9c27b0', '#ff9800', '#4caf50']
    }
  },
  computed: {
    chartOptions() {
      return {
        tooltip: {
          trigger: 'item',
          formatter: '{a} <br/>{b}: {c} ({d}%)'
        },
        legend: {
          orient: 'vertical',
          left: '5%',
          top: 'center',
          itemWidth: 12,
          itemHeight: 8,
          textStyle: {
            fontSize: 12
          }
        },
        series: [
          {
            name: this.title,
            type: 'pie',
            radius: [20, 110],
            center: ['50%', '50%'],
            roseType: 'area',
            itemStyle: {
              borderRadius: 8
            },
            label: {
              show: false
            },
            emphasis: {
              label: {
                show: true
              },
              itemStyle: {
                shadowBlur: 10,
                shadowOffsetX: 0,
                shadowColor: 'rgba(0, 0, 0, 0.5)'
              }
            },
            data: this.data.map((item, index) => ({
              ...item,
              itemStyle: {
                color: this.colors[index % this.colors.length]
              }
            })),
            label: {
              show: true,
              formatter: '{b}: {c}',
              fontSize: 12
            }
          }
        ]
      }
    }
  }
}
</script>
