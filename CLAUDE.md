# RAG 项目

本项目包含火山引擎知识库检索 skill。

## Skills

### knowledge-base

火山引擎知识库检索 skill，调用 `/api/knowledge/collection/search_knowledge` 接口。

**位置**: `.claude/skills/knowledge-base/`

**核心文件**:
- `skill.md` - Skill 定义
- `search_knowledge.py` - API 调用代码

**环境变量**:
- `VOLCENGINE_APIKEY` - 火山引擎 API 密钥

**使用方法**:
```python
from knowledge_base.search_knowledge import search_knowledge

result = search_knowledge(
    query="你的查询内容",
    collection_name="你的collection名称",
    project_name="default",
    limit=10
)
```
