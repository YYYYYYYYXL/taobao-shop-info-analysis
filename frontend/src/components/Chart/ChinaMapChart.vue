<template>
  <div ref="chartRef" class="chart-content" :style="{ height: height + 'px' }"></div>
</template>

<script>
import * as echarts from 'echarts'
import chinaMap from '@/utils/china.json'

export default {
  name: 'ChinaMapChart',
  props: {
    title: {
      type: String,
      default: '中国地图'
    },
    height: {
      type: Number,
      default: 400
    },
    data: {
      type: Array,
      required: true
    },
    theme: {
      type: String,
      default: 'default'
    },
    mapName: {
      type: String,
      default: 'china'
    },
    roam: {
      type: Boolean,
      default: false
    },
    showLabel: {
      type: Boolean,
      default: true
    },
    visualMapMin: {
      type: Number,
      default: 0
    },
    visualMapMax: {
      type: Number,
      default: 30000000
    },
    colorRange: {
      type: Array,
      default: () => ['#ffe5e5', '#800000']
    },
    calculable: {
      type: Boolean,
      default: true
    }
  },
  computed: {
    chartOptions() {
      return {
        tooltip: {
          trigger: 'item',
          formatter: (params) => {
            if (params.data && params.data.value !== undefined) {
              return `${params.name}: ${params.data.value}`
            }
            return params.name
          }
        },
        visualMap: {
          min: this.visualMapMin,
          max: Math.max(...this.data.map(item => Number(item.value) || 0),0),
          left: '5%',
          top: '5%',
          text: ['高', '低'],
          textStyle: {
            fontSize: 12
          },
          inRange: {
            color: this.colorRange
          },
          calculable: this.calculable
        },
        series: [
          {
            name: this.title,
            type: 'map',
            map: this.mapName,
            roam: this.roam,
            label: {
              show: this.showLabel
            },
            emphasis: {
              show: true
            },
            data: this.data
          }
        ]
      }
    }
  },
  data() {
    return {
      chart: null
    }
  },
  mounted() {
    this.initChart()
    window.addEventListener('resize', this.handleResize)
  },
  beforeDestroy() {
    if (this.chart) {
      this.chart.dispose()
    }
    window.removeEventListener('resize', this.handleResize)
  },
  watch: {
    chartOptions: {
      handler(newOptions) {
        if (this.chart) {
          this.chart.setOption(newOptions, true)
        }
      },
      deep: true
    }
  },
  methods: {
    initChart() {
      // 注册地图
      echarts.registerMap(this.mapName, chinaMap)
      
      // 初始化图表
      this.chart = echarts.init(this.$refs.chartRef, this.theme)
      this.chart.setOption(this.chartOptions)
    },
    handleResize() {
      if (this.chart) {
        this.chart.resize()
      }
    }
  }
}
</script>
