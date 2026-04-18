<template>
  <el-card class="chart-card" shadow="hover">
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
    title: {
      type: String,
      default: ''
    },
    type: {
      type: String,
      required: true,
      validator: value => [
        'line', 'bar', 'pie', 'bar-line',
        'rose', 'horizontal-bar', 'radar', 'word-cloud', 'china-map',
        'dual-bar', 'dual-line'
      ].includes(value)
    },
    height: {
      type: Number,
      default: 400
    },
    data: {
      type: Array,
      required: true
    },
    chartProps: {
      type: Object,
      default: () => ({})
    },
    xAxisName: {
      type: String,
      default: ''
    },
    yAxisName: {
      type: String,
      default: ''
    },
    yAxis2Name: {
      type: String,
      default: ''
    },
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
        { label: '柱线组合图', value: 'bar-line' },
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
        line: 'LineChart',
        bar: 'BarChart',
        pie: 'PieChart',
        'bar-line': 'BarLineChart',
        rose: 'RoseChart',
        'horizontal-bar': 'HorizontalBarChart',
        radar: 'RadarChart',
        'word-cloud': 'WordCloudChart',
        'china-map': 'ChinaMapChart',
        'dual-bar': 'DualBarChart',
        'dual-line': 'DualLineChart'
      }
      return componentMap[this.currentChartType]
    },
    filteredChartTypeOptions() {
      const isMultiValueChart = ['dual-bar', 'dual-line', 'bar-line'].includes(this.currentChartType)

      if (isMultiValueChart) {
        return this.chartTypeOptions.filter(option =>
          ['dual-bar', 'dual-line', 'bar-line'].includes(option.value)
        )
      }

      return this.chartTypeOptions.filter(option =>
        !['dual-bar', 'dual-line', 'bar-line'].includes(option.value)
      )
    },
    showColorPicker() {
      const noColorCharts = ['pie', 'rose', 'word-cloud', 'dual-bar', 'dual-line', 'china-map']
      return !noColorCharts.includes(this.currentChartType)
    },
    finalChartProps() {
      const props = { ...this.chartProps }

      switch (this.currentChartType) {
        case 'bar':
        case 'horizontal-bar':
        case 'line':
          props.color = this.currentColor
          break
        case 'pie':
        case 'rose':
          props.color = [
            this.currentColor,
            this.adjustColorBrightness(this.currentColor, 0.8)
          ]
          break
        case 'radar':
          props.color = this.currentColor
          break
        case 'word-cloud':
          props.textStyle = {
            ...props.textStyle,
            color: this.currentColor
          }
          break
        case 'bar-line':
          props.barColor = this.currentColor
          props.lineColor = this.adjustColorBrightness(this.currentColor, 0.7)
          break
      }

      return props
    }
  },
  methods: {
    handleChartTypeChange(newType) {
      this.currentChartType = newType
    },
    handleColorChange(newColor) {
      this.currentColor = newColor
    },
    getDefaultColor() {
      if (this.chartProps && this.chartProps.color) {
        if (Array.isArray(this.chartProps.color)) {
          return this.chartProps.color[0]
        }
        return this.chartProps.color
      }
      return '#409EFF'
    },
    adjustColorBrightness(color, factor) {
      const hex = color.replace('#', '')
      const r = parseInt(hex.substr(0, 2), 16)
      const g = parseInt(hex.substr(2, 2), 16)
      const b = parseInt(hex.substr(4, 2), 16)

      const newR = Math.min(255, Math.max(0, Math.round(r * factor)))
      const newG = Math.min(255, Math.max(0, Math.round(g * factor)))
      const newB = Math.min(255, Math.max(0, Math.round(b * factor)))

      return `#${newR.toString(16).padStart(2, '0')}${newG.toString(16).padStart(2, '0')}${newB.toString(16).padStart(2, '0')}`
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
