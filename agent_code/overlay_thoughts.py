#!/usr/bin/env python3
"""
AI 思維字幕生成器
實時提取並顯示 AI 的決策思維
"""

import re
import time
from pathlib import Path
from datetime import datetime

def extract_latest_thought():
    """從日誌中提取最新的 AI 思維"""
    try:
        log_dir = Path('agent_logs')
        if not log_dir.exists():
            return {
                'type': 'status',
                'text': '⏳ 等待 AI 啟動...'
            }
        
        log_files = sorted(log_dir.glob('*.log'))
        if not log_files:
            return {
                'type': 'status',
                'text': '⏳ 等待 AI 啟動...'
            }
        
        latest_log = log_files[-1]
        
        with open(latest_log, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()
        
        # 從最後開始往前找最有價值的信息
        for line in reversed(lines):
            line = line.strip()
            
            # AI 決策
            if 'AI Decision' in line or '決策' in line:
                match = re.search(r'Decision[:\s]+(.+)', line, re.IGNORECASE)
                if match:
                    return {
                        'type': 'decision',
                        'text': f'💡 決策: {match.group(1)}'
                    }
            
            # 思考過程
            if 'Thinking' in line or '思考' in line:
                match = re.search(r'Thinking[:\s]+(.+)', line, re.IGNORECASE)
                if match:
                    return {
                        'type': 'thinking',
                        'text': f'🤔 思考: {match.group(1)}'
                    }
            
            # 執行動作
            if 'Executing' in line or '執行' in line:
                match = re.search(r'Executing[:\s]+(.+)', line, re.IGNORECASE)
                if match:
                    return {
                        'type': 'action',
                        'text': f'⚡ 執行: {match.group(1)}'
                    }
            
            # 目標設定
            if 'Goal' in line or '目標' in line:
                match = re.search(r'Goal[:\s]+(.+)', line, re.IGNORECASE)
                if match:
                    return {
                        'type': 'goal',
                        'text': f'🎯 目標: {match.group(1)}'
                    }
            
            # 觀察環境
            if 'Observing' in line or '觀察' in line:
                match = re.search(r'Observing[:\s]+(.+)', line, re.IGNORECASE)
                if match:
                    return {
                        'type': 'observe',
                        'text': f'👁️ 觀察: {match.group(1)}'
                    }
            
            # 學習反思
            if 'Learning' in line or 'Learned' in line or '學習' in line:
                match = re.search(r'Learn(?:ing|ed)[:\s]+(.+)', line, re.IGNORECASE)
                if match:
                    return {
                        'type': 'learning',
                        'text': f'📚 學習: {match.group(1)}'
                    }
            
            # 錯誤信息
            if 'ERROR' in line or 'Error' in line:
                match = re.search(r'(?:ERROR|Error)[:\s]+(.+)', line)
                if match:
                    return {
                        'type': 'error',
                        'text': f'⚠️ 錯誤: {match.group(1)[:80]}'
                    }
        
        return {
            'type': 'idle',
            'text': '😴 AI 思考中...'
        }
    
    except Exception as e:
        return {
            'type': 'error',
            'text': f'❌ 讀取錯誤: {str(e)}'
        }

def write_text_file(thought):
    """寫入純文字檔（OBS 文字源）"""
    with open('current_thought.txt', 'w', encoding='utf-8') as f:
        f.write(thought['text'])

def write_html_file(thought):
    """寫入 HTML 檔（OBS 瀏覽器源，更漂亮）"""
    
    # 根據類型選擇顏色
    color_map = {
        'decision': '#00ff88',
        'thinking': '#ffaa00',
        'action': '#00d4ff',
        'goal': '#ff00ff',
        'observe': '#88ff00',
        'learning': '#ffd700',
        'error': '#ff4444',
        'status': '#aaaaaa',
        'idle': '#888888'
    }
    
    color = color_map.get(thought['type'], '#ffffff')
    
    html = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta http-equiv="refresh" content="2">
    <style>
        * {{
            margin: 0;
            padding: 0;
        }}
        
        body {{
            background: transparent;
            display: flex;
            align-items: center;
            justify-content: center;
            height: 100vh;
            font-family: 'Segoe UI', 'Microsoft JhengHei', sans-serif;
        }}
        
        .thought-container {{
            background: linear-gradient(135deg, rgba(0, 0, 0, 0.9), rgba(20, 20, 20, 0.9));
            padding: 20px 40px;
            border-radius: 15px;
            border: 2px solid {color};
            box-shadow: 
                0 0 20px rgba(0, 0, 0, 0.8),
                0 0 40px {color}44;
            backdrop-filter: blur(10px);
            max-width: 1200px;
            animation: slideUp 0.5s ease-out;
        }}
        
        @keyframes slideUp {{
            from {{
                opacity: 0;
                transform: translateY(20px);
            }}
            to {{
                opacity: 1;
                transform: translateY(0);
            }}
        }}
        
        .thought-text {{
            color: {color};
            font-size: 28px;
            font-weight: bold;
            text-shadow: 
                0 0 10px {color}88,
                0 2px 4px rgba(0, 0, 0, 0.8);
            line-height: 1.4;
        }}
        
        @keyframes pulse {{
            0%, 100% {{ 
                box-shadow: 
                    0 0 20px rgba(0, 0, 0, 0.8),
                    0 0 40px {color}44;
            }}
            50% {{ 
                box-shadow: 
                    0 0 20px rgba(0, 0, 0, 0.8),
                    0 0 60px {color}88;
            }}
        }}
        
        .thought-container {{
            animation: slideUp 0.5s ease-out, pulse 2s infinite;
        }}
    </style>
</head>
<body>
    <div class="thought-container">
        <div class="thought-text">{thought['text']}</div>
    </div>
</body>
</html>
    """
    
    with open('thought_overlay.html', 'w', encoding='utf-8') as f:
        f.write(html)

def main():
    """主循環"""
    print("💭 AI 思維字幕生成器已啟動")
    print("📝 生成文件:")
    print("   - current_thought.txt (純文字)")
    print("   - thought_overlay.html (HTML 動畫)")
    print("\n💡 在 OBS 中添加:")
    print("   文字源 → 從檔案讀取 → current_thought.txt")
    print("   或")
    print("   瀏覽器源 → 本機檔案 → thought_overlay.html")
    print("\n按 Ctrl+C 停止\n")
    
    last_text = ""
    
    try:
        while True:
            thought = extract_latest_thought()
            
            # 只在內容改變時更新和輸出
            if thought['text'] != last_text:
                write_text_file(thought)
                write_html_file(thought)
                
                timestamp = datetime.now().strftime('%H:%M:%S')
                print(f"[{timestamp}] {thought['text']}")
                
                last_text = thought['text']
            
            time.sleep(2)
    
    except KeyboardInterrupt:
        print("\n👋 AI 思維字幕生成器已停止")

if __name__ == '__main__':
    main()
