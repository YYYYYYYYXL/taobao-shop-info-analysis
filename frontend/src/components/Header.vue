<template>
  <div class="header-bar">
    <div class="header-left">
      <BreadCrumbs />
    </div>
    <div class="header-right">
      <div class="header-actions">
<!--        <el-tooltip content="返回前台" placement="bottom">-->
<!--          <div class="back-to-front" @click="goToFront">-->
<!--            <i class="el-icon-s-home"></i>-->
<!--            <span>返回前台</span>-->
<!--          </div>-->
<!--        </el-tooltip>-->
<!--        <el-tooltip content="刷新页面" placement="bottom">-->
<!--        <i class="el-icon-refresh-right action-icon" @click="refreshPage"></i>-->
<!--        </el-tooltip>-->
<!--        <el-tooltip :content="isFullscreen ? '退出全屏' : '全屏显示'" placement="bottom">-->
<!--          <i :class="isFullscreen ? 'el-icon-close' : 'el-icon-full-screen'" -->
<!--             class="action-icon"-->
<!--             @click="toggleFullScreen"></i>-->
<!--        </el-tooltip>-->
<!--        <el-divider direction="vertical"></el-divider>-->
        <UserAvatar />
      </div>
    </div>
  </div>
</template>

<script>
import BreadCrumbs from '../components/BreadCrumbs/index.vue'
import UserAvatar from '../components/UserAvatar/index.vue'

export default {
  name: 'HeaderBar',
  components: {
    BreadCrumbs,
    UserAvatar
  },
  data() {
    return {
      isFullscreen: false
    }
  },
  methods: {
    refreshPage() {
      window.location.reload()
    },
    toggleFullScreen() {
      if (!document.fullscreenElement) {
        document.documentElement.requestFullscreen()
        this.isFullscreen = true
      } else {
        if (document.exitFullscreen) {
          document.exitFullscreen()
          this.isFullscreen = false
        }
      }
    },
    goToFront() {
      this.$router.push('/');
    }
  },
  mounted() {
    document.addEventListener('fullscreenchange', () => {
      this.isFullscreen = !!document.fullscreenElement
    })
  }
}
</script>

<style lang="less" scoped>
.header-bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 100%;
  width: 100%;
  
  .header-left {
    display: flex;
    align-items: center;
    flex: 1;
    min-width: 0;
  }
  
  .header-right {
    display: flex;
    align-items: center;
    flex-shrink: 0;
    
    .header-actions {
      display: flex;
      align-items: center;
      gap: 16px;
      
      .back-to-front {
        display: flex;
        align-items: center;
        gap: 8px;
        padding: 8px 16px;
        border-radius: 8px;
        cursor: pointer;
        transition: all 0.3s ease;
        color: #6b7280;
        font-size: 14px;
        font-weight: 500;
        
        &:hover {
          color: #667eea;
          background: rgba(102, 126, 234, 0.08);
        }
        
        i {
          font-size: 18px;
        }
        
        span {
          font-size: 14px;
        }
      }
      
      .action-icon {
        font-size: 18px;
        color: #6b7280;
        cursor: pointer;
        transition: all 0.3s ease;
        padding: 8px;
        border-radius: 8px;
        width: 36px;
        height: 36px;
        display: flex;
        align-items: center;
        justify-content: center;
        
        &:hover {
          color: #667eea;
          background: rgba(102, 126, 234, 0.08);
          transform: scale(1.05);
        }
        
        &.el-icon-refresh-right:hover {
          animation: rotate 0.6s ease;
        }
      }
      
      .el-divider--vertical {
        height: 20px;
        margin: 0;
      }
    }
  }
}

@keyframes rotate {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(180deg);
  }
}

:deep(.el-badge__content.is-fixed) {
  top: 8px;
  right: 18px;
  border: 2px solid #fff;
}

:deep(.el-badge__content) {
  background-color: #667eea;
  border: none;
  box-shadow: 0 2px 8px rgba(102, 126, 234, 0.3);
}

:deep(.el-divider--vertical) {
  background-color: #e5e7eb;
  margin: 0 8px;
}
</style>