export const staticMenuList = [
  {
    id: 100,
    name: '答辩总览',
    path: '/home',
    icon: 'home',
    pagePath: 'Home'
  },
  {
    id: 200,
    name: '数据分析',
    icon: 'statistics',
    children: [
      {
        id: 201,
        pid: 200,
        name: '分类销量分析',
        path: '/analysis-category-sales',
        pagePath: 'analysis/AnalysisCategorySales',
        icon: 'pie-chart',
        apiUrl: '/category-sales/',
        chartType: 'bar',
        chartColor: '#4a90e2',
        tableColumnName: '分类',
        tableColumnValueOne: '销量'
      },
      {
        id: 202,
        pid: 200,
        name: '省份销量分析',
        path: '/analysis-province-sales',
        pagePath: 'analysis/AnalysisProvinceSales',
        icon: 'location',
        apiUrl: '/analysis/province-sales',
        chartType: 'china-map',
        chartColor: '#4a90e2',
        tableColumnName: '省份',
        tableColumnValueOne: '销量'
      },
      {
        id: 203,
        pid: 200,
        name: '店铺销量分析',
        path: '/analysis-shop-sales',
        pagePath: 'analysis/AnalysisShopSales',
        icon: 'shop',
        apiUrl: '/analysis/shop-sales',
        chartType: 'horizontal-bar',
        chartColor: '#667eea',
        tableColumnName: '店铺',
        tableColumnValueOne: '销量'
      },
      {
        id: 204,
        pid: 200,
        name: '风格价格分析',
        path: '/analysis-style-price',
        pagePath: 'analysis/AnalysisStylePrice',
        icon: 'chart',
        apiUrl: '/analysis/style-price',
        chartType: 'bar',
        chartColor: '#34a853',
        tableColumnName: '风格',
        tableColumnValueOne: '均价'
      },
      {
        id: 205,
        pid: 200,
        name: '款式价格分析',
        path: '/analysis-pattern-price',
        pagePath: 'analysis/AnalysisPatternPrice',
        icon: 'picture',
        apiUrl: '/analysis/pattern-price',
        chartType: 'bar',
        chartColor: '#f59e0b',
        tableColumnName: '款式',
        tableColumnValueOne: '均价'
      },
      {
        id: 206,
        pid: 200,
        name: '面料价格分析',
        path: '/analysis-fabric-price',
        pagePath: 'analysis/AnalysisFabricPrice',
        icon: 'grid',
        apiUrl: '/analysis/fabric-price',
        chartType: 'bar',
        chartColor: '#8b5cf6',
        tableColumnName: '面料',
        tableColumnValueOne: '均价'
      },
      {
        id: 207,
        pid: 200,
        name: '版型价格分析',
        path: '/analysis-fit-price',
        pagePath: 'analysis/AnalysisFitTypePrice',
        icon: 'data-analysis',
        apiUrl: '/analysis/fit-price',
        chartType: 'bar',
        chartColor: '#ef4444',
        tableColumnName: '版型',
        tableColumnValueOne: '均价'
      }
    ]
  }
]

export function flattenStaticMenus(menuList = staticMenuList) {
  return menuList.reduce((acc, item) => {
    if (item.path) {
      acc.push(item)
    }
    if (item.children && item.children.length > 0) {
      acc.push(...flattenStaticMenus(item.children))
    }
    return acc
  }, [])
}
