<template>
  <el-card class="operation-area" shadow="hover">
    <div class="search-form-container">
      <el-form :inline="true" :model="searchForm" class="search-form">
        <el-form-item>
          <el-select v-model="searchForm.category" placeholder="请选择类别" clearable multiple collapse-tags>
            <el-option v-for="item in categories" :key="item" :label="item" :value="item" />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button size="medium" plain type="primary" @click="handleSearch">查询</el-button>
          <el-button size="medium" plain type="success" @click="handleRefresh">刷新</el-button>
          <el-button
            v-if="showDetailsButton"
            size="medium"
            plain
            type="info"
            :disabled="detailsDisabled"
            @click="handleOpenDetails"
          >
            明细
          </el-button>
          <el-button
            v-if="showDownloadButton"
            size="medium"
            plain
            type="warning"
            :disabled="downloadDisabled"
            @click="handleDownload"
          >
            下载
          </el-button>
          <el-button size="medium" plain @click="resetSearch">重置</el-button>
        </el-form-item>
      </el-form>
    </div>
  </el-card>
</template>

<script>
export default {
  name: 'AnalysisFilter',
  props: {
    initialValue: {
      type: Object,
      default: () => ({
        category: []
      })
    },
    showDetailsButton: {
      type: Boolean,
      default: false
    },
    showDownloadButton: {
      type: Boolean,
      default: false
    },
    detailsDisabled: {
      type: Boolean,
      default: false
    },
    downloadDisabled: {
      type: Boolean,
      default: false
    }
  },
  data() {
    return {
      searchForm: {
        category: []
      },
      categories: []
    }
  },
  created() {
    this.searchForm = { ...this.initialValue }
  },
  methods: {
    handleSearch() {
      this.$emit('search', this.searchForm)
    },
    resetSearch() {
      this.searchForm = {
        category: []
      }
      this.$emit('search', this.searchForm)
    },
    handleRefresh() {
      this.$emit('refresh')
    },
    handleOpenDetails() {
      if (!this.detailsDisabled) {
        this.$emit('open-details')
      }
    },
    handleDownload() {
      if (!this.downloadDisabled) {
        this.$emit('download')
      }
    }
  }
}
</script>

<style lang="less" scoped>
.operation-area {
  background: white;
  border-radius: 16px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.04);
  margin-bottom: 16px;
  border: none;
  padding: 20px 24px;

  :deep(.el-card__body) {
    padding: 0;
  }
}

:deep(.el-form-item) {
  margin-bottom: 0;
  display: flex;
  align-items: center;
}

:deep(.el-form-item__content) {
  display: flex;
  align-items: center;
  line-height: 1;
}

:deep(.el-input__inner) {
  border-radius: 10px;
  border-color: #e5e7eb;
  transition: all 0.3s ease;
  font-size: 14px;
  height: 40px;
  line-height: 40px;

  &:focus {
    border-color: #667eea;
    box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
  }

  &:hover {
    border-color: #d1d5db;
  }
}

:deep(.el-select) {
  width: 280px;
}

.search-form-container {
  display: flex;
  justify-content: flex-start;
  align-items: center;
  flex-wrap: wrap;
  gap: 16px;
}

.search-form {
  display: flex;
  align-items: center;
  margin: 0;
  gap: 16px;
  flex-wrap: wrap;
}

:deep(.el-button) {
  border-radius: 10px;
  font-weight: 500;
  transition: all 0.3s ease;
  height: 40px;
  padding: 0 20px;
  font-size: 14px;
}
</style>
