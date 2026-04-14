<template>
  <div class="register-container">
    <div class="title-wrapper">
      <img :src="logoImg" alt="Logo" class="register-logo" />
      <h2 class="register-title">欢迎注册</h2>
    </div>
    <el-form ref="registerForm" :model="registerForm" :rules="rules" class="register-form">
      <div class="form-content">
        <el-form-item prop="username">
          <el-input
            v-model="registerForm.username"
            placeholder="请输入用户名"
            prefix-icon="el-icon-user"
          />
        </el-form-item>

        <el-form-item prop="password">
          <el-input
            v-model="registerForm.password"
            type="password"
            placeholder="请输入密码"
            prefix-icon="el-icon-lock"
          />
        </el-form-item>

        <el-form-item prop="name">
          <el-input
            v-model="registerForm.name"
            placeholder="请输入姓名"
            prefix-icon="el-icon-user-solid"
          />
        </el-form-item>

        <el-form-item prop="email">
          <el-input
            v-model="registerForm.email"
            placeholder="请输入邮箱"
            prefix-icon="el-icon-message"
          />
        </el-form-item>

        <el-form-item prop="role">
          <el-select v-model="registerForm.role" placeholder="请选择角色" class="role-select">
            <el-option label="普通用户" value="USER" />
            <el-option label="管理员" value="ADMIN" />
          </el-select>
        </el-form-item>

        <el-form-item>
          <el-button type="primary" class="register-button" @click="onRegister">
            立即注册
          </el-button>
        </el-form-item>

        <div class="register-actions">
          <el-link type="success" @click="$router.push('/login')">
            <i class="el-icon-arrow-left"></i> 返回登录
          </el-link>
        </div>
      </div>
    </el-form>
  </div>
</template>

<script>
import request from '@/utils/request'
import logoImg from '@/assets/logo.png'

export default {
  name: 'Register',
  data() {
    return {
      logoImg,
      registerForm: {
        username: '',
        password: '',
        name: '',
        email: '',
        role: 'USER',
        status: 1
      },
      rules: {
        username: [
          { required: true, message: '请输入用户名', trigger: 'blur' },
          { min: 3, max: 20, message: '用户名长度需在 3 到 20 个字符之间', trigger: 'blur' }
        ],
        password: [
          { required: true, message: '请输入密码', trigger: 'blur' },
          { min: 6, max: 20, message: '密码长度需在 6 到 20 个字符之间', trigger: 'blur' }
        ],
        name: [
          { required: true, message: '请输入姓名', trigger: 'blur' }
        ],
        email: [
          { required: true, message: '请输入邮箱', trigger: 'blur' },
          { type: 'email', message: '请输入正确的邮箱格式', trigger: 'blur' }
        ],
        role: [
          { required: true, message: '请选择角色', trigger: 'change' }
        ]
      }
    }
  },
  methods: {
    onRegister() {
      this.$refs.registerForm.validate((valid) => {
        if (!valid) {
          return false
        }

        request.post('/user/add', this.registerForm).then((res) => {
          if (res.code === '0') {
            this.$message({
              type: 'success',
              message: '注册成功，请登录'
            })
            this.$router.push('/login')
          } else {
            this.$message({
              type: 'error',
              message: res.msg || '注册失败'
            })
          }
        })
      })
    }
  }
}
</script>

<style scoped>
.register-container {
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

.register-logo {
  width: 40px;
  height: 40px;
  object-fit: contain;
}

.register-title {
  font-size: 26px;
  color: #1f2937;
  margin: 0;
  text-align: center;
  font-weight: 700;
  letter-spacing: -0.3px;
}

.register-form {
  margin-top: 0;
}

.form-content {
  width: 100%;
  margin: 0 auto;
}

.role-select {
  width: 100%;
}

.register-button {
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

.register-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(74, 144, 226, 0.4);
}

:deep(.register-button:hover) {
  background: linear-gradient(135deg, #3d7bc8 0%, #5568d3 100%) !important;
  border-color: transparent !important;
}

:deep(.register-button:focus) {
  background: linear-gradient(135deg, #4a90e2 0%, #667eea 100%) !important;
  border-color: transparent !important;
}

.register-actions {
  display: flex;
  justify-content: center;
  margin-top: 24px;
  font-size: 13px;
}

.register-actions .el-link {
  display: flex;
  align-items: center;
  gap: 6px;
  color: #64748b;
}

.register-actions .el-link :deep(.el-link__inner) {
  color: #4a90e2;
  font-weight: 500;
  transition: color 0.2s;
}

.register-actions .el-link :deep(.el-link__inner:hover) {
  color: #3d7bc8;
}

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

:deep(.el-input__prefix) {
  left: 12px;
  top: 0;
  height: 100%;
  display: flex;
  align-items: center;
}

:deep(.el-input__prefix i) {
  color: #94a3b8;
  font-size: 18px;
  line-height: 1;
  display: flex;
  align-items: center;
}

:deep(.el-input__inner) {
  padding-left: 44px;
}

:deep(.el-select .el-input__inner) {
  padding-left: 16px;
  background: #f8fafc;
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

@media (max-width: 480px) {
  .title-wrapper {
    margin-bottom: 24px;
    gap: 10px;
  }

  .register-logo {
    width: 36px;
    height: 36px;
  }

  .register-title {
    font-size: 22px;
  }

  .form-content {
    width: 100%;
  }

  .register-button {
    height: 44px;
    margin-top: 24px;
  }
}
</style>
