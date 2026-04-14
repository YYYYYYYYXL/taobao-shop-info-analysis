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
  name: 'PieChart',
  components: {
    BaseChart
  },
  props: {
    title: {
      type: String,
      default: '饼图'
    },
    height: {
      type: Number,
      default: 350
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
      default: () => ['#409eff', '#67c23a', '#e6a23c', '#f56c6c', '#909399']
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
        },
        series: [
          {
            name: this.title,
            type: 'pie',
            radius: ['40%', '70%'],
            center: ['50%', '50%'],
            avoidLabelOverlap: false,
            itemStyle: {
              borderRadius: 10,
              borderColor: '#fff',
              borderWidth: 2
            },
            emphasis: {
              label: {
                show: true,
                fontSize: '18',
                fontWeight: 'bold'
              }
            },
            labelLine: {
              show: false
            },
            data: this.data.map((item, index) => ({
              ...item,
              itemStyle: {
                color: this.colors[index % this.colors.length]
              }
            })),
            label: {
              show: true,
              formatter: '{b}: {c}\n({d}%)',
              fontSize: 12
            }
          }
        ]
      }
    }
  }
}
</script>
