<template>
  <div class="password-page">
    <div class="page-header">
      <h2></h2>
    </div>
    <div class="card-container">
      <el-card class="password-card" shadow="hover">
        <el-form 
          :model="passwordForm" 
          :rules="passwordRules" 
          ref="passwordForm" 
          label-width="100px"
          class="password-form"
        >
          <el-form-item label="旧密码" prop="oldPassword">
            <el-input 
              type="password" 
              v-model="passwordForm.oldPassword" 
              :show-password="true"
              autocomplete="off"
              placeholder="请输入旧密码"
            />
          </el-form-item>

          <el-form-item label="新密码" prop="newPassword">
            <el-input 
              type="password" 
              v-model="passwordForm.newPassword" 
              :show-password="true"
              autocomplete="off"
              placeholder="请输入新密码（至少6位）"
            />
          </el-form-item>

          <el-form-item label="确认密码" prop="confirmPassword">
            <el-input 
              type="password" 
              v-model="passwordForm.confirmPassword" 
              :show-password="true"
              autocomplete="off"
              placeholder="请再次输入新密码"
            />
          </el-form-item>

          <el-form-item class="button-group">
            <el-button type="primary" @click="submitForm" icon="el-icon-check">
              确认修改
            </el-button>
            <el-button @click="resetForm" icon="el-icon-refresh" plain>
              重置
            </el-button>
          </el-form-item>
        </el-form>
      </el-card>
    </div>
  </div>
</template>

<script>
import request from '@/utils/request';

export default {
  inject: ['userInfo'],
  
  data() {
    const validatePassword = (rule, value, callback) => {
      if (value.length < 6) {
        callback(new Error('密码长度不能少于6位'));
      } else {
        callback();
      }
    };
    
    const validateConfirmPassword = (rule, value, callback) => {
      if (value !== this.passwordForm.newPassword) {
        callback(new Error('两次输入密码不一致'));
      } else {
        callback();
      }
    };
    
    return {
      passwordForm: {
        oldPassword: '',
        newPassword: '',
        confirmPassword: '',
      },
      passwordRules: {
        oldPassword: [
          { required: true, message: '请输入旧密码', trigger: 'blur' },
        ],
        newPassword: [
          { required: true, validator: validatePassword, trigger: 'blur' },
        ],
        confirmPassword: [
          { required: true, validator: validateConfirmPassword, trigger: 'blur' },
        ],
      },
    };
  },

  methods: {
    getRoleName(role) {
      const roleMap = {
        'ADMIN': '管理员',
        'USER': '普通用户'
      }
      return roleMap[role]
    },

    submitForm() {
      this.$refs.passwordForm.validate((valid) => {
        if (valid) {
          request.put('/user/password/' + this.userInfo.id, this.passwordForm).then(response => {
            if (response.code == '0') {
              this.$message({
                type: 'success',
                message: '密码修改成功!请重新登录！'
              });
              this.resetForm();
              localStorage.removeItem("userInfo");
              this.$router.push({ path: '/login'});

            } else {
              this.$message({
                type: 'error',
                message: response.msg
              });
            }
          });
        } else {
          return false;
        }
      });
    },

    resetForm() {
      this.$refs.passwordForm.resetFields();
    },
  },
};
</script>

<style lang="less" scoped>
.password-page {
  padding: 20px;
  background: transparent;
  min-height: calc(100vh - 70px);
}

.page-header {
  margin-bottom: 20px;
  
  h2 {
    font-size: 20px;
    font-weight: 600;
    color: #1f2937;
    margin: 0;
    letter-spacing: 0.3px;
  }
}

.card-container {
  max-width: 600px;
  margin: 0 auto;
}

.password-card {
  border-radius: 16px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.04);
  border: none;
  background: white;
  
  :deep(.el-card__body) {
    padding: 32px;
  }
}

.password-form {
  :deep(.el-form-item) {
    margin-bottom: 24px;
    
    &:last-of-type {
      margin-bottom: 0;
    }
  }
  
  :deep(.el-form-item__label) {
    font-weight: 500;
    color: #374151;
    font-size: 14px;
    padding-bottom: 8px;
  }
  
  :deep(.el-input__inner) {
    border-radius: 10px;
    border-color: #e5e7eb;
    height: 40px;
    line-height: 40px;
    font-size: 14px;
    transition: all 0.3s ease;
    
    &:focus {
      border-color: #667eea;
      box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    }
    
    &:hover {
      border-color: #d1d5db;
    }
  }
}

.button-group {
  display: flex;
  gap: 12px;
  margin-top: 8px;
  padding-top: 8px;
  
  :deep(.el-button) {
    flex: 1;
    height: 40px;
    border-radius: 8px;
    font-weight: 500;
    font-size: 14px;
    transition: all 0.3s ease;
  }
  
  :deep(.el-button--primary) {
    background: rgba(74, 144, 226, 0.2);
    border-color: rgba(74, 144, 226, 0.3);
    color: #4a90e2;
    
    &:hover:not(:disabled) {
      background: rgba(74, 144, 226, 0.3);
      border-color: rgba(74, 144, 226, 0.4);
      color: #3d7bc8;
      transform: translateY(-1px);
      box-shadow: 0 2px 8px rgba(74, 144, 226, 0.2);
    }
    
    &:active {
      transform: translateY(0);
    }
  }
  
  :deep(.el-button.is-plain) {
    border-color: rgba(0, 0, 0, 0.15);
    color: #6b7280;
    background: rgba(0, 0, 0, 0.04);
    
    &:hover:not(:disabled) {
      background: rgba(0, 0, 0, 0.08);
      border-color: rgba(0, 0, 0, 0.2);
      color: #374151;
      transform: translateY(-1px);
      box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    }
  }
}
</style>