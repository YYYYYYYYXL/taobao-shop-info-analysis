<template>
    <div class="chart-only-container">
      <AnalysisChart
        :title="''"
        :type="finalChartType"
        :height="height"
        :data="chartData"
        :chart-props="finalChartProps"
        :x-axis-name="finalXAxisName"
        :y-axis-name="finalYAxisName"
        :y-axis2-name="finalYAxis2Name"
        :show-controls="false"
        :theme="theme"
      />
    </div>
  </template>

  <script>
  import AnalysisChart from '@/components/analysis/AnalysisChart.vue'
  import Request from '@/utils/request'
  import { staticMenuList } from '@/utils/staticMenu'

  export default {
    name: 'AnalysisChartOnly',
    components: {
      AnalysisChart
    },
    props: {
      title: {
        type: String,
        required: true
      },
      height: {
        type: Number,
        default: 170
      },
      theme: {
        type: String,
        default: 'default'
      }
    },
    data() {
      return {
        chartData: []
      }
    },
    computed: {
      currentMenu() {
        const findMenu = (menus, targetName) => {
          for (const menu of menus) {
            if (menu.name === targetName) {
              return menu
            }
            if (menu.children && menu.children.length > 0) {
              const found = findMenu(menu.children, targetName)
              if (found) {
                return found
              }
            }
          }
          return null
        }

        return findMenu(staticMenuList, this.title)
      },
      apiUrl() {
        return this.currentMenu?.apiUrl || ''
      },
      finalChartType() {
        return this.currentMenu?.chartType || 'bar'
      },
      finalChartProps() {
        return {
          color: this.currentMenu?.chartColor || '#409EFF'
        }
      },
      finalTableColumns() {
        return {
          name: this.currentMenu?.tableColumnName || '名称',
          value: this.currentMenu?.tableColumnValueOne || '数值',
          value1: this.currentMenu?.tableColumnValueOne || '数值',
          value2: this.currentMenu?.tableColumnValueTwo || '数值'
        }
      },
      finalXAxisName() {
        if (this.finalChartType === 'horizontal-bar') {
          return this.finalTableColumns.value || ''
        }
        return this.finalTableColumns.name || ''
      },
      finalYAxisName() {
        if (this.finalChartType === 'horizontal-bar') {
          return this.finalTableColumns.name || ''
        }
        return this.finalTableColumns.value1 || ''
      },
      finalYAxis2Name() {
        const isMultiValueChart = ['dual-bar', 'dual-line', 'bar-line'].includes(this.finalChartType)
        if (isMultiValueChart) {
          return this.finalTableColumns.value2 || ''
        }
        return ''
      }
    },
    created() {
      this.fetchData()
    },
    methods: {
      async fetchData() {
        try {
          if (!this.apiUrl) {
            return
          }

          const res = await Request.get(this.apiUrl)
          if (res.code === '0') {
            const rawData = res.data || []
            this.chartData = this.finalChartType === 'horizontal-bar' ? [...rawData].reverse() : rawData
          }
        } catch (error) {
          console.error('获取大屏分析数据失败:', error)
        }
      }
    }
  }
  </script>

  <style scoped>
  .chart-only-container {
    width: 100%;
    height: 100%;
  }
  </style>