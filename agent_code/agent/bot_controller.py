"""
Bot Controller - 負責與 Minecraft 遊戲互動的控制器
通過 Node.js bridge 調用 Mineflayer API
"""

import json
import subprocess
import os
import logging
import uuid
from typing import Dict, List, Any

logger = logging.getLogger(__name__)


class BotController:
    """Minecraft 機器人控制器"""
    
    def __init__(self, host: str, port: int, username: str):
        self.host = host
        self.port = port
        self.username = username
        self.bot_process = None
        self.is_connected = False
        
    def connect(self):
        """連接到 Minecraft 伺服器"""
        try:
            # 啟動 Node.js bot 進程
            bot_script = os.path.join(os.path.dirname(__file__), '../bot.js')
            
            env = os.environ.copy()
            env['MC_HOST'] = self.host
            env['MC_PORT'] = str(self.port)
            env['BOT_USERNAME'] = self.username
            
            self.bot_process = subprocess.Popen(
                ['node', bot_script],
                env=env,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=None,  # 讓 stderr 直接輸出到 Docker logs
                text=True,
                bufsize=1
            )
            
            # 等待 bot.js 發送 ready 信號
            logger.info("⏳ Waiting for bot.js to be ready...")
            ready_signal = self.bot_process.stdout.readline()
            logger.info(f"📨 Received: {ready_signal.strip()}")
            
            self.is_connected = True
            logger.info(f"✅ Bot connected as {self.username}")
            
        except Exception as e:
            logger.error(f"Failed to connect bot: {e}")
            raise
    
    def get_observation(self) -> Dict[str, Any]:
        """
        獲取當前遊戲狀態觀察
        
        Returns:
            包含位置、生命值、背包、周圍實體等信息的字典
        """
        try:
            # 向 bot.js 發送獲取狀態的命令
            request_id = str(uuid.uuid4())
            command = json.dumps({'action': 'get_state', 'id': request_id}) + '\n'
            self.bot_process.stdin.write(command)
            self.bot_process.stdin.flush()
            
            # 讀取響應並驗證 ID
            response = self.bot_process.stdout.readline()
            state = json.loads(response)
            
            # 驗證響應 ID
            if state.get('id') != request_id:
                logger.warning(f"Response ID mismatch: expected {request_id}, got {state.get('id')}")
                return self._default_observation()
            
            return {
                'position': state.get('position', {}),
                'health': state.get('health', 20),
                'food': state.get('food', 20),
                'inventory': state.get('inventory', []),
                'nearby_entities': state.get('nearby_entities', []),
                'nearby_blocks': state.get('nearby_blocks', []),
                'time_of_day': state.get('time_of_day', 'day'),
                'weather': state.get('weather', 'clear'),
                'biome': state.get('biome', 'unknown')
            }
            
        except Exception as e:
            logger.error(f"Failed to get observation: {e}")
            return self._default_observation()
    
    def execute_code(self, code: str) -> Dict[str, Any]:
        """
        執行動態生成的 JavaScript 代碼
        
        Args:
            code: JavaScript 代碼字符串
            
        Returns:
            執行結果字典
        """
        try:
            request_id = str(uuid.uuid4())
            command = json.dumps({
                'action': 'execute_code',
                'code': code,
                'id': request_id
            }) + '\n'
            
            logger.info(f"📤 Sending execute_code (ID: {request_id[:8]}...)")
            
            self.bot_process.stdin.write(command)
            self.bot_process.stdin.flush()
            
            # 讀取執行結果並驗證 ID（60秒超時）
            logger.info(f"📥 Waiting for response (60s timeout)...")
            
            import select
            ready, _, _ = select.select([self.bot_process.stdout], [], [], 60)
            if not ready:
                logger.error("Timeout waiting for bot.js response!")
                return {'success': False, 'error': 'Response timeout (60s)'}
            
            response = self.bot_process.stdout.readline()
            
            result = json.loads(response)
            
            # 驗證響應 ID
            if result.get('id') != request_id:
                logger.error(f"Response ID mismatch! Expected {request_id[:8]}, got {result.get('id', 'None')[:8]}")
                # 嘗試再讀一行
                response = self.bot_process.stdout.readline()
                result = json.loads(response)
                if result.get('id') != request_id:
                    return {'success': False, 'error': 'Response ID mismatch'}
            
            logger.info(f"✅ Response verified (ID: {result.get('id', '')[:8]}...)")
            
            return result
            
        except Exception as e:
            logger.error(f"Failed to execute code: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def disconnect(self):
        """斷開連接"""
        if self.bot_process:
            self.bot_process.terminate()
            self.bot_process.wait(timeout=5)
            self.is_connected = False
            logger.info("Bot disconnected")
    
    def _default_observation(self) -> Dict[str, Any]:
        """返回默認觀察值（出錯時使用）"""
        return {
            'position': {'x': 0, 'y': 64, 'z': 0},
            'health': 20,
            'food': 20,
            'inventory': [],
            'nearby_entities': [],
            'nearby_blocks': [],
            'time_of_day': 'day',
            'weather': 'clear',
            'biome': 'unknown'
        }
