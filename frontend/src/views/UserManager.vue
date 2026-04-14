<template>
  <div class="user-manager">
    <!-- 数据统计卡片 -->
    <div class="statistics-cards">
      <el-row :gutter="20">
        <el-col :span="6">
          <el-card shadow="hover" class="stat-card">
            <div class="stat-content">
              <div class="stat-left">
                <div class="stat-icon"><i class="el-icon-user-solid"></i></div>
                <div class="stat-title">总用户数</div>
              </div>
              <div class="stat-value">
                <count-to :startVal="0" :endVal="userStats.userTotal" :duration="2000">
                </count-to>
              </div>
            </div>
          </el-card>
        </el-col>
        <el-col :span="6">
          <el-card shadow="hover" class="stat-card">
            <div class="stat-content">
              <div class="stat-left">
                <div class="stat-icon"><i class="el-icon-user"></i></div>
                <div class="stat-title">普通用户</div>
              </div>
              <div class="stat-value">
                <count-to :startVal="0" :endVal="userStats.normalUsers" :duration="2000">
                </count-to>
              </div>
            </div>
          </el-card>
        </el-col>
        <el-col :span="6">
          <el-card shadow="hover" class="stat-card">
            <div class="stat-content">
              <div class="stat-left">
                <div class="stat-icon"><i class="el-icon-s-custom"></i></div>
                <div class="stat-title">管理员</div>
              </div>
              <div class="stat-value">
                <count-to :startVal="0" :endVal="userStats.admins" :duration="2000">
                </count-to>
              </div>
            </div>
          </el-card>
        </el-col>
        <el-col :span="6">
          <el-card shadow="hover" class="stat-card">
            <div class="stat-content">
              <div class="stat-left">
                <div class="stat-icon"><i class="el-icon-warning-outline"></i></div>
                <div class="stat-title">禁用账号</div>
              </div>
              <div class="stat-value">
                <count-to :startVal="0" :endVal="userStats.disabled" :duration="2000">
                </count-to>
              </div>
            </div>
          </el-card>
        </el-col>
      </el-row>
    </div>

    <!-- 搜索和操作区域 -->
    <el-card class="operation-area" shadow="hover">
      <el-form :inline="true" :model="searchForm" class="search-form">
        <el-form-item label="用户名">
          <el-input v-model="searchForm.username" placeholder="请输入用户名" clearable></el-input>
        </el-form-item>
        <el-form-item label="用户角色">
          <el-select v-model="searchForm.role" placeholder="请选择角色" clearable>
            <el-option
              v-for="option in roleOptions"
              :key="option.value"
              :label="option.label"
              :value="option.value">
            </el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="账号状态">
          <el-select v-model="searchForm.status" placeholder="请选择状态" clearable>
            <el-option label="启用" :value="1"></el-option>
            <el-option label="禁用" :value="0"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button size="medium" type="primary" @click="handleSearch" plain>查询</el-button>
          <el-button size="medium" @click="resetSearch" plain>重置</el-button>
        </el-form-item>
      </el-form>
      <div class="operation-buttons">
        <el-button type="primary" plain size="medium" @click="exportVisible = true">
          <i class="el-icon-download"></i> 导出数据
        </el-button>
        <el-button  type="primary" plain size="medium" @click="handleAdd">
          <i class="el-icon-plus"></i> 新增用户
        </el-button>
        <el-button plain size="medium" @click="getList">
          <i class="el-icon-refresh"></i> 刷新
        </el-button>
      </div>
    </el-card>

        <!-- 用户列表 -->
    <el-card class="table-card" shadow="hover">
      <el-table :data="users" v-loading="listLoading" style="width: 100%" class="card-table">
        <el-table-column prop="id" label="ID" width="80" align="center"></el-table-column>
        <el-table-column prop="username" label="用户名" min-width="120"></el-table-column>
        <el-table-column prop="name" label="真实姓名" min-width="120"></el-table-column>
        <el-table-column prop="email" label="邮箱" min-width="180"></el-table-column>
        <el-table-column prop="role" label="角色" width="120">
          <template slot-scope="scope">
            <el-tag v-if="scope.row.role === 'ADMIN'" type="warning">管理员</el-tag>
            <el-tag v-else type="info">普通用户</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="status" label="状态" width="100" align="center">
          <template slot-scope="scope">
            <el-switch
              v-model="scope.row.status"
              :active-value="1"
              :inactive-value="0"
              @change="handleStatusChange(scope.row)"
              active-color="#13ce66"
              inactive-color="#ff4949">
            </el-switch>
          </template>
        </el-table-column>
        <el-table-column label="创建时间" width="180">
          <template slot-scope="scope">
            {{ scope.row.createdAt | formatDate }}
          </template>
        </el-table-column>
        <el-table-column label="操作" width="200" align="center">
          <template slot-scope="scope">
            <el-button type="text" size="small" @click="handleEdit(scope.row)">
              <i class="el-icon-edit"></i> 编辑
            </el-button>
            <el-button type="text" size="small" class="delete-btn" @click="handleDelete(scope.row)">
              <i class="el-icon-delete"></i> 删除
            </el-button>
          </template>
        </el-table-column>
      </el-table>

      <!-- 分页 -->
      <pagination
        v-show="total > 0"
        :total="total"
        :page.sync="queryParams.currentPage"
        :limit.sync="queryParams.size"
        @pagination="getList"
      />
    </el-card>

    <!-- 导出数据 弹出栏 -->
    <el-dialog title="导出数据" :visible.sync="exportVisible" width="600px" :close-on-click-modal="false" append-to-body>
      <div class="export-data">
        <el-button type="primary" plain @click="exportTable('xlsx')" :disabled="isExporting">
          <i class="el-icon-document"></i> EXCEL格式
        </el-button>
        <el-button type="primary" plain @click="exportTable('csv')" :disabled="isExporting">
          <i class="el-icon-document"></i> CSV格式
        </el-button>
        <el-button type="primary" plain @click="exportTable('txt')" :disabled="isExporting">
          <i class="el-icon-document"></i> TXT格式
        </el-button>
      </div>
      <div v-if="isExporting" class="export-progress">
        <el-progress :percentage="exportProgress" :status="exportProgress === 100 ? 'success' : null" :stroke-width="20"></el-progress>
        <div class="progress-text">{{ exportProgressText }}</div>
      </div>
      <div class="hints">提示：请选择要导出数据的格式</div>
    </el-dialog>

    <!-- 用户表单对话框 -->
    <el-dialog :title="dialogTitle" :visible.sync="dialogVisible" width="500px" :close-on-click-modal="false" append-to-body>
      <el-form :model="form" :rules="rules" ref="form" label-width="100px">
        <el-form-item label="用户名" prop="username">
          <el-input v-model="form.username" placeholder="请输入用户名" :disabled="dialogMode === 'edit'"></el-input>
        </el-form-item>
        <el-form-item label="真实姓名" prop="name">
          <el-input v-model="form.name" placeholder="请输入真实姓名"></el-input>
        </el-form-item>
        <el-form-item label="邮箱" prop="email">
          <el-input v-model="form.email" placeholder="请输入邮箱"></el-input>
        </el-form-item>
        <el-form-item label="密码" prop="password" v-if="dialogMode === 'add'">
          <el-input v-model="form.password" type="password" placeholder="请输入密码"></el-input>
        </el-form-item>
        <el-form-item label="用户角色" prop="role">
          <el-select v-model="form.role" placeholder="请选择角色" style="width: 100%;">
            <el-option
              v-for="option in roleOptions"
              :key="option.value"
              :label="option.label"
              :value="option.value">
            </el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="账号状态" prop="status">
          <el-switch
            v-model="form.status"
            :active-value="1"
            :inactive-value="0"
            active-text="启用"
            inactive-text="禁用">
          </el-switch>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="dialogVisible = false">取 消</el-button>
        <el-button type="primary" @click="submitForm">确 定</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import Request from '@/utils/request'
import Pagination from '@/components/Pagination/index.vue'
import CountTo from 'vue-count-to'
import excel from '@/utils/excel.js'
// import { hasInviteCode, isValidDate } from '@/utils/inviteCode'

export default {
  name: 'UserManager',
  components: { Pagination, CountTo },
  inject: ['userInfo'],
  data() {
    // 邮箱验证规则
    const validateEmail = (rule, value, callback) => {
      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
      if (!value) {
        callback(new Error('请输入邮箱地址'))
      } else if (!emailRegex.test(value)) {
        callback(new Error('请输入正确的邮箱地址'))
      } else {
        callback()
      }
    }

    return {
      // 搜索表单
      searchForm: {
        username: '',
        role: '',
        status: ''
      },
      // 查询参数
      queryParams: {
        currentPage: 1,
        size: 10
      },
      // 用户列表
      users: [],
      // 总数
      total: 0,
      // 加载状态
      listLoading: false,
      // 对话框显示
      dialogVisible: false,
      // 对话框标题
      dialogTitle: '',
      // 对话框模式
      dialogMode: 'add',
      // 导出数据弹出框显示/隐藏
      exportVisible: false,
      // 导出进度
      exportProgress: 0,
      // 是否正在导出
      isExporting: false,
      // 导出进度文本
      exportProgressText: '',
      // 表单数据
      form: {
        username: '',
        name: '',
        email: '',
        password: '',
        role: '',
        status: 1
      },
      // 用户统计
      userStats: {
        normalUsers: 0,
        userTotal: 0,
        admins: 0,
        disabled: 0
      },
      // 表单校验规则
      rules: {
        username: [
          { required: true, message: '请输入用户名', trigger: 'blur' },
          { min: 3, max: 20, message: '长度在 3 到 20 个字符', trigger: 'blur' }
        ],
        name: [
          { required: true, message: '请输入真实姓名', trigger: 'blur' }
        ],
        email: [
          { required: true, validator: validateEmail, trigger: 'blur' }
        ],
        password: [
          { required: true, message: '请输入密码', trigger: 'blur' },
          { min: 6, message: '密码长度不能小于6位', trigger: 'blur' }
        ],
        role: [
          { required: true, message: '请选择用户角色', trigger: 'change' }
        ]
      },
      // 添加当前用户角色相关数据
      currentRole: '',
      roleOptions: [], // 动态角色选项
    }
  },
  created() {
    // this.checkInviteCode()
    this.currentRole = this.userInfo.role
    this.initRoleOptions()
    this.getList()
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
    // 初始化角色选项
    */
    // role options
    initRoleOptions() {
      switch (this.currentRole) {
        case 'USER':
          this.roleOptions = [
            { label: '普通用户', value: 'USER' }
          ]
          break
        case 'ADMIN':
          this.roleOptions = [
            { label: '管理员', value: 'ADMIN' },
            { label: '普通用户', value: 'USER' }
          ]
          break
        default:
          this.roleOptions = [
            { label: '普通用户', value: 'USER' },
            { label: '管理员', value: 'ADMIN' }
          ]
      }
    },

    // 获取用户列表
    async getList() {
      this.listLoading = true
      try {
        const params = {
          ...this.queryParams,
          ...this.searchForm
        }
        const res = await Request.get('/user/page', { params })
        if (res.code === '0') {
          // 修改用户列表过滤逻辑
          this.users = res.data.records.filter(user => {
            // 管理员可以看到普通用户和管理员
            if (this.currentRole === 'ADMIN') {
              return ['USER', 'ADMIN'].includes(user.role)
            }
            // 普通用户只能看到自己
            if (this.currentRole === 'USER') {
              return user.id === this.userInfo.id
            }
            return false
          })
          // 使用后端返回的总数，而不是过滤后的长度
          this.total = res.data.total
          this.calculateUserStats()
        }
      } catch (error) {
        // 静默处理获取用户列表失败
      } finally {
        this.listLoading = false
      }
    },

    // 计算用户统计数据
    calculateUserStats() {
      this.userStats = {
        normalUsers: this.users.filter(user => user.role === 'USER').length,
        userTotal: this.users.length,
        admins: this.users.filter(user => user.role === 'ADMIN').length,
        disabled: this.users.filter(user => user.status === 0).length
      }
    },

    // 搜索
    handleSearch() {
      this.queryParams.currentPage = 1
      this.getList()
    },

    // 重置搜索
    resetSearch() {
      this.searchForm = {
        username: '',
        role: '',
        status: ''
      }
      this.handleSearch()
    },

    // 新增用户
    handleAdd() {
      this.dialogMode = 'add'
      this.dialogTitle = '新增用户'
      this.form = {
        username: '',
        name: '',
        email: '',
        password: '',
        role: '',
        status: 1
      }
      this.dialogVisible = true
    },

    // 编辑用户
    handleEdit(row) {
      // 检查权限
      // if (this.currentRole === 'ADMIN' && (row.role === 'SUPER_ADMIN' || row.role === 'ADMIN')) {
      //   this.$message.error('没有权限编辑该用户')
      //   return
      // }
      
      this.dialogMode = 'edit'
      this.dialogTitle = '编辑用户'
      this.form = { ...row }
      delete this.form.password
      this.dialogVisible = true
    },

    // 删除用户
    handleDelete(row) {
      // 检查权限
      // if (this.currentRole === 'ADMIN' && (row.role === 'SUPER_ADMIN' || row.role === 'ADMIN')) {
      //   this.$message.error('没有权限删除该用户')
      //   return
      // }

      this.$confirm('确认删除该用户?', '提示', {
        type: 'warning'
      }).then(async () => {
        try {
          const res = await Request.delete(`/user/delete/${row.id}`)
          if (res.code === '0') {
            this.$message.success('删除成功')
            this.getList()
          }
        } catch (error) {
          // 静默处理删除用户失败
        }
      }).catch(() => {})
    },

    // 更改用户状态
    async handleStatusChange(row) {
      // 检查权限
      // if (this.currentRole === 'ADMIN' && (row.role === 'SUPER_ADMIN' || row.role === 'ADMIN')) {
      //   this.$message.error('没有权限修改该用户状态')
      //   row.status = row.status === 1 ? 0 : 1 // 恢复状态
      //   return
      // }

      try {
        const res = await Request.put(`/user/${row.id}`, {
          status: row.status
        })
        if (res.code === '0') {
          this.$message.success('状态更新成功')
          this.calculateUserStats()
        } else {
          row.status = row.status === 1 ? 0 : 1
          this.$message.error('状态更新失败')
        }
      } catch (error) {
        row.status = row.status === 1 ? 0 : 1
        // 静默处理更新用户状态失败
        this.$message.error('更新失败')
      }
    },

    // 提交表单
    submitForm() {
      this.$refs.form.validate(async (valid) => {
        if (valid) {
          try {
            const method = this.dialogMode === 'add' ? 'post' : 'put'
            const url = this.dialogMode === 'add' ? '/user/add' : `/user/${this.form.id}`
            
            // 添加加载状态
            this.$loading({
              lock: true,
              text: '提交中...',
              spinner: 'el-icon-loading'
            })
            
            const res = await Request[method](url, this.form)
            
            if (res.code === '0') {
              this.$message.success(`${this.dialogMode === 'add' ? '添加' : '更新'}成功`)
              this.dialogVisible = false
              this.getList()
            } else {
              // 处理后端返回的错误
              this.$message.error(res.msg || '操作失败')
            }
          } catch (error) {
            // 静默处理提交表单失败
            this.$message.error(error.response?.data?.msg || '操作失败，请稍后重试')
          } finally {
            // 关闭加载状态
            this.$loading().close()
          }
        } else {
          // 表单验证失败
          this.$message.warning('请填写完整所有必填项')
          return false
        }
      })
    },

    // 导出数据--excel格式
    async exportTable(type) {
      if (this.users.length) {
        try {
          // 初始化导出状态
          this.isExporting = true
          this.exportProgress = 0
          this.exportProgressText = '准备导出...'
          
          // 进度更新回调函数
          const updateProgress = (progress, text) => {
            this.exportProgress = progress
            this.exportProgressText = text
          }
          
          // 格式化数据（占0-70%）
          updateProgress(10, '正在格式化数据...')
          const exportData = []
          const totalItems = this.users.length
          
          for (let i = 0; i < this.users.length; i++) {
            const user = this.users[i]
            exportData.push({
              ...user,
              role: user.role === 'ADMIN' ? '管理员' : '普通用户',
              status: user.status === 1 ? '启用' : '禁用',
              createdAt: user.createdAt ? new Date(user.createdAt).toLocaleString() : ''
            })
            
            // 每处理10条更新一次进度
            if ((i + 1) % 10 === 0 || i === this.users.length - 1) {
              const progress = 10 + Math.round(((i + 1) / totalItems) * 60)
              updateProgress(progress, `正在格式化数据: ${i + 1}/${totalItems}`)
              // 使用 setTimeout 让 UI 有机会更新
              await new Promise(resolve => setTimeout(resolve, 0))
            }
          }
          
          // 导出文件（占70%-100%）
          updateProgress(75, '正在生成文件...')
          const params = {
            header: ['ID', '用户名', '真实姓名', '邮箱', '角色', '状态', '创建时间'],
            key: ['id', 'username', 'name', 'email', 'role', 'status', 'createdAt'],
            data: exportData,
            autoWidth: true,
            fileName: '用户数据表',
            bookType: type
          }
          
          // 使用 setTimeout 确保进度条更新
          await new Promise(resolve => setTimeout(resolve, 100))
          updateProgress(90, '正在保存文件...')
          
          excel.exportDataToExcel(params)
          
          // 完成
          updateProgress(100, '导出完成！')
          await new Promise(resolve => setTimeout(resolve, 500))
          
          this.isExporting = false
          this.exportProgress = 0
          this.exportProgressText = ''
          this.exportVisible = false
          this.$message.success('导出成功')
        } catch (error) {
          console.error('导出失败:', error)
          this.isExporting = false
          this.exportProgress = 0
          this.exportProgressText = ''
          this.$message.error('导出失败，请稍后重试')
        }
      } else {
        this.$message.warning('暂无数据可导出')
      }
    }
  },
  filters: {
    formatDate(timestamp) {
      if (!timestamp) return ''
      const date = new Date(timestamp)
      return date.toLocaleString()
    }
  }
}
</script>

<style lang="less" scoped>
.user-manager {
  padding: 12px;
  background: linear-gradient(to bottom, #f5f7fa 0%, #ffffff 100%);
  min-height: calc(100vh - 70px);
  position: relative;

  &::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background-image: 
      radial-gradient(circle at 20% 50%, rgba(102, 126, 234, 0.03) 0%, transparent 50%),
      radial-gradient(circle at 80% 80%, rgba(118, 75, 162, 0.03) 0%, transparent 50%);
    pointer-events: none;
    z-index: 0;
  }

  > * {
    position: relative;
    z-index: 1;
  }
}

.page-header {
  display: flex;
  align-items: center;
  margin-bottom: 20px;

  h2 {
    font-size: 18px;
    font-weight: 600;
    color: #1f2937;
    margin: 0;
    margin-right: 15px;
    letter-spacing: 0.3px;
  }
}

.operation-area {
  background: rgba(255, 255, 255, 0.95);
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
  margin-bottom: 24px;
  padding: 24px;
  border: 1px solid rgba(0, 0, 0, 0.06);
  backdrop-filter: blur(10px);

  :deep(.el-card__body) {
    padding: 0;
  }
}

.search-form {
  margin-bottom: 0;
  padding-bottom: 16px;
  border-bottom: 1px solid #f3f4f6;
  
  :deep(.el-form-item) {
    margin-bottom: 0;
    margin-right: 20px;
    
    &:last-child {
      margin-right: 0;
    }
  }
  
  :deep(.el-form-item__label) {
    color: #374151;
    font-weight: 500;
    font-size: 14px;
    padding-right: 8px;
  }
}

.operation-buttons {
  margin-top: 16px;
  display: flex;
  gap: 12px;
  padding-top: 16px;
}

.statistics-cards {
  margin-bottom: 24px;
}

.stat-card {
  border-radius: 12px;
  transition: all 0.3s ease;
  border: none;
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.9) 0%, rgba(255, 255, 255, 0.95) 100%);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
  position: relative;
  overflow: hidden;
  backdrop-filter: blur(10px);

  &::before {
    display: none;
  }

  &:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
  }

  :deep(.el-card__body) {
    padding: 0;
  }
}

.stat-content {
  padding: 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.stat-left {
  display: flex;
  align-items: center;
  gap: 14px;
}

.stat-icon {
  font-size: 28px;
  color: #4a90e2;
  opacity: 0.9;
  width: 52px;
  height: 52px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 12px;
  background: linear-gradient(135deg, rgba(74, 144, 226, 0.1) 0%, rgba(74, 144, 226, 0.05) 100%);
  transition: all 0.3s ease;
}

.stat-card:nth-child(1) .stat-icon {
  background: linear-gradient(135deg, rgba(74, 144, 226, 0.12) 0%, rgba(74, 144, 226, 0.06) 100%);
  color: #4a90e2;
}

.stat-card:nth-child(2) .stat-icon {
  background: linear-gradient(135deg, rgba(102, 126, 234, 0.12) 0%, rgba(102, 126, 234, 0.06) 100%);
  color: #667eea;
}

.stat-card:nth-child(3) .stat-icon {
  background: linear-gradient(135deg, rgba(139, 92, 246, 0.12) 0%, rgba(139, 92, 246, 0.06) 100%);
  color: #8b5cf6;
}

.stat-card:nth-child(4) .stat-icon {
  background: linear-gradient(135deg, rgba(236, 72, 153, 0.12) 0%, rgba(236, 72, 153, 0.06) 100%);
  color: #ec4899;
}

.stat-card:hover .stat-icon {
  transform: scale(1.05);
}

.stat-title {
  font-size: 14px;
  color: #6b7280;
  font-weight: 500;
  letter-spacing: 0.2px;
}

.stat-value {
  font-size: 28px;
  font-weight: 700;
  color: #1f2937;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
  letter-spacing: 0.5px;
  
  &::after {
    display: none;
  }
}

.table-card {
  border-radius: 16px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.04);
  padding-bottom: 20px;
  background: white;
  border: none;

  :deep(.el-card__header) {
    background: transparent;
  }

  :deep(.el-card__body) {
    padding: 20px;
  }
}

.operation-buttons {
  margin-top: 16px;
  display: flex;
  gap: 12px;
}

:deep(.el-form) {
  margin-bottom: 0;
}

:deep(.el-form-item) {
  margin-bottom: 16px;
}

:deep(.el-table) {
  border-radius: 12px;
  overflow: visible;
  box-shadow: none;
  border: none;
  background: transparent;

  .el-table__header-wrapper {
    th {
      background-color: transparent;
      font-weight: 600;
      color: #374151;
      padding: 16px 12px;
      font-size: 14px;
      border-bottom: none;
    }
  }

  .el-table__body-wrapper {
    .el-table__body {
      tr {
        background: white;
        border-radius: 8px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
        transition: all 0.3s ease;
        margin-bottom: 12px;
        display: table-row;
        
        &:hover {
          transform: translateY(-2px);
          box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
          background: white;
        }
        
        td {
          padding: 16px 12px;
          color: #4b5563;
          font-size: 14px;
          border-bottom: none;
        }
      }
      
      // 创建行间距
      tr + tr {
        margin-top: 12px;
      }
    }
  }
  
  &::before {
    display: none;
  }
  
  .el-table__header,
  .el-table__body {
    border: none;
  }
  
  .el-table__header th,
  .el-table__body td {
    border: none;
  }
}

// 卡片式表格样式
.card-table {
  :deep(.el-table__body-wrapper) {
    padding: 12px 0;
    
    .el-table__body {
      border-collapse: separate;
      border-spacing: 0 12px;
      
      tr {
        background: white;
        border-radius: 8px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
        transition: all 0.3s ease;
        
        &:hover {
          transform: translateY(-2px);
          box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
        }
        
        td {
          border-bottom: none;
          background: white;
          padding: 16px 12px;
          
          &:first-child {
            border-top-left-radius: 8px;
            border-bottom-left-radius: 8px;
          }
          
          &:last-child {
            border-top-right-radius: 8px;
            border-bottom-right-radius: 8px;
          }
        }
      }
    }
  }
  
  :deep(.el-table__header-wrapper) {
    .el-table__header {
      border-collapse: separate;
      
      th {
        background-color: transparent;
        border-bottom: none;
        padding: 16px 12px;
      }
    }
  }
}

.delete-btn {
  color: #ef4444;
  margin-left: 12px;
  transition: color 0.3s ease;

  &:hover {
    color: #dc2626;
  }
}

:deep(.el-button--text) {
  padding: 0 8px;
  font-size: 14px;
  transition: all 0.3s ease;
  color: #6b7280;

  &:hover {
    background-color: rgba(74, 144, 226, 0.1);
    color: #4a90e2;
  }
}

:deep(.el-input__inner) {
  border-radius: 8px;
  border-color: #e5e7eb;
  transition: all 0.3s ease;

  &:focus {
    border-color: #667eea;
  }
}

:deep(.el-select .el-input__inner) {
  border-radius: 8px;
}

:deep(.el-button) {
  border-radius: 8px;
  font-weight: 500;
  transition: all 0.3s ease;

  // 主要按钮 - 浅色风格
  &.el-button--primary.is-plain {
    border-color: rgba(74, 144, 226, 0.3);
    color: #4a90e2;
    background: rgba(74, 144, 226, 0.08);

    &:hover:not(:disabled) {
      background: rgba(74, 144, 226, 0.15);
      border-color: rgba(74, 144, 226, 0.4);
      color: #3d7bc8;
      transform: translateY(-1px);
      box-shadow: 0 2px 8px rgba(74, 144, 226, 0.2);
    }

    &:disabled {
      border-color: rgba(74, 144, 226, 0.15);
      color: rgba(74, 144, 226, 0.4);
      background: rgba(74, 144, 226, 0.04);
      cursor: not-allowed;
    }
  }

  // 普通按钮 - 浅色风格
  &.el-button--default.is-plain {
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

    &:disabled {
      border-color: rgba(0, 0, 0, 0.08);
      color: rgba(0, 0, 0, 0.25);
      background: rgba(0, 0, 0, 0.02);
      cursor: not-allowed;
    }
  }

  // 普通按钮（非plain）- 浅色风格
  &.el-button--default:not(.is-plain) {
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

  // 成功按钮 - 浅色风格
  &.el-button--success.is-plain {
    border-color: rgba(16, 185, 129, 0.3);
    color: #10b981;
    background: rgba(16, 185, 129, 0.08);

    &:hover:not(:disabled) {
      background: rgba(16, 185, 129, 0.15);
      border-color: rgba(16, 185, 129, 0.4);
      color: #059669;
      transform: translateY(-1px);
      box-shadow: 0 2px 8px rgba(16, 185, 129, 0.2);
    }
  }

  // 危险按钮 - 浅色风格
  &.el-button--danger.is-plain {
    border-color: rgba(239, 68, 68, 0.3);
    color: #ef4444;
    background: rgba(239, 68, 68, 0.08);

    &:hover:not(:disabled) {
      background: rgba(239, 68, 68, 0.15);
      border-color: rgba(239, 68, 68, 0.4);
      color: #dc2626;
      transform: translateY(-1px);
      box-shadow: 0 2px 8px rgba(239, 68, 68, 0.2);
    }
  }

  // 主要按钮（非plain）- 浅色风格
  &.el-button--primary:not(.is-plain) {
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
  }

  // 所有尺寸统一样式
  &.el-button--mini,
  &.el-button--small,
  &.el-button--medium {
    border-radius: 6px;
    font-weight: 500;
  }
}

:deep(.el-button--text) {
  padding: 0 8px;
  font-size: 14px;
  transition: all 0.3s ease;
  color: #6b7280;

  &:hover {
    background-color: rgba(74, 144, 226, 0.1);
    color: #4a90e2;
  }
}

.delete-btn {
  color: #ef4444;
  margin-left: 12px;
  transition: color 0.3s ease;

  &:hover {
    color: #dc2626;
    background-color: rgba(239, 68, 68, 0.1);
  }
}

.export-data {
  display: flex;
  justify-content: space-around;
  margin-bottom: 20px;
  gap: 12px;
}

.export-progress {
  margin: 20px 0;
  padding: 20px;
  background: #f9fafb;
  border-radius: 8px;
  
  .progress-text {
    text-align: center;
    margin-top: 12px;
    color: #374151;
    font-size: 14px;
    font-weight: 500;
  }
}

.hints {
  text-align: center;
  color: #6b7280;
  font-size: 13px;
}

/* 美化对话框 */
:deep(.el-dialog) {
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.12);
}

:deep(.el-dialog__header) {
  padding: 20px 24px;
  border-bottom: 1px solid #e5e7eb;
  margin: 0;
  background: #f9fafb;
}

:deep(.el-dialog__title) {
  font-size: 18px;
  font-weight: 600;
  color: #1f2937;
  letter-spacing: 0.3px;
}

:deep(.el-dialog__body) {
  padding: 24px;
}

:deep(.el-dialog__footer) {
  padding: 16px 24px;
  border-top: 1px solid #e5e7eb;
  background: #f9fafb;
}
</style>
