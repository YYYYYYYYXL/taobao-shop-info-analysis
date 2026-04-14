<template>
    <div ref="chartRef" class="chart-content" :style="{ height: height + 'px' }"></div>
</template>

<script>
import * as echarts from 'echarts'

export default {
  name: 'BaseChart',
  props: {
    title: {
      type: String,
      default: ''
    },
    height: {
      type: Number,
      default: 300
    },
    options: {
      type: Object,
      required: true
    },
    theme: {
      type: String,
      default: 'default'
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
    options: {
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
      this.chart = echarts.init(this.$refs.chartRef, this.theme)
      this.chart.setOption(this.options)
    },
    handleResize() {
      if (this.chart) {
        this.chart.resize()
      }
    }
  }
}
</script>

<style scoped>
.chart-content {
  width: 100%;
}
</style>
