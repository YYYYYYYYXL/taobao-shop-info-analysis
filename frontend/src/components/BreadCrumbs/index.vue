<template>
  <div class="route-search-wrapper">
    <el-input
      v-model="searchKeyword"
      placeholder="搜索路由页面名称..."
      prefix-icon="el-icon-search"
      class="route-search-input"
      clearable
      @keyup.enter.native="handleSearch"
      @clear="handleClear"
    >
      <el-button
        slot="append"
        icon="el-icon-search"
        @click="handleSearch"
        class="search-button"
      ></el-button>
    </el-input>
  </div>
</template>

<script>
export default {
  name: 'RouteSearch',
  data() {
    return {
      searchKeyword: ''
    }
  },
  methods: {
    // 获取所有路由（扁平化处理）
    getAllRoutes() {
      const routes = []
      
      // 递归函数，扁平化路由树
      const flattenRoutes = (routeList, parentPath = '') => {
        routeList.forEach(route => {
          // 跳过没有name的路由和特定路由
          if (!route.name || route.name === 'Layout' || route.name === 'home' || route.name === 'LRLayout') {
            // 继续处理子路由
            if (route.children && route.children.length > 0) {
              const currentPath = route.path || parentPath
              flattenRoutes(route.children, currentPath)
            }
            return
          }
          
          // 构建完整路径
          let fullPath = route.path
          
          // 如果路径不是绝对路径，需要拼接父路径
          if (!route.path.startsWith('/')) {
            if (parentPath) {
              // 确保父路径不以 / 结尾
              const cleanParentPath = parentPath.endsWith('/') ? parentPath.slice(0, -1) : parentPath
              fullPath = `${cleanParentPath}/${route.path}`
            } else {
              fullPath = `/${route.path}`
            }
          } else if (parentPath && route.path === '/') {
            // 如果当前路径是根路径，使用父路径
            fullPath = parentPath
          }
          
          // 确保路径以 / 开头
          if (!fullPath.startsWith('/')) {
            fullPath = `/${fullPath}`
          }
          
          routes.push({
            name: route.name,
            path: fullPath,
            meta: route.meta || {}
          })
          
          // 递归处理子路由
          if (route.children && route.children.length > 0) {
            flattenRoutes(route.children, fullPath)
          }
        })
      }
      
      // 从路由实例获取所有路由
      const allRoutes = this.$router.getRoutes()
      flattenRoutes(allRoutes)
      
      return routes
    },
    
    // 搜索路由
    handleSearch() {
      if (!this.searchKeyword || !this.searchKeyword.trim()) {
        this.$message.warning('请输入搜索关键词')
        return
      }
      
      const keyword = this.searchKeyword.trim()
      const allRoutes = this.getAllRoutes()
      
      // 只搜索路由名称（name）
      const matchedRoute = allRoutes.find(route => {
        return route.name && route.name === keyword
      })
      
      if (!matchedRoute) {
        // 如果没有完全匹配，尝试模糊匹配
        const fuzzyMatched = allRoutes.find(route => {
          return route.name && route.name.includes(keyword)
        })
        
        if (fuzzyMatched) {
          this.navigateToRoute(fuzzyMatched)
        } else {
          this.$message.warning(`未找到名称为"${keyword}"的路由`)
        }
      } else {
        this.navigateToRoute(matchedRoute)
      }
    },
    
    // 跳转到路由
    navigateToRoute(route) {
      if (!route || !route.path) {
        return
      }
      
      // 判断是否是全屏页面
      if (route.path === '/dashboard-fullscreen' || route.path === '/chat-fullscreen') {
        window.open(route.path, '_blank')
      } else {
        this.$router.push(route.path).catch(err => {
          if (err.name !== 'NavigationDuplicated') {
            console.error('路由跳转失败:', err)
            this.$message.error('路由跳转失败')
          }
        })
      }
      
      // 清空搜索关键词
      this.searchKeyword = ''
    },
    
    // 清空搜索
    handleClear() {
      this.searchKeyword = ''
    }
  }
}
</script>

<style lang="less" scoped>
.route-search-wrapper {
  display: flex;
  align-items: center;
  width: 100%;
  max-width: 400px;
}

.route-search-input {
  width: 100%;
  
  :deep(.el-input__inner) {
    border-radius: 20px 0 0 20px;
    border: 1px solid #e5e7eb;
    border-right: none;
    padding-left: 40px;
    padding-right: 12px;
    height: 36px;
    line-height: 36px;
    font-size: 14px;
    transition: all 0.3s ease;
    
    &:focus {
      border-color: #667eea;
      box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    }
  }
  
  :deep(.el-input__prefix) {
    left: 12px;
    
    .el-input__icon {
      color: #9ca3af;
      font-size: 16px;
    }
  }
  
  :deep(.el-input-group__append) {
    border-radius: 0 20px 20px 0;
    border: 1px solid #e5e7eb;
    border-left: none;
    background: #fff;
    
    .search-button {
      border: none;
      background: transparent;
      color: #667eea;
      padding: 0 16px;
      height: 36px;
      transition: all 0.3s ease;
      
      &:hover {
        background: rgba(102, 126, 234, 0.1);
        color: #667eea;
      }
      
      i {
        font-size: 16px;
      }
    }
  }
  
  &:focus-within {
    :deep(.el-input__inner),
    :deep(.el-input-group__append) {
      border-color: #667eea;
    }
  }
}
</style>