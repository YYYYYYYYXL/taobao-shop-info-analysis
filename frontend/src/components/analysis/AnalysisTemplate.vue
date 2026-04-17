<template>
  <div class="analysis-container">
    <!-- 查询条件区域 -->
    <AnalysisFilter 
      v-if="showFilter" 
      :show-details-button="true"
      :show-download-button="true"
      :details-disabled="tableData.length === 0 || loading"
      :download-disabled="tableData.length === 0 || loading"
      @search="handleSearch" 
      @refresh="handleRefresh" 
      @open-details="detailsVisible = true"
      @download="showProgressDialog = true"
    />

    <!-- 图表展示区域 -->
    <div class="chart-container">
      <AnalysisChart
        :title="title"
        :type="chartType"
        :height="height"
        :data="chartData"
        :chart-props="chartProps"
        :x-axis-name="finalXAxisName"
        :y-axis-name="finalYAxisName"
        :y-axis2-name="finalYAxis2Name"
        @refresh="refreshChart"
      />
    </div>

    

    <!-- 右侧抽屉：数据网格展示 -->
    <el-drawer
      :visible.sync="detailsVisible"
      title="数据明细"
      direction="rtl"
      size="840px"
      custom-class="details-drawer"
      :append-to-body="true"
    >
      <div class="drawer-body" v-loading="loading">
        <div class="data-table">
          <div class="table-header" :class="{ 'has-multiple-values': hasMultipleValues }">
            <div class="th-rank">排名</div>
            <div class="th-name">名称</div>
            <div class="th-value">{{ tableColumns.value1 }}</div>
            <div class="th-value2" v-if="hasMultipleValues">{{ tableColumns.value2 }}</div>
            <div class="th-percent" v-if="!hasMultipleValues">占比</div>
          </div>
          <div class="table-body">
            <div 
              class="table-row" 
              :class="{ 'has-multiple-values': hasMultipleValues }"
              v-for="(item, index) in sortedTableData" 
              :key="index"
            >
              <div class="td-rank">
                <span class="rank-badge" :class="getRankClass(index)">{{ index + 1 }}</span>
              </div>
              <div class="td-name" :title="item.name">{{ item.name }}</div>
              <div class="td-value">
                <span class="value-number">{{ formatNumber(item.value1) }}</span>
              </div>
              <div class="td-value2" v-if="hasMultipleValues">
                <span class="value-number secondary">{{ formatNumber(item.value2) }}</span>
              </div>
              <div class="td-percent" v-if="!hasMultipleValues">
                <span class="percent-text">{{ getPercentage(item.value1) }}%</span>
                <div class="percent-bar">
                  <div class="percent-bar-fill" :style="{ width: getPercentage(item.value1) + '%' }"></div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </el-drawer>

    <!-- 进度条弹窗 -->
    <el-dialog 
      title="数据加载进度" 
      :visible.sync="showProgressDialog" 
      width="500px" 
      :close-on-click-modal="true"
      :close-on-press-escape="true"
    >
      <div class="progress-content">
        <div class="progress-info">
          <div class="progress-text">正在加载数据...</div>
          <div class="progress-percent">{{ progressPercent }}%</div>
        </div>
        <el-progress 
          :percentage="progressPercent" 
          :color="progressColor"
          :stroke-width="8"
          :show-text="false"
        ></el-progress>
        <div class="progress-stats">
          <div class="stat-item">
            <span class="stat-label">总数据量：</span>
            <span class="stat-value">{{ sortedTableData.length }}</span>
          </div>
          <div class="stat-item">
            <span class="stat-label">已处理：</span>
            <span class="stat-value">{{ processedCount }}</span>
          </div>
        </div>
      </div>
      <div slot="footer" class="dialog-footer">
        <el-button @click="closeProgressDialog">关闭</el-button>
        <el-button type="primary" @click="downloadData">导出数据</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import AnalysisFilter from '@/components/analysis/AnalysisFilter.vue'
import AnalysisChart from '@/components/analysis/AnalysisChart.vue'
import Request from '@/utils/request'
// import { hasInviteCode, isValidDate } from '@/utils/inviteCode'

export default {
  name: 'AnalysisTemplate',
  components: {
    AnalysisFilter,
    AnalysisChart
  },
  props: {
    height: {
      type: Number,
      default: 600
    },
    category: {
      type: String,
      default: ''
    },
    showFilter: {
      type: Boolean,
      default: false
    },
    // 图表配置
    title: {
      type: String,
      required: true
    },
    chartType: {
      type: String,
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
    // API配置（使用 path 字段）
    apiUrl: {
      type: String,
      required: true
    },
    // 表格列配置
    tableColumns: {
      type: Object,
      default: () => ({
        name: '名称',
        value: '数值',
        value1: '数值1',
        value2: '数值2'
      })
    }
  },
  computed: {
    // 判断是否为多值图表类型
    hasMultipleValues() {
      return ['dual-bar', 'dual-line', 'bar-line'].includes(this.chartType)
    },
    // 排序后的表格数据（按value1降序）
    sortedTableData() {
      const data = [...this.tableData]
      return data.sort((a, b) => {
        const valueA = parseFloat(a.value1) || 0
        const valueB = parseFloat(b.value1) || 0
        return valueB - valueA // 降序排序
      })
    },
    // 自动从 tableColumns 获取轴名称
    finalXAxisName() {
      // 水平条形图的轴名称是相反的
      if (this.chartType === 'horizontal-bar') {
        return this.xAxisName || this.tableColumns.value1 || ''
      }
      return this.xAxisName || this.tableColumns.name || ''
    },
    finalYAxisName() {
      // 水平条形图的轴名称是相反的
      if (this.chartType === 'horizontal-bar') {
        return this.yAxisName || this.tableColumns.name || ''
      }
      return this.yAxisName || this.tableColumns.value1 || ''
    },
    finalYAxis2Name() {
      // 只有多值图表才需要第二个Y轴名称
      if (this.hasMultipleValues) {
        return this.tableColumns.value2 || ''
      }
      return ''
    }
  },
  data() {
    return {
      chartData: [],
      tableData: [],
      loading: false,
      detailsVisible: false,
      searchForm: {
        category: ''
      },
      showProgressDialog: false,
      progressPercent: 0,
      processedCount: 0,
      progressTimer: null,
      progressColor: '#667eea'
    }
  },
  watch: {
    category: {
      handler(newVal) {
        this.searchForm.category = newVal
        this.fetchData()
      },
      immediate: true
    },
    showProgressDialog(newVal) {
      if (newVal) {
        this.$nextTick(() => {
          this.startProgress()
        })
      } else {
        this.resetProgress()
      }
    }
  },
  created() {
    // this.checkInviteCode()
    this.searchForm.category = this.category
  },
  methods: {
    // 处理数据属性映射
    // process data mapping
    processDataMapping(rawData) {
      return rawData.map(item => {
        const processedItem = { ...item }
        
        // 如果是单值图表，将 value 映射到 value1
        if (!this.hasMultipleValues && item.hasOwnProperty('value') && !item.hasOwnProperty('value1')) {
          processedItem.value1 = item.value
        }
        
        return processedItem
      })
    },
    async fetchData() {
      try {
        this.loading = true
        const params = {}
        if (this.searchForm.category && this.searchForm.category.length > 0) {
          // 多选类目，用逗号分隔
          params.category = Array.isArray(this.searchForm.category) 
            ? this.searchForm.category.join(',') 
            : this.searchForm.category
        }
        
        const res = await Request.get(this.apiUrl, { params })
        if (res.code === '0') {
          const rawData = res.data || []
          
          // 处理数据属性映射
          const processedData = this.processDataMapping(rawData)
          
          // 如果是水平条形图，需要反转数据顺序
          this.chartData = this.chartType === 'horizontal-bar' ? [...processedData].reverse() : processedData
          this.tableData = processedData
        }
      } catch (error) {
      } finally {
        this.loading = false
      }
    },
    handleSearch(searchForm) {
      this.searchForm = { ...searchForm }
      this.fetchData()
    },
    refreshChart() {
      this.fetchData()
    },
    handleRefresh() {
      this.fetchData()
    },
    handleDownload() {
      this.downloadData()
    },
    downloadData() {
      if (this.sortedTableData && this.sortedTableData.length > 0) {
        // 生成Excel数据
        let headers, data
        
        if (this.hasMultipleValues) {
          headers = [this.tableColumns.name, this.tableColumns.value1, this.tableColumns.value2]
          data = this.sortedTableData.map(item => [
            item.name,
            this.formatNumber(item.value1),
            this.formatNumber(item.value2)
          ])
        } else {
          headers = [this.tableColumns.name, this.tableColumns.value1, '占比']
          data = this.sortedTableData.map(item => [
            item.name,
            this.formatNumber(item.value1),
            this.getPercentage(item.value1) + '%'
          ])
        }
        
        // 创建CSV内容
        const csvContent = [headers, ...data]
          .map(row => row.join(','))
          .join('\n')
        
        // 下载文件
        const blob = new Blob(['\ufeff' + csvContent], { type: 'text/csv;charset=utf-8;' })
        const link = document.createElement('a')
        const url = URL.createObjectURL(blob)
        link.setAttribute('href', url)
        link.setAttribute('download', `${this.title}数据.csv`)
        link.style.visibility = 'hidden'
        document.body.appendChild(link)
        link.click()
        document.body.removeChild(link)
        
        this.$message.success('数据下载成功')
      } else {
        this.$message.warning('暂无数据可下载')
      }
    },
    formatNumber(value) {
      if (typeof value === 'number') {
        return value.toString()
      }
      return value
    },
       getPercentage(value) {
         if (!this.tableData || this.tableData.length === 0) return '0.00'
         const total = this.tableData.reduce((sum, item) => sum + (parseFloat(item.value1) || 0), 0)
         if (total === 0) return '0.00'
         return ((parseFloat(value) || 0) / total * 100).toFixed(2)
       },
       // 获取排名样式类
       getRankClass(index) {
         if (index === 0) return 'rank-first'
         if (index === 1) return 'rank-second'
         if (index === 2) return 'rank-third'
         return 'rank-normal'
       },
    // 关闭进度条弹窗
    closeProgressDialog() {
      this.showProgressDialog = false
      this.resetProgress()
    },
    // 重置进度
    resetProgress() {
      this.progressPercent = 0
      this.processedCount = 0
      if (this.progressTimer) {
        clearInterval(this.progressTimer)
        this.progressTimer = null
      }
    },
    // 启动进度条动画
    startProgress() {
      this.resetProgress()
      const total = this.sortedTableData.length
      if (total === 0) {
        this.progressPercent = 100
        this.processedCount = 0
        return
      }
      
      let current = 0
      const step = Math.max(1, Math.ceil(total / 50)) // 分50步完成
      
      this.progressTimer = setInterval(() => {
        current += step
        if (current >= total) {
          current = total
          this.progressPercent = 100
          this.processedCount = total
          clearInterval(this.progressTimer)
          this.progressTimer = null
        } else {
          this.progressPercent = Math.round((current / total) * 100)
          this.processedCount = current
        }
      }, 50) // 每50ms更新一次
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
      const menuData = JSON.parse(localStorage.getItem('userMenuList') || '[]')
      
      const updateMenu = (menus) => {
        menus.forEach(menu => {
          if (menu.id === menuId) {
            Object.assign(menu, updateData)
          }
          if (menu.children && menu.children.length > 0) {
            updateMenu(menu.children)
          }
        })
      }
      
      updateMenu(menuData)
      localStorage.setItem('userMenuList', JSON.stringify(menuData))
    }
  }
}
</script>

<style lang="less" scoped>
.analysis-container {
  padding: 0;
  background: transparent;
}

.chart-container {
  margin-bottom: 16px;
  background: white;
  border-radius: 16px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.04);
  overflow: hidden;
}

.data-grid-card {
  border-radius: 16px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.04);
  border: none;
  margin-bottom: 30px;
  
  :deep(.el-card__header) {
    padding: 20px 24px;
    border-bottom: 1px solid #e5e7eb;
    background: transparent;
  }
  
  :deep(.el-card__body) {
    padding: 24px;
  }
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.card-title {
  font-size: 18px;
  font-weight: 600;
  color: #1f2937;
  letter-spacing: 0.3px;
}

.progress-btn {
  color: #667eea;
  font-size: 14px;
  padding: 6px 12px;
  border-radius: 8px;
  transition: all 0.3s ease;
  
  &:hover {
    background: rgba(102, 126, 234, 0.08);
    color: #764ba2;
  }
}

.data-table {
  background: white;
  border-radius: 12px;
  overflow: hidden;
  border: 1px solid #e5e7eb;
}

.table-header {
  display: grid;
  gap: 12px;
  padding: 12px 16px;
  background: linear-gradient(135deg, #f9fafb 0%, #f3f4f6 100%);
  border-bottom: 2px solid #e5e7eb;
  font-weight: 600;
  font-size: 13px;
  color: #374151;
}

.table-header:not(.has-multiple-values) {
  grid-template-columns: 60px 1fr 120px 100px;
}

.table-header.has-multiple-values {
  grid-template-columns: 60px 1fr 120px 120px;
}

.table-body {
  max-height: calc(100vh - 300px);
  overflow-y: auto;
}

.table-row {
  display: grid;
  gap: 12px;
  padding: 14px 16px;
  border-bottom: 1px solid #f3f4f6;
  transition: all 0.2s ease;
  align-items: center;
  
  &:hover {
    background: #f9fafb;
  }
  
  &:last-child {
    border-bottom: none;
  }
}

.table-row:not(.has-multiple-values) {
  grid-template-columns: 60px 1fr 120px 100px;
}

.table-row.has-multiple-values {
  grid-template-columns: 60px 1fr 120px 120px;
}

.rank-badge {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 28px;
  height: 28px;
  border-radius: 6px;
  font-size: 13px;
  font-weight: 600;
  
  &.rank-first {
    background: linear-gradient(135deg, #fbbf24 0%, #f59e0b 100%);
    color: white;
  }
  
  &.rank-second {
    background: linear-gradient(135deg, #94a3b8 0%, #64748b 100%);
    color: white;
  }
  
  &.rank-third {
    background: linear-gradient(135deg, #f97316 0%, #ea580c 100%);
    color: white;
  }
  
  &.rank-normal {
    background: #f3f4f6;
    color: #6b7280;
  }
}

.td-name {
  font-size: 14px;
  font-weight: 500;
  color: #1f2937;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.value-number {
  font-size: 15px;
  font-weight: 700;
  color: #1f2937;
  
  &.secondary {
    color: #4a90e2;
  }
}

.td-percent {
  display: flex;
  align-items: center;
  gap: 8px;
}

.percent-text {
  font-size: 13px;
  font-weight: 600;
  color: #667eea;
  min-width: 45px;
}

.percent-bar {
  flex: 1;
  height: 6px;
  background: #e5e7eb;
  border-radius: 3px;
  overflow: hidden;
}

.percent-bar-fill {
  height: 100%;
  background: linear-gradient(90deg, #4a90e2 0%, #667eea 100%);
  border-radius: 3px;
  transition: width 0.3s ease;
}

.details-drawer {
  :deep(.el-drawer__header) {
    margin: 0;
    padding: 16px 20px;
    border-bottom: 1px solid #eef0f3;
  }
  
  :deep(.el-drawer__body) {
    padding: 16px 20px 24px 20px;
    overflow: auto;
  }
}

.drawer-body {
  min-height: 100%;
}

.list-container {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.data-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.list-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: white;
  border: 1px solid #e5e7eb;
  border-radius: 10px;
  padding: 14px 16px;
  transition: all 0.2s ease;
  
  &:hover {
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
    border-color: #a7c7ed;
    transform: translateY(-1px);
  }
}

.list-left {
  display: flex;
  align-items: center;
  gap: 12px;
  flex: 1;
  min-width: 0;
}

.list-rank {
  width: 32px;
  height: 32px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 14px;
  font-weight: 600;
  flex-shrink: 0;
  
  &.rank-first {
    background: linear-gradient(135deg, #fbbf24 0%, #f59e0b 100%);
    color: white;
  }
  
  &.rank-second {
    background: linear-gradient(135deg, #94a3b8 0%, #64748b 100%);
    color: white;
  }
  
  &.rank-third {
    background: linear-gradient(135deg, #f97316 0%, #ea580c 100%);
    color: white;
  }
  
  &.rank-normal {
    background: #f3f4f6;
    color: #6b7280;
  }
}

.list-info {
  flex: 1;
  min-width: 0;
}

.list-name {
  font-size: 14px;
  font-weight: 600;
  color: #1f2937;
  margin-bottom: 8px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.list-progress {
  width: 100%;
}

.list-progress-bar {
  width: 100%;
  height: 6px;
  background: #e5e7eb;
  border-radius: 3px;
  overflow: hidden;
}

.list-progress-fill {
  height: 100%;
  background: linear-gradient(90deg, #4a90e2 0%, #667eea 100%);
  border-radius: 3px;
  transition: width 0.3s ease;
}

.list-right {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-left: 16px;
}

.list-values {
  display: flex;
  flex-direction: column;
  gap: 6px;
  align-items: flex-end;
}

.list-value-item {
  display: flex;
  align-items: center;
  gap: 8px;
}

.value-label {
  font-size: 12px;
  color: #6b7280;
  font-weight: 400;
}

.value-number {
  font-size: 15px;
  font-weight: 700;
  color: #1f2937;
  min-width: 60px;
  text-align: right;
  
  &.secondary {
    color: #4a90e2;
  }
}

.value-percent {
  font-size: 15px;
  font-weight: 700;
  color: #667eea;
  min-width: 60px;
  text-align: right;
}

.list-row {
  display: grid;
  grid-template-columns: 36px 1fr auto auto;
  align-items: center;
  gap: 12px;
  padding: 10px 12px;
  background: #fff;
  border: 1px solid #eef0f3;
  border-radius: 10px;
  transition: all 0.2s ease;

  &:hover {
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.06);
    transform: translateY(-1px);
  }
}

.list-rank {
  width: 32px;
  height: 32px;
  border-radius: 8px;
  background: #f3f4f6;
  color: #6b7280;
  font-weight: 700;
  display: flex;
  align-items: center;
  justify-content: center;
}

.list-main {
  min-width: 0;
}

.list-name {
  font-size: 14px;
  font-weight: 600;
  color: #1f2937;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.list-bar {
  margin-top: 6px;
  height: 6px;
  background: #eef0f3;
  border-radius: 3px;
  overflow: hidden;
}

.list-bar-fill {
  height: 100%;
  background: linear-gradient(90deg, #8b5cf6 0%, #6366f1 100%);
  transition: width 0.3s ease;
}

.list-value {
  font-weight: 700;
  color: #374151;
}

.list-percent {
  font-size: 12px;
  color: #667eea;
}

.progress-content {
  padding: 20px 0;
}

.progress-info {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.progress-text {
  font-size: 15px;
  color: #374151;
  font-weight: 500;
}

.progress-percent {
  font-size: 18px;
  font-weight: 700;
  color: #667eea;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
}

:deep(.el-progress) {
  margin-bottom: 20px;
  
  .el-progress-bar__outer {
    border-radius: 10px;
    background-color: #f3f4f6;
  }
  
  .el-progress-bar__inner {
    border-radius: 10px;
    background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
    transition: width 0.3s ease;
  }
}

.progress-stats {
  display: flex;
  justify-content: space-around;
  padding: 16px;
  background: #f9fafb;
  border-radius: 12px;
  margin-top: 20px;
}

.stat-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  
  .stat-label {
    font-size: 13px;
    color: #6b7280;
    font-weight: 400;
  }
  
  .stat-value {
    font-size: 20px;
    font-weight: 700;
    color: #1f2937;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
  }
}

:deep(.el-dialog) {
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.12);
}

:deep(.el-dialog__header) {
  padding: 20px 24px;
  border-bottom: 1px solid #e5e7eb;
  margin: 0;
  background: #f9fafb;
}

:deep(.el-dialog__title) {
  font-size: 18px;
  font-weight: 600;
  color: #1f2937;
  letter-spacing: 0.3px;
}

:deep(.el-dialog__body) {
  padding: 24px;
}

:deep(.el-dialog__footer) {
  padding: 16px 24px;
  border-top: 1px solid #e5e7eb;
  background: #f9fafb;
  
  .el-button {
    border-radius: 8px;
    font-weight: 500;
  }
}
</style>
