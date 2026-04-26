import json
import os
import requests

try:
    from dotenv import load_dotenv
    _env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))), '.env')
    if os.path.exists(_env_path):
        load_dotenv(_env_path)
except ImportError:
    pass


def search_knowledge(
    query: str,
    collection_name: str = "FundInvest",
    project_name: str = "default",
    apikey: str = None,
    domain: str = "api-knowledgebase.mlp.cn-beijing.volces.com",
    limit: int = 10,
    image_query: str = "",
    dense_weight: float = 0.5,
    need_instruction: bool = True,
    return_token_usage: bool = True,
) -> dict:
    """
    搜索火山引擎知识库

    Args:
        query: 自然语言查询
        collection_name: 知识库 collection 名称
        project_name: 项目名称
        apikey: API密钥（默认从环境变量 VOLCENGINE_APIKEY 获取）
        domain: API域名
        limit: 返回结果数量
        image_query: 图片查询（可传入URL或Base64编码）
        dense_weight: 稠密向量权重 (0-1)
        need_instruction: 是否需要指令增强
        return_token_usage: 是否返回token使用量

    Returns:
        API响应结果
    """
    apikey = apikey or os.environ.get("VOLCENGINE_APIKEY", "")
    base_url = f"http://{domain}" if not domain.startswith("http") else domain

    method = "POST"
    path = "/api/knowledge/collection/search_knowledge"

    request_params = {
        "project": project_name,
        "name": collection_name,
        "query": query,
        "limit": limit,
        "pre_processing": {
            "need_instruction": need_instruction,
            "return_token_usage": return_token_usage,
            "messages": [
                {"role": "system", "content": ""},
                {"role": "user"},
            ],
        },
        "dense_weight": dense_weight,
        "post_processing": {
            "get_attachment_link": True,
            "rerank_only_chunk": False,
            "rerank_switch": False,
        },
        "image_query": image_query,
    }

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json; charset=utf-8",
        "Host": domain,
        "Authorization": f"Bearer {apikey}",
    }

    rsp = requests.request(
        method=method,
        url=f"{base_url}{path}",
        headers=headers,
        data=json.dumps(request_params),
        timeout=30,
    )

    if rsp.status_code != 200:
        return {"error": f"HTTP {rsp.status_code}", "detail": rsp.text}

    try:
        return rsp.json()
    except json.JSONDecodeError:
        return {"error": "Invalid JSON response", "raw": rsp.text}


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python search_knowledge.py <query>")
        sys.exit(1)

    query = sys.argv[1]
    result = search_knowledge(query)
    print(json.dumps(result, ensure_ascii=False, indent=2))
