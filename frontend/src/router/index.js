import Vue from 'vue'
import VueRouter from 'vue-router'
import home from '../layout/index.vue'
import Home from '@/views/Home.vue'
import { staticMenuList, flattenStaticMenus } from '@/utils/staticMenu'

Vue.use(VueRouter)

const businessChildren = [
  {
    path: '/home',
    name: 'Home',
    component: Home,
    meta: { title: '工作台' }
  },
  {
    path: '/analysis-category-sales',
    name: 'AnalysisCategorySales',
    component: () => import('../views/analysis/AnalysisCategorySales.vue'),
    meta: { title: '分类销量分析' }
  },
  {
    path: '/analysis-province-sales',
    name: 'AnalysisProvinceSales',
    component: () => import('../views/analysis/AnalysisProvinceSales.vue'),
    meta: { title: '省份销量分析' }
  },
  {
    path: '/analysis-shop-sales',
    name: 'AnalysisShopSales',
    component: () => import('../views/analysis/AnalysisShopSales.vue'),
    meta: { title: '店铺销量分析' }
  },
  {
    path: '/analysis-style-price',
    name: 'AnalysisStylePrice',
    component: () => import('../views/analysis/AnalysisStylePrice.vue'),
    meta: { title: '风格价格分析' }
  },
  {
    path: '/analysis-pattern-price',
    name: 'AnalysisPatternPrice',
    component: () => import('../views/analysis/AnalysisPatternPrice.vue'),
    meta: { title: '款式价格分析' }
  },
  {
    path: '/analysis-fabric-price',
    name: 'AnalysisFabricPrice',
    component: () => import('../views/analysis/AnalysisFabricPrice.vue'),
    meta: { title: '面料价格分析' }
  },
  {
    path: '/analysis-fit-price',
    name: 'AnalysisFitTypePrice',
    component: () => import('../views/analysis/AnalysisFitTypePrice.vue'),
    meta: { title: '版型价格分析' }
  }
]

const routes = [
  {
    path: '/',
    component: home,
    redirect: '/home',
    children: businessChildren
  },
  {
    path: '/404',
    name: 'NotFound',
    component: () => import('../views/404.vue')
  }
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export const setRoutes = () => {
  localStorage.setItem('userMenuList', JSON.stringify(staticMenuList))
  localStorage.setItem(
    'staticRoutePaths',
    JSON.stringify(flattenStaticMenus().map(item => item.path))
  )
}

setRoutes()

router.onError((error) => {
  if (error.message.includes('Cannot find module')) {
    router.replace('/404')
  }
})

router.beforeEach((to, from, next) => {
  if (to.name) {
    localStorage.setItem('currentPathName', to.name)
  }
  next()
})

const originalPush = VueRouter.prototype.push
VueRouter.prototype.push = function push(location) {
  return originalPush.call(this, location).catch(err => err)
}

export default router
