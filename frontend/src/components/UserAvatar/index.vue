<template>
  <el-dropdown class="user-avatar-wrapper" @command="handleCommand">
    <div class="avatar-box">
      <el-avatar 
        :size="32" 
        :src="avatarUrl"
        class="user-avatar"
      >
        <span v-if="!avatarUrl">{{userInfo.name ? userInfo.name.charAt(0) : 'U'}}</span>
      </el-avatar>
      <span class="username">{{userInfo.name}}</span>
      <i class="el-icon-caret-bottom" />
    </div>

    <el-dropdown-menu slot="dropdown">
      <el-dropdown-item command="userCenter">个人中心</el-dropdown-item>
      <el-dropdown-item command="loginOut">退出登录</el-dropdown-item>
    </el-dropdown-menu>
  </el-dropdown>
</template>

<script>

export default {
  inject: ['userInfo'],
  name: 'UserAvatar',
  computed: {
    avatarUrl() {
      if (this.userInfo && this.userInfo.avatar) {
        // avatar 是相对路径，如 /img/avatar/xxx.jpg，需要拼接 API 前缀
        if (this.userInfo.avatar.startsWith('/')) {
          // 使用相对路径，会被 request.js 的 baseURL 处理
          return `/api${this.userInfo.avatar}`
        }
        return this.userInfo.avatar
      }
      return null
    }
  },
  data() {
    return {
      // userInfo: {},
      imgBaseUrl: this.HOST,
    }
  },
  methods: {
    handleCommand(command) {
      if (command === 'userCenter') {
          this.$router.push({ path: '/person-info' })
      }
      if (command === 'loginOut') {
          this.loginOut()
      }
    },
    loginOut() {
      this.$confirm('确定注销并退出系统吗？', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        localStorage.removeItem("userInfo")
        localStorage.removeItem("userMenuList")
        localStorage.removeItem("deviceId")
        localStorage.removeItem("token")
        this.$router.push({ path: '/login'});
      })
    }
  }
}
</script>

<style lang="less">
.user-avatar-wrapper {
  float: left;
  // width: 120px;
  padding: 3px 0 3px 20px;
  margin-left: 20px;
  cursor: pointer;

  .avatar-box {
    outline: none;
    display: flex;
    align-items: center; /* 垂直居中对齐 */
    justify-content: space-between; /* 头像和下拉箭头之间留有空间 */
  }

  .user-avatar {
    margin-right: 8px;
  }

  .username {
    font-size: 14px;
    /* 根据需要调整字体大小 */
    color: #333;
    /* 字体颜色 */
    margin-left: 0;
    /* 与头像之间的间距 */
  }

  .el-avatar--small {
    display: inline-block;
    vertical-align: middle;
    width: 32px;
    height: 32px;
    line-height: 32px;
  }

  i {
    display: inline-block;
    vertical-align: middle;
    margin-left: 2px;
  }
}
</style>