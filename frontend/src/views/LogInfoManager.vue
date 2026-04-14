<template>
  <div class="log-manager">
    <!-- 数据统计卡片 -->
    <div class="statistics-cards">
      <el-row :gutter="20">
        <el-col :span="6">
          <el-card shadow="hover" class="stat-card">
            <div class="stat-content">
              <div class="stat-left">
                <div class="stat-icon"><i class="el-icon-document"></i></div>
                <div class="stat-title">总日志数</div>
              </div>
              <div class="stat-value">
                <count-to :startVal="0" :endVal="statistics.totalCount" :duration="2000">
                </count-to>
              </div>
            </div>
          </el-card>
        </el-col>
        <el-col :span="6">
          <el-card shadow="hover" class="stat-card">
            <div class="stat-content">
              <div class="stat-left">
                <div class="stat-icon"><i class="el-icon-user"></i></div>
                <div class="stat-title">活跃用户</div>
              </div>
              <div class="stat-value">
                <count-to :startVal="0" :endVal="statistics.userCount" :duration="2000">
                </count-to>
              </div>
            </div>
          </el-card>
        </el-col>
        <el-col :span="6">
          <el-card shadow="hover" class="stat-card">
            <div class="stat-content">
              <div class="stat-left">
                <div class="stat-icon"><i class="el-icon-view"></i></div>
                <div class="stat-title">今日访问</div>
              </div>
              <div class="stat-value">
                <count-to :startVal="0" :endVal="statistics.todayCount" :duration="2000">
                </count-to>
              </div>
            </div>
          </el-card>
        </el-col>
        <el-col :span="6">
          <el-card shadow="hover" class="stat-card">
            <div class="stat-content">
              <div class="stat-left">
                <div class="stat-icon"><i class="el-icon-edit"></i></div>
                <div class="stat-title">操作类型</div>
              </div>
              <div class="stat-value">
                <count-to :startVal="0" :endVal="statistics.actionTypes" :duration="2000">
                </count-to>
              </div>
            </div>
          </el-card>
        </el-col>
      </el-row>
    </div>

    <!-- 搜索和操作区域 -->
    <el-card class="operation-area" shadow="hover">
      <el-form :inline="true" :model="searchForm" class="search-form">
        <el-form-item label="页面名称">
          <el-input v-model="searchForm.pageName" placeholder="请输入页面名称" clearable></el-input>
        </el-form-item>
        <el-form-item label="操作类型">
          <el-select v-model="searchForm.action" placeholder="请选择操作类型" clearable>
            <el-option label="查看" value="VIEW"></el-option>
            <el-option label="新增" value="ADD"></el-option>
            <el-option label="编辑" value="EDIT"></el-option>
            <el-option label="删除" value="DELETE"></el-option>
            <el-option label="导出" value="EXPORT"></el-option>
            <el-option label="导入" value="IMPORT"></el-option>
            <el-option label="登录" value="LOGIN"></el-option>
            <el-option label="登出" value="LOGOUT"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="日期范围">
          <el-date-picker
            v-model="dateRange"
            type="daterange"
            range-separator="至"
            start-placeholder="开始日期"
            end-placeholder="结束日期"
            value-format="yyyy-MM-dd"
            @change="handleDateRangeChange"
          ></el-date-picker>
        </el-form-item>
        <el-form-item>
          <el-button size="medium" plain type="primary" @click="handleSearch">查询</el-button>
          <el-button size="medium" plain @click="resetSearch">重置</el-button>
        </el-form-item>
      </el-form>
      <div class="operation-buttons">
        <el-button plain size="medium" type="primary" @click="exportVisible = true">
          <i class="el-icon-download"></i> 导出数据
        </el-button>
        <el-button plain size="medium" icon="el-icon-refresh" @click="getList">刷新</el-button>
      </div>
    </el-card>

    <!-- 日志数据列表 -->
    <el-card class="table-card" shadow="hover">
      <el-table 
        :data="logList" 
        style="width: 100%"
        class="card-table"
      >
        <el-table-column prop="id" label="ID" width="80" show-overflow-tooltip></el-table-column>
        <el-table-column prop="username" label="用户名" width="120" show-overflow-tooltip></el-table-column>
        <el-table-column prop="pageName" label="页面名称" width="150" show-overflow-tooltip></el-table-column>
        <el-table-column prop="action" label="操作类型" width="100">
          <template slot-scope="scope">
            <el-tag :type="getActionType(scope.row.action)" size="small">
              {{ getActionLabel(scope.row.action) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="actionDesc" label="操作描述" show-overflow-tooltip></el-table-column>
        <el-table-column prop="requestMethod" label="请求方法" width="100">
          <template slot-scope="scope">
            <el-tag :type="getMethodType(scope.row.requestMethod)" size="small">
              {{ scope.row.requestMethod }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="ipAddress" label="IP地址" width="140" show-overflow-tooltip></el-table-column>
        <el-table-column prop="createdAt" label="操作时间" width="200">
          <template slot-scope="scope">
            {{ formatDateTime(scope.row.createdAt) }}
          </template>
        </el-table-column>
        <el-table-column label="操作" width="120" >
          <template slot-scope="scope">
            <el-button type="text" size="small" icon="el-icon-delete" class="delete-btn" @click="handleDelete(scope.row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
      <!-- 分页 -->
      <pagination v-show="total > 0" :total="total" :page.sync="queryParams.currentPage" :limit.sync="queryParams.size" @pagination="getList" />
    </el-card>

    <!-- 导出数据 弹出栏 -->
    <el-dialog title="导出数据" :visible.sync="exportVisible" width="600px" :close-on-click-modal="false" append-to-body>
      <div class="export-data">
        <el-button type="primary" plain @click="exportTable('xlsx')" :disabled="isExporting">
          <i class="el-icon-document"></i> EXCEL格式
        </el-button>
        <el-button type="primary" plain @click="exportTable('csv')" :disabled="isExporting">
          <i class="el-icon-document"></i> CSV格式
        </el-button>
        <el-button type="primary" plain @click="exportTable('txt')" :disabled="isExporting">
          <i class="el-icon-document"></i> TXT格式
        </el-button>
      </div>
      <div v-if="isExporting" class="export-progress">
        <el-progress :percentage="exportProgress" :status="exportProgress === 100 ? 'success' : null" :stroke-width="20"></el-progress>
        <div class="progress-text">{{ exportProgressText }}</div>
      </div>
      <div class="hints">提示：请选择要导出数据的格式</div>
    </el-dialog>
  </div>
</template>

<script>
import Request from '@/utils/request'
import Pagination from '@/components/Pagination/index.vue'
import CountTo from 'vue-count-to'
import excel from '@/utils/excel.js'

export default {
  name: 'LogInfoManager',
  inject: ['userInfo'],
  components: {
    Pagination,
    CountTo
  },
  data() {
    return {
      // 搜索表单
      searchForm: {
        username: '',
        pageName: '',
        action: ''
      },
      // 日期范围
      dateRange: null,
      // 查询参数
      queryParams: {
        currentPage: 1,
        size: 10
      },
      // 日志列表
      logList: [],
      // 总数
      total: 0,
      // 统计数据
      statistics: {
        totalCount: 0,
        userCount: 0,
        todayCount: 0,
        actionTypes: 0
      },
      // 导出数据弹出框显示/隐藏
      exportVisible: false,
      // 导出进度
      exportProgress: 0,
      // 是否正在导出
      isExporting: false,
      // 导出进度文本
      exportProgressText: ''
    }
  },
  created() {
    this.getList()
    this.getStatistics()
  },
  methods: {
    // 获取日志列表
    async getList() {
      try {
        const params = {
          ...this.queryParams,
          username: this.searchForm.username,
          pageName: this.searchForm.pageName,
          action: this.searchForm.action
        }
        const res = await Request.get('/actionLog/page', { params })
        if (res.code === '0') {
          this.logList = res.data.records || []
          this.total = res.data.total || 0
        }
      } catch (error) {
        console.error('获取日志列表失败:', error)
        this.logList = []
        this.total = 0
      }
    },
    // 获取统计数据
    async getStatistics() {
      try {
        // 获取总日志数
        const totalRes = await Request.get('/actionLog/page', { 
          params: { currentPage: 1, size: 1 } 
        })
        if (totalRes.code === '0') {
          this.statistics.totalCount = totalRes.data.total || 0
        }

        // 获取今日日志数
        const today = new Date().toISOString().split('T')[0]
        const todayRes = await Request.get('/actionLog/page', {
          params: { currentPage: 1, size: 1 }
        })
        // 这里可以根据实际需求统计今日数据
        this.statistics.todayCount = this.logList.filter(log => {
          const logDate = log.createdAt ? log.createdAt.split(' ')[0] : ''
          return logDate === today
        }).length

        // 统计活跃用户数（去重）
        const users = new Set(this.logList.map(log => log.userId).filter(Boolean))
        this.statistics.userCount = users.size

        // 统计操作类型数（去重）
        const actions = new Set(this.logList.map(log => log.action).filter(Boolean))
        this.statistics.actionTypes = actions.size
      } catch (error) {
        console.error('获取统计数据失败:', error)
      }
    },
    // 搜索
    handleSearch() {
      this.queryParams.currentPage = 1
      this.getList()
    },
    // 重置搜索
    resetSearch() {
      this.searchForm = {
        username: '',
        pageName: '',
        action: ''
      }
      this.dateRange = null
      this.handleSearch()
    },
    // 日期范围变化
    handleDateRangeChange(val) {
      // 可以根据日期范围过滤，这里简化处理
      if (val && val.length === 2) {
        // 可以在后端添加日期范围查询，这里暂时只在前端过滤
        this.handleSearch()
      }
    },
    // 删除单条日志
    handleDelete(row) {
      this.$confirm('确认删除该日志记录?', '提示', {
        type: 'warning'
      }).then(async () => {
        try {
          const res = await Request.delete(`/actionLog/${row.id}`)
          if (res.code === '0') {
            this.$message.success('删除成功')
            this.getList()
            this.getStatistics()
          } else {
            this.$message.error(res.msg || '删除失败')
          }
        } catch (error) {
          this.$message.error('删除失败')
        }
      }).catch(() => {})
    },
    // 获取操作类型标签
    getActionLabel(action) {
      const labels = {
        'VIEW': '查看',
        'ADD': '新增',
        'EDIT': '编辑',
        'DELETE': '删除',
        'EXPORT': '导出',
        'IMPORT': '导入',
        'LOGIN': '登录',
        'LOGOUT': '登出',
        'POST': '提交'
      }
      return labels[action] || action
    },
    // 获取操作类型颜色
    getActionType(action) {
      const types = {
        'VIEW': 'info',
        'ADD': 'success',
        'EDIT': 'warning',
        'DELETE': 'danger',
        'EXPORT': 'primary',
        'IMPORT': 'primary',
        'LOGIN': 'success',
        'LOGOUT': 'info'
      }
      return types[action] || ''
    },
    // 获取请求方法类型颜色
    getMethodType(method) {
      const types = {
        'GET': 'info',
        'POST': 'success',
        'PUT': 'warning',
        'DELETE': 'danger',
        'PATCH': 'warning'
      }
      return types[method] || ''
    },
    // 格式化日期时间
    formatDateTime(dateTime) {
      if (!dateTime) return ''
      // 如果已经是字符串格式，直接返回
      if (typeof dateTime === 'string') {
        // 如果包含 T，说明是 ISO 格式，需要转换
        if (dateTime.includes('T')) {
          const date = new Date(dateTime)
          const year = date.getFullYear()
          const month = String(date.getMonth() + 1).padStart(2, '0')
          const day = String(date.getDate()).padStart(2, '0')
          const hours = String(date.getHours()).padStart(2, '0')
          const minutes = String(date.getMinutes()).padStart(2, '0')
          const seconds = String(date.getSeconds()).padStart(2, '0')
          return `${year}-${month}-${day} ${hours}:${minutes}:${seconds}`
        }
        // 如果已经是 yyyy-MM-dd HH:mm:ss 格式，直接返回
        if (/^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$/.test(dateTime)) {
          return dateTime
        }
        // 如果是 yyyy-MM-dd HH:mm:ss.SSS 格式，去掉毫秒
        if (/^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d+$/.test(dateTime)) {
          return dateTime.split('.')[0]
        }
        return dateTime
      }
      // 如果是 Date 对象
      if (dateTime instanceof Date) {
        const year = dateTime.getFullYear()
        const month = String(dateTime.getMonth() + 1).padStart(2, '0')
        const day = String(dateTime.getDate()).padStart(2, '0')
        const hours = String(dateTime.getHours()).padStart(2, '0')
        const minutes = String(dateTime.getMinutes()).padStart(2, '0')
        const seconds = String(dateTime.getSeconds()).padStart(2, '0')
        return `${year}-${month}-${day} ${hours}:${minutes}:${seconds}`
      }
      return ''
    },
    // 获取所有数据（不分页）
    async getAllData(onProgress) {
      try {
        const allData = []
        let currentPage = 1
        const pageSize = 1000
        let totalCount = 0
        let isFirstPage = true
        
        while (true) {
          const params = {
            currentPage,
            size: pageSize,
            username: this.searchForm.username,
            pageName: this.searchForm.pageName,
            action: this.searchForm.action
          }
          
          const res = await Request.get('/actionLog/page', { params })
          if (res.code === '0' && res.data && res.data.records) {
            if (isFirstPage) {
              totalCount = res.data.total || res.data.records.length || 0
              isFirstPage = false
            }
            
            const records = res.data.records || []
            if (records.length === 0) {
              break
            }
            
            allData.push(...records)
            
            if (onProgress && totalCount > 0) {
              const progress = Math.min(Math.round((allData.length / totalCount) * 50), 50)
              onProgress(progress, `正在获取数据: ${allData.length}/${totalCount}`)
            } else if (onProgress) {
              onProgress(5, `正在获取数据: ${allData.length} 条...`)
            }
            
            if (records.length < pageSize || (totalCount > 0 && allData.length >= totalCount)) {
              break
            }
            currentPage++
          } else {
            break
          }
        }
        
        return allData
      } catch (error) {
        console.error('获取所有数据失败:', error)
        return []
      }
    },
    // 导出数据
    async exportTable(type) {
      try {
        this.isExporting = true
        this.exportProgress = 0
        this.exportProgressText = '准备导出...'
        
        const updateProgress = (progress, text) => {
          this.exportProgress = progress
          this.exportProgressText = text
        }
        
        updateProgress(5, '正在获取数据...')
        const allData = await this.getAllData(updateProgress)
        
        if (allData.length === 0) {
          this.isExporting = false
          this.exportProgress = 0
          this.exportProgressText = ''
          this.$message.warning('暂无数据可导出')
          return
        }
        
        updateProgress(55, '正在格式化数据...')
        const exportData = []
        const totalItems = allData.length
        for (let i = 0; i < allData.length; i++) {
          const item = allData[i]
          exportData.push({
            id: item.id || '',
            username: item.username || '',
            pageName: item.pageName || '',
            action: this.getActionLabel(item.action) || '',
            actionDesc: item.actionDesc || '',
            requestMethod: item.requestMethod || '',
            requestUrl: item.requestUrl || '',
            ipAddress: item.ipAddress || '',
            createdAt: this.formatDateTime(item.createdAt) || ''
          })
          
          if ((i + 1) % 100 === 0 || i === allData.length - 1) {
            const progress = 55 + Math.round(((i + 1) / totalItems) * 25)
            updateProgress(progress, `正在格式化数据: ${i + 1}/${totalItems}`)
            await new Promise(resolve => setTimeout(resolve, 0))
          }
        }
        
        updateProgress(85, '正在生成文件...')
        await new Promise(resolve => setTimeout(resolve, 100))
        updateProgress(95, '正在保存文件...')
        
        const params = {
          header: ['ID', '用户名', '页面名称', '操作类型', '操作描述', '请求方法', '请求URL', 'IP地址', '操作时间'],
          key: ['id', 'username', 'pageName', 'action', 'actionDesc', 'requestMethod', 'requestUrl', 'ipAddress', 'createdAt'],
          data: exportData,
          autoWidth: true,
          fileName: '行为日志表',
          bookType: type
        }
        
        excel.exportDataToExcel(params)
        
        updateProgress(100, '导出完成！')
        await new Promise(resolve => setTimeout(resolve, 500))
        
        this.isExporting = false
        this.exportProgress = 0
        this.exportProgressText = ''
        this.exportVisible = false
        this.$message.success('导出成功')
      } catch (error) {
        console.error('导出失败:', error)
        this.isExporting = false
        this.exportProgress = 0
        this.exportProgressText = ''
        this.$message.error('导出失败，请稍后重试')
      }
    }
  }
}
</script>

<style lang="less" scoped>
.log-manager {
  padding: 12px;
  background: linear-gradient(to bottom, #f5f7fa 0%, #ffffff 100%);
  min-height: calc(100vh - 70px);
  position: relative;

  &::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background-image: 
      radial-gradient(circle at 20% 50%, rgba(102, 126, 234, 0.03) 0%, transparent 50%),
      radial-gradient(circle at 80% 80%, rgba(118, 75, 162, 0.03) 0%, transparent 50%);
    pointer-events: none;
    z-index: 0;
  }

  > * {
    position: relative;
    z-index: 1;
  }
}

.statistics-cards {
  margin-bottom: 24px;
}

.stat-card {
  border-radius: 12px;
  transition: all 0.3s ease;
  border: none;
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.9) 0%, rgba(255, 255, 255, 0.95) 100%);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
  position: relative;
  overflow: hidden;
  backdrop-filter: blur(10px);

  &::before {
    display: none;
  }

  &:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
  }

  :deep(.el-card__body) {
    padding: 0;
  }
}

.stat-content {
  padding: 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.stat-left {
  display: flex;
  align-items: center;
  gap: 14px;
}

.stat-icon {
  font-size: 28px;
  color: #4a90e2;
  opacity: 0.9;
  width: 52px;
  height: 52px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 12px;
  background: linear-gradient(135deg, rgba(74, 144, 226, 0.1) 0%, rgba(74, 144, 226, 0.05) 100%);
  transition: all 0.3s ease;
}

.stat-card:nth-child(1) .stat-icon {
  background: linear-gradient(135deg, rgba(74, 144, 226, 0.12) 0%, rgba(74, 144, 226, 0.06) 100%);
  color: #4a90e2;
}

.stat-card:nth-child(2) .stat-icon {
  background: linear-gradient(135deg, rgba(102, 126, 234, 0.12) 0%, rgba(102, 126, 234, 0.06) 100%);
  color: #667eea;
}

.stat-card:nth-child(3) .stat-icon {
  background: linear-gradient(135deg, rgba(139, 92, 246, 0.12) 0%, rgba(139, 92, 246, 0.06) 100%);
  color: #8b5cf6;
}

.stat-card:nth-child(4) .stat-icon {
  background: linear-gradient(135deg, rgba(236, 72, 153, 0.12) 0%, rgba(236, 72, 153, 0.06) 100%);
  color: #ec4899;
}

.stat-card:hover .stat-icon {
  transform: scale(1.05);
}

.stat-title {
  font-size: 14px;
  color: #6b7280;
  font-weight: 500;
  letter-spacing: 0.2px;
}

.stat-value {
  font-size: 28px;
  font-weight: 700;
  color: #1f2937;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
  letter-spacing: 0.5px;
  
  &::after {
    display: none;
  }
}

.operation-area {
  background: rgba(255, 255, 255, 0.95);
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
  margin-bottom: 24px;
  padding: 24px;
  border: 1px solid rgba(0, 0, 0, 0.06);
  backdrop-filter: blur(10px);

  :deep(.el-card__body) {
    padding: 0;
  }
}

.search-form {
  margin-bottom: 0;
  padding-bottom: 16px;
  border-bottom: 1px solid #f3f4f6;
  
  :deep(.el-form-item) {
    margin-bottom: 0;
    margin-right: 20px;
    
    &:last-child {
      margin-right: 0;
    }
  }
  
  :deep(.el-form-item__label) {
    color: #374151;
    font-weight: 500;
    font-size: 14px;
    padding-right: 8px;
  }
}

.operation-buttons {
  margin-top: 16px;
  display: flex;
  gap: 12px;
  padding-top: 16px;
}

.table-card {
  border-radius: 16px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.04);
  padding-bottom: 20px;
  background: white;
  border: none;

  :deep(.el-card__header) {
    background: transparent;
  }

  :deep(.el-card__body) {
    padding: 20px;
  }
}

.operation-buttons {
  margin-top: 16px;
  display: flex;
  gap: 12px;
}

:deep(.el-table) {
  border-radius: 12px;
  overflow: visible;
  box-shadow: none;
  border: none;
  background: transparent;

  .el-table__header-wrapper {
    th {
      background-color: transparent;
      font-weight: 600;
      color: #374151;
      padding: 16px 12px;
      font-size: 14px;
      border-bottom: none;
    }
  }

  .el-table__body-wrapper {
    .el-table__body {
      tr {
        background: white;
        border-radius: 8px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
        transition: all 0.3s ease;
        
        &:hover {
          transform: translateY(-2px);
          box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
          background: white;
        }
        
        td {
          padding: 16px 12px;
          color: #4b5563;
          font-size: 14px;
          border-bottom: none;
          background: white;
        }
        
        &:first-child td:first-child {
          border-top-left-radius: 8px;
        }
        
        &:first-child td:last-child {
          border-top-right-radius: 8px;
        }
        
        &:last-child td:first-child {
          border-bottom-left-radius: 8px;
        }
        
        &:last-child td:last-child {
          border-bottom-right-radius: 8px;
        }
      }
    }
  }
  
  &::before {
    display: none;
  }
  
  .el-table__header,
  .el-table__body {
    border: none;
  }
  
  .el-table__header th,
  .el-table__body td {
    border: none;
  }
}

.card-table {
  :deep(.el-table__body-wrapper) {
    padding: 12px 0;
    
    .el-table__body {
      border-collapse: separate;
      border-spacing: 0 12px;
      
      tr {
        background: white;
        border-radius: 8px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
        transition: all 0.3s ease;
        
        &:hover {
          transform: translateY(-2px);
          box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
        }
        
        td {
          border-bottom: none;
          background: white;
          padding: 16px 12px;
          
          &:first-child {
            border-top-left-radius: 8px;
            border-bottom-left-radius: 8px;
          }
          
          &:last-child {
            border-top-right-radius: 8px;
            border-bottom-right-radius: 8px;
          }
        }
      }
    }
  }
  
  :deep(.el-table__header-wrapper) {
    .el-table__header {
      border-collapse: separate;
      
      th {
        background-color: transparent;
        border-bottom: none;
        padding: 16px 12px;
      }
    }
  }
}

.delete-btn {
  color: #ef4444;
  margin-left: 12px;
  transition: color 0.3s ease;
  
  &:hover:not(:disabled) {
    color: #dc2626;
  }
  
  &:disabled {
    color: #d1d5db;
    cursor: not-allowed;
  }
}

:deep(.el-button--text) {
  padding: 0 8px;
  font-size: 14px;
  transition: all 0.3s ease;

  &:hover {
    background-color: rgba(102, 126, 234, 0.08);
  }
}

:deep(.el-button) {
  border-radius: 8px;
  font-weight: 500;
  transition: all 0.3s ease;

  // 主要按钮 - 浅色风格
  &.el-button--primary.is-plain {
    border-color: rgba(74, 144, 226, 0.3);
    color: #4a90e2;
    background: rgba(74, 144, 226, 0.08);

    &:hover:not(:disabled) {
      background: rgba(74, 144, 226, 0.15);
      border-color: rgba(74, 144, 226, 0.4);
      color: #3d7bc8;
      transform: translateY(-1px);
      box-shadow: 0 2px 8px rgba(74, 144, 226, 0.2);
    }

    &:disabled {
      border-color: rgba(74, 144, 226, 0.15);
      color: rgba(74, 144, 226, 0.4);
      background: rgba(74, 144, 226, 0.04);
      cursor: not-allowed;
    }
  }

  // 普通按钮 - 浅色风格
  &.el-button--default.is-plain {
    border-color: rgba(0, 0, 0, 0.15);
    color: #6b7280;
    background: rgba(0, 0, 0, 0.04);

    &:hover:not(:disabled) {
      background: rgba(0, 0, 0, 0.08);
      border-color: rgba(0, 0, 0, 0.2);
      color: #374151;
      transform: translateY(-1px);
      box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    }

    &:disabled {
      border-color: rgba(0, 0, 0, 0.08);
      color: rgba(0, 0, 0, 0.25);
      background: rgba(0, 0, 0, 0.02);
      cursor: not-allowed;
    }
  }

  // 普通按钮（非plain）- 浅色风格
  &.el-button--default:not(.is-plain) {
    border-color: rgba(0, 0, 0, 0.15);
    color: #6b7280;
    background: rgba(0, 0, 0, 0.04);

    &:hover:not(:disabled) {
      background: rgba(0, 0, 0, 0.08);
      border-color: rgba(0, 0, 0, 0.2);
      color: #374151;
      transform: translateY(-1px);
      box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    }
  }

  // 成功按钮 - 浅色风格
  &.el-button--success.is-plain {
    border-color: rgba(16, 185, 129, 0.3);
    color: #10b981;
    background: rgba(16, 185, 129, 0.08);

    &:hover:not(:disabled) {
      background: rgba(16, 185, 129, 0.15);
      border-color: rgba(16, 185, 129, 0.4);
      color: #059669;
      transform: translateY(-1px);
      box-shadow: 0 2px 8px rgba(16, 185, 129, 0.2);
    }
  }

  // 危险按钮 - 浅色风格
  &.el-button--danger.is-plain {
    border-color: rgba(239, 68, 68, 0.3);
    color: #ef4444;
    background: rgba(239, 68, 68, 0.08);

    &:hover:not(:disabled) {
      background: rgba(239, 68, 68, 0.15);
      border-color: rgba(239, 68, 68, 0.4);
      color: #dc2626;
      transform: translateY(-1px);
      box-shadow: 0 2px 8px rgba(239, 68, 68, 0.2);
    }
  }

  // 主要按钮（非plain）- 浅色风格
  &.el-button--primary:not(.is-plain) {
    background: rgba(74, 144, 226, 0.2);
    border-color: rgba(74, 144, 226, 0.3);
    color: #4a90e2;

    &:hover:not(:disabled) {
      background: rgba(74, 144, 226, 0.3);
      border-color: rgba(74, 144, 226, 0.4);
      color: #3d7bc8;
      transform: translateY(-1px);
      box-shadow: 0 2px 8px rgba(74, 144, 226, 0.2);
    }
  }

  // 所有尺寸统一样式
  &.el-button--mini,
  &.el-button--small,
  &.el-button--medium {
    border-radius: 6px;
    font-weight: 500;
  }
}

:deep(.el-button--text) {
  padding: 0 8px;
  font-size: 14px;
  transition: all 0.3s ease;
  color: #6b7280;

  &:hover {
    background-color: rgba(74, 144, 226, 0.1);
    color: #4a90e2;
  }
}

.delete-btn {
  color: #ef4444;
  margin-left: 12px;
  transition: color 0.3s ease;

  &:hover:not(:disabled) {
    color: #dc2626;
    background-color: rgba(239, 68, 68, 0.1);
  }
  
  &:disabled {
    color: #d1d5db;
    cursor: not-allowed;
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

.export-data {
  display: flex;
  justify-content: space-around;
  margin-bottom: 20px;
  gap: 12px;
}

.export-progress {
  margin: 20px 0;
  padding: 20px;
  background: #f9fafb;
  border-radius: 8px;
  
  .progress-text {
    text-align: center;
    margin-top: 12px;
    color: #374151;
    font-size: 14px;
    font-weight: 500;
  }
}

.hints {
  text-align: center;
  color: #6b7280;
  font-size: 13px;
}
</style>
