<template>
  <div class="analysis-actions">
    <el-button class="action-btn" size="small" type="primary" plain icon="el-icon-document" @click="$emit('open-details')">数据明细</el-button>
    <el-button class="action-btn" size="small" plain icon="el-icon-download" @click="$emit('download')">下载数据</el-button>
  </div>
</template>

<script>
export default {
  name: 'AnalysisActions'
}
</script>

<style lang="less" scoped>
.analysis-actions {
  display: flex;
  flex-direction: column;
  gap: 8px;
  position: sticky;
  top: 12px;
  z-index: 12;
  align-items: flex-end;
}

.action-btn {
  border-radius: 999px;
}
</style>


