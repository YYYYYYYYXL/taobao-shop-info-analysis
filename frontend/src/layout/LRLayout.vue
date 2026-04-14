<template>
    <div class="lr-container">
<!--        <el-button class="back-home-btn" type="success" @click="goToHome">-->
<!--            <i class="el-icon-back"></i>-->
<!--            返回首页-->
<!--        </el-button>-->
        <div class="lr-content">
            <div class="lr-right">
                <router-view />
            </div>
        </div>
    </div>
</template>

<script>
export default {
    name: 'LRLayout',
    data() {
        return {
            title: process.env.VUE_APP_TITLE || '数据分析系统'
        }
    },
    mounted() {
        // 禁用页面滚动
        document.body.style.overflow = 'hidden'
    },
    beforeDestroy() {
        // 恢复页面滚动
        document.body.style.overflow = ''
    },
    methods: {
        goToHome() {
            this.$router.push('/')
        }
    }
}
</script>

<style scoped>
.lr-container {
    height: 100vh;
    overflow: hidden;
    display: flex;
    align-items: center;
    justify-content: center;
    background: linear-gradient(90deg, #4a90e2 0%, #e8f4fd 100%);
    position: relative;
}

.lr-content {
    display: flex;
    width: 100%;
    max-width: 420px;
    max-height: 100vh;
    background: rgba(255, 255, 255, 0.98);
    backdrop-filter: blur(20px);
    border-radius: 16px;
    box-shadow: 
        0 20px 60px rgba(74, 144, 226, 0.15),
        0 0 0 1px rgba(255, 255, 255, 0.5);
    overflow-y: auto;
    overflow-x: hidden;
    animation: slideUp 0.6s ease-out;
    position: relative;
    z-index: 1;
    
    /* 隐藏滚动条 */
    scrollbar-width: none; /* Firefox */
    -ms-overflow-style: none; /* IE 和 Edge */
    
    &::-webkit-scrollbar {
      display: none; /* Chrome, Safari, Opera */
    }
}

.lr-left {
    flex: 1;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 60px;
    position: relative;
    overflow: hidden;
}

.brand-info {
    position: relative;
    color: white;
    text-align: center;
    z-index: 1;
}

.logo-container {
    width: 80px;
    height: 80px;
    margin: 0 auto 24px;
    background: rgba(255, 255, 255, 0.2);
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
}

.logo-container i {
    font-size: 40px;
}

.brand-info h1 {
    font-size: 36px;
    font-weight: 600;
    margin-bottom: 16px;
    letter-spacing: 1px;
}

.brand-info p {
    font-size: 18px;
    opacity: 0.9;
    margin-bottom: 40px;
}

.features {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 20px;
    margin-top: 60px;
}

.feature-item {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 12px;
}

.feature-item i {
    font-size: 32px;
    opacity: 0.9;
}

.feature-item span {
    font-size: 14px;
}

.lr-right {
    flex: 1;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 40px 36px;
    background: transparent;
}

@keyframes slideUp {
    from {
        opacity: 0;
        transform: translateY(30px) scale(0.95);
    }
    to {
        opacity: 1;
        transform: translateY(0) scale(1);
    }
}

@media (max-width: 1200px) {
    .lr-content {
        max-width: 400px;
    }
}

@media (max-width: 768px) {
    .lr-container {
        padding: 16px;
    }
    
    .lr-content {
        max-width: 100%;
        border-radius: 16px;
    }
    
    .lr-right {
        padding: 32px 28px;
    }
    
    .lr-left {
        display: none;
    }
}

.back-home-btn {
    position: fixed;
    top: 20px;
    left: 20px;
    font-size: 14px;
    padding: 8px 12px;
    border-radius: 8px;
    transition: all 0.3s ease;
    z-index: 100;
}

.back-home-btn:hover {
    transform: translateX(-4px);
    box-shadow: 0 2px 8px rgba(103, 194, 58, 0.2);
}

.back-home-btn i {
    margin-right: 4px;
    transition: transform 0.3s ease;
}

.back-home-btn:hover i {
    transform: translateX(-2px);
}
</style>