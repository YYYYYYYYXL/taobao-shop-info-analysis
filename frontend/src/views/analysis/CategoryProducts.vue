<template>
  <div class="category-products-page">
    <div class="page-hero">
      <div>
        <p class="hero-kicker">TOP 10 商品</p>
        <h1 class="hero-title">{{ currentCategory || '分类商品详情' }}</h1>
        <p class="hero-subtitle">按销量排序的商品展示页，当前共 {{ products.length }} 个商品。</p>
      </div>
    </div>

    <el-card shadow="never" class="data-card" v-loading="loading">
      <div class="data-header">
        <span class="data-title">商品列表</span>
        <span class="data-count">{{ products.length }} items</span>
      </div>

      <el-empty
        v-if="!loading && !products.length"
        description="当前分类暂无商品数据"
      />

      <div v-else class="product-grid">
        <article
          v-for="(item, index) in products"
          :key="item.item_id || `${item.title}-${index}`"
          class="product-card"
        >
          <div class="product-cover">
            <div class="cover-badge">热销</div>
            <div class="cover-rank">TOP {{ index + 1 }}</div>
            <div class="cover-brand">TAOBAO PICKS</div>
          </div>

          <div class="product-body">
            <h3 class="product-title" :title="item.title">{{ item.title || '未命名商品' }}</h3>

            <div class="product-sales">
              <span class="sales-label">销量</span>
              <span class="sales-value">{{ formatSales(item.sales) }}</span>
            </div>

            <div class="product-footer">
              <span class="price">￥{{ formatPrice(item.price) }}</span>
              <span class="shop" :title="item.shop">{{ item.shop || '店铺信息缺失' }}</span>
            </div>
          </div>
        </article>
      </div>
    </el-card>
  </div>
</template>

<script>
import Request from '@/utils/request'

export default {
  name: 'CategoryProducts',
  data() {
    return {
      loading: false,
      products: []
    }
  },
  computed: {
    currentCategory() {
      return this.$route.query.category || ''
    }
  },
  watch: {
    currentCategory: {
      immediate: true,
      handler() {
        this.fetchCategoryProducts()
      }
    }
  },
  methods: {
    async fetchCategoryProducts() {
      if (!this.currentCategory) {
        this.products = []
        return
      }

      try {
        this.loading = true
        const res = await Request.get('/analysis/top-products-by-categories')
        const normalizedRes = this.normalizeResponse(res)
        const categoryMap = normalizedRes?.data || {}
        const targetCategory = String(this.currentCategory).trim()
        const matchedKey = Object.keys(categoryMap).find(
          key => String(key).trim() === targetCategory
        )

        console.log('currentCategory:', targetCategory)
        console.log('matchedCategoryKey:', matchedKey)

        this.products = matchedKey ? categoryMap[matchedKey] : []
      } catch (error) {
        this.products = []
        this.$message.error('获取分类商品数据失败')
      } finally {
        this.loading = false
      }
    },
    formatPrice(price) {
      const value = Number(price)
      if (Number.isNaN(value)) {
        return '--'
      }
      return value.toFixed(2)
    },
    formatSales(sales) {
      const value = Number(sales)
      if (Number.isNaN(value)) {
        return '--'
      }
      return value.toLocaleString('zh-CN')
    },
    normalizeResponse(res) {
      if (res && typeof res === 'object') {
        return res
      }

      if (typeof res === 'string') {
        try {
          return JSON.parse(res.replace(/\bNaN\b/g, 'null'))
        } catch (error) {
          console.error('Failed to parse response:', error)
        }
      }

      return { data: {} }
    }
  }
}
</script>

<style lang="less" scoped>
.category-products-page {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.page-hero {
  padding: 28px 32px;
  border-radius: 28px;
  background:
    radial-gradient(circle at top right, rgba(255, 214, 153, 0.9), transparent 28%),
    linear-gradient(135deg, #fff4e8 0%, #ffe2c1 48%, #ffd0a6 100%);
  border: 1px solid rgba(255, 140, 51, 0.18);
}

.hero-kicker {
  margin: 0 0 8px;
  font-size: 12px;
  font-weight: 700;
  letter-spacing: 0.18em;
  color: #d65a00;
  text-transform: uppercase;
}

.hero-title {
  margin: 0;
  font-size: 34px;
  line-height: 1.1;
  color: #742a00;
}

.hero-subtitle {
  margin: 12px 0 0;
  font-size: 14px;
  color: #8b4a18;
}

.data-card {
  border-radius: 24px;
  border: 1px solid #f1e3d3;
  background: linear-gradient(180deg, #fffdfb 0%, #fff7ef 100%);
}

.data-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 18px;
}

.data-title {
  font-size: 18px;
  font-weight: 700;
  color: #2f241c;
}

.data-count {
  font-size: 13px;
  color: #9b7b63;
  text-transform: uppercase;
  letter-spacing: 0.08em;
}

.product-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
  gap: 18px;
}

.product-card {
  overflow: hidden;
  border-radius: 24px;
  background: #fff;
  border: 1px solid #ffd8b5;
  box-shadow: 0 10px 25px rgba(195, 110, 30, 0.08);
  transition: transform 0.22s ease, box-shadow 0.22s ease;
}

.product-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 16px 32px rgba(195, 110, 30, 0.15);
}

.product-cover {
  position: relative;
  min-height: 220px;
  padding: 18px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  background:
    linear-gradient(140deg, rgba(255, 255, 255, 0.14), rgba(255, 255, 255, 0) 36%),
    linear-gradient(135deg, #ff7b22 0%, #ff5c00 45%, #ff3d00 100%);
  color: #fff7ec;
}

.product-cover::after {
  content: '';
  position: absolute;
  right: -28px;
  bottom: -28px;
  width: 120px;
  height: 120px;
  border-radius: 50%;
  background: rgba(255, 223, 181, 0.18);
}

.cover-badge {
  position: relative;
  z-index: 1;
  align-self: flex-start;
  padding: 6px 12px;
  border-radius: 999px;
  background: rgba(255, 247, 236, 0.16);
  font-size: 12px;
  font-weight: 700;
  letter-spacing: 0.08em;
}

.cover-rank {
  position: relative;
  z-index: 1;
  font-size: 44px;
  font-weight: 800;
  line-height: 1;
  letter-spacing: -0.04em;
}

.cover-brand {
  position: relative;
  z-index: 1;
  font-size: 13px;
  font-weight: 600;
  letter-spacing: 0.14em;
}

.product-body {
  padding: 16px 16px 18px;
}

.product-title {
  margin: 0 0 14px;
  min-height: 44px;
  font-size: 16px;
  line-height: 1.4;
  color: #2f241c;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.product-sales {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 7px 12px;
  border-radius: 999px;
  background: #fff1e3;
}

.sales-label {
  font-size: 12px;
  color: #a45718;
}

.sales-value {
  font-size: 14px;
  font-weight: 700;
  color: #d9480f;
}

.product-footer {
  margin-top: 16px;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.price {
  font-size: 28px;
  font-weight: 800;
  line-height: 1;
  color: #ff5a1f;
}

.shop {
  font-size: 13px;
  color: #8a6b57;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

@media (max-width: 768px) {
  .page-hero {
    padding: 22px 20px;
    border-radius: 22px;
  }

  .hero-title {
    font-size: 28px;
  }

  .product-grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
    gap: 14px;
  }

  .product-cover {
    min-height: 180px;
  }

  .cover-rank {
    font-size: 34px;
  }

  .price {
    font-size: 24px;
  }
}

@media (max-width: 520px) {
  .product-grid {
    grid-template-columns: 1fr;
  }
}
</style>
