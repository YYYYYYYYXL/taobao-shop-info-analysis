<template>
  <div class="person-info">
    <div class="page-header">
      <h2></h2>
    </div>
    <div class="card-container">
      <el-card class="info-card" shadow="hover">
        <!-- 头像上传区域 - 独立于表单之外 -->
        <div class="avatar-section">
          <el-upload
            class="avatar-uploader"
            action="#"
            :show-file-list="false"
            :before-upload="beforeAvatarUpload"
            :http-request="uploadAvatar"
            accept="image/*"
          >
            <div class="avatar-wrapper">
              <el-avatar 
                :size="120" 
                :src="avatarUrl"
                class="avatar-preview"
              >
                <span v-if="!avatarUrl">{{userInfo.name ? userInfo.name.charAt(0) : 'U'}}</span>
              </el-avatar>
              <div class="avatar-overlay">
                <i class="el-icon-camera"></i>
                <span>上传头像</span>
              </div>
            </div>
          </el-upload>
          <div class="avatar-tips">
            <p>支持 JPG、PNG 格式，大小不超过 5MB</p>
          </div>
        </div>

        <el-form 
          :model="userInfo" 
          :rules="rules" 
          ref="userInfoForm" 
          label-width="100px"
          class="info-form"
        >
          <el-form-item label="用户名" prop="username">
            <el-input 
              v-model="userInfo.username" 
              disabled
              placeholder="用户名不可修改"
            />
          </el-form-item>

          <el-form-item label="姓名" prop="name">
            <el-input 
              v-model="userInfo.name"
              placeholder="请输入姓名"
            />
          </el-form-item>

          <el-form-item label="邮箱" prop="email">
            <el-input 
              v-model="userInfo.email"
              placeholder="请输入邮箱地址"
            />
          </el-form-item>
        </el-form>
        
        <el-button type="primary" @click="update" icon="el-icon-check" class="save-button">
          保存修改
        </el-button>
      </el-card>
    </div>
  </div>
</template>

<script>
import request from '@/utils/request';
import axios from 'axios';
import { getDeviceId } from '@/utils/deviceId';

export default {
  name: 'PersonInfo',
  inject: ['userInfo'],
  
  data() {
    return {
      rules: {
        name: [
          { required: true, message: '姓名不能为空', trigger: 'blur' },
          { min: 2, max: 10, message: '姓名长度必须在2到10个字符之间', trigger: 'blur' }
        ],
        email: [
          { required: true, message: '邮箱不能为空', trigger: 'blur' },
          { type: 'email', message: '请输入正确的邮箱地址', trigger: ['blur', 'change'] }
        ]
      }
    };
  },

  computed: {
    avatarUrl() {
      if (this.userInfo && this.userInfo.avatar) {
        // avatar 是相对路径，如 /img/avatar/xxx.jpg，需要拼接 API 前缀
        if (this.userInfo.avatar.startsWith('/')) {
          return `/api${this.userInfo.avatar}`
        }
        return this.userInfo.avatar
      }
      return null
    }
  },

  methods: {
    getRoleName(role) {
      const roleMap = {
        'ADMIN': '管理员',
        'USER': '普通用户'
      }
      return roleMap[role]
    },

    beforeAvatarUpload(file) {
      const isImage = file.type.startsWith('image/');
      const isLt5M = file.size / 1024 / 1024 < 5;

      if (!isImage) {
        this.$message.error('只能上传图片文件!');
        return false;
      }
      if (!isLt5M) {
        this.$message.error('图片大小不能超过 5MB!');
        return false;
      }
      return true;
    },

    uploadAvatar(options) {
      const formData = new FormData();
      formData.append('file', options.file);

      // 使用 axios 直接上传，因为需要使用 multipart/form-data
      const token = this.userInfo.token;
      const deviceId = getDeviceId();
      
      axios.post(`/api/user/avatar/${this.userInfo.id}`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
          'token': token,
          'X-Device-Id': deviceId
        }
      }).then(response => {
        if (response.data.code === '0') {
          this.$message({
            type: 'success',
            message: '头像上传成功!'
          });
          // 更新用户信息（确保包含 avatar 字段）
          const updatedUser = response.data.data;
          Object.assign(this.userInfo, updatedUser);
          // 更新 localStorage
          localStorage.setItem("userInfo", JSON.stringify(this.userInfo));
          // 触发更新事件，通知父组件
          this.$emit("update:user", this.userInfo);
          // 强制更新视图
          this.$forceUpdate();
        } else {
          this.$message({
            type: 'error',
            message: response.data.msg || '头像上传失败'
          });
        }
      }).catch(error => {
        this.$message({
          type: 'error',
          message: '头像上传失败：' + (error.response?.data?.msg || error.message)
        });
      });
    },

    update() {
      this.$refs.userInfoForm.validate((valid) => {
        if (valid) {
          // 确保包含 avatar 字段
          const updateData = {
            ...this.userInfo,
            avatar: this.userInfo.avatar || null
          };
          
          request.put("/user/" + this.userInfo.id, updateData).then(response => {
            if (response.code == '0') {
              this.$message({
                type: 'success',
                message: '信息保存成功!'
              });
              // 更新用户信息（使用后端返回的最新数据）
              const updatedUser = response.data || updateData;
              // 确保 avatar 字段被保留
              if (updatedUser.avatar) {
                this.userInfo.avatar = updatedUser.avatar;
              }
              Object.assign(this.userInfo, updatedUser);
              localStorage.setItem("userInfo", JSON.stringify(this.userInfo));
              this.$emit("update:user", this.userInfo);
              // 强制更新视图
              this.$forceUpdate();
            } else {
              this.$message({
                type: 'error',
                message: response.msg
              })
            }
          })
        } else {
          return false;
        }
      });
    }
  }
};
</script>

<style lang="less" scoped>
.person-info {
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

.info-card {
  border-radius: 16px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.04);
  border: none;
  background: white;
  
  :deep(.el-card__body) {
    padding: 32px;
  }
}

.info-form {
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
    
    &:disabled {
      background-color: #f9fafb;
      color: #6b7280;
      cursor: not-allowed;
    }
  }
  
}

.save-button {
  width: calc(100% - 80px);
  height: 40px;
  border-radius: 10px;
  font-weight: 500;
  font-size: 14px;
  transition: all 0.3s ease;
  margin: 20px 40px 0 40px;
}

  :deep(.save-button.el-button--primary) {
    background: rgba(74, 144, 226, 0.2);
    border-color: rgba(74, 144, 226, 0.3);
    color: #4a90e2;
    border-radius: 8px;
    
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

/* 头像区域样式 */
.avatar-section {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 32px 0;
  border-bottom: 1px solid #f0f0f0;
  margin-bottom: 24px;
}

.avatar-uploader {
  :deep(.el-upload) {
    border: none;
    border-radius: 0;
    cursor: pointer;
    position: relative;
    overflow: visible;
  }
}

.avatar-wrapper {
  position: relative;
  width: 120px;
  height: 120px;
  cursor: pointer;
  
  .avatar-preview {
    width: 120px !important;
    height: 120px !important;
    border-radius: 50%;
    transition: all 0.3s ease;
  }
  
  .avatar-overlay {
    position: absolute;
    top: 0;
    left: 0;
    width: 120px;
    height: 120px;
    border-radius: 50%;
    background-color: rgba(0, 0, 0, 0.5);
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    opacity: 0;
    transition: all 0.3s ease;
    color: white;
    
    i {
      font-size: 24px;
      margin-bottom: 8px;
    }
    
    span {
      font-size: 14px;
    }
  }
  
  &:hover {
    .avatar-overlay {
      opacity: 1;
      transform: scale(1.05);
    }
    
    .avatar-preview {
      transform: scale(1.05);
    }
  }
}

.avatar-tips {
  margin-top: 16px;
  color: #909399;
  font-size: 12px;
  text-align: center;
  
  p {
    margin: 0;
  }
}
</style>