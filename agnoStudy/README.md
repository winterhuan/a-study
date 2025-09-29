# Agno OpenRouter 免费模型示例

这是一个使用 Agno v2.0.9 框架和 OpenRouter 免费模型的基本示例。

## 功能特点

- 🆓 使用 OpenRouter 的免费 AI 模型
- 🤖 基于 Agno v2.0.9 框架的简单集成
- 📝 多种使用示例（问答、编程帮助、创意写作）
- 🔄 支持多个免费模型测试

## 可用的免费模型

### 推理模型
- `deepseek/deepseek-r1:free` - DeepSeek R1 推理模型 ⭐️ 推荐
- `deepseek/deepseek-r1-0528:free` - DeepSeek R1 0528版本
- `tngtech/deepseek-r1t2-chimera:free` - DeepSeek R1T2 Chimera
- `tngtech/deepseek-r1t-chimera:free` - DeepSeek R1T Chimera

### 聊天模型
- `deepseek/deepseek-chat-v3.1:free` - DeepSeek Chat v3.1
- `deepseek/deepseek-chat-v3-0324:free` - DeepSeek Chat v3 0324版本
- `x-ai/grok-4-fast:free` - xAI 的 Grok-4 Fast
- `google/gemini-2.0-flash-exp:free` - Google 的 Gemini 2.0 Flash

### 编程模型
- `qwen/qwen3-coder:free` - 阿里 Qwen 3 编程专用模型
- `qwen/qwen3-235b-a22b:free` - 阿里 Qwen 3 235B

### 其他模型
- `openai/gpt-oss-120b:free` - OpenAI GPT OSS 120B
- `openai/gpt-oss-20b:free` - OpenAI GPT OSS 20B
- `microsoft/mai-ds-r1:free` - Microsoft MAI DS R1
- `nvidia/nemotron-nano-9b-v2:free` - NVIDIA Nemotron Nano 9B v2
- `z-ai/glm-4.5-air:free` - 智谱 GLM-4.5 Air

### 经典模型
- `meta-llama/llama-3.1-8b-instruct:free` - Meta 的 Llama 3.1 8B
- `google/gemma-2-9b-it:free` - Google 的 Gemma 2 9B  
- `microsoft/phi-3-mini-128k-instruct:free` - Microsoft 的 Phi-3 Mini

## 版本信息

本项目使用 **Agno v2.0.9**，这是 Agno 2.0 系列的稳定版本。

### v2.0 主要变化：
- 📊 简化了导入语句：`from agno import Agent`
- ⚡️ 提升了性能和稳定性
- 🔧 更好的错误处理和日志
- 🔄 向下兼容，但建议使用新的导入方式

## 安装和设置

### 快速安装

使用自动安装脚本：

```bash
./install.sh
```

### 手动安装

#### 1. 创建虚拟环境

```bash
python3 -m venv .venv
source .venv/bin/activate
```

#### 2. 安装依赖

```bash
pip install -r requirements.txt

# 或者直接安装指定版本
pip install agno==2.0.9
```

#### 3. 测试安装

```bash
python test_version.py
```

#### 4. 设置 API 密钥

访问 [OpenRouter](https://openrouter.ai/keys) 获取免费的 API 密钥，然后设置环境变量：

```bash
export OPENROUTER_API_KEY=your_api_key_here
```

## 使用方法

### 运行示例

```bash
# 最简单的入门示例
python simple_example.py

# 基本功能演示
python basic_openrouter.py

# 高级用例演示
python advanced_example.py

# 最新免费模型展示
python new_models_showcase.py
```

### 代码结构

```python
from agno import Agent
from agno.models.openrouter import OpenRouter

# 创建使用免费模型的 Agent
agent = Agent(
    model=OpenRouter(
        id="deepseek/deepseek-r1:free",  # 推理模型，适合复杂问题
        max_tokens=1024,
    ),
    markdown=True
)

# 使用 Agent
agent.print_response("你好，介绍一下自己")
```

## 示例输出

脚本将演示：

1. **简单问答** - 询问关于免费 AI 模型的好处
2. **编程帮助** - 请求编写 Python 函数
3. **创意写作** - 生成关于人工智能的俳句

## 注意事项

- 免费模型可能有使用限制和速率限制
- 某些模型可能在特定时间不可用
- 建议在生产环境中使用付费模型以获得更好的性能和稳定性

## 参考资料

- [Agno 文档](https://docs.agno.com/)
- [OpenRouter 文档](https://openrouter.ai/docs)
- [OpenRouter 免费模型列表](https://openrouter.ai/models?q=free)