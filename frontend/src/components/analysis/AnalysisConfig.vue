<template>
    <AnalysisTemplate
      :title="title"
      :chart-type="finalChartType"
      :chart-props="finalChartProps"
      :api-url="apiUrl"
      :table-columns="finalTableColumns"
    />
  </template>

  <script>
  import AnalysisTemplate from '@/components/analysis/AnalysisTemplate.vue'
  import { staticMenuList } from '@/utils/staticMenu'

  export default {
    name: 'AnalysisConfig',
    components: {
      AnalysisTemplate
    },
    props: {
      title: {
        type: String,
        required: true
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
          value1: this.currentMenu?.tableColumnValueOne || '数值',
          value2: this.currentMenu?.tableColumnValueTwo || '数值'
        }
      }
    }
  }
  </script>