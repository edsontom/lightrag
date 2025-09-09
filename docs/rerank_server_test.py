import requests
from typing import Dict

def rerank_service(base_url: str = "http://localhost:8182") -> Dict:
    try:
        test_data = {
            "query": "机器学习算法的基本原理",
            "documents": [
                "机器学习是人工智能的一个分支，通过算法让计算机自动从数据中学习模式。",
                "深度学习使用神经网络来模拟人脑的学习过程。",
                "监督学习需要标注的训练数据来训练模型。",
                "今天天气很好，适合户外运动。",
                "线性回归是最简单的机器学习算法之一。"
            ],
            "top_n": 10
        }
        rerank_response = requests.post(
            f"{base_url}/rerank",
            json=test_data,
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        if rerank_response.status_code == 200:
            rerank_data = rerank_response.json()
            print(f"✅ 重排序成功:")
            print(f"   模型: {rerank_data.get('model', 'unknown')}")
            print(f"   结果数量: {len(rerank_data.get('results', []))}")
            for i, result in enumerate(rerank_data.get('results', [])):
                doc_idx = result.get('index', 0)
                score = result.get('relevance_score', 0)
                doc_preview = test_data['documents'][doc_idx][:50] + "..."
                print(f"   第{i+1}名: 文档{doc_idx}, 得分{score:.4f}, 内容: {doc_preview}")
        else:
            print(f"❌ 重排序失败: {rerank_response.status_code}")
            print(f"   响应内容: {rerank_response.text}")
    except Exception as e:
        print(f"❌ 重排序异常: {e}")

if __name__ == "__main__":
    # 替换为你的实际服务地址
    service_url = "http://10.0.20.73:8182"
    rerank_service(service_url)