"""
Project Observer - Dashboard
AI 觀測儀表板 - 實時顯示 AI 的思維過程和學習進度
"""

import streamlit as st
import json
import os
from pathlib import Path
from datetime import datetime
import time
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# 頁面配置
st.set_page_config(
    page_title="Project Observer - AI Dashboard",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 自定義 CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        padding: 1rem;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .status-card {
        padding: 1.5rem;
        border-radius: 0.5rem;
        background-color: #f0f2f6;
        margin: 1rem 0;
    }
    .log-entry {
        padding: 0.5rem;
        margin: 0.2rem 0;
        border-left: 3px solid #667eea;
        background-color: #f8f9fa;
    }
</style>
""", unsafe_allow_html=True)


class Dashboard:
    """儀表板主類"""
    
    def __init__(self):
        self.logs_dir = Path(os.getenv('LOG_SOURCE', '/app/logs'))
        self.skills_dir = Path('/app/skills')
        self.memory_dir = Path('/app/memory')
    
    def get_latest_log_file(self):
        """獲取最新的日誌文件"""
        try:
            log_files = sorted(self.logs_dir.glob('agent_*.log'))
            if log_files:
                return log_files[-1]
        except:
            pass
        return None
    
    def read_recent_logs(self, num_lines=50):
        """讀取最近的日誌"""
        log_file = self.get_latest_log_file()
        if not log_file or not log_file.exists():
            return []
        
        try:
            with open(log_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                return lines[-num_lines:]
        except:
            return []
    
    def get_skills_list(self):
        """獲取技能列表"""
        skills = []
        
        try:
            if self.skills_dir.exists():
                for skill_file in self.skills_dir.glob('*.json'):
                    with open(skill_file, 'r', encoding='utf-8') as f:
                        skill = json.load(f)
                        skills.append(skill)
        except:
            pass
        
        return skills
    
    def parse_log_entry(self, line):
        """解析日誌條目"""
        try:
            parts = line.split('|')
            if len(parts) >= 3:
                return {
                    'time': parts[0].strip(),
                    'level': parts[1].strip(),
                    'message': parts[2].strip()
                }
        except:
            pass
        return None


def main():
    """主函數"""
    dashboard = Dashboard()
    
    # === 標題 ===
    st.markdown('<h1 class="main-header">🤖 Project Observer</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; font-size: 1.2rem; color: #666;">觀察 AI 在 Minecraft 世界中學習與進化</p>', unsafe_allow_html=True)
    
    # === 側邊欄 ===
    with st.sidebar:
        st.image("https://via.placeholder.com/300x150/667eea/ffffff?text=Project+Observer", use_container_width=True)
        st.markdown("---")
        
        st.subheader("⚙️ 設置")
        auto_refresh = st.checkbox("自動刷新", value=True)
        refresh_interval = st.slider("刷新間隔 (秒)", 1, 10, 3)
        log_lines = st.slider("顯示日誌行數", 10, 100, 30)
        
        st.markdown("---")
        st.subheader("📊 系統信息")
        
        # 獲取技能數量
        skills = dashboard.get_skills_list()
        st.metric("已學會技能", len(skills))
        
        # 獲取日誌文件
        log_file = dashboard.get_latest_log_file()
        if log_file:
            st.info(f"📝 當前日誌:\n{log_file.name}")
        else:
            st.warning("⚠️ 未找到日誌文件")
    
    # === 主要內容區域 ===
    tab1, tab2, tab3, tab4 = st.tabs(["🔴 實時日誌", "🧠 AI 思維", "🎯 技能樹", "📈 統計分析"])
    
    # --- Tab 1: 實時日誌 ---
    with tab1:
        st.subheader("🔴 實時活動日誌")
        
        log_container = st.container()
        
        with log_container:
            logs = dashboard.read_recent_logs(log_lines)
            
            if logs:
                # 反向顯示（最新的在上面）
                for line in reversed(logs):
                    entry = dashboard.parse_log_entry(line)
                    if entry:
                        level = entry['level']
                        color = {
                            'INFO': '🟢',
                            'WARNING': '🟡',
                            'ERROR': '🔴',
                            'DEBUG': '🔵'
                        }.get(level, '⚪')
                        
                        st.markdown(f"""
                        <div class="log-entry">
                            {color} <strong>{entry['time']}</strong> | {entry['message']}
                        </div>
                        """, unsafe_allow_html=True)
            else:
                st.info("📭 暫無日誌數據。請確保 AI Agent 正在運行。")
    
    # --- Tab 2: AI 思維 ---
    with tab2:
        st.subheader("🧠 AI 當前思維狀態")
        
        # 從日誌中提取最新狀態
        logs = dashboard.read_recent_logs(100)
        
        position = "未知"
        health = "N/A"
        food = "N/A"
        current_goal = "觀察中..."
        thinking = "等待 AI 思考..."
        
        for line in reversed(logs):
            if "位置:" in line:
                try:
                    position = line.split("位置:")[1].strip()
                except:
                    pass
            if "生命值:" in line:
                try:
                    health = line.split("生命值:")[1].strip()
                except:
                    pass
            if "飢餓值:" in line:
                try:
                    food = line.split("飢餓值:")[1].strip()
                except:
                    pass
            if "💭 LLM Decision:" in line:
                try:
                    current_goal = line.split("💭 LLM Decision:")[1].strip()
                except:
                    pass
            if "思考過程:" in line:
                try:
                    thinking = line.split("思考過程:")[1].strip()
                except:
                    pass
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 📍 當前狀態")
            st.markdown(f"""
            <div class="status-card">
                <p><strong>位置:</strong> {position}</p>
                <p><strong>生命值:</strong> {health} ❤️</p>
                <p><strong>飢餓值:</strong> {food} 🍖</p>
                <p><strong>當前目標:</strong> {current_goal}</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("### 💭 內心獨白")
            st.markdown(f"""
            <div class="status-card">
                <p><em>"{thinking}"</em></p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("### 📝 最近決策")
        
        decisions = []
        for line in reversed(logs):
            if "💭 LLM Decision:" in line:
                decisions.append(line)
                if len(decisions) >= 5:
                    break
        
        if decisions:
            for decision in decisions:
                st.markdown(f"- {decision.strip()}")
        else:
            st.info("暫無決策記錄")
    
    # --- Tab 3: 技能樹 ---
    with tab3:
        st.subheader("🎯 AI 技能樹")
        
        skills = dashboard.get_skills_list()
        
        if skills:
            # 按成功率排序
            skills_sorted = sorted(skills, key=lambda x: x.get('success_count', 0), reverse=True)
            
            for skill in skills_sorted:
                success_count = skill.get('success_count', 0)
                failure_count = skill.get('failure_count', 0)
                total = success_count + failure_count
                success_rate = (success_count / total * 100) if total > 0 else 0
                
                with st.expander(f"🎓 {skill['name']} (成功率: {success_rate:.1f}%)"):
                    col1, col2 = st.columns([2, 1])
                    
                    with col1:
                        st.markdown(f"**目標:** {skill.get('goal', 'N/A')}")
                        st.markdown(f"**描述:** {skill.get('description', 'N/A')}")
                        st.code(skill.get('code', '// No code'), language='javascript')
                    
                    with col2:
                        st.metric("成功次數", success_count)
                        st.metric("失敗次數", failure_count)
                        st.caption(f"創建於: {skill.get('created_at', 'Unknown')}")
        else:
            st.info("🌱 AI 還沒有學會任何技能。耐心等待它的第一次成功！")
    
    # --- Tab 4: 統計分析 ---
    with tab4:
        st.subheader("📈 學習進度統計")
        
        # 從日誌計算真實統計
        logs = dashboard.read_recent_logs(1000)
        
        iteration_count = 0
        success_count = 0
        failure_count = 0
        
        for line in logs:
            if "Iteration #" in line:
                iteration_count += 1
            if "✅ [REFLECT] Action succeeded!" in line:
                success_count += 1
            if "❌" in line or "ERROR" in line:
                failure_count += 1
        
        total_actions = success_count + failure_count
        success_rate = (success_count / total_actions * 100) if total_actions > 0 else 0
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("總迭代次數", iteration_count)
            st.metric("學會技能數", len(skills))
        
        with col2:
            st.metric("成功行動數", success_count)
            st.metric("失敗行動數", failure_count)
        
        with col3:
            st.metric("成功率", f"{success_rate:.1f}%")
            
            # 計算記憶條目
            memory_count = 0
            try:
                if dashboard.memory_dir.exists():
                    memory_files = list(dashboard.memory_dir.glob('*.json'))
                    memory_count = len(memory_files)
            except:
                pass
            st.metric("記憶條目數", memory_count)
        
        st.markdown("---")
        
        # 技能分佈
        if skills:
            st.markdown("### 🎯 技能使用頻率")
            
            skill_names = [s['name'] for s in skills]
            skill_counts = [s.get('success_count', 0) for s in skills]
            
            if sum(skill_counts) > 0:
                fig = px.pie(
                    names=skill_names,
                    values=skill_counts,
                    title='各技能使用次數分佈'
                )
                st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("🌱 AI 正在學習中，尚未掌握技能...")
    
    # === 自動刷新 ===
    if auto_refresh:
        time.sleep(refresh_interval)
        st.rerun()


if __name__ == "__main__":
    main()
