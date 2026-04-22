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
      <div class="main-content">
        <router-view />
      </div>
    </div>
  </div>
</template>

<script>
import SideMenu from '../components/Aside.vue'
import logoImg from '../assets/logo.png'

export default {
  name: 'AppLayout',
  components: { SideMenu },
  data() {
    return {
      title: process.env.VUE_APP_TITLE || '淘宝商品信息分析',
      logoImg
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
    scrollbar-width: none;
    -ms-overflow-style: none;
    position: relative;
    z-index: 2;

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
      }

      .logo-text {
        margin: 0;
        font-size: 19px;
        color: #000;
        font-weight: 600;
        letter-spacing: 0.5px;
        white-space: nowrap;
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

    .main-content {
      background: #f5f7fa;
      min-height: 100vh;
      max-height: 100vh;
      overflow-y: auto;
      overflow-x: hidden;
      padding: 20px;
      flex: 1;
    }
  }
}
</style>
