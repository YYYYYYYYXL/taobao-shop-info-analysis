import Vue from 'vue'
  import VueRouter from 'vue-router'
  import ElementUI from 'element-ui'
  import request from '@/utils/request'
  import home from '../layout/index.vue'
  import Home from '@/views/Home.vue'
  import Login from '@/views/Login.vue'
  import LRLayout from '@/layout/LRLayout.vue'
  import Register from '@/views/Register.vue'
  import TestApi from '@/views/TestApi.vue'
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
      meta: { title: '图案价格分析' }
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
    },
    {
      path: '/person-info',
      name: 'PersonInfo',
      component: () => import('../views/PersonInfo.vue'),
      meta: { title: '基本信息' }
    },
    {
      path: '/password',
      name: 'Password',
      component: () => import('../views/Password.vue'),
      meta: { title: '修改密码' }
    }
  ]

  const routes = [
    {
      path: '/login',
      name: 'LRLayout',
      redirect: '/login',
      component: LRLayout,
      children: [
        {
          path: '/login',
          name: 'Login',
          component: Login
        },
        {
          path: '/register',
          name: 'Register',
          component: Register
        }
      ]
    },
    {
      path: '/',
      component: home,
      redirect: '/home',
      children: businessChildren
    },
    {
      path: '/test-api',
      name: 'TestApi',
      component: TestApi
    },
    {
      path: '/404',
      name: 'NotFound',
      component: () => import('../views/404.vue')
    },
    {
      path: '/dashboard-fullscreen',
      name: 'DashboardFullscreen',
      component: () => import('../views/DashboardFullscreen.vue'),
      meta: { title: '数据大屏' }
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

    const publicPaths = ['/login', '/register', '/404', '/test-api']
    const requiresAuth = !publicPaths.includes(to.path)
    const userInfo = localStorage.getItem('userInfo')

    if (requiresAuth && !userInfo) {
      ElementUI.Message({
        message: '请先登录',
        type: 'warning'
      })
      next('/login')
      return
    }

    next()
  })

  router.afterEach((to, from) => {
    if (to.path === '/login' || to.path === '/register') {
      return
    }

    const userInfoStr = localStorage.getItem('userInfo')
    if (!userInfoStr) {
      return
    }

    try {
      const userInfo = JSON.parse(userInfoStr)
      if (!userInfo || !userInfo.id) {
        return
      }

      const actionLog = {
        userId: userInfo.id,
        username: userInfo.username || userInfo.name,
        pageName: null,
        action: 'VIEW',
        actionDesc: `访问页面: ${to.path}`,
        requestMethod: 'GET',
        requestUrl: to.path
      }

      request.post('/actionLog/recordPageView', actionLog).catch(() => {})
    } catch (error) {
      console.debug('记录页面访问日志失败:', error)
    }
  })

  const originalPush = VueRouter.prototype.push
  VueRouter.prototype.push = function push(location) {
    return originalPush.call(this, location).catch(err => err)
  }

  export default router