# LightRAG Web UI 组件文档

## 概述

LightRAG Web UI 是一个现代化的 React 前端应用，使用 TypeScript、Vite、Tailwind CSS 和 Zustand 构建。提供了完整的文档管理、知识图谱可视化和检索测试功能。

## 技术栈

### 核心框架
- **React 19**: 用户界面框架
- **TypeScript**: 类型安全的 JavaScript 超集
- **Vite**: 快速的开发构建工具
- **React Router DOM**: 路由管理

### UI 组件库
- **Radix UI**: 无样式、可访问的组件原语
- **Tailwind CSS**: 实用优先的 CSS 框架
- **Lucide React**: 美观的图标库
- **Sonner**: 现代化的 Toast 通知

### 图形可视化
- **Sigma.js**: 图形可视化引擎
- **React-Sigma**: Sigma.js 的 React 绑定
- **Graphology**: 图数据结构库

### 状态管理和工具
- **Zustand**: 轻量级状态管理
- **i18next**: 国际化解决方案
- **Axios**: HTTP 客户端
- **React Markdown**: Markdown 渲染
- **Mermaid**: 图表绘制

## 项目结构

```
lightrag_webui/src/
├── api/                    # API 接口层
│   └── lightrag.ts         # LightRAG API 客户端
├── components/             # 组件库
│   ├── documents/          # 文档管理组件
│   ├── graph/              # 图谱可视化组件
│   ├── retrieval/          # 检索测试组件
│   ├── status/             # 状态显示组件
│   └── ui/                 # 基础 UI 组件
├── contexts/               # React Context
│   ├── TabVisibilityProvider.tsx
│   ├── context.ts
│   ├── types.ts
│   └── useTabVisibility.ts
├── features/               # 功能特性模块
│   ├── ApiSite.tsx         # API 文档页面
│   ├── DocumentManager.tsx # 文档管理器
│   ├── GraphViewer.tsx     # 图谱查看器
│   ├── LoginPage.tsx       # 登录页面
│   ├── RetrievalTesting.tsx # 检索测试
│   └── SiteHeader.tsx      # 站点头部
├── hooks/                  # 自定义 Hooks
│   ├── useDebounce.tsx
│   ├── useLightragGraph.tsx
│   ├── useRandomGraph.tsx
│   └── useTheme.tsx
├── lib/                    # 工具库
│   ├── constants.ts        # 常量定义
│   └── utils.ts            # 工具函数
├── locales/                # 国际化资源
│   ├── ar.json             # 阿拉伯语
│   ├── en.json             # 英语
│   ├── fr.json             # 法语
│   ├── zh.json             # 简体中文
│   └── zh_TW.json          # 繁体中文
├── services/               # 服务层
│   └── navigation.ts       # 导航服务
├── stores/                 # 状态管理
│   ├── graph.ts            # 图谱状态
│   ├── settings.ts         # 设置状态
│   └── state.ts            # 全局状态
├── App.tsx                 # 主应用组件
├── AppRouter.tsx           # 路由配置
├── i18n.ts                 # 国际化配置
├── index.css               # 全局样式
├── main.tsx                # 应用入口点
└── vite-env.d.ts           # Vite 类型定义
```

## 核心功能模块

### 1. 文档管理器 (`DocumentManager.tsx`)

**功能概述**：
- 文档上传和管理
- 批量操作支持
- 文档状态跟踪
- 处理管道监控

**主要特性**：
```typescript
// 文档状态类型
type DocStatus = 'pending' | 'processing' | 'completed' | 'failed'

// 支持的操作
- 上传单个/多个文档
- 扫描目录
- 删除文档
- 清空所有数据
- 实时状态更新
```

**核心组件**：
- `UploadDocumentsDialog`: 文档上传对话框
- `PipelineStatusDialog`: 处理状态监控
- `ClearDocumentsDialog`: 清理确认对话框
- `DeleteDocumentsDialog`: 删除确认对话框

### 2. 知识图谱查看器 (`GraphViewer.tsx`)

**功能概述**：
- 交互式图谱可视化
- 多种布局算法
- 节点和边的属性编辑
- 搜索和导航功能

**主要特性**：
```typescript
// Sigma.js 配置
const sigmaSettings = {
  allowInvalidContainer: true,
  defaultNodeType: 'default',
  defaultEdgeType: 'curvedNoArrow',
  enableEdgeEvents: true,
  renderEdgeLabels: false
}

// 支持的布局
- Force Atlas 2
- Force
- Circular
- Random
- Circle Pack
- NoOverlap
```

**核心组件**：
- `GraphControl`: 图谱控制器
- `GraphSearch`: 节点搜索
- `LayoutsControl`: 布局控制
- `ZoomControl`: 缩放控制
- `PropertiesView`: 属性面板
- `Legend`: 图例显示

### 3. 检索测试器 (`RetrievalTesting.tsx`)

**功能概述**：
- 多模式 RAG 查询
- 流式响应支持
- 对话历史管理
- 查询参数调优

**主要特性**：
```typescript
// 查询模式
type QueryMode = 'naive' | 'local' | 'global' | 'hybrid' | 'mix' | 'bypass'

// 查询参数
interface QuerySettings {
  mode: QueryMode
  top_k: number
  chunk_top_k: number
  max_entity_tokens: number
  max_relation_tokens: number
  max_total_tokens: number
  history_turns: number
  enable_rerank: boolean
}
```

**核心组件**：
- `QuerySettings`: 查询参数配置
- `ChatMessage`: 消息显示组件
- Mermaid 图表支持
- 流式响应处理

### 4. 站点头部 (`SiteHeader.tsx`)

**功能概述**：
- 顶部导航栏
- 标签页切换
- 主题切换
- 语言切换

**主要特性**：
```typescript
// 标签页配置
const tabs = [
  { id: 'documents', icon: FileTextIcon, label: t('tabs.documents') },
  { id: 'graph', icon: NetworkIcon, label: t('tabs.graph') },
  { id: 'retrieval', icon: SearchIcon, label: t('tabs.retrieval') },
  { id: 'api', icon: CodeIcon, label: t('tabs.api') }
]
```

## 状态管理

### 1. 全局状态 (`state.ts`)

```typescript
// 后端状态
interface BackendState {
  health: boolean
  message: string
  pipelineBusy: boolean
  check: () => Promise<void>
  clear: () => void
}

// 认证状态
interface AuthState {
  token: string | null
  isGuestMode: boolean
  coreVersion: string | null
  apiVersion: string | null
  webuiTitle: string | null
  webuiDescription: string | null
  login: (token: string, isGuest: boolean, ...) => void
  logout: () => void
}
```

### 2. 图谱状态 (`graph.ts`)

```typescript
interface GraphState {
  sigmaInstance: Sigma | null
  selectedNode: string | null
  focusedNode: string | null
  isFetching: boolean
  nodeFilter: string
  edgeFilter: string
  // 操作方法
  setSelectedNode: (nodeId: string | null, move?: boolean) => void
  setFocusedNode: (nodeId: string | null) => void
  setSigmaInstance: (sigma: Sigma | null) => void
}
```

### 3. 设置状态 (`settings.ts`)

```typescript
interface SettingsState {
  // UI 设置
  currentTab: string
  showPropertyPanel: boolean
  showNodeSearchBar: boolean
  showLegend: boolean
  enableNodeDrag: boolean
  
  // 查询设置
  querySettings: QuerySettings
  retrievalHistory: MessageWithError[]
  
  // 系统设置
  enableHealthCheck: boolean
}
```

## UI 组件库

### 基础组件 (`components/ui/`)

**Button**:
```typescript
interface ButtonProps {
  variant?: 'default' | 'destructive' | 'outline' | 'secondary' | 'ghost' | 'link'
  size?: 'default' | 'sm' | 'lg' | 'icon'
  asChild?: boolean
}
```

**Input**:
```typescript
interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  error?: string
}
```

**Card**:
```typescript
interface CardProps {
  children: React.ReactNode
  className?: string
}
```

**Table**:
```typescript
// 完整的表格组件集
<Table>
  <TableHeader>
    <TableRow>
      <TableHead>标题</TableHead>
    </TableRow>
  </TableHeader>
  <TableBody>
    <TableRow>
      <TableCell>内容</TableCell>
    </TableRow>
  </TableBody>
</Table>
```

### 专用组件

#### 文档组件 (`components/documents/`)

- `UploadDocumentsDialog`: 支持拖拽上传，多文件选择
- `PipelineStatusDialog`: 实时显示处理进度
- `ClearDocumentsDialog`: 危险操作确认
- `DeleteDocumentsDialog`: 批量删除确认

#### 图谱组件 (`components/graph/`)

- `GraphControl`: 图谱数据管理和渲染控制
- `GraphSearch`: 智能节点搜索，支持模糊匹配
- `LayoutsControl`: 一键切换布局算法
- `PropertiesView`: 节点/边属性的详细显示和编辑
- `Settings`: 图谱显示参数调整
- `Legend`: 动态图例生成

#### 检索组件 (`components/retrieval/`)

- `QuerySettings`: 详细的查询参数配置面板
- `ChatMessage`: 支持 Markdown 和 Mermaid 渲染

## 国际化支持

### 语言配置

支持的语言：
- 简体中文 (`zh`)
- 繁体中文 (`zh_TW`)
- 英语 (`en`)
- 法语 (`fr`)
- 阿拉伯语 (`ar`)

### 使用方式

```typescript
import { useTranslation } from 'react-i18next'

function Component() {
  const { t, i18n } = useTranslation()
  
  return (
    <div>
      <h1>{t('common.title')}</h1>
      <button onClick={() => i18n.changeLanguage('en')}>
        {t('common.switchLanguage')}
      </button>
    </div>
  )
}
```

### 资源结构

```json
{
  "common": {
    "title": "LightRAG",
    "loading": "加载中...",
    "error": "错误",
    "success": "成功"
  },
  "tabs": {
    "documents": "文档管理",
    "graph": "知识图谱",
    "retrieval": "检索测试",
    "api": "API 文档"
  },
  "documentPanel": {
    "upload": "上传文档",
    "scan": "扫描目录",
    "delete": "删除",
    "clear": "清空所有"
  }
}
```

## 主题系统

### 主题提供者

```typescript
// ThemeProvider.tsx
function ThemeProvider({ children }: { children: React.ReactNode }) {
  const theme = useSettingsStore.use.theme()
  
  useEffect(() => {
    const root = window.document.documentElement
    root.classList.remove('light', 'dark')
    
    if (theme === 'system') {
      const systemTheme = window.matchMedia('(prefers-color-scheme: dark)').matches
        ? 'dark' : 'light'
      root.classList.add(systemTheme)
    } else {
      root.classList.add(theme)
    }
  }, [theme])
  
  return children
}
```

### 主题切换

```typescript
// ThemeToggle.tsx
function ThemeToggle() {
  const theme = useSettingsStore.use.theme()
  const setTheme = useSettingsStore.use.setTheme()
  
  const toggleTheme = () => {
    const nextTheme = theme === 'light' ? 'dark' : 
                     theme === 'dark' ? 'system' : 'light'
    setTheme(nextTheme)
  }
  
  return (
    <Button variant="ghost" size="icon" onClick={toggleTheme}>
      {theme === 'light' && <SunIcon />}
      {theme === 'dark' && <MoonIcon />}
      {theme === 'system' && <ComputerIcon />}
    </Button>
  )
}
```

## API 集成

### HTTP 客户端

```typescript
// api/lightrag.ts
import axios from 'axios'

const client = axios.create({
  baseURL: '/api',
  headers: {
    'Content-Type': 'application/json'
  }
})

// 请求拦截器 - 添加认证
client.interceptors.request.use((config) => {
  const token = localStorage.getItem('LIGHTRAG-API-TOKEN')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

// 响应拦截器 - 错误处理
client.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // 处理认证失败
      useAuthStore.getState().logout()
    }
    return Promise.reject(error)
  }
)
```

### API 方法

```typescript
// 文档管理
export const uploadText = (text: string, fileSource?: string) =>
  client.post('/documents/text', { text, file_source: fileSource })

export const getDocuments = () =>
  client.get('/documents')

// 查询检索
export const queryText = (params: QueryParams) =>
  client.post('/query', params)

export const queryTextStream = (params: QueryParams) =>
  client.post('/query/stream', params, { responseType: 'stream' })

// 知识图谱
export const getKnowledgeGraph = (label: string, maxDepth?: number) =>
  client.get('/graphs', { params: { label, max_depth: maxDepth } })
```

## 性能优化

### 代码分割

```typescript
// 懒加载组件
const GraphViewer = lazy(() => import('@/features/GraphViewer'))
const DocumentManager = lazy(() => import('@/features/DocumentManager'))

// 路由级别的代码分割
const routes = [
  {
    path: '/graph',
    element: <Suspense fallback={<Loading />}><GraphViewer /></Suspense>
  }
]
```

### 虚拟化

```typescript
// 大列表虚拟化
import { FixedSizeList as List } from 'react-window'

function VirtualizedDocumentList({ items }: { items: Document[] }) {
  const Row = ({ index, style }: { index: number, style: React.CSSProperties }) => (
    <div style={style}>
      <DocumentItem document={items[index]} />
    </div>
  )
  
  return (
    <List
      height={600}
      itemCount={items.length}
      itemSize={50}
      width="100%"
    >
      {Row}
    </List>
  )
}
```

### 内存管理

```typescript
// 清理 Sigma 实例
useEffect(() => {
  return () => {
    const sigma = useGraphStore.getState().sigmaInstance
    if (sigma) {
      sigma.kill()
      useGraphStore.getState().setSigmaInstance(null)
    }
  }
}, [])

// 防抖处理
const debouncedSearch = useDebounce(searchTerm, 300)
useEffect(() => {
  if (debouncedSearch) {
    performSearch(debouncedSearch)
  }
}, [debouncedSearch])
```

## 开发和构建

### 开发环境

```bash
# 安装依赖
bun install
# 或
npm install

# 启动开发服务器
bun run dev
# 或
npm run dev
```

### 构建配置

```typescript
// vite.config.ts
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react-swc'
import path from 'path'

export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src')
    }
  },
  build: {
    outDir: 'dist',
    rollupOptions: {
      output: {
        manualChunks: {
          vendor: ['react', 'react-dom'],
          ui: ['@radix-ui/react-dialog', '@radix-ui/react-tabs'],
          graph: ['sigma', '@react-sigma/core']
        }
      }
    }
  }
})
```

### 类型检查

```typescript
// tsconfig.json
{
  "compilerOptions": {
    "target": "ES2020",
    "lib": ["ES2020", "DOM", "DOM.Iterable"],
    "module": "ESNext",
    "skipLibCheck": true,
    "moduleResolution": "bundler",
    "allowImportingTsExtensions": true,
    "resolveJsonModule": true,
    "isolatedModules": true,
    "noEmit": true,
    "jsx": "react-jsx",
    "strict": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noFallthroughCasesInSwitch": true,
    "baseUrl": ".",
    "paths": {
      "@/*": ["./src/*"]
    }
  }
}
```

## 部署

### 静态文件服务

构建后的文件会输出到 `lightrag/api/webui/` 目录，由 FastAPI 作为静态文件服务：

```python
# lightrag_server.py
app.mount("/webui", StaticFiles(directory="lightrag/api/webui", html=True), name="webui")

@app.get("/")
async def redirect_to_webui():
    return RedirectResponse(url="/webui/")
```

### 环境变量

```bash
# Web UI 配置
WEBUI_TITLE="My LightRAG Instance"
WEBUI_DESCRIPTION="Knowledge Graph RAG System"

# API 端点
LIGHTRAG_API_BASE_URL=http://localhost:8020
```

这份文档详细介绍了 LightRAG Web UI 的所有主要组件、架构设计和开发实践，为开发者提供了完整的技术参考。