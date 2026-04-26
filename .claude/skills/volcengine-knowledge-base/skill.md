---
name: volcengine-knowledge-base
description: 火山引擎知识库检索skill，通过自然语言查询知识库内容。支持自定义collection名称、API域名、apikey等参数。
---

# volcengine-knowledge-base

本 skill 用于调用火山引擎知识库 API 进行自然语言检索。

## 使用方式

当用户提供查询内容时，使用本 skill 调用知识库 API 进行检索。

### 输入参数

| 参数 | 说明 | 来源 |
|------|------|------|
| `query` | 自然语言查询内容 | 用户提供 |
| `collection_name` | 知识库 collection 名称 | 用户提供或配置 |
| `project_name` | 项目名称 | 用户提供或配置 (默认: "default") |
| `apikey` | API密钥 | 用户提供或环境变量 |
| `domain` | API域名 | 用户提供或配置 |

### 执行流程

1. 读取环境变量或用户提供的配置
2. 调用 `search_knowledge.py` 中的 `search_knowledge` 函数
3. 返回检索结果

### 代码文件

- `search_knowledge.py` - 包含调用火山引擎知识库 API 的 Python 代码

## 配置文件

配置文件位于项目根目录的 `.env` 文件：

```bash
VOLCENGINE_APIKEY=your-api-key-here
VOLCENGINE_DOMAIN=api-knowledgebase.mlp.cn-beijing.volces.com
COLLECTION_NAME=FundInvest
PROJECT_NAME=default
```

### 配置优先级

1. 代码中传入的参数（最高优先级）
2. `.env` 文件中的配置
3. 环境变量
4. 默认值

## 注意事项

- `apikey` 优先从环境变量 `VOLCENGINE_APIKEY` 获取
- `domain` 默认为 `api-knowledgebase.mlp.cn-beijing.volces.com`
- `collection_name` 和 `project_name` 可在调用时指定
- 需要 python-dotenv 库支持 .env 文件加载：`pip install python-dotenv`
