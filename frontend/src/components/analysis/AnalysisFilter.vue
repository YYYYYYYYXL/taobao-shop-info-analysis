<template>
  <el-card class="operation-area" shadow="hover">
    <div class="search-form-container">
      <el-form :inline="true" :model="searchForm" class="search-form">
        <el-form-item >
          <el-select v-model="searchForm.category" placeholder="请选择类目" clearable multiple collapse-tags>
            <el-option v-for="item in categories" :key="item" :label="item" :value="item"></el-option>
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
          >明细</el-button>
          <el-button 
            v-if="showDownloadButton" 
            size="medium" 
            plain 
            type="warning" 
            :disabled="downloadDisabled"
            @click="handleDownload"
          >下载</el-button>
          <el-button size="medium" plain @click="resetSearch">重置</el-button>
        </el-form-item>
      </el-form>
    </div>
  </el-card>
</template>

<script>
import Request from '@/utils/request'

export default {
  name: 'AnalysisFilter',
  props: {
    // 初始值
    initialValue: {
      type: Object,
      default: () => ({
        category: []
      })
    },
    // 是否显示明细按钮
    showDetailsButton: {
      type: Boolean,
      default: false
    },
    // 是否显示下载按钮
    showDownloadButton: {
      type: Boolean,
      default: false
    },
    // 明细按钮是否禁用
    detailsDisabled: {
      type: Boolean,
      default: false
    },
    // 下载按钮是否禁用
    downloadDisabled: {
      type: Boolean,
      default: false
    }
  },
  data() {
    return {
      // 查询表单
      searchForm: {
        category: []
      },
      // 类目列表
      categories: []
    }
  },
  created() {
    this.searchForm = { ...this.initialValue }
    this.getCategories()
  },
  methods: {
    // 获取类目列表
    async getCategories() {
      try {
        const res = await Request.get('/category/all')
        if (res.code === '0') {
          // 从分类数据中提取name字段作为大类名称
          const data = res.data || []
          this.categories = data.map(item => item.name)
        }
      } catch (error) {
        // 静默处理获取大类名称列表失败
      }
    },
    // 查询
    handleSearch() {
      this.$emit('search', this.searchForm)
    },
    // 重置查询
    resetSearch() {
      this.searchForm = {
        category: []
      }
      this.$emit('search', this.searchForm)
    },
    // 刷新数据
    handleRefresh() {
      this.$emit('refresh')
    },
    // 打开明细
    handleOpenDetails() {
      if (!this.detailsDisabled) {
        this.$emit('open-details')
      }
    },
    // 下载数据
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

/* 美化表单 */
:deep(.el-form-item) {
  margin-bottom: 0;
  display: flex;
  align-items: center;
}

:deep(.el-form-item__label) {
  font-weight: 500;
  color: #374151;
  line-height: 1;
  font-size: 14px;
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

  .el-input__inner {
    border-radius: 10px;
  }
}

:deep(.el-date-editor) {
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

  &.el-button--primary.is-plain {
    border-color: #667eea;
    color: #667eea;
    background: rgba(102, 126, 234, 0.05);

    &:hover {
      background: #667eea;
      border-color: #667eea;
      color: white;
      transform: translateY(-1px);
      box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
    }
  }

  &.el-button--success.is-plain {
    border-color: #10b981;
    color: #10b981;
    background: rgba(16, 185, 129, 0.05);

    &:hover {
      background: #10b981;
      border-color: #10b981;
      color: white;
      transform: translateY(-1px);
      box-shadow: 0 4px 12px rgba(16, 185, 129, 0.3);
    }
  }

  &.el-button--info.is-plain {
    border-color: #4a90e2 !important;
    color: #4a90e2 !important;
    background: rgba(74, 144, 226, 0.05) !important;

    &:hover:not(:disabled) {
      background: #4a90e2 !important;
      border-color: #4a90e2 !important;
      color: white !important;
      transform: translateY(-1px);
      box-shadow: 0 4px 12px rgba(74, 144, 226, 0.3);
    }

    &:disabled {
      border-color: #d1d5db !important;
      color: #9ca3af !important;
      background: #f3f4f6 !important;
      cursor: not-allowed;
    }
  }

  &.el-button--warning.is-plain {
    border-color: #10b981;
    color: #10b981;
    background: rgba(16, 185, 129, 0.05);

    &:hover:not(:disabled) {
      background: #10b981;
      border-color: #10b981;
      color: white;
      transform: translateY(-1px);
      box-shadow: 0 4px 12px rgba(16, 185, 129, 0.3);
    }

    &:disabled {
      border-color: #d1d5db !important;
      color: #9ca3af !important;
      background: #f3f4f6 !important;
      cursor: not-allowed;
    }
  }

  &.is-plain:not(.el-button--primary):not(.el-button--success):not(.el-button--warning):not(.el-button--info) {
    border-color: #e5e7eb;
    color: #6b7280;
    background: #f9fafb;

    &:hover {
      border-color: #d1d5db;
      color: #374151;
      background: #ffffff;
      transform: translateY(-1px);
      box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
    }
  }
}

:deep(.el-select__tags) {
  .el-tag {
    border-radius: 6px;
    background: rgba(102, 126, 234, 0.1);
    border-color: rgba(102, 126, 234, 0.2);
    color: #667eea;
  }
}
</style>
