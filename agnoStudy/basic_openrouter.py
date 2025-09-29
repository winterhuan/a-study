#!/usr/bin/env python3
"""
Basic Agno example using OpenRouter with free models

This example demonstrates how to use Agno with OpenRouter's free models.
You need to set your OPENROUTER_API_KEY environment variable.

Get your API key from: https://openrouter.ai/keys
"""
from agno.agent import Agent
from agno.run import RunOutput
from agno.models.openrouter import OpenRouter

def main():
    """Basic OpenRouter Agent example using free models."""
    
    # Common free models available on OpenRouter:
    # - "meta-llama/llama-3.1-8b-instruct:free" - Meta's Llama 3.1 8B
    # - "google/gemma-2-9b-it:free" - Google's Gemma 2 9B
    # - "microsoft/phi-3-mini-128k-instruct:free" - Microsoft's Phi-3 Mini
    # - "x-ai/grok-4-fast:free" - xAI's Grok-4 Fast
    # - "deepseek/deepseek-chat-v3.1:free" - DeepSeek Chat v3.1
    # - "deepseek/deepseek-r1:free" - DeepSeek R1 (reasoning model)
    # - "google/gemini-2.0-flash-exp:free" - Google's Gemini 2.0 Flash
    # - "qwen/qwen3-coder:free" - Qwen 3 Coder
    # - "openai/gpt-oss-120b:free" - OpenAI GPT OSS 120B
    
    # Create agent with OpenRouter using a free model
    agent = Agent(
        model=OpenRouter(
            id="deepseek/deepseek-r1:free",  # Using DeepSeek R1 (reasoning model, free)
            max_tokens=1024,
        ),
        markdown=True,
        description="An AI assistant using OpenRouter's free models"
    )
    
    print("🤖 Agno OpenRouter Free Model Example")
    print("=" * 50)
    print(f"Using model: {agent.model.id}")
    print(f"Provider: {agent.model.provider}")
    print("=" * 50)
    
    # Example 1: Simple response
    print("\n📝 Example 1: Simple Question")
    agent.print_response("What are the benefits of using free AI models?")
    
    print("\n" + "=" * 50)
    
    # Example 2: Get response as variable
    print("\n📝 Example 2: Programming Help")
    run: RunOutput = agent.run(
        "Write a simple Python function to calculate the factorial of a number."
    )
    print("Response received:")
    print(run.content)
    
    print("\n" + "=" * 50)
    
    # Example 3: Creative writing
    print("\n📝 Example 3: Creative Writing")
    agent.print_response("Write a haiku about artificial intelligence.")

def demo_multiple_models():
    """Demo showing different free models available."""
    
    free_models = [
        "deepseek/deepseek-r1:free",
        "x-ai/grok-4-fast:free",
        "google/gemini-2.0-flash-exp:free",
        "deepseek/deepseek-chat-v3.1:free",
        "qwen/qwen3-coder:free",
        "openai/gpt-oss-120b:free",
        "meta-llama/llama-3.1-8b-instruct:free",
    ]
    
    print("\n🔄 Testing Multiple Free Models")
    print("=" * 50)
    
    prompt = "Explain quantum computing in one sentence."
    
    for model_id in free_models:
        try:
            print(f"\n🤖 Model: {model_id}")
            agent = Agent(
                model=OpenRouter(id=model_id, max_tokens=100),
                markdown=True
            )
            agent.print_response(prompt)
        except Exception as e:
            print(f"❌ Error with {model_id}: {e}")
        print("-" * 30)

if __name__ == "__main__":
    import os
    
    # Check if API key is set
    if not os.getenv("OPENROUTER_API_KEY"):
        print("⚠️  Please set your OPENROUTER_API_KEY environment variable")
        print("   Get your key from: https://openrouter.ai/keys")
        print("   Run: export OPENROUTER_API_KEY=your_api_key_here")
        exit(1)
    
    try:
        main()
        
        # Uncomment to test multiple models
        # demo_multiple_models()
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("Make sure you have installed agno: pip install agno")
        print("And set your OPENROUTER_API_KEY environment variable")