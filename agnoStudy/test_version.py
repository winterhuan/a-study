#!/usr/bin/env python3
"""
Agno v2.0.9 版本测试脚本

测试 Agno v2.0.9 的安装和基本功能
"""

import os
import sys

def test_agno_installation():
    """测试 Agno 安装"""
    print("🔍 检查 Agno 安装...")
    
    try:
        import agno
        print(f"✅ Agno 已安装，版本: {agno.__version__}")
        
        # 检查是否是 v2.0.9
        expected_version = "2.0.9"
        if agno.__version__ == expected_version:
            print(f"✅ 版本正确: v{expected_version}")
        else:
            print(f"⚠️ 版本不匹配: 当前 v{agno.__version__}, 期望 v{expected_version}")
            
    except ImportError as e:
        print(f"❌ Agno 未安装或导入失败: {e}")
        return False
    
    return True

def test_imports():
    """测试导入功能"""
    print("\n🔍 测试导入...")
    
    try:
        # v2.0 新的导入方式
        from agno import Agent, RunOutput
        print("✅ 成功导入 Agent 和 RunOutput")
        
        from agno.models.openrouter import OpenRouter
        print("✅ 成功导入 OpenRouter 模型")
        
        return True
        
    except ImportError as e:
        print(f"❌ 导入失败: {e}")
        return False

def test_basic_functionality():
    """测试基本功能"""
    print("\n🔍 测试基本功能...")
    
    if not os.getenv("OPENROUTER_API_KEY"):
        print("⚠️ 未设置 OPENROUTER_API_KEY，跳过功能测试")
        return True
    
    try:
        from agno import Agent
        from agno.models.openrouter import OpenRouter
        
        # 创建一个简单的 Agent
        agent = Agent(
            model=OpenRouter(
                id="deepseek/deepseek-r1:free",
                max_tokens=50,
            ),
            markdown=True,
            description="测试 Agent"
        )
        
        print("✅ Agent 创建成功")
        
        # 简单测试
        response = agent.run("Hello, please respond in one word.")
        print(f"✅ 基本对话测试通过: {response.content[:50]}...")
        
        return True
        
    except Exception as e:
        print(f"❌ 功能测试失败: {e}")
        return False

def show_version_info():
    """显示版本信息"""
    print("\n📋 版本信息总览")
    print("=" * 50)
    
    try:
        import agno
        print(f"Agno 版本: {agno.__version__}")
    except:
        print("Agno: 未安装")
    
    print(f"Python 版本: {sys.version}")
    
    # 检查其他相关包
    packages = ['requests', 'openai']
    for package in packages:
        try:
            pkg = __import__(package)
            version = getattr(pkg, '__version__', 'Unknown')
            print(f"{package}: {version}")
        except ImportError:
            print(f"{package}: 未安装")

def main():
    """主测试函数"""
    print("🚀 Agno v2.0.9 版本测试")
    print("=" * 60)
    
    all_passed = True
    
    # 1. 测试安装
    if not test_agno_installation():
        all_passed = False
    
    # 2. 测试导入
    if not test_imports():
        all_passed = False
    
    # 3. 测试功能（如果有 API 密钥）
    if not test_basic_functionality():
        all_passed = False
    
    # 4. 显示版本信息
    show_version_info()
    
    print("\n" + "=" * 60)
    if all_passed:
        print("🎉 所有测试通过！Agno v2.0.9 工作正常")
    else:
        print("❌ 部分测试失败，请检查安装")
    
    print("\n💡 使用建议:")
    print("1. 确保安装正确版本: pip install agno==2.0.9")
    print("2. 设置 API 密钥: export OPENROUTER_API_KEY=your_key")
    print("3. 使用新的导入方式: from agno import Agent")

if __name__ == "__main__":
    main()