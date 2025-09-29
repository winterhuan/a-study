#!/usr/bin/env python3
"""
最简单的 Agno + OpenRouter 免费模型示例

运行前请先设置环境变量：
export OPENROUTER_API_KEY=your_api_key_here

获取API密钥: https://openrouter.ai/keys
"""

from agno.agent import Agent
from agno.models.openrouter import OpenRouter

# 创建一个使用免费模型的 Agent
agent = Agent(
    model=OpenRouter(id="deepseek/deepseek-r1:free"),  # DeepSeek R1 推理模型
    markdown=True
)

# 简单对话
print("🤖 使用 OpenRouter 免费模型的 Agno Agent")
print("-" * 50)

agent.print_response("你好！请用中文简单介绍一下你自己。")