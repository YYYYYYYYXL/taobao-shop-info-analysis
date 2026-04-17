<template>
  <div class="login-container">
    <div class="title-wrapper">
      <img :src="logoImg" alt="Logo" class="login-logo" />
      <h2 class="login-title">欢迎登录</h2>
    </div>
    <el-form ref="loginForm" :model="loginForm" :rules="rules" class="login-form">
      <div class="form-content">
        <el-form-item prop="username">
          <el-input v-model="loginForm.username" placeholder="用户名" prefix-icon="el-icon-user">
          </el-input>
        </el-form-item>

        <el-form-item prop="password">
          <el-input type="password" v-model="loginForm.password" placeholder="密码" prefix-icon="el-icon-lock">
          </el-input>
        </el-form-item>

        <el-form-item>
          <div class="validate-container">
            <el-input v-model="loginForm.validCode" placeholder="验证码" prefix-icon="el-icon-key">
            </el-input>
            <ValidCode @input="createValidCode" class="validate-code" />
          </div>
        </el-form-item>

        <el-form-item>
          <el-button type="primary" class="login-button" @click="onLogin">
            登录
          </el-button>
        </el-form-item>

        <div class="login-actions">
          <el-link type="success" @click="$router.push('/forget')" class="forget-link">
<!--            <i class="el-icon-question"></i> 忘记密码？-->
          </el-link>
          <div class="register-link">
            还没有账号？
            <el-link type="success" @click="toRegister">立即注册</el-link>
          </div>
        </div>
      </div>
    </el-form>
  </div>
</template>

<script>
import ValidCode from "../components/Validate";
import request from "@/utils/request";
import { setRoutes } from "@/router";
import logoImg from '@/assets/logo.png';


export default {
  name: 'Login',
  components: {
    ValidCode
  },
  data() {
    return {
      logoImg: logoImg,
      validCode: '', //通过valicode获取的验证码
      loginForm: {
        username: '',
        password: '',
        validCode: ''
      },
      rules: {
        username: [
          { required: true, message: '请输入用户名', trigger: 'blur' },
          { min: 3, max: 20, message: '长度在 3 到 20 个字符', trigger: 'blur' }
        ],
        password: [
          { required: true, message: '请输入密码', trigger: 'blur' },
          { min: 6, max: 20, message: '长度在 6 到 20 个字符', trigger: 'blur' }
        ]
      },
    };
  },
  created() {
    // this.checkInviteCode();
  },
  methods: {
    toRegister() {
      this.$router.push("/register");
    },
    createValidCode(data) {
      this.validCode = data
    },
    onLogin() {

      this.$refs.loginForm.validate((valid) => {
        if (valid) {
          // 验证码比较时转换为小写，实现不区分大小写
          if (this.loginForm.validCode.toLowerCase() !== this.validCode.toLowerCase()) {
            this.$message.error("验证码错误");
            return;
          }
          request.post("/user/login", this.loginForm)
            .then(res => {
              if (res.code === "0") {
                this.$message.success("登录成功");
                if (res.data.token) {
                  localStorage.setItem("token", res.data.token);
                }
                if (res.data) {
                  localStorage.setItem("userInfo", JSON.stringify(res.data));
                }

                if (res.data.menuList) {
                  localStorage.setItem("userMenuList", JSON.stringify(res.data.menuList));
                }
                setRoutes();
                this.$router.push('/home');
              } else {
                this.$message.error(res.msg);
              }
            })
            .catch(error => {
              console.error("登录失败:", error);
            });
        } else {
          return false;
        }
      });
    }
  }
};
</script>

<style scoped>
.login-container {
  width: 100%;
  max-width: 100%;
  animation: fadeIn 0.6s ease-out;
}

.title-wrapper {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: center;
  gap: 12px;
  margin-bottom: 28px;
}

.login-logo {
  width: 40px;
  height: 40px;
  object-fit: contain;
}

.login-title {
  font-size: 26px;
  color: #1f2937;
  margin: 0;
  text-align: center;
  font-weight: 700;
  letter-spacing: -0.3px;
}

.login-subtitle {
  font-size: 16px;
  color: #7f8c8d;
  margin-bottom: 40px;
  text-align: center;
}

.login-form {
  margin-top: 0;
}

.validate-container {
  display: flex;
  gap: 12px;
}

.validate-code {
  flex-shrink: 0;
  width: 110px;
  border-radius: 10px;
  overflow: hidden;
}

.login-button {
  width: 100%;
  height: 44px;
  font-size: 15px;
  font-weight: 600;
  letter-spacing: 0.3px;
  margin-top: 28px;
  border-radius: 10px;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0;
  background: linear-gradient(135deg, #4a90e2 0%, #667eea 100%);
  border: none;
  box-shadow: 0 4px 12px rgba(74, 144, 226, 0.3);
}

.login-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(74, 144, 226, 0.4);
}

.login-button:active {
  transform: translateY(0);
}

/* 覆盖Element UI按钮的默认悬停样式 */
:deep(.login-button:hover) {
  background: linear-gradient(135deg, #3d7bc8 0%, #5568d3 100%) !important;
  border-color: transparent !important;
}

:deep(.login-button:focus) {
  background: linear-gradient(135deg, #4a90e2 0%, #667eea 100%) !important;
  border-color: transparent !important;
}

:deep(.login-button:active) {
  background: linear-gradient(135deg, #3d7bc8 0%, #5568d3 100%) !important;
  border-color: transparent !important;
}

.login-actions {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-top: 24px;
  font-size: 13px;
}

.forget-link {
  display: none;
}

.register-link {
  color: #64748b;
  font-size: 14px;
}

.register-link :deep(.el-link__inner) {
  color: #4a90e2;
  font-weight: 500;
  transition: color 0.2s;
}

.register-link :deep(.el-link__inner:hover) {
  color: #3d7bc8;
}

/* Element UI 组件样式覆盖 */
:deep(.el-input__inner) {
  height: 44px;
  line-height: 44px;
  border-radius: 10px;
  border: 1.5px solid #e2e8f0;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  background: #f8fafc;
  font-size: 14px;
}

:deep(.el-input__inner:hover) {
  border-color: #cbd5e1;
  background: #ffffff;
}

:deep(.el-input__inner:focus) {
  border-color: #4a90e2;
  background: #ffffff;
  box-shadow: 0 0 0 4px rgba(74, 144, 226, 0.1);
}

:deep(.el-form-item) {
  margin-bottom: 18px;
}

/* 修复图标垂直居中 */
:deep(.el-input__prefix) {
  left: 12px;
  top: 0;
  height: 100%;
  display: flex;
  align-items: center;
}

:deep(.el-input__prefix i) {
  font-size: 16px;
  line-height: 1;
  display: flex;
  align-items: center;
}

:deep(.el-input__inner) {
  padding-left: 44px;
}

:deep(.el-input__prefix i) {
  color: #94a3b8;
  font-size: 18px;
}

:deep(.el-input__inner:focus + .el-input__prefix i) {
  color: #4a90e2;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.form-content {
  width: 100%;
  margin: 0 auto;
}

/* 响应式调整 */
@media (max-width: 480px) {
  .title-wrapper {
    margin-bottom: 24px;
    gap: 10px;
  }
  
  .login-logo {
    width: 36px;
    height: 36px;
  }
  
  .login-title {
    font-size: 22px;
  }
  
  .form-content {
    width: 100%;
  }
  
  :deep(.el-input__inner) {
    height: 44px;
    line-height: 44px;
  }
  
  .login-button {
    height: 44px;
    margin-top: 24px;
  }
}

.invite-dialog :deep(.el-dialog) {
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.15);
  background: linear-gradient(135deg, #ffffff 0%, #f9fafb 100%);
}

.invite-dialog :deep(.el-dialog__header) {
  padding: 0;
  border-bottom: none;
  margin: 0;
}

.invite-dialog :deep(.el-dialog__body) {
  padding: 28px 24px 20px;
}

.invite-content {
  position: relative;
}

.invite-icon-wrapper {
  display: flex;
  justify-content: center;
  margin-bottom: 16px;
}

.invite-icon {
  width: 64px;
  height: 64px;
  border-radius: 50%;
  background: linear-gradient(135deg, #4a90e2 0%, #667eea 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 8px 20px rgba(74, 144, 226, 0.3);
  animation: iconBounce 2s ease-in-out infinite;
  position: relative;
}

.invite-icon::before {
  content: '';
  position: absolute;
  top: -4px;
  left: -4px;
  right: -4px;
  bottom: -4px;
  border-radius: 50%;
  background: linear-gradient(135deg, #4a90e2 0%, #667eea 100%);
  opacity: 0.2;
  animation: iconPulse 2s ease-in-out infinite;
}

.invite-icon i {
  font-size: 28px;
  color: white;
  z-index: 1;
  position: relative;
}

.invite-title {
  font-size: 20px;
  font-weight: 700;
  color: #1f2937;
  text-align: center;
  margin: 0 0 8px 0;
  letter-spacing: 0.3px;
}

.invite-tip {
  margin: 0 0 24px 0;
  font-size: 13px;
  color: #6b7280;
  text-align: center;
  line-height: 1.5;
}

.invite-input {
  margin-bottom: 16px;
}

.invite-input :deep(.el-input__inner) {
  height: 44px;
  border-radius: 10px;
  border: 2px solid #e5e7eb;
  transition: all 0.3s ease;
  font-size: 14px;
  background: #ffffff;
}

.invite-input :deep(.el-input__inner:focus) {
  border-color: #4a90e2;
  box-shadow: 0 0 0 4px rgba(74, 144, 226, 0.1);
}

.invite-input :deep(.el-input__prefix) {
  left: 12px;
}

.invite-input :deep(.el-input__prefix i) {
  color: #4a90e2;
  font-size: 16px;
}

.invite-error {
  color: #f56565;
  font-size: 12px;
  text-align: center;
  margin-top: 8px;
  min-height: 32px;
  padding: 8px 12px;
  background: #fef2f2;
  border-radius: 8px;
  border: 1px solid #fecaca;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  animation: shake 0.5s ease;
}

.invite-error i {
  font-size: 14px;
}

.invite-dialog :deep(.el-dialog__footer) {
  padding: 0 24px 24px;
  text-align: center;
  border-top: none;
  margin: 0;
}

.invite-submit-btn {
  width: 100%;
  height: 44px;
  border-radius: 10px;
  font-size: 15px;
  font-weight: 600;
  background: linear-gradient(135deg, #4a90e2 0%, #667eea 100%);
  border: none;
  box-shadow: 0 4px 12px rgba(74, 144, 226, 0.3);
  transition: all 0.3s ease;
}

.invite-submit-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(74, 144, 226, 0.4);
  background: linear-gradient(135deg, #3d7bc8 0%, #5568d3 100%);
}

.invite-submit-btn:active:not(:disabled) {
  transform: translateY(0);
}

.invite-submit-btn i {
  margin-right: 6px;
  font-size: 16px;
}

/* 动画效果 */
@keyframes iconBounce {
  0%, 100% {
    transform: translateY(0) scale(1);
  }
  50% {
    transform: translateY(-8px) scale(1.05);
  }
}

@keyframes iconPulse {
  0%, 100% {
    transform: scale(1);
    opacity: 0.2;
  }
  50% {
    transform: scale(1.2);
    opacity: 0;
  }
}

@keyframes shake {
  0%, 100% {
    transform: translateX(0);
  }
  10%, 30%, 50%, 70%, 90% {
    transform: translateX(-4px);
  }
  20%, 40%, 60%, 80% {
    transform: translateX(4px);
  }
}
</style>
