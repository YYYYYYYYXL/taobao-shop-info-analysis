<template>
  <div style="padding: 20px;">
    <h1 style="color: red;">我进入 TestApi 页面了</h1>

    <p>loading: {{ loading }}</p>
    <p>errorMsg: {{ errorMsg }}</p>
    <p>categorySales长度: {{ categorySales.length }}</p>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'TestApi',
  data() {
    return {
      loading: true,
      errorMsg: '',
      categorySales: []
    }
  },
  async mounted() {
    console.log('页面 mounted 开始执行')

    try {
      const res = await axios.get('http://127.0.0.1:8000/api/summary/')
      console.log('后端返回数据：', res.data)

      this.categorySales = res.data.data.category_sales
      console.log('categorySales：', this.categorySales)
    } catch (error) {
      console.error('请求失败详情：', error)

      if (error.response) {
        this.errorMsg = `请求失败，状态码：${error.response.status}`
      } else if (error.request) {
        this.errorMsg = '请求已发出，但后端没有正常响应'
      } else {
        this.errorMsg = `请求错误：${error.message}`
      }
    } finally {
      this.loading = false
      console.log('mounted 执行结束')
    }
  }
}
</script>