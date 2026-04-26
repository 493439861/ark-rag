import json
import os
import requests

try:
    from dotenv import load_dotenv
    # 尝试从项目根目录加载 .env 文件
    _env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))), '.env')
    if os.path.exists(_env_path):
        load_dotenv(_env_path)
except ImportError:
    pass  # dotenv 未安装时跳过


class VolcengineKnowledgeBase:
    """火山引擎知识库 API 调用封装"""

    def __init__(
        self,
        collection_name: str = "FundInvest",
        project_name: str = "default",
        domain: str = "api-knowledgebase.mlp.cn-beijing.volces.com",
        apikey: str = None,
    ):
        self.collection_name = collection_name
        self.project_name = project_name
        self.domain = domain
        self.apikey = apikey or os.environ.get("VOLCENGINE_APIKEY", "")
        self.base_url = f"http://{domain}" if not domain.startswith("http") else domain

    def _prepare_request(self, method: str, path: str, params=None, data=None, doseq: int = 0):
        """准备请求对象"""
        if params:
            for key in params:
                if isinstance(params[key], (int, float, bool)):
                    params[key] = str(params[key])
                elif isinstance(params[key], list):
                    if not doseq:
                        params[key] = ",".join(str(v) for v in params[key])

        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json; charset=utf-8",
            "Host": self.domain,
            "Authorization": f"Bearer {self.apikey}",
        }

        request_info = {
            "method": method,
            "path": path,
            "headers": headers,
            "body": json.dumps(data) if data is not None else None,
        }
        return request_info

    def search(
        self,
        query: str,
        limit: int = 10,
        image_query: str = "",
        dense_weight: float = 0.5,
        need_instruction: bool = True,
        return_token_usage: bool = True,
    ) -> dict:
        """
        搜索知识库

        Args:
            query: 自然语言查询
            limit: 返回结果数量限制
            image_query: 图片查询（可传入URL或Base64编码）
            dense_weight: 稠密向量权重 (0-1)
            need_instruction: 是否需要指令增强
            return_token_usage: 是否返回token使用量

        Returns:
            API响应结果 (dict)
        """
        method = "POST"
        path = "/api/knowledge/collection/search_knowledge"

        request_params = {
            "project": self.project_name,
            "name": self.collection_name,
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

        req_info = self._prepare_request(method=method, path=path, data=request_params)

        rsp = requests.request(
            method=req_info["method"],
            url=f"{self.base_url}{req_info['path']}",
            headers=req_info["headers"],
            data=req_info["body"],
            timeout=30,
        )

        if rsp.status_code != 200:
            return {"error": f"HTTP {rsp.status_code}", "detail": rsp.text}

        try:
            return rsp.json()
        except json.JSONDecodeError:
            return {"error": "Invalid JSON response", "raw": rsp.text}


def search_knowledge(
    query: str,
    collection_name: str = "FundInvest",
    project_name: str = "default",
    apikey: str = None,
    domain: str = "api-knowledgebase.mlp.cn-beijing.volces.com",
    limit: int = 10,
) -> dict:
    """
    便捷函数：搜索火山引擎知识库

    Args:
        query: 自然语言查询
        collection_name: 知识库 collection 名称
        project_name: 项目名称
        apikey: API密钥（默认从环境变量 VOLCENGINE_APIKEY 获取）
        domain: API域名
        limit: 返回结果数量

    Returns:
        API响应结果
    """
    kb = VolcengineKnowledgeBase(
        collection_name=collection_name,
        project_name=project_name,
        domain=domain,
        apikey=apikey,
    )
    return kb.search(query=query, limit=limit)


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python search_knowledge.py <query>")
        sys.exit(1)

    query = sys.argv[1]
    result = search_knowledge(query)
    print(json.dumps(result, ensure_ascii=False, indent=2))
