# LightRAG API 接口文档

## 概述

LightRAG 提供完整的 REST API 服务，基于 FastAPI 构建，支持文档管理、查询检索、知识图谱操作等功能。API 还兼容 Ollama 接口，可以无缝集成到现有的 AI 聊天系统中。

## 基础信息

- **基础 URL**: `http://localhost:8020` (默认)
- **API 版本**: 动态获取自 `lightrag.api.__api_version__`
- **认证方式**: Bearer Token (可选)
- **内容类型**: `application/json`
- **文档地址**: 
  - Swagger UI: `http://localhost:8020/docs`
  - ReDoc: `http://localhost:8020/redoc`

## 认证

API 支持可选的认证机制：

```bash
# 设置 API Key
export LIGHTRAG_API_KEY="your-api-key"

# 或在启动时指定
lightrag-server --key your-api-key
```

认证请求头：
```http
Authorization: Bearer your-api-key
```

## API 路由概览

### 核心 API 路由

| 路由前缀 | 功能 | 说明 |
|---------|------|------|
| `/documents` | 文档管理 | 上传、扫描、删除文档 |
| `/query` | 查询检索 | RAG 查询接口 |
| `/graph` | 知识图谱 | 图谱查看和编辑 |
| `/v1` | Ollama 兼容 | 兼容 Ollama API |

### 系统路由

| 路由 | 功能 | 说明 |
|------|------|------|
| `/health` | 健康检查 | 服务状态检查 |
| `/` | Web UI | 重定向到前端界面 |
| `/webui/*` | 静态文件 | 前端资源服务 |

## 1. 文档管理 API (`/documents`)

### 1.1 上传文本文档

**POST** `/documents/text`

插入单个文本文档到 RAG 系统。

**请求体**:
```json
{
  "text": "要插入的文本内容",
  "file_source": "文本来源（可选）"
}
```

**响应**:
```json
{
  "status": "success",
  "message": "Document inserted successfully"
}
```

### 1.2 批量上传文本

**POST** `/documents/texts`

批量插入多个文本文档。

**请求体**:
```json
{
  "texts": [
    "第一个文本内容",
    "第二个文本内容"
  ],
  "file_sources": [
    "来源1",
    "来源2"
  ]
}
```

### 1.3 上传文件

**POST** `/documents/upload`

上传文件到系统。

**请求**:
- Content-Type: `multipart/form-data`
- 字段: `file` (文件)

**响应**:
```json
{
  "message": "File uploaded successfully",
  "filename": "uploaded_file.txt"
}
```

### 1.4 扫描目录

**POST** `/documents/scan`

扫描指定目录中的文档并建立索引。

**响应**:
```json
{
  "status": "scanning_started",
  "message": "Scanning process has been initiated in the background"
}
```

### 1.5 获取文档列表

**GET** `/documents`

获取已上传的文档列表。

**查询参数**:
- `skip`: 跳过数量 (默认: 0)
- `limit`: 返回数量 (默认: 100)

**响应**:
```json
{
  "files": [
    {
      "name": "document1.txt",
      "size": 1024,
      "created_at": "2024-01-01T00:00:00Z",
      "status": "completed"
    }
  ],
  "total": 1
}
```

### 1.6 获取处理状态

**GET** `/documents/pipeline_status`

获取文档处理管道的状态。

**响应**:
```json
{
  "total_documents": 10,
  "processed_documents": 8,
  "failed_documents": 1,
  "pending_documents": 1,
  "processing": true
}
```

### 1.7 删除文档

**DELETE** `/documents/{file_path}`

删除指定文档。

**路径参数**:
- `file_path`: 文档路径

**响应**:
```json
{
  "message": "Document deleted successfully"
}
```

### 1.8 清空所有数据

**DELETE** `/documents/clear_all_data`

清空所有文档和索引数据。

**响应**:
```json
{
  "message": "All data cleared successfully"
}
```

## 2. 查询检索 API (`/query`)

### 2.1 文本查询

**POST** `/query`

执行 RAG 查询获取回答。

**请求体**:
```json
{
  "query": "用户查询文本",
  "mode": "mix",
  "only_need_context": false,
  "only_need_prompt": false,
  "response_type": "Multiple Paragraphs",
  "top_k": 60,
  "chunk_top_k": 10,
  "max_entity_tokens": 10000,
  "max_relation_tokens": 10000,
  "max_total_tokens": 32000,
  "conversation_history": [
    {
      "role": "user",
      "content": "之前的用户消息"
    },
    {
      "role": "assistant", 
      "content": "之前的助手回复"
    }
  ],
  "history_turns": 3,
  "ids": ["doc1", "doc2"],
  "user_prompt": "自定义用户提示词",
  "enable_rerank": true
}
```

**查询模式**:
- `local`: 基于实体的本地检索
- `global`: 基于关系的全局检索  
- `hybrid`: 混合检索模式
- `naive`: 基础向量检索
- `mix`: 综合知识图谱和向量检索
- `bypass`: 绕过检索直接生成

**响应**:
```json
{
  "response": "基于检索内容生成的回答"
}
```

### 2.2 流式查询

**POST** `/query/stream`

执行流式 RAG 查询，实时返回生成内容。

**请求体**: 同 `/query`

**响应**: Server-Sent Events (SSE) 流
```
data: {"response": "生成的"}
data: {"response": "内容片段"}
data: {"response": "..."}
```

## 3. 知识图谱 API (`/graph`)

### 3.1 获取图谱标签

**GET** `/graph/label/list`

获取知识图谱中的所有标签。

**响应**:
```json
[
  "Person",
  "Organization", 
  "Location",
  "Event"
]
```

### 3.2 获取知识图谱

**GET** `/graphs`

获取指定标签的知识图谱子图。

**查询参数**:
- `label`: 起始节点标签 (必需)
- `max_depth`: 最大深度 (默认: 3)
- `max_nodes`: 最大节点数 (默认: 1000)

**响应**:
```json
{
  "nodes": [
    {
      "id": "entity1",
      "label": "Person",
      "properties": {
        "name": "张三",
        "description": "软件工程师"
      }
    }
  ],
  "edges": [
    {
      "source": "entity1",
      "target": "entity2",
      "relation": "works_for",
      "properties": {
        "description": "在...工作",
        "weight": 1.0
      }
    }
  ]
}
```

### 3.3 检查实体存在

**GET** `/graph/entity/exists`

检查指定实体是否存在。

**查询参数**:
- `name`: 实体名称

**响应**:
```json
{
  "exists": true
}
```

### 3.4 编辑实体

**POST** `/graph/entity/edit`

更新实体属性。

**请求体**:
```json
{
  "entity_name": "张三",
  "updated_data": {
    "description": "高级软件工程师",
    "entity_type": "person"
  },
  "allow_rename": false
}
```

**响应**:
```json
{
  "status": "success",
  "message": "Entity updated successfully",
  "data": {
    "entity_name": "张三",
    "description": "高级软件工程师"
  }
}
```

### 3.5 编辑关系

**POST** `/graph/relation/edit`

更新关系属性。

**请求体**:
```json
{
  "source_id": "张三",
  "target_id": "ABC公司", 
  "updated_data": {
    "description": "担任技术主管",
    "weight": 2.0
  }
}
```

**响应**:
```json
{
  "status": "success",
  "message": "Relation updated successfully",
  "data": {
    "source": "张三",
    "target": "ABC公司",
    "relation": "works_for"
  }
}
```

## 4. Ollama 兼容 API (`/v1`)

LightRAG 提供与 Ollama 完全兼容的 API 接口，可以无缝替换 Ollama 服务。

### 4.1 聊天补全

**POST** `/v1/chat/completions`

兼容 OpenAI Chat Completions API 格式。

**请求体**:
```json
{
  "model": "lightrag",
  "messages": [
    {
      "role": "user",
      "content": "用户查询内容"
    }
  ],
  "stream": false,
  "temperature": 0.7,
  "max_tokens": 2048
}
```

### 4.2 文本补全

**POST** `/v1/completions`

兼容文本补全接口。

### 4.3 模型列表

**GET** `/v1/models`

获取可用模型列表。

**响应**:
```json
{
  "object": "list",
  "data": [
    {
      "id": "lightrag",
      "object": "model",
      "created": 1234567890,
      "owned_by": "lightrag"
    }
  ]
}
```

## 5. 系统 API

### 5.1 健康检查

**GET** `/health`

检查服务健康状态。

**响应**:
```json
{
  "status": "healthy",
  "timestamp": "2024-01-01T00:00:00Z",
  "version": "1.4.5"
}
```

## 错误处理

API 使用标准 HTTP 状态码：

- `200`: 成功
- `400`: 请求参数错误
- `401`: 认证失败
- `404`: 资源不存在
- `500`: 服务器内部错误

错误响应格式：
```json
{
  "detail": "错误详细信息"
}
```

## 使用示例

### Python 客户端示例

```python
import requests
import json

# 基础配置
BASE_URL = "http://localhost:8020"
API_KEY = "your-api-key"  # 可选

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {API_KEY}"  # 如果需要认证
}

# 上传文本
def upload_text(text: str):
    url = f"{BASE_URL}/documents/text"
    data = {"text": text}
    response = requests.post(url, json=data, headers=headers)
    return response.json()

# 查询
def query_rag(query: str, mode: str = "mix"):
    url = f"{BASE_URL}/query"
    data = {
        "query": query,
        "mode": mode,
        "top_k": 10
    }
    response = requests.post(url, json=data, headers=headers)
    return response.json()

# 流式查询
def query_rag_stream(query: str):
    url = f"{BASE_URL}/query/stream"
    data = {"query": query, "mode": "mix"}
    
    with requests.post(url, json=data, headers=headers, stream=True) as response:
        for line in response.iter_lines():
            if line:
                data = json.loads(line.decode('utf-8'))
                print(data.get('response', ''), end='', flush=True)

# 获取知识图谱
def get_knowledge_graph(label: str):
    url = f"{BASE_URL}/graphs"
    params = {"label": label, "max_depth": 2}
    response = requests.get(url, params=params, headers=headers)
    return response.json()

# 使用示例
if __name__ == "__main__":
    # 上传文档
    upload_text("这是一个测试文档，包含关于人工智能的内容。")
    
    # 执行查询
    result = query_rag("什么是人工智能？")
    print(result["response"])
    
    # 获取图谱
    graph = get_knowledge_graph("人工智能")
    print(f"图谱包含 {len(graph['nodes'])} 个节点")
```

### JavaScript 客户端示例

```javascript
class LightRAGClient {
    constructor(baseUrl = 'http://localhost:8020', apiKey = null) {
        this.baseUrl = baseUrl;
        this.headers = {
            'Content-Type': 'application/json'
        };
        if (apiKey) {
            this.headers['Authorization'] = `Bearer ${apiKey}`;
        }
    }

    async uploadText(text, fileSource = null) {
        const response = await fetch(`${this.baseUrl}/documents/text`, {
            method: 'POST',
            headers: this.headers,
            body: JSON.stringify({ text, file_source: fileSource })
        });
        return response.json();
    }

    async query(query, options = {}) {
        const data = {
            query,
            mode: options.mode || 'mix',
            top_k: options.topK || 10,
            ...options
        };
        
        const response = await fetch(`${this.baseUrl}/query`, {
            method: 'POST',
            headers: this.headers,
            body: JSON.stringify(data)
        });
        return response.json();
    }

    async *queryStream(query, options = {}) {
        const data = {
            query,
            mode: options.mode || 'mix',
            ...options
        };
        
        const response = await fetch(`${this.baseUrl}/query/stream`, {
            method: 'POST',
            headers: this.headers,
            body: JSON.stringify(data)
        });
        
        const reader = response.body.getReader();
        const decoder = new TextDecoder();
        
        while (true) {
            const { done, value } = await reader.read();
            if (done) break;
            
            const chunk = decoder.decode(value);
            const lines = chunk.split('\n');
            
            for (const line of lines) {
                if (line.trim()) {
                    try {
                        const data = JSON.parse(line);
                        yield data.response;
                    } catch (e) {
                        // 忽略解析错误
                    }
                }
            }
        }
    }

    async getKnowledgeGraph(label, maxDepth = 3, maxNodes = 1000) {
        const params = new URLSearchParams({
            label,
            max_depth: maxDepth.toString(),
            max_nodes: maxNodes.toString()
        });
        
        const response = await fetch(`${this.baseUrl}/graphs?${params}`, {
            headers: this.headers
        });
        return response.json();
    }
}

// 使用示例
const client = new LightRAGClient();

// 上传文档
await client.uploadText('这是一个测试文档。');

// 查询
const result = await client.query('这个文档说了什么？');
console.log(result.response);

// 流式查询
for await (const chunk of client.queryStream('详细解释一下内容')) {
    process.stdout.write(chunk);
}
```

## 配置和部署

### 环境变量

```bash
# 服务配置
HOST=0.0.0.0
PORT=8020
CORS_ORIGINS=*

# API 密钥
LIGHTRAG_API_KEY=your-secret-key

# LLM 配置
OPENAI_API_KEY=sk-...
LLM_MODEL=gpt-4o-mini

# 存储配置
WORKING_DIR=./rag_storage
WORKSPACE=default

# 查询参数
TOP_K=60
CHUNK_TOP_K=10
MAX_TOKENS=32000
```

### Docker 部署

```bash
# 使用 Docker Compose
git clone https://github.com/HKUDS/LightRAG.git
cd LightRAG
cp env.example .env
# 编辑 .env 文件设置必要的配置
docker compose up -d
```

### 开发模式

```bash
# 安装依赖
pip install -e ".[api]"

# 启动开发服务器
lightrag-server --host 0.0.0.0 --port 8020 --reload
```

## 最佳实践

1. **批量操作**: 使用批量 API 提升性能
2. **流式查询**: 对于长内容生成使用流式接口
3. **缓存利用**: 相同查询会自动使用缓存
4. **错误处理**: 实现适当的重试和错误处理机制
5. **认证安全**: 在生产环境中启用 API 密钥认证
6. **监控日志**: 关注健康检查接口和日志输出

这份 API 文档涵盖了 LightRAG 的所有主要接口，提供了完整的使用指南和示例代码，方便开发者快速集成和使用。