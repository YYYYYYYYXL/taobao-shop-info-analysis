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
import 'echarts-wordcloud'

export default {
  name: 'WordCloudChart',
  components: {
    BaseChart
  },
  props: {
    title: {
      type: String,
      default: '词云图'
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
    }
  },
  computed: {
    chartOptions() {
      return {
        tooltip: {
          trigger: 'item',
          formatter: (params) => {
            return `${params.name}: ${params.value}`
          }
        },
        series: [
          {
            type: 'wordCloud',
            shape: 'rectangle',
            keepAspect: false,
            left: 'center',
            top: 'center',
            width: '90%',
            height: '70%',
            sizeRange: [25, 100],
            rotationRange: [-90, 90],
            rotationStep: 45,
            gridSize: 6,
            drawOutOfBound: false,
            layoutAnimation: false,
            textStyle: {
              fontFamily: 'Microsoft YaHei',
              fontWeight: 'bold',
              color: () => {
                // 生成随机 RGB 颜色
                return `rgb(${[0, 1, 2]
                  .map(() => Math.round(Math.random() * 255))
                  .join(",")})`
              }
            },
            emphasis: {
              focus: 'self',
              textStyle: {
                textShadowBlur: 10,
                textShadowColor: '#333'
              }
            },
            data: this.data
          }
        ]
      }
    }
  }
}
</script>
