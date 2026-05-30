# 淘宝店铺信息分析系统

## 1. 项目概述

淘宝店铺信息分析系统是一个面向淘宝电商商品数据的数据清洗、统计分析与可视化展示项目。系统采用前后端分离架构，后端负责读取原始 CSV 数据、完成数据清洗、执行统计分析并提供 HTTP API；前端负责调用后端接口并以图表和表格形式展示分析结果。

项目主要围绕淘宝商品数据中的分类、地区、店铺、风格、款式、面料、版型等字段进行分析，支持从销量和价格两个角度观察不同维度下的商品分布特征，为电商商品数据分析、数据可视化课程设计和前后端分离项目实践提供完整实现。

## 2. 功能说明

### 2.1 数据清洗

后端提供独立的数据清洗流程，主要处理内容包括：

- 统一字段命名，将原始中文字段转换为后端内部使用的英文字段；
- 清理商品 ID、商品标题、店铺名称等文本字段中的多余空格；
- 将商品价格转换为可计算的数值类型；
- 将“人付款”“万人付款”等销量文本转换为整数销量；
- 过滤价格无效、销量无效的数据记录；
- 对风格、面料、版型、季节等字段进行标准化处理；
- 将清洗结果保存为 `cleaned_data.csv`，供后续分析和接口读取。

### 2.2 数据分析

系统围绕销量和价格两个方向进行统计分析，当前包含以下分析内容：

- 商品分类销量分析；
- 省份销量分析；
- 店铺销量分析；
- 风格平均价格分析；
- 款式平均价格分析；
- 面料平均价格分析；
- 版型平均价格分析；
- 指定分类、地区、店铺、风格、款式、面料、版型下的商品销量排行查询。

### 2.3 数据可视化

前端根据后端 API 返回的数据进行可视化展示，主要页面包括：

- 工作台首页；
- 分类销量分析页面；
- 省份销量分析页面；
- 店铺销量分析页面；
- 风格价格分析页面；
- 款式价格分析页面；
- 面料价格分析页面；
- 版型价格分析页面；
- 商品详情页面。

前端图表主要使用 ECharts 实现，页面组件基于 Vue 2 和 Element UI 构建。

## 3. 技术架构

### 3.1 后端技术栈

- Python
- Django
- pandas
- django-cors-headers
- python-dotenv
- SQLite

### 3.2 前端技术栈

- Vue 2
- Vue Router
- Vuex
- Element UI
- Axios
- ECharts
- Sass

### 3.3 架构说明

系统采用前后端分离模式：

- 后端运行在 `127.0.0.1:8000`，通过 Django 提供 API 服务；
- 前端运行在 `localhost:8080`，通过开发服务器代理将 `/api` 请求转发到后端；
- 数据源以 CSV 文件形式存放在后端 `data` 目录中；
- 后端接口统一返回 JSON 数据，前端根据接口结果渲染图表和详情列表。

## 4. 项目目录结构

```text
taobao-shop-info-analysis
├── backend
│   ├── analysis
│   │   ├── urls.py
│   │   └── views.py
│   ├── config
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── wsgi.py
│   ├── data
│   │   ├── 淘宝电商数据集.csv
│   │   └── cleaned_data.csv
│   ├── src
│   │   ├── analyze_data.py
│   │   ├── clean_data.py
│   │   ├── config.py
│   │   └── main.py
│   └── manage.py
│
├── frontend
│   ├── public
│   ├── src
│   │   ├── assets
│   │   ├── components
│   │   ├── layout
│   │   ├── router
│   │   ├── store
│   │   ├── utils
│   │   ├── views
│   │   ├── App.vue
│   │   └── main.js
│   ├── package.json
│   └── vue.config.js
│
├── requirements.txt
└── .gitignore
```

## 5. 环境要求

建议使用以下运行环境：

- Python 3.10 及以上；
- Node.js 16 及以上；
- npm；
- Git。

说明：后端代码中使用了 `str | Path` 类型标注语法，因此 Python 版本建议不低于 3.10。

## 6. 后端运行说明

### 6.1 克隆项目

```bash
git clone https://github.com/YYYYYYYYXL/taobao-shop-info-analysis.git
cd taobao-shop-info-analysis
```

### 6.2 创建虚拟环境

Windows PowerShell：

```bash
python -m venv .venv
.\.venv\Scripts\activate
```

macOS / Linux：

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 6.3 安装 Python 依赖

在项目根目录执行：

```bash
pip install -r requirements.txt
```

### 6.4 执行数据库迁移

进入后端目录：

```bash
cd backend
```

执行迁移命令：

```bash
python manage.py migrate
```

### 6.5 启动后端服务

```bash
python manage.py runserver 127.0.0.1:8000
```

服务启动后，访问以下地址进行后端状态检查：

```text
http://127.0.0.1:8000/
```

如果返回后端服务信息，说明后端启动成功。

## 7. 数据清洗与分析

后端默认读取原始数据文件：

```text
backend/data/淘宝电商数据集.csv
```

清洗后的数据默认保存为：

```text
backend/data/cleaned_data.csv
```

如需重新执行完整的数据清洗与分析流程，在 `backend` 目录下运行：

```bash
python -m src.main
```

如只需执行数据清洗流程，可运行：

```bash
python -m src.clean_data
```

数据路径支持通过 `.env` 文件进行配置。可在 `backend` 目录下创建 `.env` 文件，并按需配置：

```env
RAW_CSV_PATH=data/淘宝电商数据集.csv
CLEANED_CSV_PATH=data/cleaned_data.csv
```

## 8. 前端运行说明

打开新的终端窗口，进入前端目录：

```bash
cd frontend
```

安装前端依赖：

```bash
npm install
```

启动前端开发服务：

```bash
npm run dev
```

前端默认访问地址：

```text
http://localhost:8080
```

前端开发服务器已配置代理规则，`/api` 开头的请求会被转发至：

```text
http://127.0.0.1:8000
```

因此，运行完整项目时需要同时启动后端服务和前端服务。

## 9. API 接口说明

后端接口统一返回 JSON 格式数据，基础结构如下：

```json
{
  "code": "0",
  "msg": "success",
  "data": []
}
```

### 9.1 状态检查接口

| 接口 | 方法 | 说明 |
|---|---|---|
| `/` | GET | 后端服务状态检查 |

### 9.2 分析接口

| 接口 | 方法 | 说明 |
|---|---|---|
| `/api/category-sales/` | GET | 获取分类销量分析数据 |
| `/api/analysis/province-sales` | GET | 获取省份销量分析数据 |
| `/api/analysis/shop-sales` | GET | 获取店铺销量分析数据 |
| `/api/analysis/style-price` | GET | 获取风格平均价格分析数据 |
| `/api/analysis/pattern-price` | GET | 获取款式平均价格分析数据 |
| `/api/analysis/fabric-price` | GET | 获取面料平均价格分析数据 |
| `/api/analysis/fit-price` | GET | 获取版型平均价格分析数据 |
| `/api/analysis/top-products-by-categories` | GET | 获取 Top 分类下的商品销量排行 |
| `/api/analysis/top-products-by-dimension` | GET | 获取指定维度下的商品销量排行 |

### 9.3 指定维度商品排行接口

接口地址：

```text
/api/analysis/top-products-by-dimension
```

请求参数：

| 参数 | 是否必填 | 说明 |
|---|---|---|
| `field` | 是 | 查询维度，支持 `category`、`province`、`shop`、`style`、`pattern`、`fabric`、`fit` |
| `value` | 是 | 查询维度对应的具体值 |

请求示例：

```text
/api/analysis/top-products-by-dimension?field=category&value=外套
```

## 10. 数据字段说明

清洗后的数据主要字段如下：

| 字段 | 含义 |
|---|---|
| `item_id` | 商品 ID |
| `category` | 商品分类 |
| `title` | 商品标题 |
| `price` | 商品价格 |
| `province` | 商品所属省份 |
| `sales` | 商品销量 |
| `shop` | 店铺名称 |
| `shop_tag` | 店铺标签 |
| `pay_later` | 是否支持先用后付 |
| `return_flag` | 是否包含退货相关标记 |
| `style` | 商品风格 |
| `pattern` | 商品款式 |
| `fabric` | 商品面料 |
| `fit` | 商品版型 |
| `season` | 适用季节 |

## 11. 常见问题

### 11.1 后端接口报找不到 `cleaned_data.csv`

后端接口依赖清洗后的数据文件。如果 `backend/data/cleaned_data.csv` 不存在，需要先在 `backend` 目录下执行：

```bash
python -m src.main
```

### 11.2 前端页面无法获取数据

需要确认以下事项：

1. 后端服务是否已启动；
2. 后端地址是否为 `http://127.0.0.1:8000`；
3. 前端代理配置是否与后端端口一致；
4. 浏览器控制台中是否存在接口请求错误。

### 11.3 修改后端端口后前端无法访问

前端代理配置位于：

```text
frontend/vue.config.js
```

如果后端端口发生变化，需要同步修改代理配置中的 `target` 地址。

## 12. 开发说明

当前项目以本地开发和课程实践场景为主，Django 配置中默认开启 `DEBUG`，并使用 SQLite 作为默认数据库。若项目需要部署到生产环境，应至少完成以下调整：

- 关闭 `DEBUG`；
- 将 `SECRET_KEY` 等敏感配置迁移到环境变量；
- 按实际部署环境配置 `ALLOWED_HOSTS`；
- 使用生产环境 Web 服务器托管前端静态资源；
- 根据实际业务需要选择更稳定的数据库服务；
- 对接口访问权限、异常处理和日志记录进行完善。

## 13. 项目特点

本项目覆盖了从原始数据读取、数据清洗、统计分析、接口封装到前端图表展示的完整流程。相比单纯的数据分析脚本，本项目增加了前后端分离接口设计和可视化页面实现，更适合作为数据分析系统、Web 可视化系统或课程设计项目的实践样例。
