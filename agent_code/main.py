"""
Project Observer - AI Agent Main Entry Point
AI 代理人主程序 - 負責連接 Minecraft、LLM 和記憶系統
"""

import os
import sys
import time
import json
import logging
from datetime import datetime
from pathlib import Path

from agent.bot_controller import BotController
from agent.llm_brain import LLMBrain
from agent.memory_manager import MemoryManager
from agent.skill_manager import SkillManager
from utils.logger import setup_logger

# 設置日誌
logger = setup_logger()


class AIAgent:
    """AI 代理人核心類"""
    
    def __init__(self):
        """初始化 AI 代理人"""
        logger.info("=" * 60)
        logger.info("🤖 Project Observer - AI Agent Starting...")
        logger.info("=" * 60)
        
        # 從環境變量讀取配置
        self.mc_host = os.getenv('MC_HOST', 'mc-server')
        self.mc_port = int(os.getenv('MC_PORT', '25565'))
        self.bot_username = os.getenv('BOT_USERNAME', 'Agent_001')
        
        # 初始化各個模組
        logger.info("📚 Initializing Memory Manager...")
        self.memory_manager = MemoryManager()
        
        logger.info("🧠 Initializing LLM Brain...")
        self.llm_brain = LLMBrain(self.memory_manager)
        
        logger.info("🎯 Initializing Skill Manager...")
        self.skill_manager = SkillManager(self.memory_manager)
        
        logger.info("🎮 Initializing Bot Controller...")
        self.bot_controller = BotController(
            host=self.mc_host,
            port=self.mc_port,
            username=self.bot_username
        )
        
        # 運行狀態
        self.is_running = False
        self.iteration_count = 0
        
    def start(self):
        """啟動 AI 代理人"""
        logger.info("🚀 Starting AI Agent...")
        self.is_running = True
        
        try:
            # 連接到 Minecraft 伺服器
            logger.info(f"🔌 Connecting to Minecraft server at {self.mc_host}:{self.mc_port}...")
            self.bot_controller.connect()
            
            # 等待機器人準備就緒
            time.sleep(3)
            
            # 測試通訊 - 發送一次測試命令清空 buffer
            logger.info("🧪 Testing bot.js communication...")
            test_obs = self.bot_controller.get_observation()
            if test_obs.get('position'):
                logger.info(f"✅ Bot connected successfully! Position: ({test_obs.get('position', {}).get('x', 0):.1f}, {test_obs.get('position', {}).get('y', 0):.1f}, {test_obs.get('position', {}).get('z', 0):.1f})")
            else:
                logger.warning("⚠️ Bot connected but position data incomplete")
            
            # 多給一點時間讓 bot.js 穩定
            time.sleep(3)
            
            # 開始主循環
            self.main_loop()
            
        except KeyboardInterrupt:
            logger.info("⚠️  Received interrupt signal, shutting down...")
            self.shutdown()
        except Exception as e:
            logger.error(f"❌ Fatal error: {e}", exc_info=True)
            self.shutdown()
    
    def main_loop(self):
        """
        主要循環 - The Evolution Loop
        
        這是讓 AI 持續進化的核心機制：
        1. Observe (觀察): 獲取遊戲狀態
        2. Think (思考): LLM 分析並制定計劃
        3. Act (行動): 生成並執行代碼
        4. Reflect (反思): 根據結果優化
        5. Learn (學習): 將成功的技能存入記憶
        """
        logger.info("🔄 Entering main evolution loop...")
        
        while self.is_running:
            try:
                self.iteration_count += 1
                logger.info(f"\n{'='*60}")
                logger.info(f"🔄 Iteration #{self.iteration_count}")
                logger.info(f"{'='*60}\n")
                
                # === 1. OBSERVE (觀察) ===
                logger.info("👁️  [OBSERVE] Gathering environment data...")
                observation = self.bot_controller.get_observation()
                self.log_observation(observation)
                
                # === 2. THINK (思考) ===
                logger.info("🧠 [THINK] Consulting LLM for decision...")
                decision = self.llm_brain.make_decision(observation)
                self.log_decision(decision)
                
                # === 3. ACT (行動) ===
                logger.info("⚡ [ACT] Executing action...")
                result = self.execute_action(decision)
                self.log_result(result)
                
                # === 4. REFLECT (反思) ===
                if not result['success']:
                    logger.warning("❌ [REFLECT] Action failed, analyzing...")
                    self.reflect_on_failure(decision, result)
                else:
                    logger.info("✅ [REFLECT] Action succeeded!")
                
                # === 5. LEARN (學習) ===
                if result['success'] and decision.get('is_new_skill'):
                    logger.info("💾 [LEARN] Saving new skill to memory...")
                    self.skill_manager.save_skill(decision, result)
                
                # 適當的循環延遲
                time.sleep(5)
                
            except Exception as e:
                logger.error(f"❌ Error in main loop: {e}", exc_info=True)
                time.sleep(10)  # 錯誤後等待更長時間
    
    def execute_action(self, decision: dict) -> dict:
        """執行 LLM 決策的行動"""
        action_type = decision.get('action_type')
        
        try:
            if action_type == 'execute_skill':
                # 執行已知技能
                skill_name = decision.get('skill_name')
                params = decision.get('parameters', {})
                result = self.skill_manager.execute_skill(skill_name, params, self.bot_controller)
                
            elif action_type == 'generate_code':
                # 執行新生成的代碼
                code = decision.get('code')
                result = self.bot_controller.execute_code(code)
                
            elif action_type == 'wait':
                # 等待或觀察
                result = {'success': True, 'message': 'Waiting and observing'}
                
            else:
                result = {'success': False, 'error': f'Unknown action type: {action_type}'}
            
            # 確保結果包含 success 字段
            if 'success' not in result:
                return {'success': False, 'error': result.get('error', 'Unknown error')}
            
            return result
            
        except Exception as e:
            logger.error(f"Error executing action: {e}")
            return {'success': False, 'error': str(e)}
    
    def reflect_on_failure(self, decision: dict, result: dict):
        """失敗後的反思與改進"""
        error_context = {
            'decision': decision,
            'result': result,
            'iteration': self.iteration_count,
            'timestamp': datetime.now().isoformat()
        }
        
        # 讓 LLM 分析失敗原因並提出改進方案
        improvement = self.llm_brain.analyze_failure(error_context)
        logger.info(f"💡 [IMPROVEMENT] {improvement}")
        
        # 將失敗案例存入記憶，避免重蹈覆轍
        self.memory_manager.store_failure(error_context, improvement)
    
    def log_observation(self, obs: dict):
        """記錄觀察結果"""
        logger.info(f"  位置: ({obs.get('position', {}).get('x', 0):.1f}, "
                   f"{obs.get('position', {}).get('y', 0):.1f}, "
                   f"{obs.get('position', {}).get('z', 0):.1f})")
        logger.info(f"  生命值: {obs.get('health', 0)}/20")
        logger.info(f"  飢餓值: {obs.get('food', 0)}/20")
        logger.info(f"  附近實體: {len(obs.get('nearby_entities', []))} 個")
        logger.info(f"  附近方塊: {len(obs.get('nearby_blocks', []))} 個")
    
    def log_decision(self, decision: dict):
        """記錄決策"""
        # LLM Brain 已經記錄了決策，這裡只記錄詳情
        logger.info(f"  行動類型: {decision.get('action_type', 'None')}")
        if decision.get('reasoning'):
            logger.info(f"  思考過程: {decision.get('reasoning')}")
    
    def log_result(self, result: dict):
        """記錄執行結果"""
        if result.get('success'):
            logger.info(f"  結果: ✅ {result.get('message', 'Success')}")
        else:
            logger.error(f"  結果: ❌ {result.get('error', 'Unknown error')}")
    
    def shutdown(self):
        """關閉 AI 代理人"""
        logger.info("🛑 Shutting down AI Agent...")
        self.is_running = False
        
        if self.bot_controller:
            self.bot_controller.disconnect()
        
        logger.info("👋 AI Agent stopped. Goodbye!")
        sys.exit(0)


def main():
    """主函數"""
    # 確保必要的目錄存在
    Path('/app/skills').mkdir(exist_ok=True)
    Path('/app/logs').mkdir(exist_ok=True)
    Path('/app/memory').mkdir(exist_ok=True)
    
    # 創建並啟動 AI 代理人
    agent = AIAgent()
    agent.start()


if __name__ == "__main__":
    main()
