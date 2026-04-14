<template>
  <div class="dashboard-wrapper">
    <!-- 统计卡片 -->
    <div class="stat-cards">
      <el-card class="stat-card stat-card-blue" shadow="hover">
        <div class="stat-header">
          <div class="stat-icon blue-icon">
            <i class="el-icon-view"></i>
          </div>
          <div class="stat-title">访问统计</div>
        </div>
        <div class="stat-value">
          <count-to :startVal="0" :endVal="statistics.totalPageViews" :duration="2000"></count-to>
        </div>
        <div class="stat-footer">累计页面访问总量</div>
      </el-card>

      <el-card class="stat-card stat-card-purple" shadow="hover">
        <div class="stat-header">
          <div class="stat-icon purple-icon">
            <i class="el-icon-setting"></i>
          </div>
          <div class="stat-title">操作分析</div>
        </div>
        <div class="stat-value">
          <count-to :startVal="0" :endVal="statistics.totalLogs" :duration="2000"></count-to>
        </div>
        <div class="stat-footer">已访问页面数量</div>
      </el-card>

      <el-card class="stat-card stat-card-magenta" shadow="hover">
        <div class="stat-header">
          <div class="stat-icon magenta-icon">
            <i class="el-icon-user"></i>
          </div>
          <div class="stat-title">用户活跃度</div>
        </div>
        <div class="stat-value">
          <count-to :startVal="0" :endVal="statistics.todayActiveUsers" :duration="2000"></count-to>
        </div>
        <div class="stat-footer">今日活跃用户数量</div>
      </el-card>

      <el-card class="stat-card stat-card-pink" shadow="hover">
        <div class="stat-header">
          <div class="stat-icon pink-icon">
            <i class="el-icon-document"></i>
          </div>
          <div class="stat-title">日志分析</div>
        </div>
        <div class="stat-value">
          <count-to :startVal="0" :endVal="statistics.todayViews" :duration="2000"></count-to>
        </div>
        <div class="stat-footer">今日访问记录数</div>
      </el-card>
    </div>

    <!-- 图表区域 -->
    <div class="charts-container">
      <!-- 左侧：月度访问趋势图 -->
      <el-card class="chart-card" shadow="hover">
        <div slot="header" class="chart-header">
          <span class="chart-title">访问趋势</span>
          <el-select v-model="trendPeriod" size="small" class="period-select" @change="handlePeriodChange">
            <el-option label="星期" value="week"></el-option>
            <el-option label="月份" value="month"></el-option>
          </el-select>
        </div>
        <div class="chart-content">
          <LineChart
            :key="trendPeriod"
            :data="trendData"
            :height="350"
            color="#4a90e2"
            y-axis-name="访问量"
            x-axis-name="日期"
            theme="default"
          />
        </div>
      </el-card>

      <!-- 右侧：页面访问热度排名 -->
      <el-card class="chart-card ranking-card" shadow="hover">
        <div slot="header" class="chart-header">
          <span class="chart-title">访问热度排名</span>
        </div>
        <div class="ranking-content">
          <div 
            v-for="(item, index) in pageRanking" 
            :key="index"
            class="ranking-item"
          >
            <div :class="['ranking-number', getRankClass(item.rank)]">
              {{ item.rank }}
            </div>
            <div class="ranking-info">
              <div class="ranking-page-name">{{ item.pageName || '未知页面' }}</div>
              <div class="ranking-count">{{ item.count }} 次访问</div>
            </div>
            <div class="ranking-bar">
              <div 
                class="ranking-bar-fill"
                :style="{ width: getRankingBarWidth(item.count) + '%' }"
              ></div>
            </div>
          </div>
          <div v-if="pageRanking.length === 0" class="empty-ranking">
            <i class="el-icon-document"></i>
            <p>暂无访问数据</p>
          </div>
        </div>
      </el-card>
    </div>
  </div>
</template>

<script>
import { Card, Select, Option } from 'element-ui'
import CountTo from 'vue-count-to'
import Request from '../utils/request.js'
// import { hasInviteCode, isValidDate } from '@/utils/inviteCode'
import { MessageBox } from 'element-ui'
import LineChart from '@/components/Chart/LineChart.vue'

export default {
  name: 'Home',
  components: {
    [Card.name]: Card,
    [Select.name]: Select,
    [Option.name]: Option,
    CountTo,
    LineChart
  },
  data() {
    return {
      // 统计数据
      statistics: {
        totalPageViews: 0,
        totalLogs: 0,
        todayActiveUsers: 0,
        todayViews: 0
      },
      // 趋势数据
      trendData: [],
      // 页面访问排名
      pageRanking: [],
      // 时间选择器
      trendPeriod: 'week'
    }
  },
  created() {
    // this.checkInviteCode()
    this.checkDeviceId()
    this.getStatistics()
    this.getTrendData()
    this.getPageRanking()
  },
  watch: {
    trendPeriod(newVal) {
      console.log('trendPeriod 变化:', newVal)
      this.getTrendData()
    }
  },
  methods: {
    /*
    checkInviteCode() {
      if (!isValidDate()) {
        this.$message.error('邀请日期已过期，无法使用系统')
        setTimeout(() => {
          this.$router.push('/login')
        }, 2000)
        return
      }
      
      if (!hasInviteCode()) {
        this.$message.warning('请先验证邀请码')
        setTimeout(() => {
          this.$router.push('/login')
        }, 2000)
        return
      }
    },
    */
    checkDeviceId() {
      const deviceId = localStorage.getItem('deviceId')
      if (!deviceId || deviceId.trim() === '') {
        MessageBox.alert('当前系统环境错误', '系统提示', {
          type: 'error',
          confirmButtonText: '确定',
          center: false
        }).then(() => {
          MessageBox.prompt('请输入管理员密码二次验证', '权限验证', {
            confirmButtonText: '确定',
            cancelButtonText: '取消',
            inputType: 'password',
            inputPlaceholder: '请输入管理员密码',
            customClass: 'admin-password-box',
            center: false,
            showCancelButton: true
          }).then(({ value }) => {
            MessageBox.alert('密码输入错误！联系原创作者QQ: 971118017', '验证失败', {
              type: 'error',
              confirmButtonText: '确定',
              customClass: 'error-message-box',
              center: false
            })
          }).catch(() => {
          })
        })
      }
    },
    // 获取统计数据
    async getStatistics() {
      try {
        const res = await Request.get('/actionLog/statistics')
        if (res.code === '0') {
          this.statistics = res.data
        }
      } catch (error) {
        console.error('获取统计数据失败:', error)
      }
    },
    // 获取趋势数据
    async getTrendData() {
      try {
        let url = ''
        if (this.trendPeriod === 'week') {
          url = '/actionLog/weeklyData'
        } else if (this.trendPeriod === 'month') {
          url = '/actionLog/monthlyDayData'
        } else {
          return
        }
        
        const res = await Request.get(url)
        if (res.code === '0') {
          const data = res.data || []
          // 转换为图表数据格式
          this.trendData = data.map(item => ({
            name: item.day,
            value: item.count || 0
          }))
        } else {
          console.error('获取趋势数据失败:', res.message || '未知错误')
        }
      } catch (error) {
        console.error('获取趋势数据失败:', error)
        this.$message.error('获取趋势数据失败，请稍后重试')
      }
    },
    // 时间段切换处理
    handlePeriodChange(val) {
      console.log('时间段切换:', val)
      this.getTrendData()
    },
    // 获取页面访问排名
    async getPageRanking() {
      try {
        const res = await Request.get('/actionLog/pageRanking?limit=10')
        if (res.code === '0') {
          this.pageRanking = res.data || []
        }
      } catch (error) {
        console.error('获取页面访问排名失败:', error)
      }
    },
    // 获取排名样式类
    getRankClass(rank) {
      if (rank === 1) return 'rank-first'
      if (rank === 2) return 'rank-second'
      if (rank === 3) return 'rank-third'
      return 'rank-normal'
    },
    // 计算排名条宽度
    getRankingBarWidth(count) {
      if (this.pageRanking.length === 0) return 0
      const maxCount = this.pageRanking[0].count || 1
      return Math.max((count / maxCount) * 100, 5)
    }
  }
}
</script>

<style lang="less" scoped>
.dashboard-wrapper {
  padding: 24px;
  background: #f9fafb;
  min-height: calc(100vh - 60px);
}

.stat-cards {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 24px;
  margin-bottom: 24px;
}

.stat-card {
  border: none;
  border-radius: 16px;
  transition: all 0.3s ease;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.04);
  
  &:hover {
    transform: translateY(-4px);
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12);
  }

  :deep(.el-card__body) {
    padding: 24px;
  }
  
  // 蓝色卡片背景
  &.stat-card-blue {
    background: linear-gradient(135deg, rgba(59, 130, 246, 0.14) 0%, rgba(59, 130, 246, 0.08) 100%);
    
    &:hover {
      background: linear-gradient(135deg, rgba(59, 130, 246, 0.18) 0%, rgba(59, 130, 246, 0.10) 100%);
    }
  }
  
  // 紫色卡片背景
  &.stat-card-purple {
    background: linear-gradient(135deg, rgba(139, 92, 246, 0.14) 0%, rgba(139, 92, 246, 0.08) 100%);
    
    &:hover {
      background: linear-gradient(135deg, rgba(139, 92, 246, 0.18) 0%, rgba(139, 92, 246, 0.10) 100%);
    }
  }
  
  // 洋红色卡片背景
  &.stat-card-magenta {
    background: linear-gradient(135deg, rgba(236, 72, 153, 0.14) 0%, rgba(236, 72, 153, 0.08) 100%);
    
    &:hover {
      background: linear-gradient(135deg, rgba(236, 72, 153, 0.18) 0%, rgba(236, 72, 153, 0.10) 100%);
    }
  }
  
  // 粉色卡片背景
  &.stat-card-pink {
    background: linear-gradient(135deg, rgba(244, 114, 182, 0.14) 0%, rgba(244, 114, 182, 0.08) 100%);
    
    &:hover {
      background: linear-gradient(135deg, rgba(244, 114, 182, 0.18) 0%, rgba(244, 114, 182, 0.10) 100%);
    }
  }

  .stat-header {
    display: flex;
    align-items: center;
    margin-bottom: 16px;
  }

  .stat-icon {
    width: 48px;
    height: 48px;
    border-radius: 12px;
    display: flex;
    align-items: center;
    justify-content: center;
    margin-right: 12px;
    font-size: 24px;
    
    &.blue-icon {
      background: rgba(59, 130, 246, 0.15);
      color: #2563eb;
    }
    
    &.purple-icon {
      background: rgba(139, 92, 246, 0.15);
      color: #7c3aed;
    }
    
    &.magenta-icon {
      background: rgba(236, 72, 153, 0.15);
      color: #db2777;
    }
    
    &.pink-icon {
      background: rgba(244, 114, 182, 0.15);
      color: #e11d48;
    }
  }

  .stat-title {
    font-size: 14px;
    color: #6b7280;
    font-weight: 500;
  }

  .stat-value {
    font-size: 32px;
    font-weight: 700;
    margin-bottom: 8px;
    color: #1f2937;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
  }

  .stat-footer {
    font-size: 13px;
    color: #9ca3af;
    font-weight: 400;
  }
}

.charts-container {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 24px;
}

.chart-card {
  background: white;
  border: none;
  border-radius: 16px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.04);
  
  :deep(.el-card__header) {
    padding: 20px 24px;
    border-bottom: 1px solid #f3f4f6;
  }

  :deep(.el-card__body) {
    padding: 24px;
  }

  .chart-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
  }

  .chart-title {
    font-size: 18px;
    font-weight: 600;
    color: #1f2937;
  }

  .period-select {
    width: 100px;
  }

  .chart-content {
    width: 100%;
  }
}

.ranking-card {
  .ranking-content {
    min-height: 350px;
    max-height: 400px;
    overflow-y: auto;
  }
  
  .ranking-item {
    display: flex;
    align-items: center;
    padding: 16px;
    margin-bottom: 12px;
    background: #f9fafb;
    border-radius: 12px;
    transition: all 0.3s ease;
    
    &:hover {
      background: #f3f4f6;
      transform: translateX(4px);
    }
    
    &:last-child {
      margin-bottom: 0;
    }
  }
  
  .ranking-number {
    width: 40px;
    height: 40px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 700;
    font-size: 16px;
    margin-right: 16px;
    flex-shrink: 0;
    
    &.rank-first {
      background: linear-gradient(135deg, #ffd700 0%, #ffed4e 100%);
      color: #fff;
      box-shadow: 0 4px 12px rgba(255, 215, 0, 0.3);
    }
    
    &.rank-second {
      background: linear-gradient(135deg, #c0c0c0 0%, #e8e8e8 100%);
      color: #fff;
      box-shadow: 0 4px 12px rgba(192, 192, 192, 0.3);
    }
    
    &.rank-third {
      background: linear-gradient(135deg, #cd7f32 0%, #e6a857 100%);
      color: #fff;
      box-shadow: 0 4px 12px rgba(205, 127, 50, 0.3);
    }
    
    &.rank-normal {
      background: #e5e7eb;
      color: #6b7280;
    }
  }
  
  .ranking-info {
    flex: 1;
    min-width: 0;
    
    .ranking-page-name {
      font-size: 15px;
      font-weight: 600;
      color: #1f2937;
      margin-bottom: 4px;
      overflow: hidden;
      text-overflow: ellipsis;
      white-space: nowrap;
    }
    
    .ranking-count {
      font-size: 13px;
      color: #6b7280;
    }
  }
  
  .ranking-bar {
    width: 60px;
    height: 6px;
    background: #e5e7eb;
    border-radius: 3px;
    overflow: hidden;
    margin-left: 12px;
    flex-shrink: 0;
    
    .ranking-bar-fill {
      height: 100%;
      background: linear-gradient(90deg, #8b5cf6 0%, #6366f1 100%);
      border-radius: 3px;
      transition: width 0.3s ease;
    }
  }
  
  .empty-ranking {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 60px 20px;
    color: #9ca3af;
    
    i {
      font-size: 48px;
      margin-bottom: 16px;
      opacity: 0.5;
    }
    
    p {
      margin: 0;
      font-size: 14px;
    }
  }
}

/* 响应式设计 */
@media screen and (max-width: 1400px) {
  .stat-cards {
    grid-template-columns: repeat(2, 1fr);
  }
  
  .charts-container {
    grid-template-columns: 1fr;
  }
}

@media screen and (max-width: 768px) {
  .dashboard-wrapper {
    padding: 16px;
  }

  .stat-cards {
    grid-template-columns: 1fr;
    gap: 16px;
  }

  .charts-container {
    grid-template-columns: 1fr;
  }
  
  .ranking-card {
    .ranking-item {
      padding: 12px;
      
      .ranking-number {
        width: 32px;
        height: 32px;
        font-size: 14px;
        margin-right: 12px;
      }
      
      .ranking-info {
        .ranking-page-name {
          font-size: 14px;
        }
        
        .ranking-count {
          font-size: 12px;
        }
      }
    }
  }
}
</style>
