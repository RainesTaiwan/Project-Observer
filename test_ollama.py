#!/usr/bin/env python3
"""測試 Ollama 連接"""
import os
import sys
import requests
from openai import OpenAI

print("=== Ollama 連接測試 ===\n")

# 環境變數
api_base = os.getenv('OPENAI_API_BASE', 'http://172.18.0.1:11434/v1')
api_key = os.getenv('OPENAI_API_KEY', 'ollama')
model = os.getenv('LLM_MODEL', 'llama3.2:3b')

print(f"配置:")
print(f"  API Base: {api_base}")
print(f"  Model: {model}")
print(f"  API Key: {api_key}")
print()

# 測試 1: 原始 HTTP 請求
print("測試 1: 直接 HTTP 請求...")
try:
    url = api_base.replace('/v1', '/api/version')
    resp = requests.get(url, timeout=5)
    print(f"  ✅ HTTP 連接成功！版本: {resp.json()}")
except Exception as e:
    print(f"  ❌ HTTP 連接失敗: {e}")
    sys.exit(1)

# 測試 2: OpenAI SDK
print("\n測試 2: OpenAI SDK...")
try:
    client = OpenAI(base_url=api_base, api_key=api_key)
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": "Say 'test'"}],
        max_tokens=5,
        temperature=0.1
    )
    print(f"  ✅ OpenAI SDK 成功！回應: {response.choices[0].message.content}")
except Exception as e:
    print(f"  ❌ OpenAI SDK 失敗: {type(e).__name__}: {e}")
    sys.exit(1)

print("\n✅ 所有測試通過！")
