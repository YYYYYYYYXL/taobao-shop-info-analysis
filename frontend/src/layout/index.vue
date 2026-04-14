<template>
  <div class="app-wrapper">
    <div class="side-container">
      <div class="logo-container">
        <img :src="logoImg" alt="Logo" class="logo-icon" />
        <h1 class="logo-text">{{ title }}</h1>
      </div>
      <SideMenu ref="sideMenu" />
    </div>
    <div class="main-container">
      <div class="main-header"> 
        <HeaderBar />
      </div>
      <div class="main-content">
        <router-view @update:user="updateUser" />
      </div>
    </div>
  </div>
</template>

<script>
import HeaderBar from '../components/Header.vue'
import SideMenu from '../components/Aside.vue'
import logoImg from '../assets/logo.png'
// import { hasInviteCode, isValidDate } from '@/utils/inviteCode'
import { MessageBox } from 'element-ui'

export default {
  name: 'Layout',
  data() {
    return {
      userInfo: JSON.parse(localStorage.getItem("userInfo") || "{}"),
      title: process.env.VUE_APP_TITLE,
      logoImg: logoImg
    };
  },
  created() {
    // this.checkInviteCode()
    this.checkDeviceId()
    
    // 判断是否登录
    if(!this.userInfo || !this.userInfo.username){
      this.$message.warning('请先登录')
      this.$router.push('/login')
    }
  },
  provide() {
    return {
      userInfo: this.userInfo,
    
    };
  },
  components: { HeaderBar, SideMenu },
  computed: {

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
    updateUser(user) {
      this.userInfo = user;
      this.$refs.sideMenu.refreshMenu();
    }
  }
}
</script>

<style lang="less">
@import "../assets/less/scroller-bar";

.app-wrapper {
  width: 100%;
  height: 100%;
  overflow: hidden;
  background-color: #f5f7fa;

  .side-container {
    box-shadow: 2px 0 12px rgba(0, 0, 0, 0.08);
    background-color: transparent;
    float: left;
    width: 240px;
    height: 100vh;
    overflow-y: auto;
    overflow-x: hidden;
    scrollbar-width: none; /* Firefox */
    -ms-overflow-style: none; /* IE 和 Edge */
    position: relative;
    z-index: 2;

    /* Chrome, Safari, Opera */
    &::-webkit-scrollbar {
      display: none;
    }

    .logo-container {
      height: 70px;
      background: linear-gradient(90deg, #4a90e2 0%, #e8f4fd 100%);
      display: flex;
      align-items: center;
      padding: 0 24px;
      border-bottom: 1px solid rgba(255, 255, 255, 0.2);
      
      .logo-icon {
        width: 28px;
        height: 28px;
        object-fit: contain;
        margin-right: 12px;
        position: relative;
        z-index: 1;
        opacity: 0.95;
      }
      
      .logo-text {
        margin: 0;
        font-size: 19px;
        color: #000000;
        font-weight: 600;
        letter-spacing: 0.5px;
        white-space: nowrap;
        position: relative;
        z-index: 1;
        text-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
      }
    }
  }

  .main-container {
    margin-left: 240px;
    min-height: 100vh;
    background-color: #f5f7fa;
    padding: 0;
    position: relative;
    overflow: hidden;
    display: flex;
    flex-direction: column;

    .main-header {
      background: linear-gradient(180deg, #4a90e2 0%, #e8f4fd 100%);
      margin-bottom: 0;
      box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
      padding: 0 24px;
      height: 70px;
      display: flex;
      align-items: center;
      border-bottom: 1px solid rgba(255, 255, 255, 0.2);
      position: relative;
      
      &::after {
        content: '';
        position: absolute;
        bottom: 0;
        left: 0;
        right: 0;
        height: 1px;
        background: linear-gradient(90deg, transparent 0%, rgba(255, 255, 255, 0.2) 50%, transparent 100%);
      }
      
      .el-header {
        padding: 0;
        height: auto;
      }
    }

    .main-content {
      background: #f5f7fa;
      min-height: calc(100vh - 70px);
      max-height: calc(100vh - 70px);
      overflow-y: auto;
      overflow-x: hidden;
      padding: 20px;
      flex: 1;
    }
  }
}
</style>
