#!/bin/bash

# Agno v2.0.9 项目安装脚本

echo "🚀 开始安装 Agno v2.0.9 OpenRouter 示例项目"
echo "=" * 60

# 检查 Python 版本
echo "🔍 检查 Python 环境..."
python3 --version

# 创建虚拟环境
echo "📦 创建虚拟环境..."
python3 -m venv .venv

# 激活虚拟环境
echo "⚡️ 激活虚拟环境..."
source .venv/bin/activate

# 安装依赖
echo "📥 安装依赖包..."
pip install --upgrade pip
pip install -r requirements.txt

# 验证安装
echo "🔍 验证安装..."
python test_version.py

echo ""
echo "🎉 安装完成！"
echo ""
echo "📋 使用说明："
echo "1. 激活虚拟环境: source .venv/bin/activate"
echo "2. 设置 API 密钥: export OPENROUTER_API_KEY=your_key"
echo "3. 运行示例: python simple_example.py"
echo ""
echo "📚 更多示例："
echo "- python basic_openrouter.py"
echo "- python advanced_example.py" 
echo "- python new_models_showcase.py"
echo ""
echo "🔗 获取 API 密钥: https://openrouter.ai/keys"