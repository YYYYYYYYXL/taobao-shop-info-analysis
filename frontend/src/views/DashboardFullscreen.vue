<template>
  <div class="dashboard-container">
    <!-- 数据大屏标题 -->
    <div class="dashboard-header">
      <h1 class="main-title">
        <span class="title-icon"></span>
        淘宝店铺销售数据分析可视化大屏
        <span class="title-icon"></span>
      </h1>
      <div class="subtitle">高效数据监控 · 智能分析洞察</div>
    </div>

    <!-- 图表网格布局 -->
    <div class="charts-grid">
      <!-- 顶部两列 -->
      <div class="top-row">
        <div class="chart-block top-block">
          <div class="chart-label">分类销量分析</div>
          <AnalysisDashboard title="分类销量分析" />
        </div>
        <div class="chart-block top-block">
          <div class="chart-label">店铺销量分析</div>
          <AnalysisDashboard title="店铺销量分析" />
        </div>
      </div>

      <!-- 中间大图 + 两侧图表 -->
      <div class="middle-row">
        <div class="side-column">
          <div class="chart-block side-block">
            <div class="chart-label">风格价格分析</div>
            <AnalysisDashboard title="风格价格分析" />
          </div>
          <div class="chart-block side-block">
            <div class="chart-label">款式价格分析</div>
            <AnalysisDashboard title="款式价格分析" />
          </div>
        </div>

        <div class="center-block">
          <div class="chart-block center-main">
            <div class="chart-label">省份销量分析</div>
            <AnalysisDashboard height="500" title="省份销量分析" />
          </div>
        </div>

        <div class="side-column">
          <div class="chart-block side-block">
            <div class="chart-label">面料价格分析</div>
            <AnalysisDashboard title="面料价格分析" />
          </div>
          <div class="chart-block side-block">
            <div class="chart-label">版型价格分析</div>
            <AnalysisDashboard title="版型价格分析" />
          </div>
        </div>
      </div>
    </div>

    <!-- 装饰性元素 -->
    <div class="decorative-elements">
      <div class="floating-circle circle-1"></div>
      <div class="floating-circle circle-2"></div>
      <div class="floating-circle circle-3"></div>
      <div class="floating-circle circle-4"></div>
      
      <!-- 15个随机气泡 -->
      <div class="random-bubble bubble-1"></div>
      <div class="random-bubble bubble-2"></div>
      <div class="random-bubble bubble-3"></div>
      <div class="random-bubble bubble-4"></div>
      <div class="random-bubble bubble-5"></div>
      <div class="random-bubble bubble-6"></div>
      <div class="random-bubble bubble-7"></div>
      <div class="random-bubble bubble-8"></div>
      <div class="random-bubble bubble-9"></div>
      <div class="random-bubble bubble-10"></div>
      <div class="random-bubble bubble-11"></div>
      <div class="random-bubble bubble-12"></div>
      <div class="random-bubble bubble-13"></div>
      <div class="random-bubble bubble-14"></div>
      <div class="random-bubble bubble-15"></div>
    </div>
  </div>
</template>

<script>
// import { hasInviteCode, isValidDate } from '@/utils/inviteCode'
import { MessageBox } from 'element-ui'

export default {
  name: 'DashboardFullscreen',
  created() {
    // this.checkInviteCode()
    this.checkDeviceId()
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
    }
  }
}
</script>

<style scoped>
.dashboard-container {
  padding: 20px;
  background: #f5f7fb;
  min-height: 100vh;
  color: #1f2937;
  position: relative;
  overflow-y: auto;
}

.dashboard-header {
  text-align: center;
  position: relative;
  z-index: 10;
  padding: 10px 0;
}

.main-title {
  font-size: 48px;
  font-weight: 800;
  margin: 0 0 5px 0;
  background: linear-gradient(135deg, #1a56db 0%, #4f46e5 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  letter-spacing: 3px;
  position: relative;
}

.main-title::before {
  content: '';
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 110%;
  height: 130%;
  background: radial-gradient(ellipse, rgba(79, 70, 229, 0.15) 0%, transparent 70%);
  z-index: -1;
}

.title-icon {
  font-size: 36px;
  margin: 0 12px;
  color: #4f46e5;
  opacity: 0.7;
}

.subtitle {
  font-size: 18px;
  font-weight: 400;
  color: #6b7280;
  letter-spacing: 3px;
  position: relative;
  display: inline-block;
  padding: 0 20px;
}

.subtitle::before,
.subtitle::after {
  content: '';
  position: absolute;
  top: 50%;
  width: 40px;
  height: 1px;
  background: linear-gradient(90deg, transparent, #00ffff, transparent);
  box-shadow: 0 0 10px rgba(0, 255, 255, 0.8);
}

.subtitle::before {
  left: -50px;
}

.subtitle::after {
  right: -50px;
}

.charts-grid {
  display: flex;
  flex-direction: column;
  gap: 10px;
  min-height: calc(100vh - 180px);
}

.chart-block {
  position: relative;
  background: #ffffff;
  border-radius: 12px;
  padding: 10px;
  border: 1px solid rgba(79, 70, 229, 0.08);
  box-shadow: 
    0 10px 30px rgba(79, 70, 229, 0.08),
    inset 0 0 0 rgba(79, 70, 229, 0.05);
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  overflow: hidden;
}

.chart-block::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(135deg, rgba(79, 70, 229, 0.08) 0%, rgba(99, 102, 241, 0.02) 100%);
  border-radius: 12px;
  z-index: 1;
  opacity: 0;
  transition: opacity 0.4s ease;
}

.chart-block::after {
  content: '';
  position: absolute;
  top: -2px;
  left: -2px;
  right: -2px;
  bottom: -2px;
  background: linear-gradient(45deg, rgba(79, 70, 229, 0.45), rgba(99, 102, 241, 0.35), rgba(129, 140, 248, 0.3));
  border-radius: 12px;
  z-index: -1;
  opacity: 0;
  transition: opacity 0.4s ease;
  background-size: 250% 250%;
}

/* 移除悬停效果，保持静态 */

.chart-label {
  position: relative;
  z-index: 2;
  font-size: 14px;
  font-weight: 600;
  margin-bottom: 10px;
  text-align: center;
  color: #1f2937;
  letter-spacing: 2px;
  padding-bottom: 5px;
  border-bottom: 1px solid rgba(99, 102, 241, 0.2);
}

.top-row {
  display: flex;
  gap: 10px;
}

.top-block {
  flex: 1;
  min-height: 220px;
}

.middle-row {
  display: flex;
  gap: 10px;
  flex: 1;
}

.side-column {
  display: flex;
  flex-direction: column;
  gap: 10px;
  flex: 0 0 300px;
}

.side-block {
  flex: 1;
  min-height: 200px;
}

.center-block {
  flex: 1;
  display: flex;
}

.center-main {
  flex: 1;
  min-height: 400px;
}

/* 装饰性元素 */
.decorative-elements {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
  z-index: 1;
  overflow: hidden;
}

.floating-circle {
  position: absolute;
  border: 2px solid rgba(99, 102, 241, 0.15);
  border-radius: 50%;
  background: radial-gradient(circle, rgba(99, 102, 241, 0.08) 0%, transparent 70%);
  box-shadow: 0 0 25px rgba(99, 102, 241, 0.2);
  animation: float 8s ease-in-out infinite;
}

.circle-1 {
  width: 120px;
  height: 120px;
  top: 10%;
  left: 5%;
  animation-delay: 0s;
}

.circle-2 {
  width: 80px;
  height: 80px;
  top: 20%;
  right: 8%;
  animation-delay: 2s;
}

.circle-3 {
  width: 100px;
  height: 100px;
  bottom: 15%;
  left: 10%;
  animation-delay: 4s;
}

.circle-4 {
  width: 60px;
  height: 60px;
  bottom: 25%;
  right: 15%;
  animation-delay: 1s;
}

/* 动画效果 */
@keyframes titleGlow {
  0% {
    filter: drop-shadow(0 0 10px rgba(0, 255, 255, 0.5)) drop-shadow(0 0 20px rgba(0, 191, 255, 0.3));
  }
  100% {
    filter: drop-shadow(0 0 20px rgba(0, 255, 255, 0.8)) drop-shadow(0 0 40px rgba(0, 191, 255, 0.5));
  }
}

@keyframes titlePulse {
  0%, 100% {
    opacity: 0.5;
    transform: translate(-50%, -50%) scale(1);
  }
  50% {
    opacity: 0.8;
    transform: translate(-50%, -50%) scale(1.1);
  }
}

@keyframes iconPulse {
  0%, 100% {
    opacity: 0.8;
    transform: scale(1);
  }
  50% {
    opacity: 1;
    transform: scale(1.1);
  }
}

@keyframes float {
  0%, 100% {
    transform: translateY(0px) translateX(0px) scale(1);
    opacity: 0.4;
  }
  33% {
    transform: translateY(-30px) translateX(20px) scale(1.1);
    opacity: 0.7;
  }
  66% {
    transform: translateY(-15px) translateX(-15px) scale(0.9);
    opacity: 0.5;
  }
}

@keyframes borderGlow {
  0% {
    background-position: 0% 50%;
  }
  50% {
    background-position: 100% 50%;
  }
  100% {
    background-position: 0% 50%;
  }
}

/* 随机气泡样式 - 改为几何线条 */
.random-bubble {
  position: absolute;
  pointer-events: none;
  transform-origin: center;
}

.bubble-1,
.bubble-2,
.bubble-3,
.bubble-4,
.bubble-5,
.bubble-6,
.bubble-7,
.bubble-8,
.bubble-9,
.bubble-10,
.bubble-11,
.bubble-12,
.bubble-13,
.bubble-14,
.bubble-15 {
  width: 3px;
  height: 60px;
  background: linear-gradient(180deg, transparent, rgba(79, 70, 229, 0.5), transparent);
  box-shadow: 0 0 12px rgba(79, 70, 229, 0.45);
  animation: lineFloat 15s ease-in-out infinite;
}

.bubble-1::before,
.bubble-2::before,
.bubble-3::before,
.bubble-4::before,
.bubble-5::before,
.bubble-6::before,
.bubble-7::before,
.bubble-8::before,
.bubble-9::before,
.bubble-10::before,
.bubble-11::before,
.bubble-12::before,
.bubble-13::before,
.bubble-14::before,
.bubble-15::before {
  content: '';
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%) rotate(90deg);
  width: 60px;
  height: 3px;
  background: linear-gradient(90deg, transparent, rgba(79, 70, 229, 0.5), transparent);
  box-shadow: 0 0 12px rgba(79, 70, 229, 0.4);
}

@keyframes lineFloat {
  0% {
    transform: translateY(0px) rotate(0deg);
    opacity: 0.25;
  }
  25% {
    transform: translateY(-25px) rotate(90deg);
    opacity: 0.7;
  }
  50% {
    transform: translateY(-50px) rotate(180deg);
    opacity: 0.35;
  }
  75% {
    transform: translateY(-25px) rotate(270deg);
    opacity: 0.6;
  }
  100% {
    transform: translateY(0px) rotate(360deg);
    opacity: 0.25;
  }
}

/* 响应式设计 */
@media (max-width: 1600px) {
  .top-block {
    min-height: 200px;
  }
  
  .side-block {
    min-height: 180px;
  }
  
  .center-main {
    min-height: 380px;
  }
  .main-title {
    font-size: 42px;
  }
}

@media (max-width: 1200px) {
  .dashboard-container {
    padding: 10px;
  }
  
  .main-title {
    font-size: 36px;
  }
  
  .charts-grid {
    min-height: calc(100vh - 160px);
  }
  
  .top-row,
  .middle-row {
    flex-direction: column;
    gap: 10px;
  }
  
  .side-column {
    flex-direction: row;
    flex-wrap: wrap;
    justify-content: space-between;
  }
  
  .side-block {
    flex: 1 1 calc(50% - 5px);
    min-height: 150px;
  }
  
  .center-main {
    min-height: 320px;
  }
}

@media (max-width: 768px) {
  .dashboard-container {
    padding: 10px;
  }
  
  .main-title {
    font-size: 28px;
  }
  
  .title-icon {
    font-size: 24px;
    margin: 0 10px;
  }
  
  .subtitle {
    font-size: 14px;
  }
  
  .charts-grid {
    min-height: calc(100vh - 140px);
    gap: 10px;
  }
  
  .chart-block {
    padding: 10px;
  }
  
  .top-block,
  .side-block {
    min-height: 130px;
  }
  
  .center-main {
    min-height: 260px;
  }
}

/* 网格背景装饰 */
.dashboard-container::before {
  content: '';
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-image: 
    linear-gradient(rgba(99, 102, 241, 0.04) 1px, transparent 1px),
    linear-gradient(90deg, rgba(99, 102, 241, 0.04) 1px, transparent 1px);
  background-size: 60px 60px;
  pointer-events: none;
  z-index: 0;
}
</style>
