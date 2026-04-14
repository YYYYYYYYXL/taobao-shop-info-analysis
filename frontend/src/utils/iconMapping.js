/**
 * 图标映射配置 - 兼容Element UI和Element Plus
 * 支持Vue2(Element UI)和Vue3(Element Plus)
 */

// 检测Vue版本
export function getVueVersion() {
  // 检测是否为Vue 3
  if (typeof window !== 'undefined' && window.Vue && window.Vue.version && window.Vue.version.startsWith('3')) {
    return 3
  }
  // 检测Vue实例上的版本信息
  if (typeof window !== 'undefined' && window.Vue && window.Vue.version && window.Vue.version.startsWith('2')) {
    return 2
  }
  // 通过import检测Vue版本
  try {
    const Vue = require('vue')
    if (Vue.version && Vue.version.startsWith('3')) {
      return 3
    }
    if (Vue.version && Vue.version.startsWith('2')) {
      return 2
    }
  } catch (e) {
    // ignore
  }
  
  // 默认返回3（当前项目）
  return 3
}

// 图标映射列表 - 包含Element UI和Element Plus的图标
export const iconMappings = [
  {
    key: 'home',
    name: '首页',
    elementUI: 'el-icon-house',
    elementPlus: 'House',
    category: '导航'
  },
  {
    key: 'menu',
    name: '菜单',
    elementUI: 'el-icon-menu',
    elementPlus: 'Menu',
    category: '导航'
  },
  {
    key: 'user',
    name: '用户',
    elementUI: 'el-icon-user',
    elementPlus: 'User',
    category: '用户'
  },
  {
    key: 'user-group',
    name: '用户组',
    elementUI: 'el-icon-user-solid',
    elementPlus: 'UserFilled',
    category: '用户'
  },
  {
    key: 'setting',
    name: '设置',
    elementUI: 'el-icon-setting',
    elementPlus: 'Setting',
    category: '操作'
  },
  {
    key: 'edit',
    name: '编辑',
    elementUI: 'el-icon-edit',
    elementPlus: 'Edit',
    category: '操作'
  },
  {
    key: 'delete',
    name: '删除',
    elementUI: 'el-icon-delete',
    elementPlus: 'Delete',
    category: '操作'
  },
  {
    key: 'add',
    name: '添加',
    elementUI: 'el-icon-plus',
    elementPlus: 'Plus',
    category: '操作'
  },
  {
    key: 'document',
    name: '文档',
    elementUI: 'el-icon-document',
    elementPlus: 'Document',
    category: '文件'
  },
  {
    key: 'folder',
    name: '文件夹',
    elementUI: 'el-icon-folder',
    elementPlus: 'Folder',
    category: '文件'
  },
  {
    key: 'picture',
    name: '图片',
    elementUI: 'el-icon-picture',
    elementPlus: 'Picture',
    category: '文件'
  },
  {
    key: 'download',
    name: '下载',
    elementUI: 'el-icon-download',
    elementPlus: 'Download',
    category: '操作'
  },
  {
    key: 'upload',
    name: '上传',
    elementUI: 'el-icon-upload',
    elementPlus: 'Upload',
    category: '操作'
  },
  {
    key: 'search',
    name: '搜索',
    elementUI: 'el-icon-search',
    elementPlus: 'Search',
    category: '操作'
  },
  {
    key: 'refresh',
    name: '刷新',
    elementUI: 'el-icon-refresh',
    elementPlus: 'Refresh',
    category: '操作'
  },
  {
    key: 'shopping-cart',
    name: '购物车',
    elementUI: 'el-icon-shopping-cart-2',
    elementPlus: 'ShoppingCart',
    category: '商务'
  },
  {
    key: 'goods',
    name: '商品',
    elementUI: 'el-icon-goods',
    elementPlus: 'Goods',
    category: '商务'
  },
  {
    key: 'order',
    name: '订单',
    elementUI: 'el-icon-s-order',
    elementPlus: 'List',
    category: '商务'
  },
  {
    key: 'statistics',
    name: '统计',
    elementUI: 'el-icon-data-analysis',
    elementPlus: 'DataAnalysis',
    category: '数据'
  },
  {
    key: 'chart',
    name: '图表',
    elementUI: 'el-icon-data-line',
    elementPlus: 'DataLine',
    category: '数据'
  },
  {
    key: 'wallet',
    name: '钱包',
    elementUI: 'el-icon-wallet',
    elementPlus: 'Wallet',
    category: '商务'
  },
  {
    key: 'favorite',
    name: '收藏',
    elementUI: 'el-icon-star-off',
    elementPlus: 'Star',
    category: '操作'
  },
  {
    key: 'message',
    name: '消息',
    elementUI: 'el-icon-message',
    elementPlus: 'Message',
    category: '通讯'
  },
  {
    key: 'notification',
    name: '通知',
    elementUI: 'el-icon-bell',
    elementPlus: 'Bell',
    category: '通讯'
  },
  {
    key: 'email',
    name: '邮件',
    elementUI: 'el-icon-message-solid',
    elementPlus: 'ChatDotRound',
    category: '通讯'
  },
  {
    key: 'location',
    name: '位置',
    elementUI: 'el-icon-location',
    elementPlus: 'Location',
    category: '地图'
  },
  {
    key: 'date',
    name: '日期',
    elementUI: 'el-icon-date',
    elementPlus: 'Calendar',
    category: '时间'
  },
  {
    key: 'time',
    name: '时间',
    elementUI: 'el-icon-time',
    elementPlus: 'Timer',
    category: '时间'
  },
  {
    key: 'help',
    name: '帮助',
    elementUI: 'el-icon-question',
    elementPlus: 'QuestionFilled',
    category: '提示'
  },
  {
    key: 'info',
    name: '信息',
    elementUI: 'el-icon-info',
    elementPlus: 'InfoFilled',
    category: '提示'
  },
  {
    key: 'warning',
    name: '警告',
    elementUI: 'el-icon-warning',
    elementPlus: 'Warning',
    category: '提示'
  },
  {
    key: 'success',
    name: '成功',
    elementUI: 'el-icon-success',
    elementPlus: 'SuccessFilled',
    category: '提示'
  },
  {
    key: 'error',
    name: '错误',
    elementUI: 'el-icon-error',
    elementPlus: 'CircleClose',
    category: '提示'
  },
  {
    key: 'lock',
    name: '锁定',
    elementUI: 'el-icon-lock',
    elementPlus: 'Lock',
    category: '安全'
  },
  {
    key: 'unlock',
    name: '解锁',
    elementUI: 'el-icon-unlock',
    elementPlus: 'Unlock',
    category: '安全'
  },
  {
    key: 'view',
    name: '查看',
    elementUI: 'el-icon-view',
    elementPlus: 'View',
    category: '操作'
  },
  {
    key: 'hide',
    name: '隐藏',
    elementUI: 'el-icon-turn-off',
    elementPlus: 'Hide',
    category: '操作'
  },
  {
    key: 'close',
    name: '关闭',
    elementUI: 'el-icon-close',
    elementPlus: 'Close',
    category: '操作'
  },
  {
    key: 'arrow-left',
    name: '箭头左',
    elementUI: 'el-icon-arrow-left',
    elementPlus: 'ArrowLeft',
    category: '箭头'
  },
  {
    key: 'arrow-right',
    name: '箭头右',
    elementUI: 'el-icon-arrow-right',
    elementPlus: 'ArrowRight',
    category: '箭头'
  },
  {
    key: 'arrow-up',
    name: '箭头上',
    elementUI: 'el-icon-arrow-up',
    elementPlus: 'ArrowUp',
    category: '箭头'
  },
  {
    key: 'arrow-down',
    name: '箭头下',
    elementUI: 'el-icon-arrow-down',
    elementPlus: 'ArrowDown',
    category: '箭头'
  },
  {
    key: 'agriculture',
    name: '农业',
    elementUI: 'el-icon-apple',
    elementPlus: 'Cherry',
    category: '特色'
  },
  {
    key: 'food',
    name: '食物',
    elementUI: 'el-icon-food',
    elementPlus: 'Food',
    category: '特色'
  },
  // 更多导航图标
  {
    key: 'dashboard',
    name: '仪表盘',
    elementUI: 'el-icon-s-platform',
    elementPlus: 'Platform',
    category: '导航'
  },
  {
    key: 'monitor',
    name: '数据看板',
    elementUI: 'el-icon-monitor',
    elementPlus: 'Monitor',
    category: '导航'
  },
  {
    key: 'back',
    name: '返回',
    elementUI: 'el-icon-back',
    elementPlus: 'Back',
    category: '导航'
  },
  {
    key: 'right',
    name: '右侧',
    elementUI: 'el-icon-right',
    elementPlus: 'Right',
    category: '导航'
  },
  // 更多操作图标
  {
    key: 'copy',
    name: '复制',
    elementUI: 'el-icon-document-copy',
    elementPlus: 'CopyDocument',
    category: '操作'
  },
  {
    key: 'share',
    name: '分享',
    elementUI: 'el-icon-share',
    elementPlus: 'Share',
    category: '操作'
  },
  {
    key: 'collapse',
    name: '收起',
    elementUI: 'el-icon-arrow-up',
    elementPlus: 'ArrowUp',
    category: '操作'
  },
  {
    key: 'expand',
    name: '展开',
    elementUI: 'el-icon-arrow-down',
    elementPlus: 'ArrowDown',
    category: '操作'
  },
  {
    key: 'sort',
    name: '排序',
    elementUI: 'el-icon-sort',
    elementPlus: 'Sort',
    category: '操作'
  },
  {
    key: 'filter',
    name: '筛选',
    elementUI: 'el-icon-finished',
    elementPlus: 'Filter',
    category: '操作'
  },
  {
    key: 'print',
    name: '打印',
    elementUI: 'el-icon-printer',
    elementPlus: 'Printer',
    category: '操作'
  },
  {
    key: 'zoom-in',
    name: '放大',
    elementUI: 'el-icon-zoom-in',
    elementPlus: 'ZoomIn',
    category: '操作'
  },
  {
    key: 'zoom-out',
    name: '缩小',
    elementUI: 'el-icon-zoom-out',
    elementPlus: 'ZoomOut',
    category: '操作'
  },
  {
    key: 'fullscreen',
    name: '全屏',
    elementUI: 'el-icon-full-screen',
    elementPlus: 'FullScreen',
    category: '操作'
  },
  {
    key: 'exit-fullscreen',
    name: '退出全屏',
    elementUI: 'el-icon-aim',
    elementPlus: 'Aim',
    category: '操作'
  },
  // 更多文件图标
  {
    key: 'video',
    name: '视频',
    elementUI: 'el-icon-video-play',
    elementPlus: 'VideoPlay',
    category: '文件'
  },
  {
    key: 'audio',
    name: '音频',
    elementUI: 'el-icon-headset',
    elementPlus: 'Headset',
    category: '文件'
  },
  {
    key: 'link',
    name: '链接',
    elementUI: 'el-icon-link',
    elementPlus: 'Link',
    category: '文件'
  },
  {
    key: 'archive',
    name: '压缩包',
    elementUI: 'el-icon-folder-opened',
    elementPlus: 'FolderOpened',
    category: '文件'
  },
  {
    key: 'attachment',
    name: '附件',
    elementUI: 'el-icon-paperclip',
    elementPlus: 'Paperclip',
    category: '文件'
  },
  // 更多系统图标
  {
    key: 'system',
    name: '系统',
    elementUI: 'el-icon-s-tools',
    elementPlus: 'Tools',
    category: '系统'
  },
  {
    key: 'config',
    name: '配置',
    elementUI: 'el-icon-s-operation',
    elementPlus: 'Operation',
    category: '系统'
  },
  {
    key: 'permission',
    name: '权限',
    elementUI: 'el-icon-key',
    elementPlus: 'Key',
    category: '系统'
  },
  {
    key: 'log',
    name: '日志',
    elementUI: 'el-icon-tickets',
    elementPlus: 'Tickets',
    category: '系统'
  },
  {
    key: 'monitor-system',
    name: '监控',
    elementUI: 'el-icon-view',
    elementPlus: 'View',
    category: '系统'
  },
  {
    key: 'service',
    name: '服务',
    elementUI: 'el-icon-service',
    elementPlus: 'Service',
    category: '系统'
  },
  // 更多状态图标
  {
    key: 'loading',
    name: '加载中',
    elementUI: 'el-icon-loading',
    elementPlus: 'Loading',
    category: '状态'
  },
  {
    key: 'completed',
    name: '已完成',
    elementUI: 'el-icon-circle-check',
    elementPlus: 'CircleCheck',
    category: '状态'
  },
  {
    key: 'pause',
    name: '暂停',
    elementUI: 'el-icon-video-pause',
    elementPlus: 'VideoPause',
    category: '状态'
  },
  {
    key: 'play',
    name: '播放',
    elementUI: 'el-icon-video-play',
    elementPlus: 'VideoPlay',
    category: '状态'
  },
  {
    key: 'stop',
    name: '停止',
    elementUI: 'el-icon-turn-off',
    elementPlus: 'TurnOff',
    category: '状态'
  },
  // 更多界面元素
  {
    key: 'tag',
    name: '标签',
    elementUI: 'el-icon-price-tag',
    elementPlus: 'PriceTag',
    category: '界面'
  },
  {
    key: 'badge',
    name: '徽章',
    elementUI: 'el-icon-medal',
    elementPlus: 'Medal',
    category: '界面'
  },
  {
    key: 'table',
    name: '表格',
    elementUI: 'el-icon-s-grid',
    elementPlus: 'Grid',
    category: '界面'
  },
  {
    key: 'list',
    name: '列表',
    elementUI: 'el-icon-menu',
    elementPlus: 'List',
    category: '界面'
  },
  {
    key: 'card',
    name: '卡片',
    elementUI: 'el-icon-postcard',
    elementPlus: 'Postcard',
    category: '界面'
  },
  {
    key: 'dialog',
    name: '弹窗',
    elementUI: 'el-icon-message-solid',
    elementPlus: 'ChatDotRound',
    category: '界面'
  },
  // 更多商务图标
  {
    key: 'payment',
    name: '支付',
    elementUI: 'el-icon-bank-card',
    elementPlus: 'CreditCard',
    category: '商务'
  },
  {
    key: 'coupon',
    name: '优惠券',
    elementUI: 'el-icon-present',
    elementPlus: 'Present',
    category: '商务'
  },
  {
    key: 'gift',
    name: '礼品',
    elementUI: 'el-icon-present',
    elementPlus: 'Present',
    category: '商务'
  },
  {
    key: 'shop',
    name: '店铺',
    elementUI: 'el-icon-office-building',
    elementPlus: 'OfficeBuilding',
    category: '商务'
  },
  {
    key: 'customer-service',
    name: '客服',
    elementUI: 'el-icon-service',
    elementPlus: 'Headset',
    category: '商务'
  },
  // 更多数据图标
  {
    key: 'pie-chart',
    name: '饼图',
    elementUI: 'el-icon-pie-chart',
    elementPlus: 'PieChart',
    category: '数据'
  },
  {
    key: 'trend',
    name: '趋势',
    elementUI: 'el-icon-s-operation',
    elementPlus: 'TrendCharts',
    category: '数据'
  },
  {
    key: 'report',
    name: '报表',
    elementUI: 'el-icon-data-board',
    elementPlus: 'DataBoard',
    category: '数据'
  },
  {
    key: 'database',
    name: '数据库',
    elementUI: 'el-icon-coin',
    elementPlus: 'Coin',
    category: '数据'
  },
  // 更多工具图标
  {
    key: 'finance',
    name: '金融',
    elementUI: 'el-icon-s-finance',
    elementPlus: 'Coin',
    category: '工具'
  },
  {
    key: 'calendar',
    name: '日历',
    elementUI: 'el-icon-date',
    elementPlus: 'Calendar',
    category: '工具'
  },
  {
    key: 'clock',
    name: '时钟',
    elementUI: 'el-icon-timer',
    elementPlus: 'Timer',
    category: '工具'
  },
  {
    key: 'camera',
    name: '相机',
    elementUI: 'el-icon-camera',
    elementPlus: 'Camera',
    category: '工具'
  },
  {
    key: 'scan',
    name: '扫码',
    elementUI: 'el-icon-camera',
    elementPlus: 'Camera',
    category: '工具'
  },
  {
    key: 'qrcode',
    name: '二维码',
    elementUI: 'el-icon-s-grid',
    elementPlus: 'Grid',
    category: '工具'
  },
  // 更多社交图标
  {
    key: 'phone',
    name: '电话',
    elementUI: 'el-icon-phone',
    elementPlus: 'Phone',
    category: '社交'
  },
  {
    key: 'mobile',
    name: '手机',
    elementUI: 'el-icon-mobile-phone',
    elementPlus: 'Iphone',
    category: '社交'
  },
  {
    key: 'chat',
    name: '聊天',
    elementUI: 'el-icon-chat-line-round',
    elementPlus: 'ChatDotRound',
    category: '社交'
  },
  {
    key: 'comment',
    name: '评论',
    elementUI: 'el-icon-chat-dot-round',
    elementPlus: 'ChatDotRound',
    category: '社交'
  },
  {
    key: 'like',
    name: '点赞',
    elementUI: 'el-icon-thumb',
    elementPlus: 'Star',
    category: '社交'
  },
  // 更多交通图标
  {
    key: 'map-location',
    name: '位置标记',
    elementUI: 'el-icon-map-location',
    elementPlus: 'MapLocation',
    category: '地图'
  },
  {
    key: 'navigation',
    name: '导航',
    elementUI: 'el-icon-position',
    elementPlus: 'Position',
    category: '地图'
  },
  {
    key: 'route',
    name: '路线',
    elementUI: 'el-icon-guide',
    elementPlus: 'Guide',
    category: '地图'
  },
  {
    key: 'car',
    name: '汽车',
    elementUI: 'el-icon-truck',
    elementPlus: 'Van',
    category: '交通'
  },
  {
    key: 'bicycle',
    name: '自行车',
    elementUI: 'el-icon-bicycle',
    elementPlus: 'Van',
    category: '交通'
  },
  // 更多天气图标
  {
    key: 'sunny',
    name: '晴天',
    elementUI: 'el-icon-sunny',
    elementPlus: 'Sunny',
    category: '天气'
  },
  {
    key: 'cloudy',
    name: '多云',
    elementUI: 'el-icon-cloudy',
    elementPlus: 'Cloudy',
    category: '天气'
  },
  {
    key: 'rainy',
    name: '雨天',
    elementUI: 'el-icon-heavy-rain',
    elementPlus: 'Cloudy',
    category: '天气'
  },
  {
    key: 'moon',
    name: '月亮',
    elementUI: 'el-icon-moon',
    elementPlus: 'Moon',
    category: '天气'
  }
]

/**
 * 获取图标列表（根据Vue版本）
 * @returns {Array} 图标列表
 */
export function getIconList() {
  const vueVersion = getVueVersion()
  
  return iconMappings.map(icon => ({
    itemKey: icon.name,
    itemValue: icon.key, // 现在返回key作为value，用于保存到后台
    iconClass: vueVersion === 2 ? icon.elementUI : icon.elementPlus, // 用于显示的图标类
    category: icon.category,
    vueVersion: vueVersion
  }))
}

/**
 * 根据图标key获取对应版本的图标类
 * @param {string} iconKey - 图标key
 * @returns {string} 图标class或组件名
 */
export function getIconByKey(iconKey) {
  const vueVersion = getVueVersion()
  const icon = iconMappings.find(item => item.key === iconKey)
  
  if (!icon) {
    return vueVersion === 2 ? 'el-icon-menu' : 'Menu'
  }
  
  return vueVersion === 2 ? icon.elementUI : icon.elementPlus
}

/**
 * 根据图标名称获取对应版本的图标
 * @param {string} iconName - 图标名称
 * @returns {string} 图标class或组件名
 */
export function getIconByName(iconName) {
  const vueVersion = getVueVersion()
  const icon = iconMappings.find(item => item.name === iconName)
  
  if (!icon) {
    return vueVersion === 2 ? 'el-icon-menu' : 'Menu'
  }
  
  return vueVersion === 2 ? icon.elementUI : icon.elementPlus
}

/**
 * 根据图标key获取完整的图标信息
 * @param {string} iconKey - 图标key
 * @returns {Object} 图标信息对象
 */
export function getIconInfoByKey(iconKey) {
  const vueVersion = getVueVersion()
  const icon = iconMappings.find(item => item.key === iconKey)
  
  if (!icon) {
    return {
      key: 'menu',
      name: '菜单',
      iconClass: vueVersion === 2 ? 'el-icon-menu' : 'Menu',
      category: '导航'
    }
  }
  
  return {
    key: icon.key,
    name: icon.name,
    iconClass: vueVersion === 2 ? icon.elementUI : icon.elementPlus,
    category: icon.category
  }
}

/**
 * 根据旧的图标值获取对应的key（用于数据迁移）
 * @param {string} iconValue - 旧的图标值（Element UI的class或Element Plus的组件名）
 * @returns {string} 对应的图标key
 */
export function getKeyByIconValue(iconValue) {
  const icon = iconMappings.find(item => 
    item.elementUI === iconValue || item.elementPlus === iconValue
  )
  
  return icon ? icon.key : 'menu'
}

/**
 * 根据存储的图标值获取渲染信息
 * @param {string} storedIcon - 存储的图标值（可能是key或旧的图标值）
 * @returns {Object} 包含type和value的对象
 */
export function getIconRenderInfo(storedIcon) {
  const vueVersion = getVueVersion()
  
  if (!storedIcon) {
    return {
      type: vueVersion === 2 ? 'class' : 'component',
      value: vueVersion === 2 ? 'el-icon-menu' : 'Menu',
      key: 'menu'
    }
  }
  
  // 首先尝试作为key查找
  let iconMapping = iconMappings.find(icon => icon.key === storedIcon)
  
  // 如果没找到，尝试作为旧的图标值查找（向后兼容）
  if (!iconMapping) {
    iconMapping = iconMappings.find(icon => 
      icon.elementUI === storedIcon || icon.elementPlus === storedIcon
    )
  }
  
  if (iconMapping) {
    return {
      type: vueVersion === 2 ? 'class' : 'component',
      value: vueVersion === 2 ? iconMapping.elementUI : iconMapping.elementPlus,
      key: iconMapping.key,
      name: iconMapping.name
    }
  }
  
  // 如果都没找到，返回默认值
  return {
    type: vueVersion === 2 ? 'class' : 'component',
    value: storedIcon, // 保持原值，可能是自定义图标
    key: storedIcon
  }
}

/**
 * 按分类获取图标列表
 * @param {string} category - 分类名称
 * @returns {Array} 该分类的图标列表
 */
export function getIconsByCategory(category) {
  const vueVersion = getVueVersion()
  
  return iconMappings
    .filter(icon => icon.category === category)
    .map(icon => ({
      itemKey: icon.name,
      itemValue: icon.key,
      iconClass: vueVersion === 2 ? icon.elementUI : icon.elementPlus,
      category: icon.category,
      vueVersion: vueVersion
    }))
}

/**
 * 获取所有分类
 * @returns {Array} 分类列表
 */
export function getCategories() {
  const categories = [...new Set(iconMappings.map(icon => icon.category))]
  return categories.sort()
} 