<template>
  <div class="dashboard-wrapper">
    <section class="hero-card">
      <div class="hero-copy">
        <p class="eyebrow">Taobao Data Defense</p>
        <h2>淘宝商品信息分析与可视化</h2>
        <p class="description">
          本系统聚焦课程答辩场景，只保留“数据清洗、指标分析、图表展示”三段核心能力。
          后端基于 Django 提供分析接口，分析逻辑由 pandas 完成，前端使用 Vue 与 ECharts 展示结果。
        </p>
      </div>
      <div class="hero-metrics">
        <div class="metric-card">
          <div class="metric-label">数据源</div>
          <div class="metric-value">cleaned_data.csv</div>
        </div>
        <div class="metric-card">
          <div class="metric-label">分析接口</div>
          <div class="metric-value">7 个</div>
        </div>
        <div class="metric-card">
          <div class="metric-label">图表主题</div>
          <div class="metric-value">销量 + 均价</div>
        </div>
      </div>
    </section>


  </div>
</template>

<script>
export default {
  name: 'HomeView'
}
</script>

<style lang="less" scoped>
.dashboard-wrapper {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.hero-card {
  display: grid;
  grid-template-columns: 1.5fr 1fr;
  gap: 24px;
  padding: 32px;
  border-radius: 24px;
  background: linear-gradient(135deg, #0f172a 0%, #1d4ed8 55%, #dbeafe 100%);
  color: #fff;
  overflow: hidden;
}

.eyebrow {
  margin: 0 0 10px;
  font-size: 13px;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: rgba(255, 255, 255, 0.72);
}

h2 {
  margin: 0 0 16px;
  font-size: 34px;
  line-height: 1.2;
}

.description {
  margin: 0;
  max-width: 720px;
  font-size: 15px;
  line-height: 1.8;
  color: rgba(255, 255, 255, 0.88);
}

.hero-metrics {
  display: grid;
  gap: 16px;
}

.metric-card {
  padding: 18px 20px;
  border-radius: 18px;
  background: rgba(255, 255, 255, 0.14);
  backdrop-filter: blur(10px);
}

.metric-label {
  font-size: 13px;
  color: rgba(255, 255, 255, 0.72);
}

.metric-value {
  margin-top: 8px;
  font-size: 24px;
  font-weight: 700;
}

.content-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(280px, 1fr));
  gap: 24px;
}

.info-card {
  border: none;
  border-radius: 18px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.04);
}

.info-card h3 {
  margin: 0 0 14px;
  font-size: 20px;
  color: #111827;
}

.info-card ol,
.info-card ul {
  margin: 0;
  padding-left: 20px;
  color: #4b5563;
  line-height: 1.9;
}

@media screen and (max-width: 900px) {
  .hero-card,
  .content-grid {
    grid-template-columns: 1fr;
  }

  .hero-card {
    padding: 24px;
  }

  h2 {
    font-size: 28px;
  }
}
</style>
