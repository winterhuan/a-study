#!/usr/bin/env python3
"""
OpenRouter 最新免费模型展示

展示最新添加的免费AI模型，包括推理模型、编程模型等
"""

import os
import time
from agno import Agent
from agno.models.openrouter import OpenRouter

class NewModelsShowcase:
    def __init__(self):
        """初始化新模型展示类"""
        self.reasoning_models = {
            "DeepSeek R1": "deepseek/deepseek-r1:free",
            "DeepSeek R1 0528": "deepseek/deepseek-r1-0528:free", 
            "DeepSeek R1T2 Chimera": "tngtech/deepseek-r1t2-chimera:free",
            "DeepSeek R1T Chimera": "tngtech/deepseek-r1t-chimera:free",
        }
        
        self.chat_models = {
            "DeepSeek Chat v3.1": "deepseek/deepseek-chat-v3.1:free",
            "DeepSeek Chat v3 0324": "deepseek/deepseek-chat-v3-0324:free",
            "Grok-4 Fast": "x-ai/grok-4-fast:free",
            "Gemini 2.0 Flash": "google/gemini-2.0-flash-exp:free",
            "GLM-4.5 Air": "z-ai/glm-4.5-air:free",
        }
        
        self.coding_models = {
            "Qwen3 Coder": "qwen/qwen3-coder:free",
            "Qwen3 235B": "qwen/qwen3-235b-a22b:free",
        }
        
        self.other_models = {
            "GPT OSS 120B": "openai/gpt-oss-120b:free",
            "GPT OSS 20B": "openai/gpt-oss-20b:free",
            "Microsoft MAI DS R1": "microsoft/mai-ds-r1:free",
            "NVIDIA Nemotron Nano": "nvidia/nemotron-nano-9b-v2:free",
        }
    
    def create_agent(self, model_id: str, model_name: str = "") -> Agent:
        """创建指定模型的Agent"""
        return Agent(
            model=OpenRouter(
                id=model_id,
                max_tokens=512,  # 减少token数量以节省配额
            ),
            markdown=True,
            description=f"使用{model_name}模型的AI助手"
        )
    
    def test_reasoning_models(self):
        """测试推理模型"""
        print("🧠 推理模型测试")
        print("=" * 80)
        
        # 复杂推理问题
        reasoning_prompt = """
        有一个奇怪的村庄，村里有100个人，每个人要么总是说真话，要么总是说假话。
        你遇到了三个村民A、B、C：
        - A说："我们三个人中至少有一个说假话的人"
        - B说："我们三个人中至多有一个说真话的人"  
        - C什么都没说
        
        请分析A、B、C分别是说真话的人还是说假话的人，并给出详细推理过程。
        """
        
        print(f"🧩 推理题目: {reasoning_prompt.strip()}")
        print("-" * 80)
        
        for name, model_id in list(self.reasoning_models.items())[:3]:  # 只测试前3个避免配额问题
            try:
                print(f"\n🤖 {name} ({model_id}):")
                agent = self.create_agent(model_id, name)
                agent.print_response(reasoning_prompt)
                time.sleep(2)  # 避免请求过于频繁
            except Exception as e:
                print(f"❌ {name} 模型测试失败: {e}")
            print("-" * 40)
    
    def test_coding_models(self):
        """测试编程模型"""
        print("\n💻 编程模型测试")
        print("=" * 80)
        
        coding_prompt = """
        请用Python实现一个简单的LRU缓存类，要求：
        1. 支持get(key)和put(key, value)操作
        2. 当缓存满时，删除最近最少使用的项
        3. 时间复杂度O(1)
        4. 代码要有注释
        """
        
        print(f"💡 编程任务: {coding_prompt.strip()}")
        print("-" * 80)
        
        for name, model_id in self.coding_models.items():
            try:
                print(f"\n🤖 {name} ({model_id}):")
                agent = self.create_agent(model_id, name)
                agent.print_response(coding_prompt)
                time.sleep(2)
            except Exception as e:
                print(f"❌ {name} 模型测试失败: {e}")
            print("-" * 40)
    
    def test_chat_models(self):
        """测试聊天模型"""
        print("\n💬 聊天模型测试")
        print("=" * 80)
        
        chat_prompt = """
        你是一个友善的AI助手。请用中文回答：
        1. 简单介绍一下你自己
        2. 你最擅长什么类型的任务？
        3. 对用户有什么建议？
        
        回答要简洁友好，不超过150字。
        """
        
        print(f"🗣️ 聊天测试: {chat_prompt.strip()}")
        print("-" * 80)
        
        for name, model_id in list(self.chat_models.items())[:3]:  # 只测试前3个
            try:
                print(f"\n🤖 {name} ({model_id}):")
                agent = self.create_agent(model_id, name)
                agent.print_response(chat_prompt)
                time.sleep(2)
            except Exception as e:
                print(f"❌ {name} 模型测试失败: {e}")
            print("-" * 40)
    
    def model_comparison_test(self):
        """模型对比测试"""
        print("\n⚖️ 模型能力对比")
        print("=" * 80)
        
        test_cases = [
            {
                "name": "数学推理",
                "prompt": "一个正方形的对角线长度是10√2，求这个正方形的面积。请给出详细计算过程。"
            },
            {
                "name": "创意写作", 
                "prompt": "写一首关于人工智能与人类合作的七言绝句，要押韵。"
            },
            {
                "name": "逻辑分析",
                "prompt": "如果所有的猫都是动物，所有的动物都需要食物，那么可以推出什么结论？请解释推理过程。"
            }
        ]
        
        # 选择几个代表性模型进行对比
        selected_models = {
            "DeepSeek R1 (推理)": "deepseek/deepseek-r1:free",
            "Grok-4 Fast (聊天)": "x-ai/grok-4-fast:free", 
            "Qwen3 Coder (编程)": "qwen/qwen3-coder:free",
        }
        
        for test_case in test_cases:
            print(f"\n📋 测试: {test_case['name']}")
            print(f"问题: {test_case['prompt']}")
            print("=" * 60)
            
            for model_name, model_id in selected_models.items():
                try:
                    print(f"\n🤖 {model_name}:")
                    agent = self.create_agent(model_id, model_name)
                    agent.print_response(test_case['prompt'])
                    time.sleep(1)
                except Exception as e:
                    print(f"❌ {model_name} 测试失败: {e}")
                print("-" * 30)
    
    def list_all_models(self):
        """列出所有可用模型"""
        print("📋 所有可用免费模型列表")
        print("=" * 80)
        
        all_models = {
            "🧠 推理模型": self.reasoning_models,
            "💬 聊天模型": self.chat_models, 
            "💻 编程模型": self.coding_models,
            "🔧 其他模型": self.other_models,
        }
        
        for category, models in all_models.items():
            print(f"\n{category}:")
            for name, model_id in models.items():
                print(f"  • {name}: {model_id}")
        
        print(f"\n总计: {sum(len(models) for models in all_models.values())} 个免费模型")
    
    def run_showcase(self):
        """运行完整展示"""
        print("🚀 OpenRouter 新增免费模型展示")
        print("=" * 80)
        print("注意：由于是免费模型，请合理使用以避免达到速率限制")
        print("=" * 80)
        
        showcases = [
            ("列出所有模型", self.list_all_models),
            ("推理模型测试", self.test_reasoning_models),
            ("编程模型测试", self.test_coding_models), 
            ("聊天模型测试", self.test_chat_models),
            ("模型对比测试", self.model_comparison_test),
        ]
        
        print("\n请选择要运行的展示:")
        for i, (name, _) in enumerate(showcases, 1):
            print(f"{i}. {name}")
        print("6. 运行所有展示")
        
        try:
            choice = input("\n请输入选择 (1-6): ").strip()
            
            if choice == "6":
                for name, func in showcases:
                    print(f"\n{'='*20} {name} {'='*20}")
                    func()
                    time.sleep(3)
            elif choice.isdigit() and 1 <= int(choice) <= 5:
                name, func = showcases[int(choice) - 1]
                print(f"\n{'='*20} {name} {'='*20}")
                func()
            else:
                print("无效选择，运行模型列表...")
                self.list_all_models()
                
        except KeyboardInterrupt:
            print("\n\n👋 展示已停止")
        except Exception as e:
            print(f"❌ 运行出错: {e}")

def main():
    """主函数"""
    if not os.getenv("OPENROUTER_API_KEY"):
        print("⚠️  请设置 OPENROUTER_API_KEY 环境变量")
        print("   获取密钥: https://openrouter.ai/keys") 
        print("   设置方法: export OPENROUTER_API_KEY=your_key")
        return
    
    showcase = NewModelsShowcase()
    showcase.run_showcase()

if __name__ == "__main__":
    main()