#!/usr/bin/env python3
"""
Agno + OpenRouter 高级用例示例

演示各种不同的应用场景：
- 代码生成
- 文档翻译
- 数据分析
- 创意写作
"""

import os
import time
from agno import Agent, RunOutput
from agno.models.openrouter import OpenRouter

class AgnoOpenRouterDemo:
    def __init__(self):
        """初始化演示类，使用不同的免费模型"""
        self.models = {
            "deepseek-r1": "deepseek/deepseek-r1:free",
            "grok": "x-ai/grok-4-fast:free",
            "gemini": "google/gemini-2.0-flash-exp:free",
            "deepseek-chat": "deepseek/deepseek-chat-v3.1:free",
            "qwen-coder": "qwen/qwen3-coder:free",
            "gpt-oss": "openai/gpt-oss-120b:free",
            "llama": "meta-llama/llama-3.1-8b-instruct:free",
            "gemma": "google/gemma-2-9b-it:free",
        }
        
    def create_agent(self, model_name: str) -> Agent:
        """创建指定模型的 Agent"""
        model_id = self.models.get(model_name, self.models["deepseek-r1"])
        return Agent(
            model=OpenRouter(
                id=model_id,
                max_tokens=1024,
            ),
            markdown=True,
            description=f"AI助手使用{model_name}模型"
        )
    
    def code_generation_demo(self):
        """代码生成示例"""
        print("🔧 代码生成示例")
        print("=" * 60)
        
        agent = self.create_agent("deepseek-r1")
        
        prompts = [
            "用Python写一个计算斐波那契数列的函数，包含递归和迭代两种方式",
            "创建一个简单的JavaScript待办事项应用的HTML和JS代码",
            "写一个Go语言的HTTP服务器，有健康检查端点"
        ]
        
        for i, prompt in enumerate(prompts, 1):
            print(f"\n📝 任务 {i}: {prompt}")
            print("-" * 40)
            agent.print_response(prompt)
            print("\n")
    
    def translation_demo(self):
        """文档翻译示例"""
        print("🌍 翻译示例")
        print("=" * 60)
        
        agent = self.create_agent("gemini")
        
        # 英文技术文档翻译
        english_text = """
        Machine Learning is a subset of artificial intelligence (AI) that provides 
        systems the ability to automatically learn and improve from experience without 
        being explicitly programmed. ML focuses on the development of computer programs 
        that can access data and use it to learn for themselves.
        """
        
        print("\n📄 原文:")
        print(english_text.strip())
        print("\n🔄 中文翻译:")
        agent.print_response(f"请将以下英文技术文档翻译成中文，保持专业性和准确性：\n\n{english_text}")
    
    def data_analysis_demo(self):
        """数据分析示例"""
        print("\n📊 数据分析示例")
        print("=" * 60)
        
        agent = self.create_agent("qwen-coder")
        
        # 模拟数据分析场景
        data_scenario = """
        假设你有以下销售数据：
        - 1月: 销售额 50000元，订单数 200
        - 2月: 销售额 65000元，订单数 250  
        - 3月: 销售额 48000元，订单数 180
        - 4月: 销售额 72000元，订单数 290
        - 5月: 销售额 68000元，订单数 275
        """
        
        questions = [
            "分析这5个月的销售趋势，包括总体趋势和月度变化",
            "计算每个月的平均订单价值，并分析其变化",
            "基于这些数据，对6月份销售额和订单数进行预测"
        ]
        
        print(f"\n📈 数据背景:\n{data_scenario}")
        
        for i, question in enumerate(questions, 1):
            print(f"\n❓ 问题 {i}: {question}")
            print("-" * 40)
            agent.print_response(f"{data_scenario}\n\n问题: {question}")
            print("\n")
    
    def creative_writing_demo(self):
        """创意写作示例"""
        print("✍️ 创意写作示例")
        print("=" * 60)
        
        agent = self.create_agent("grok")
        
        creative_prompts = [
            "写一首关于程序员生活的现代诗",
            "创作一个关于AI与人类友谊的短篇科幻故事（200字以内）",
            "为一个科技初创公司写一段有趣的公司介绍"
        ]
        
        for i, prompt in enumerate(creative_prompts, 1):
            print(f"\n🎨 创意任务 {i}: {prompt}")
            print("-" * 40)
            agent.print_response(prompt)
            print("\n")
    
    def model_comparison_demo(self):
        """模型对比示例"""
        print("⚖️ 模型对比示例")
        print("=" * 60)
        
        test_prompt = "解释什么是区块链技术，用简单易懂的语言，不超过100字"
        
        print(f"\n🧪 测试提示: {test_prompt}")
        print("-" * 40)
        
        for model_name in self.models.keys():
            try:
                print(f"\n🤖 {model_name.upper()} 模型回答:")
                agent = self.create_agent(model_name)
                agent.print_response(test_prompt)
                time.sleep(1)  # 避免过于频繁的请求
            except Exception as e:
                print(f"❌ {model_name} 模型出错: {e}")
            
            print("-" * 30)
    
    def run_all_demos(self):
        """运行所有演示"""
        print("🚀 Agno + OpenRouter 综合演示")
        print("=" * 80)
        
        demos = [
            self.code_generation_demo,
            self.translation_demo, 
            self.data_analysis_demo,
            self.creative_writing_demo,
            self.model_comparison_demo
        ]
        
        for demo in demos:
            try:
                demo()
                print("\n" + "=" * 80 + "\n")
                time.sleep(2)  # 短暂暂停
            except Exception as e:
                print(f"❌ 演示出错: {e}")
                continue

def main():
    """主函数"""
    # 检查API密钥
    if not os.getenv("OPENROUTER_API_KEY"):
        print("⚠️  请设置 OPENROUTER_API_KEY 环境变量")
        print("   获取密钥: https://openrouter.ai/keys")
        print("   设置方法: export OPENROUTER_API_KEY=your_key")
        return
    
    demo = AgnoOpenRouterDemo()
    
    print("请选择演示模式:")
    print("1. 运行所有演示")
    print("2. 代码生成")
    print("3. 文档翻译")
    print("4. 数据分析")
    print("5. 创意写作")
    print("6. 模型对比")
    
    try:
        choice = input("\n请输入选择 (1-6): ").strip()
        
        if choice == "1":
            demo.run_all_demos()
        elif choice == "2":
            demo.code_generation_demo()
        elif choice == "3":
            demo.translation_demo()
        elif choice == "4":
            demo.data_analysis_demo()
        elif choice == "5":
            demo.creative_writing_demo()
        elif choice == "6":
            demo.model_comparison_demo()
        else:
            print("无效选择，运行所有演示...")
            demo.run_all_demos()
            
    except KeyboardInterrupt:
        print("\n\n👋 演示已停止")
    except Exception as e:
        print(f"❌ 运行出错: {e}")

if __name__ == "__main__":
    main()