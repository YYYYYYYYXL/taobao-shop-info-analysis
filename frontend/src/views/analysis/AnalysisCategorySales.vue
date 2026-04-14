<template>
    <div style="padding: 20px;">
      <h2>分类销量分析</h2>

      <p v-if="loading">数据加载中...</p>
      <p v-else-if="errorMsg" style="color: red;">{{ errorMsg }}</p>

      <div v-else>
        <div ref="chartRef" style="width: 100%; height: 600px;"></div>
      </div>
    </div>
  </template>

  <script>
  import * as echarts from 'echarts'
  import { getAnalysisSummary } from '@/api/analysis'

  export default {
    name: 'AnalysisCategorySales',
    data() {
      return {
        loading: true,
        errorMsg: '',
        chartInstance: null,
        chartData: []
      }
    },
    async mounted() {
      try {
        const res = await getAnalysisSummary()
        this.chartData = Array.isArray(res.data?.data) ? res.data.data : []
      } catch (error) {
        if (error.response) {
          this.errorMsg = `请求失败，状态码：${error.response.status}`
        } else if (error.request) {
          this.errorMsg = '请求已发出，但后端没有正常响应'
        } else {
          this.errorMsg = `请求错误：${error.message}`
        }
        console.error(error)
      } finally {
        this.loading = false
        this.$nextTick(() => {
          this.initChart()
        })
      }
    },
    methods: {
      initChart() {
        if (!this.$refs.chartRef) return
        if (!this.chartData.length) return

        if (this.chartInstance) {
          this.chartInstance.dispose()
        }

        this.chartInstance = echarts.init(this.$refs.chartRef)
        this.chartInstance.setOption({
          tooltip: {
            trigger: 'item'
          },
          legend: {
            orient: 'vertical',
            left: 'left'
          },
          series: [
            {
              name: '分类销量',
              type: 'pie',
              radius: ['40%', '70%'],
              center: ['55%', '50%'],
              data: this.chartData,
              label: {
                show: true,
                formatter: '{b}: {c} ({d}%)'
              },
              labelLine: {
                show: true
              },
              itemStyle: {
                borderColor: '#fff',
                borderWidth: 2
              }
            }
          ]
        })

        this.chartInstance.resize()
        window.addEventListener('resize', this.handleResize)
      },
      handleResize() {
        if (this.chartInstance) {
          this.chartInstance.resize()
        }
      }
    },
    beforeDestroy() {
      window.removeEventListener('resize', this.handleResize)
      if (this.chartInstance) {
        this.chartInstance.dispose()
        this.chartInstance = null
      }
    }
  }
  </script>