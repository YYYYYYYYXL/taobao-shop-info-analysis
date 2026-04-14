<template>
  <el-card class="chart-card" shadow="hover">
    <!-- 图表类型选择器 -->
    <div class="chart-header" v-if="title || showControls">
      <div v-if="title" class="chart-title">{{ title }}</div>
      <div v-if="showControls" class="chart-controls">
        <el-color-picker
            v-if="showColorPicker"
            v-model="currentColor"
            size="small"
            :predefine="predefineColors"
            @change="handleColorChange"
        />
        <el-select
            v-model="currentChartType"
            placeholder="选择图表类型"
            size="small"
            style="width: 150px;"
            @change="handleChartTypeChange"
        >
          <el-option
              v-for="option in filteredChartTypeOptions"
              :key="option.value"
              :label="option.label"
              :value="option.value"
          />
        </el-select>
        <el-button
            size="small"
            type="primary"
            icon="el-icon-check"
            @click="saveChartConfig"
            title="保存图表配置"
        >
          保存
        </el-button>
      </div>
    </div>

    <div class="chart-content">
      <component
          :is="chartComponent"
          :title="title"
          :height="height"
          :data="data"
          :x-axis-name="xAxisName"
          :y-axis-name="yAxisName"
          :y-axis2-name="yAxis2Name"
          v-bind="finalChartProps"
          :theme="theme"
      />
    </div>
  </el-card>
</template>

<script>
import LineChart from '@/components/Chart/LineChart.vue'
import BarChart from '@/components/Chart/BarChart.vue'
import PieChart from '@/components/Chart/PieChart.vue'
import BarLineChart from '@/components/Chart/BarLineChart.vue'
import RoseChart from '@/components/Chart/RoseChart.vue'
import HorizontalBarChart from '@/components/Chart/HorizontalBarChart.vue'
import RadarChart from '@/components/Chart/RadarChart.vue'
import WordCloudChart from '@/components/Chart/WordCloudChart.vue'
import ChinaMapChart from '@/components/Chart/ChinaMapChart.vue'
import DualBarChart from '@/components/Chart/DualBarChart.vue'
import DualLineChart from '@/components/Chart/DualLineChart.vue'
import excel from '@/utils/excel.js'
import Request from '@/utils/request'

export default {
  name: 'AnalysisChart',
  components: {
    LineChart,
    BarChart,
    PieChart,
    BarLineChart,
    RoseChart,
    HorizontalBarChart,
    RadarChart,
    WordCloudChart,
    ChinaMapChart,
    DualBarChart,
    DualLineChart
  },
  props: {
    // 图表标题
    title: {
      type: String,
      default: ''
    },
    // 图表类型
    type: {
      type: String,
      required: true,
      validator: value => [
        'line', 'bar', 'pie', 'bar-line',
        'rose', 'horizontal-bar', 'radar', 'word-cloud', 'china-map',
        'dual-bar', 'dual-line'
      ].includes(value)
    },
    // 图表高度
    height: {
      type: Number,
      default: 400
    },
    // 图表数据
    data: {
      type: Array,
      required: true
    },
    // 其他图表属性
    chartProps: {
      type: Object,
      default: () => ({})
    },
    // X轴单位
    xAxisName: {
      type: String,
      default: ''
    },
    // Y轴单位
    yAxisName: {
      type: String,
      default: ''
    },
    // Y轴2单位（用于双Y轴图表）
    yAxis2Name: {
      type: String,
      default: ''
    },
    // 是否显示控制面板
    showControls: {
      type: Boolean,
      default: true
    },
    theme: {
      type: String,
      default: 'default'
    }
  },
  data() {
    return {
      currentChartType: this.type,
      currentColor: this.getDefaultColor(),
      chartTypeOptions: [
        { label: '饼图', value: 'pie' },
        { label: '柱状图', value: 'bar' },
        { label: '条形图', value: 'horizontal-bar' },
        { label: '折线图', value: 'line' },
        { label: '玫瑰图', value: 'rose' },
        { label: '对比柱状图', value: 'dual-bar' },
        { label: '对比折线图', value: 'dual-line' },
        { label: '柱折组合图', value: 'bar-line' },
        { label: '词云图', value: 'word-cloud' },
        { label: '雷达图', value: 'radar' },
        { label: '地图', value: 'china-map' }
      ],
      predefineColors: [
        '#409EFF', '#67C23A', '#E6A23C', '#F56C6C', '#909399',
        '#C71585', '#FF4500', '#32CD32', '#1E90FF', '#FFD700',
        '#FF69B4', '#00CED1', '#FF6347', '#7B68EE', '#20B2AA'
      ]
    }
  },
  computed: {
    chartComponent() {
      const componentMap = {
        'line': 'LineChart',
        'bar': 'BarChart',
        'pie': 'PieChart',
        'bar-line': 'BarLineChart',
        'rose': 'RoseChart',
        'horizontal-bar': 'HorizontalBarChart',
        'radar': 'RadarChart',
        'word-cloud': 'WordCloudChart',
        'china-map': 'ChinaMapChart',
        'dual-bar': 'DualBarChart',
        'dual-line': 'DualLineChart'
      }
      return componentMap[this.currentChartType]
    },
    // 根据当前图表类型过滤可选的图表类型
    filteredChartTypeOptions() {
      const isMultiValueChart = ['dual-bar', 'dual-line', 'bar-line'].includes(this.currentChartType)

      if (isMultiValueChart) {
        // 多值图表只能选择多值图表
        return this.chartTypeOptions.filter(option =>
            ['dual-bar', 'dual-line', 'bar-line'].includes(option.value)
        )
      } else {
        // 单值图表只能选择单值图表
        return this.chartTypeOptions.filter(option =>
            !['dual-bar', 'dual-line', 'bar-line'].includes(option.value)
        )
      }
    },
    // 控制是否显示颜色选择器
    showColorPicker() {
      const noColorCharts = ['pie', 'rose', 'word-cloud', 'dual-bar', 'dual-line', 'china-map']
      return !noColorCharts.includes(this.currentChartType)
    },
    // 合并图表属性，包含用户选择的颜色
    finalChartProps() {
      const props = { ...this.chartProps }

      // 根据图表类型设置颜色
      switch (this.currentChartType) {
        case 'bar':
        case 'horizontal-bar':
        case 'line':
          props.color = this.currentColor
          break
        case 'pie':
        case 'rose':
          // 饼图和玫瑰图使用渐变色
          props.color = [
            this.currentColor,
            this.adjustColorBrightness(this.currentColor, 0.8)
          ]
          break
        case 'radar':
          props.color = this.currentColor
          break
        case 'word-cloud':
          // 词云图使用随机颜色，这里设置主色调
          props.textStyle = {
            ...props.textStyle,
            color: this.currentColor
          }
          break
        case 'china-map':
        case 'dual-bar':
          // 对比柱状图使用两个颜色
          // props.series1Color = this.currentColor
          // props.series2Color = this.adjustColorBrightness(this.currentColor, 0.7)
          break
        case 'dual-line':
          // 双折线图使用两个颜色
          // props.series1Color = this.currentColor
          // props.series2Color = this.adjustColorBrightness(this.currentColor, 0.7)
          break
        case 'bar-line':
          // 柱状图和折线图组合
          props.barColor = this.currentColor
          props.lineColor = this.adjustColorBrightness(this.currentColor, 0.7)
          break
      }

      return props
    }
  },
  methods: {
    // 处理图表类型变化
    handleChartTypeChange(newType) {
      this.currentChartType = newType
      // 可以在这里添加图表切换的动画效果或其他逻辑
      console.log('图表类型切换为:', newType)
    },
    // 处理颜色变化
    handleColorChange(newColor) {
      this.currentColor = newColor
      console.log('颜色切换为:', newColor)
    },
    // 获取默认颜色
    getDefaultColor() {
      // 从 chartProps 中获取颜色，如果没有则使用默认颜色
      if (this.chartProps && this.chartProps.color) {
        if (Array.isArray(this.chartProps.color)) {
          return this.chartProps.color[0]
        }
        return this.chartProps.color
      }
      return '#409EFF' // 默认蓝色
    },
    // 调整颜色亮度
    adjustColorBrightness(color, factor) {
      // 简单的颜色亮度调整
      const hex = color.replace('#', '')
      const r = parseInt(hex.substr(0, 2), 16)
      const g = parseInt(hex.substr(2, 2), 16)
      const b = parseInt(hex.substr(4, 2), 16)

      const newR = Math.min(255, Math.max(0, Math.round(r * factor)))
      const newG = Math.min(255, Math.max(0, Math.round(g * factor)))
      const newB = Math.min(255, Math.max(0, Math.round(b * factor)))

      return `#${newR.toString(16).padStart(2, '0')}${newG.toString(16).padStart(2, '0')}${newB.toString(16).padStart(2, '0')}`
    },
    // 保存图表配置到菜单
    async saveChartConfig() {
      try {
        // 获取当前菜单项
        const menuData = JSON.parse(localStorage.getItem('userMenuList') || '[]')
        const currentMenu = this.findMenuByName(menuData, this.title)

        if (!currentMenu) {
          this.$message.error('未找到对应的菜单项')
          return
        }

        // 更新菜单数据
        const updateData = {
          id: currentMenu.id,
          chartType: this.currentChartType,
          chartColor: this.currentColor
        }

        // 发送更新请求
        const res = await Request.put(`/menu/${currentMenu.id}`, updateData)
        if (res.code === '0') {
          // 更新本地存储的菜单数据
          this.updateLocalMenuData(currentMenu.id, updateData)
          this.$message.success('图表配置保存成功')
        } else {
          this.$message.error('保存失败：' + res.message)
        }
      } catch (error) {
        // 静默处理保存图表配置失败
        this.$message.error('保存失败')
      }
    },
    // 递归查找菜单项
    findMenuByName(menus, targetName) {
      for (const menu of menus) {
        if (menu.name === targetName) {
          return menu
        }
        if (menu.children && menu.children.length > 0) {
          const found = this.findMenuByName(menu.children, targetName)
          if (found) {
            return found
          }
        }
      }
      return null
    },
    // 更新本地菜单数据
    updateLocalMenuData(menuId, updateData) {
      try {
        const menuData = JSON.parse(localStorage.getItem('userMenuList') || '[]')
        const updateMenu = (menus) => {
          for (const menu of menus) {
            if (menu.id === menuId) {
              Object.assign(menu, updateData)
              return true
            }
            if (menu.children && menu.children.length > 0) {
              if (updateMenu(menu.children)) {
                return true
              }
            }
          }
          return false
        }

        updateMenu(menuData)
        localStorage.setItem('userMenuList', JSON.stringify(menuData))
      } catch (error) {
        // 静默处理更新本地菜单数据失败
      }
    },
    // 格式化数字
    formatNumber(row, column, cellValue) {
      if (typeof cellValue === 'number') {
        return cellValue.toLocaleString()
      }
      return cellValue
    },
    // 格式化标签
    formatLabel(key) {
      const labelMap = {
        'value': '数值',
        'value1': '数值1',
        'value2': '数值2',
        'name': '名称'
      }
      return labelMap[key] || key
    },
    // 下载数据
    downloadData() {
      if (this.data && this.data.length > 0) {
        // 根据图表类型生成表头和数据
        const { headers, keys } = this.generateDownloadData()

        const params = {
          header: headers,
          key: keys,
          data: this.data,
          autoWidth: true,
          fileName: this.title + '_数据表',
          bookType: 'xlsx'
        }

        excel.exportDataToExcel(params)
        this.$message.success('数据下载成功')
      } else {
        this.$message.warning('暂无数据可下载')
      }
    },
    // 生成下载数据的表头和数据键
    generateDownloadData() {
      const headers = []
      const keys = []

      // 根据图表类型生成表头
      switch (this.type) {
        case 'line':
        case 'bar':
          headers.push('名称', '数值')
          keys.push('name', 'value')
          break

        case 'horizontal-bar':
          headers.push('数值', '名称')
          keys.push('value', 'name')
          break

        case 'pie':
        case 'rose':
        case 'word-cloud':
        case 'china-map':
          headers.push('名称', '数值')
          keys.push('name', 'value')
          break

        case 'dual-bar':
        case 'bar-line':
        case 'dual-line':
          headers.push('名称', '数值1', '数值2')
          keys.push('name', 'value1', 'value2')
          break

        case 'radar':
          const indicators = this.chartProps.indicators || []
          headers.push('名称')
          keys.push('name')
          indicators.forEach(indicator => {
            headers.push(indicator.name)
            keys.push('value')
          })
          break

        default:
          // 默认处理
          if (this.data.length > 0) {
            const firstItem = this.data[0]
            Object.keys(firstItem).forEach(key => {
              headers.push(this.formatLabel(key))
              keys.push(key)
            })
          }
      }

      return { headers, keys }
    }
  }
}
</script>

<style lang="less" scoped>
.chart-card {
  background: transparent;
  border: none;
}

.chart-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 0 16px 0;
  border-bottom: 1px solid #e5e7eb;
  margin-bottom: 20px;
}

.chart-title {
  font-size: 18px;
  font-weight: 600;
  color: #1f2937;
  letter-spacing: 0.3px;
}

.chart-controls {
  display: flex;
  align-items: center;
  gap: 12px;
}

.chart-content {
  padding: 0;
}

:deep(.el-button) {
  border-radius: 8px;
  font-weight: 500;
  transition: all 0.3s ease;
}

:deep(.el-select) {
  .el-input__inner {
    border-radius: 8px;
    border-color: #e5e7eb;

    &:focus {
      border-color: #667eea;
    }
  }
}
</style>
