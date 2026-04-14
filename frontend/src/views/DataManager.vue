<template>
  <div class="order-manager">
    <!-- 数据统计卡片 -->
    <div class="statistics-cards">
      <el-row :gutter="20">
        <el-col :span="6">
          <el-card shadow="hover" class="stat-card">
            <div class="stat-content">
              <div class="stat-left">
                <div class="stat-icon"><i class="el-icon-coin"></i></div>
                <div class="stat-title">总数据量</div>
              </div>
              <div class="stat-value">
                <count-to :startVal="0" :endVal="statistics.totalCount" :duration="2000">
                </count-to>
              </div>
            </div>
          </el-card>
        </el-col>
        <el-col :span="6">
          <el-card shadow="hover" class="stat-card">
            <div class="stat-content">
              <div class="stat-left">
                <div class="stat-icon"><i class="el-icon-connection"></i></div>
                <div class="stat-title">商品数量</div>
              </div>
              <div class="stat-value">
                <count-to :startVal="0" :endVal="statistics.productCount" :duration="2000">
                </count-to>
              </div>
            </div>
          </el-card>
        </el-col>
        <el-col :span="6">
          <el-card shadow="hover" class="stat-card">
            <div class="stat-content">
              <div class="stat-left">
                <div class="stat-icon"><i class="el-icon-odometer"></i></div>
                <div class="stat-title">总销量</div>
              </div>
              <div class="stat-value">
<!--                <span class="stat-amount">{{ Number(statistics.totalSalesAmount || 0).toFixed(0) }}</span>-->
                <span class="stat-amount">{{ Number(statistics.salesVolume || 0).toLocaleString() }}</span>
              </div>
            </div>
          </el-card>
        </el-col>
        <el-col :span="6">
          <el-card shadow="hover" class="stat-card">
            <div class="stat-content">
              <div class="stat-left">
                <div class="stat-icon"><i class="el-icon-place"></i></div>
                <div class="stat-title">店铺数量</div>
              </div>
              <div class="stat-value">
                <count-to :startVal="0" :endVal="statistics.shopCount" :duration="2000">
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
        <el-form-item label="类目">
          <el-input v-model="searchForm.category" placeholder="请输入商品类目" clearable></el-input>
        </el-form-item>
        <el-form-item label="省份">
          <el-input v-model="searchForm.province" placeholder="请输入省份" clearable></el-input>
        </el-form-item>
        <el-form-item label="店铺名称">
          <el-input v-model="searchForm.shopName" placeholder="请输入店铺名称" clearable></el-input>
        </el-form-item>
        <el-form-item label="商品标题">
          <el-input v-model="searchForm.productTitle" placeholder="请输入商品标题关键字" clearable></el-input>
        </el-form-item>
        <el-form-item>
          <el-button size="medium" plain type="primary" @click="handleSearch">查询</el-button>
          <el-button size="medium" plain @click="resetSearch">重置</el-button>
        </el-form-item>
      </el-form>
      <div class="operation-buttons">
        <el-button plain size="medium" type="primary" @click="exportVisible = true">
          <i class="el-icon-download"></i> 导出数据
        </el-button>
        <el-button plain size="medium" type="primary" icon="el-icon-plus" class="add-button" @click="handleAdd">新增商品数据</el-button>
        <el-button plain size="medium" icon="el-icon-refresh" @click="getList">刷新</el-button>
      </div>
    </el-card>

    <!-- 商品数据列表 -->
    <el-card class="table-card" shadow="hover">
      <el-table :data="saleDataList" style="width: 100%" class="card-table">
        <el-table-column prop="productId" label="ID" show-overflow-tooltip></el-table-column>
        <el-table-column prop="productTitle" label="标题" show-overflow-tooltip width="220"></el-table-column>
        <el-table-column prop="category" label="类目" show-overflow-tooltip></el-table-column>
        <el-table-column prop="productPrice" label="价格" show-overflow-tooltip>
          <template slot-scope="scope">
            ¥{{ Number(scope.row.productPrice || 0).toFixed(2) }}
          </template>
        </el-table-column>
        <el-table-column prop="productSales" label="销量" show-overflow-tooltip>
          <template slot-scope="scope">
            {{ Number(scope.row.productSales || 0).toLocaleString() }}
          </template>
        </el-table-column>
        <el-table-column prop="province" label="省份" show-overflow-tooltip></el-table-column>
        <el-table-column prop="shopName" label="店铺" show-overflow-tooltip></el-table-column>
        <el-table-column prop="style" label="风格" show-overflow-tooltip></el-table-column>
        <el-table-column prop="pattern" label="图案" show-overflow-tooltip></el-table-column>
        <el-table-column prop="fabric" label="面料" show-overflow-tooltip></el-table-column>
        <el-table-column prop="fitType" label="版型" show-overflow-tooltip></el-table-column>
        <el-table-column prop="season" label="季节" show-overflow-tooltip></el-table-column>
        <el-table-column label="操作"  width="200px">
          <template slot-scope="scope">
            <el-button type="text" size="small" icon="el-icon-edit" @click="handleEdit(scope.row)">编辑</el-button>
            <el-button type="text" size="small" icon="el-icon-delete" class="delete-btn" @click="handleDelete(scope.row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
      <!-- 分页 -->
      <pagination v-show="total > 0" :total="total" :page.sync="queryParams.currentPage" :limit.sync="queryParams.size" @pagination="getList" />
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

    <!-- 商品数据表单对话框 -->
    <el-dialog :title="dialogTitle" :visible.sync="dialogVisible" width="1000px" :close-on-click-modal="false" append-to-body>
      <el-form :model="form" :rules="rules" ref="form" label-width="100px" class="order-form">
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="商品ID" prop="productId">
              <el-input v-model="form.productId" placeholder="请输入商品ID"></el-input>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="商品标题" prop="productTitle">
              <el-input v-model="form.productTitle" placeholder="请输入商品标题"></el-input>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="类目" prop="category">
              <el-input v-model="form.category" placeholder="请输入商品类目"></el-input>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="省份">
              <el-input v-model="form.province" placeholder="请输入省份"></el-input>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="商品价格" prop="productPrice">
              <el-input-number v-model="form.productPrice" :precision="2" :step="0.01" :min="0" style="width: 100%;"></el-input-number>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="销量" prop="productSales">
              <el-input-number v-model="form.productSales" :precision="0" :step="1" :min="0" style="width: 100%;"></el-input-number>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="店铺名称" prop="shopName">
              <el-input v-model="form.shopName" placeholder="请输入店铺名称"></el-input>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="店铺标签">
              <el-input v-model="form.shopTag" placeholder="请输入店铺标签"></el-input>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="花呗分期">
              <el-input v-model="form.buyNowPayLater" placeholder="是否支持花呗分期"></el-input>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="退货服务">
              <el-input v-model="form.returnService" placeholder="是否支持退货服务"></el-input>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="风格">
              <el-input v-model="form.style" placeholder="请输入商品风格"></el-input>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="图案">
              <el-input v-model="form.pattern" placeholder="请输入商品图案"></el-input>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="面料">
              <el-input v-model="form.fabric" placeholder="请输入面料信息"></el-input>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="版型">
              <el-input v-model="form.fitType" placeholder="请输入版型信息"></el-input>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="季节">
              <el-input v-model="form.season" placeholder="请输入适用季节"></el-input>
            </el-form-item>
          </el-col>
        </el-row>
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
import { MessageBox } from 'element-ui'
import excel from '@/utils/excel.js'

export default {
  name: 'OrderManager',
  inject: ['userInfo'],
  components: {
    Pagination,
    CountTo
  },
  data() {
    return {
      // 搜索表单
      searchForm: {
        category: '',
        province: '',
        shopName: '',
        productTitle: ''
      },
      // 查询参数
      queryParams: {
        currentPage: 1,
        size: 10
      },
      // 商品数据列表
      saleDataList: [],
      // 总数
      total: 0,
      // 统计数据
      statistics: {
        totalCount: 0,
        productCount: 0,
        totalSalesAmount: 0,
        salesVolume: 0,
        shopCount: 0
      },
      // 对话框显示
      dialogVisible: false,
      // 对话框标题
      dialogTitle: '',
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
        id: undefined,
        productId: '',
        category: '',
        productTitle: '',
        productPrice: 0,
        province: '',
        productSales: 0,
        shopName: '',
        shopTag: '',
        buyNowPayLater: '',
        returnService: '',
        style: '',
        pattern: '',
        fabric: '',
        fitType: '',
        season: ''
      },
      // 表单校验规则
      rules: {
        productId: [
          { required: true, message: '请输入商品ID', trigger: 'blur' }
        ],
        productTitle: [
          { required: true, message: '请输入商品标题', trigger: 'blur' }
        ],
        category: [
          { required: true, message: '请输入商品类目', trigger: 'blur' }
        ],
        productPrice: [
          { required: true, message: '请输入商品价格', trigger: 'change' }
        ],
        productSales: [
          { required: true, message: '请输入商品销量', trigger: 'change' }
        ],
        shopName: [
          { required: true, message: '请输入店铺名称', trigger: 'blur' }
        ]
      }
    }
  },
  created() {
    this.checkDeviceId()
    this.getList()
    this.getStatistics()
  },
  methods: {
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
    // 获取商品数据列表
    async getList() {
      try {
        const params = {
          ...this.queryParams,
          category: this.searchForm.category,
          province: this.searchForm.province,
          shopName: this.searchForm.shopName,
          productTitle: this.searchForm.productTitle
        }
        const res = await Request.get('/sale-data/page', { params })
        if (res.code === '0') {
          this.saleDataList = res.data.records || []
          this.total = res.data.total
        }
      } catch (error) {
        // 静默处理获取商品数据列表失败
        this.saleDataList = []
        this.total = 0
      }
    },
    // 获取统计数据
    async getStatistics() {
      try {
        const res = await Request.get('/sale-data/statistics')
        if (res.code === '0') {
          const stats = res.data || {}
          this.statistics = {
            totalCount: stats.totalCount || 0,
            productCount: stats.productCount || 0,
            totalSalesAmount: stats.totalSalesAmount || 0,
            salesVolume: stats.salesVolume || 0,
            shopCount: stats.shopCount || 0
          }
        }
      } catch (error) {
        // 静默处理获取统计数据失败
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
        category: '',
        province: '',
        shopName: '',
        productTitle: ''
      }
      this.handleSearch()
    },
    // 新增商品数据
    handleAdd() {
      this.dialogTitle = '新增商品数据'
      this.form = {
        id: undefined,
        productId: '',
        category: '',
        productTitle: '',
        productPrice: 0,
        province: '',
        productSales: 0,
        shopName: '',
        shopTag: '',
        buyNowPayLater: '',
        returnService: '',
        style: '',
        pattern: '',
        fabric: '',
        fitType: '',
        season: ''
      }
      this.dialogVisible = true
    },
    // 编辑商品数据
    handleEdit(row) {
      this.dialogTitle = '编辑商品数据'
      this.form = {
        ...row,
        productPrice: Number(row.productPrice || 0),
        productSales: Number(row.productSales || 0)
      }
      this.dialogVisible = true
    },
    // 删除商品数据
    handleDelete(row) {
      this.$confirm('确认删除该商品数据?', '提示', {
        type: 'warning'
      }).then(async () => {
        try {
          const res = await Request.delete(`/sale-data/${row.id}`)
          if (res.code === '0') {
            this.$message.success('删除成功')
            this.getList()
          } else {
            this.$message({
              message: res.msg,
              type: 'error'
            })
          }
        } catch (error) {
          // 静默处理删除商品数据失败
        }
      }).catch(() => { })
    },
    // 提交表单
    submitForm() {
      this.$refs.form.validate(async (valid) => {
        if (valid) {
          try {
            const method = this.form.id ? 'put' : 'post'
            const url = this.form.id ? `/sale-data/${this.form.id}` : '/sale-data'
            
            const res = await Request[method](url, this.form)
            if (res.code === '0') {
              this.$message.success(`${this.form.id ? '更新' : '添加'}商品成功`)
              this.dialogVisible = false
              this.getList()
            }
          } catch (error) {
            // 静默处理提交表单失败
          }
        }
      })
    },
    // 获取所有数据（不分页）
    async getAllData(onProgress) {
      try {
        const allData = []
        let currentPage = 1
        const pageSize = 1000 // 每次获取1000条
        let totalCount = 0
        let isFirstPage = true
        
        while (true) {
          const params = {
            currentPage,
            size: pageSize,
            category: this.searchForm.category,
            province: this.searchForm.province,
            shopName: this.searchForm.shopName,
            productTitle: this.searchForm.productTitle
          }
          
          const res = await Request.get('/sale-data/page', { params })
          if (res.code === '0' && res.data && res.data.records) {
            // 第一次获取时，获取总数
            if (isFirstPage) {
              totalCount = res.data.total || res.data.records.length || 0
              isFirstPage = false
            }
            
            const records = res.data.records || []
            if (records.length === 0) {
              break // 没有更多数据了
            }
            
            allData.push(...records)
            
            // 更新进度（获取数据阶段占50%）
            if (onProgress && totalCount > 0) {
              const progress = Math.min(Math.round((allData.length / totalCount) * 50), 50)
              onProgress(progress, `正在获取数据: ${allData.length}/${totalCount}`)
            } else if (onProgress) {
              onProgress(5, `正在获取数据: ${allData.length} 条...`)
            }
            
            // 如果返回的数据少于页面大小，说明已经是最后一页了
            if (records.length < pageSize || (totalCount > 0 && allData.length >= totalCount)) {
              break
            }
            currentPage++
          } else {
            break
          }
        }
        
        return allData
      } catch (error) {
        console.error('获取所有数据失败:', error)
        return []
      }
    },
    // 导出数据--excel格式
    async exportTable(type) {
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
        
        // 获取所有数据
        updateProgress(5, '正在获取数据...')
        const allData = await this.getAllData(updateProgress)
        
        if (allData.length === 0) {
          this.isExporting = false
          this.exportProgress = 0
          this.exportProgressText = ''
          this.$message.warning('暂无数据可导出')
          return
        }
        
        // 格式化数据（占50%-80%）
        updateProgress(55, '正在格式化数据...')
        const exportData = []
        const totalItems = allData.length
        for (let i = 0; i < allData.length; i++) {
          const item = allData[i]
          exportData.push({
            productId: item.productId || '',
            productTitle: item.productTitle || '',
            category: item.category || '',
            productPrice: item.productPrice || 0,
            productSales: item.productSales || 0,
            province: item.province || '',
            shopName: item.shopName || '',
            shopTag: item.shopTag || '',
            buyNowPayLater: item.buyNowPayLater || '',
            returnService: item.returnService || '',
            style: item.style || '',
            pattern: item.pattern || '',
            fabric: item.fabric || '',
            fitType: item.fitType || '',
            season: item.season || ''
          })
          
          // 每处理100条更新一次进度
          if ((i + 1) % 100 === 0 || i === allData.length - 1) {
            const progress = 55 + Math.round(((i + 1) / totalItems) * 25)
            updateProgress(progress, `正在格式化数据: ${i + 1}/${totalItems}`)
            // 使用 setTimeout 让 UI 有机会更新
            await new Promise(resolve => setTimeout(resolve, 0))
          }
        }
        
        // 导出文件（占80%-100%）
        updateProgress(85, '正在生成文件...')
        const params = {
          header: ['商品ID', '商品标题', '类目', '价格', '销量', '省份', '店铺名称', '店铺标签', '花呗分期', '退货服务', '风格', '图案', '面料', '版型', '季节'],
          key: ['productId', 'productTitle', 'category', 'productPrice', 'productSales', 'province', 'shopName', 'shopTag', 'buyNowPayLater', 'returnService', 'style', 'pattern', 'fabric', 'fitType', 'season'],
          data: exportData,
          autoWidth: true,
          fileName: '淘宝商品数据表',
          bookType: type
        }
        
        // 使用 setTimeout 确保进度条更新
        await new Promise(resolve => setTimeout(resolve, 100))
        updateProgress(95, '正在保存文件...')
        
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
    }
  },
  computed: {
    getItemCount() {
      const items = new Set(this.saleDataList.map(item => item.productId).filter(Boolean))
      return items.size
    },
    getTotalSales() {
      return this.saleDataList.reduce((total, item) => {
        const price = parseFloat(item.productPrice) || 0
        const sales = parseFloat(item.productSales) || 0
        return total + price * sales
      }, 0).toFixed(2)
    },
    getTotalSaleCnt() {
      return this.saleDataList.reduce((total, item) => {
        const sales = parseFloat(item.productSales) || 0
        return total + sales
      }, 0).toFixed(2)
    },
    getMajorCount() {
      const shops = new Set(this.saleDataList.map(item => item.shopName).filter(Boolean))
      return shops.size
    }
  }
}
</script>

<style lang="less" scoped>
.order-manager {
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
  display: flex;
  flex-direction: column;
  align-items: flex-end;

  &::after {
    display: none;
  }
}

.stat-amount {
  font-size: 28px;
  font-weight: 700;
  line-height: 1.2;
}

.stat-sub {
  margin-top: 4px;
  font-size: 12px;
  color: #9ca3af;
  font-weight: 500;
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
          background: white;
        }
        
        &:first-child td:first-child {
          border-top-left-radius: 8px;
        }
        
        &:first-child td:last-child {
          border-top-right-radius: 8px;
        }
        
        &:last-child td:first-child {
          border-bottom-left-radius: 8px;
        }
        
        &:last-child td:last-child {
          border-bottom-right-radius: 8px;
        }
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

/* 美化表单 */
:deep(.el-form) {
  margin-bottom: 0;
}

:deep(.el-form-item) {
  margin-bottom: 16px;
}

:deep(.el-form-item__label) {
  font-weight: 500;
  color: #374151;
}

:deep(.el-input__inner) {
  border-radius: 8px;
  border-color: #e5e7eb;
  transition: all 0.3s ease;

  &:focus {
    border-color: #667eea;
  }
}

.delete-btn {
  color: #ef4444;
  margin-left: 12px;
  transition: color 0.3s ease;
}

.delete-btn:hover {
  color: #dc2626;
}

:deep(.el-button--text) {
  padding: 0 8px;
  font-size: 14px;
  transition: all 0.3s ease;

  &:hover {
    background-color: rgba(102, 126, 234, 0.08);
  }
}

:deep(.el-select .el-input__inner) {
  border-radius: 8px;
}

.discount-tip {
  margin-left: 10px;
  color: #6b7280;
  font-size: 13px;
}

:deep(.el-switch.is-checked .el-switch__core) {
  border-color: #667eea;
  background-color: #667eea;
}

/* 订单表单样式 */
.order-form {
  padding: 0;
}

.order-form .el-form-item {
  margin-bottom: 20px;
}

.order-form .el-input-number {
  width: 100%;
}

.order-form .el-select {
  width: 100%;
}

.order-form .el-date-picker {
  width: 100%;
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
</style> 