#!/usr/bin/env python3
"""
實時統計覆蓋層生成器
用於 OBS 直播顯示 AI 學習統計
"""

import json
import time
from pathlib import Path
from datetime import datetime, timedelta

START_TIME = datetime.now()

def get_uptime():
    """計算系統運行時間"""
    elapsed = datetime.now() - START_TIME
    hours = elapsed.seconds // 3600
    minutes = (elapsed.seconds % 3600) // 60
    return f"{hours}h {minutes}m"

def get_current_goal():
    """從日誌中提取當前目標"""
    try:
        log_dir = Path('agent_logs')
        if not log_dir.exists():
            return "等待 AI 啟動..."
        
        log_files = sorted(log_dir.glob('*.log'))
        if not log_files:
            return "等待 AI 啟動..."
        
        latest_log = log_files[-1]
        with open(latest_log, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            for line in reversed(lines):
                if 'Goal:' in line or '目標:' in line:
                    # 提取目標文本
                    goal = line.split('Goal:')[-1].split('目標:')[-1].strip()
                    return goal[:50]  # 限制長度
        
        return "探索中..."
    except Exception as e:
        return f"讀取失敗: {str(e)}"

def calculate_stats():
    """計算詳細統計數據"""
    skills_dir = Path('agent_skills')
    
    stats = {
        'total_skills': 0,
        'success_count': 0,
        'failure_count': 0,
        'success_rate': 0.0,
        'top_skills': [],
        'recent_skill': None
    }
    
    if not skills_dir.exists():
        return stats
    
    skills = list(skills_dir.glob('*.json'))
    stats['total_skills'] = len(skills)
    
    skill_data = []
    for skill_file in skills:
        try:
            with open(skill_file, 'r', encoding='utf-8') as f:
                skill = json.load(f)
                success = skill.get('success_count', 0)
                failure = skill.get('failure_count', 0)
                
                stats['success_count'] += success
                stats['failure_count'] += failure
                
                skill_data.append({
                    'name': skill.get('name', 'Unknown'),
                    'success': success,
                    'total': success + failure
                })
        except Exception:
            continue
    
    # 計算成功率
    total = stats['success_count'] + stats['failure_count']
    if total > 0:
        stats['success_rate'] = (stats['success_count'] / total * 100)
    
    # 取前 3 個最常用技能
    skill_data.sort(key=lambda x: x['total'], reverse=True)
    stats['top_skills'] = skill_data[:3]
    
    # 最新學會的技能
    if skills:
        latest_skill = max(skills, key=lambda p: p.stat().st_mtime)
        try:
            with open(latest_skill, 'r', encoding='utf-8') as f:
                skill = json.load(f)
                stats['recent_skill'] = skill.get('name', 'Unknown')
        except Exception:
            pass
    
    return stats

def generate_html(stats):
    """生成 HTML 統計頁面"""
    current_goal = get_current_goal()
    uptime = get_uptime()
    
    # 生成頂尖技能列表
    top_skills_html = ""
    for i, skill in enumerate(stats['top_skills'], 1):
        top_skills_html += f"""
        <div class="skill-item">
            <span class="skill-rank">#{i}</span>
            <span class="skill-name">{skill['name']}</span>
            <span class="skill-usage">×{skill['total']}</span>
        </div>
        """
    
    if not top_skills_html:
        top_skills_html = '<div class="skill-item">尚未學會技能</div>'
    
    html = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta http-equiv="refresh" content="3">
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            background: transparent;
            color: #ffffff;
            font-family: 'Segoe UI', 'Microsoft JhengHei', sans-serif;
            padding: 20px;
            font-size: 18px;
        }}
        
        .container {{
            display: flex;
            flex-direction: column;
            gap: 15px;
        }}
        
        .stat-card {{
            background: linear-gradient(135deg, rgba(0, 0, 0, 0.85), rgba(20, 20, 20, 0.85));
            padding: 15px 20px;
            border-radius: 12px;
            border-left: 4px solid #00ff88;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.5);
            backdrop-filter: blur(10px);
            animation: slideIn 0.5s ease-out;
        }}
        
        @keyframes slideIn {{
            from {{
                opacity: 0;
                transform: translateX(-20px);
            }}
            to {{
                opacity: 1;
                transform: translateX(0);
            }}
        }}
        
        .stat-label {{
            font-size: 14px;
            color: #aaaaaa;
            margin-bottom: 5px;
        }}
        
        .stat-value {{
            font-size: 28px;
            font-weight: bold;
            color: #00ff88;
            text-shadow: 0 0 10px rgba(0, 255, 136, 0.5);
        }}
        
        .goal-text {{
            font-size: 16px;
            color: #ffffff;
            line-height: 1.4;
        }}
        
        .skill-item {{
            display: flex;
            align-items: center;
            gap: 10px;
            padding: 8px 0;
            border-bottom: 1px solid rgba(255, 255, 255, 0.1);
        }}
        
        .skill-item:last-child {{
            border-bottom: none;
        }}
        
        .skill-rank {{
            font-size: 20px;
            font-weight: bold;
            color: #ffd700;
            width: 40px;
        }}
        
        .skill-name {{
            flex: 1;
            color: #ffffff;
        }}
        
        .skill-usage {{
            color: #00ff88;
            font-size: 14px;
        }}
        
        .progress-bar {{
            width: 100%;
            height: 8px;
            background: rgba(255, 255, 255, 0.1);
            border-radius: 4px;
            overflow: hidden;
            margin-top: 5px;
        }}
        
        .progress-fill {{
            height: 100%;
            background: linear-gradient(90deg, #00ff88, #00d4ff);
            border-radius: 4px;
            transition: width 0.3s ease;
            box-shadow: 0 0 10px rgba(0, 255, 136, 0.5);
        }}
        
        .badge {{
            display: inline-block;
            padding: 4px 12px;
            border-radius: 12px;
            font-size: 12px;
            font-weight: bold;
            margin-left: 10px;
        }}
        
        .badge-success {{
            background: rgba(0, 255, 136, 0.2);
            color: #00ff88;
        }}
        
        .badge-new {{
            background: rgba(255, 215, 0, 0.2);
            color: #ffd700;
            animation: pulse 2s infinite;
        }}
        
        @keyframes pulse {{
            0%, 100% {{ opacity: 1; }}
            50% {{ opacity: 0.5; }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <!-- 當前目標 -->
        <div class="stat-card">
            <div class="stat-label">🎯 當前目標</div>
            <div class="goal-text">{current_goal}</div>
        </div>
        
        <!-- 統計數據 -->
        <div class="stat-card">
            <div class="stat-label">📚 已學會技能</div>
            <div class="stat-value">{stats['total_skills']}</div>
            {f'<span class="badge badge-new">+1 新技能: {stats["recent_skill"]}</span>' if stats.get('recent_skill') else ''}
        </div>
        
        <div class="stat-card">
            <div class="stat-label">✅ 成功率</div>
            <div class="stat-value">{stats['success_rate']:.1f}%</div>
            <div class="progress-bar">
                <div class="progress-fill" style="width: {stats['success_rate']}%"></div>
            </div>
            <div style="margin-top: 8px; font-size: 14px; color: #aaa;">
                成功 {stats['success_count']} 次 / 失敗 {stats['failure_count']} 次
            </div>
        </div>
        
        <div class="stat-card">
            <div class="stat-label">⏱️ 運行時間</div>
            <div class="stat-value">{uptime}</div>
        </div>
        
        <!-- 熱門技能 -->
        <div class="stat-card">
            <div class="stat-label">🔥 熱門技能</div>
            {top_skills_html}
        </div>
    </div>
</body>
</html>
    """
    
    return html

def main():
    """主循環"""
    print("🎬 統計覆蓋層生成器已啟動")
    print("📊 生成文件: stats_overlay.html")
    print("💡 在 OBS 中添加「瀏覽器」來源，指向此文件")
    print("按 Ctrl+C 停止\n")
    
    try:
        while True:
            stats = calculate_stats()
            html = generate_html(stats)
            
            with open('stats_overlay.html', 'w', encoding='utf-8') as f:
                f.write(html)
            
            print(f"✅ 更新 [{datetime.now().strftime('%H:%M:%S')}] "
                  f"技能: {stats['total_skills']} | "
                  f"成功率: {stats['success_rate']:.1f}%")
            
            time.sleep(3)
    
    except KeyboardInterrupt:
        print("\n👋 統計覆蓋層生成器已停止")

if __name__ == '__main__':
    main()
