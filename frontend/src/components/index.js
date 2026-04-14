import Vue from 'vue'

// 自动导入components目录下的所有组件
const requireComponent = require.context(
  // 其组件目录的相对路径
  '.',
  // 是否查询其子目录
  true,
  // 匹配基础组件文件名的正则表达式
  /\.vue$/
)

requireComponent.keys().forEach(fileName => {
  // 获取组件配置
  const componentConfig = requireComponent(fileName)
  
  // 获取组件的 PascalCase 命名
  const componentName = fileName
    .split('/')
    .pop()
    .replace(/\.\w+$/, '')
  
  // 全局注册组件
  Vue.component(componentName, componentConfig.default || componentConfig)
})
