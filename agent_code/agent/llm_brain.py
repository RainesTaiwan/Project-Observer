"""
LLM Brain - AI 的思考核心
負責與大語言模型交互，進行決策制定
"""

import os
import json
import logging
from typing import Dict, Any, List
from openai import OpenAI

logger = logging.getLogger(__name__)


class LLMBrain:
    """LLM 思考引擎"""
    
    def __init__(self, memory_manager):
        self.memory_manager = memory_manager
        
        # 初始化 OpenAI 客戶端
        self.client = OpenAI(
            api_key=os.getenv('OPENAI_API_KEY'),
            base_url=os.getenv('OPENAI_API_BASE', 'https://api.openai.com/v1')
        )
        self.model = os.getenv('LLM_MODEL', 'gpt-4')
        
        # 系統提示詞
        self.system_prompt = self._load_system_prompt()
        
        logger.info(f"🧠 LLM Brain initialized with model: {self.model}")
    
    def make_decision(self, observation: Dict[str, Any]) -> Dict[str, Any]:
        """
        根據觀察結果做出決策
        
        Args:
            observation: 當前遊戲狀態觀察
            
        Returns:
            決策字典，包含目標、行動類型、代碼等
        """
        try:
            # 1. 檢索相關記憶
            relevant_memories = self.memory_manager.query_similar_situations(
                observation, 
                top_k=3
            )
            
            # 2. 構建提示詞
            prompt = self._build_decision_prompt(observation, relevant_memories)
            
            # 3. 調用 LLM
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a Minecraft survival AI. Reply with ONLY ONE WORD from: explore, mine_wood, mine_stone, hunt, retreat, rest. No explanations."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=10
            )
            
            # 4. 解析響應
            decision_text = response.choices[0].message.content
            logger.info(f"🔍 LLM Raw Output: '{decision_text}' (len={len(decision_text)})")
            decision = self._parse_decision(decision_text)
            
            logger.info(f"💭 LLM Decision: {decision.get('goal', 'Unknown')}")
            
            return decision
            
        except Exception as e:
            logger.error(f"LLM decision failed: {e}")
            return self._default_decision()
    
    def analyze_failure(self, error_context: Dict[str, Any]) -> str:
        """
        分析失敗原因並提出改進建議
        
        Args:
            error_context: 錯誤上下文信息
            
        Returns:
            改進建議字符串
        """
        try:
            prompt = f"""
我剛才執行了一個行動但失敗了。請分析失敗原因並提出改進方案。

## 失敗的行動
目標: {error_context['decision'].get('goal')}
行動類型: {error_context['decision'].get('action_type')}

## 錯誤信息
{error_context['result'].get('error')}

請提供：
1. 失敗的可能原因
2. 具體的改進建議
3. 下次應該避免什麼
"""
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "你是一個善於從失敗中學習的 AI 助手。"},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=500
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            logger.error(f"Failure analysis failed: {e}")
            return "無法分析失敗原因"
    
    def _build_decision_prompt(self, observation: Dict[str, Any], memories: List[str]) -> str:
        """構建決策提示詞"""
        
        prompt = f"""你是 Minecraft 生存 AI。根據當前狀態選擇最佳行動。

## 當前狀態
- 生命值: {observation['health']}/20 {'⚠️ 危險！' if observation['health'] < 10 else ''}
- 飢餓值: {observation['food']}/20 {'🍖 需要食物' if observation['food'] < 10 else ''}
- 附近實體: {len(observation.get('nearby_entities', []))} 個
- 附近方塊: {len(observation.get('nearby_blocks', []))} 個
- 時間: {observation['time_of_day']}

## 可用行動
只需回答一個單詞（不要有任何解釋）：

**基礎行動:**
- explore - 向前探索世界
- mine_wood - 尋找並砍樹獲取木頭
- mine_stone - 挖掘石頭
- hunt - 尋找動物作為食物
- retreat - 遇到危險時後退
- rest - 原地等待觀察

**生存原則:**
- 生命值 < 10: 選擇 retreat
- 飢餓值 < 10: 選擇 hunt
- 沒有資源: 選擇 mine_wood 或 mine_stone
- 其他情況: 選擇 explore

你的選擇（只回答一個單詞）:"""
        return prompt
    
    def _parse_decision(self, decision_text: str) -> Dict[str, Any]:
        """解析 LLM 返回的決策（簡化版：只需要一個動作詞）"""
        try:
            # 清理回應文本
            text = decision_text.strip().lower()
            
            # 提取第一個單詞作為動作
            words = text.split()
            if not words:
                return self._default_decision()
            
            # 找到第一個有效的動作詞
            valid_actions = ['explore', 'mine_wood', 'mine_stone', 'hunt', 'retreat', 'rest']
            action = 'explore'  # 默認探索
            
            for word in words:
                clean_word = word.strip('.,!?:;"\'')
                if clean_word in valid_actions:
                    action = clean_word
                    break
            
            # 動作映射到代碼
            action_map = {
                'explore': {
                    'goal': '探索世界',
                    'reasoning': '向前移動探索未知區域',
                    'action_type': 'generate_code',
                    'code': 'const forward = bot.entity.position.offset(10, 0, 0); await bot.pathfinder.goto(new goals.GoalNear(forward.x, forward.y, forward.z, 1));'
                },
                'mine_wood': {
                    'goal': '收集木頭',
                    'reasoning': '尋找並砍伐樹木',
                    'action_type': 'generate_code',
                    'code': 'const log = bot.findBlock({matching: block => block.name.includes("log"), maxDistance: 32}); if(log) {await bot.pathfinder.goto(new goals.GoalLookAtBlock(log.position, bot.world)); await bot.dig(log);} else {const tree = bot.findBlock({matching: block => block.name.includes("leaves"), maxDistance: 32}); if(tree) await bot.pathfinder.goto(new goals.GoalNear(tree.position.x, tree.position.y, tree.position.z, 5));}'
                },
                'mine_stone': {
                    'goal': '挖掘石頭',
                    'reasoning': '收集石頭資源',
                    'action_type': 'generate_code',
                    'code': 'const stone = bot.findBlock({matching: block => block.name === "stone", maxDistance: 32}); if(stone) {await bot.pathfinder.goto(new goals.GoalLookAtBlock(stone.position, bot.world)); await bot.dig(stone);}'
                },
                'hunt': {
                    'goal': '狩獵動物',
                    'reasoning': '尋找食物來源',
                    'action_type': 'generate_code',
                    'code': 'const animals = Object.values(bot.entities).filter(e => ["pig","cow","chicken","sheep","rabbit"].includes(e.name) && e.position.distanceTo(bot.entity.position) < 32); if(animals.length > 0) {const target = animals[0]; await bot.pathfinder.goto(new goals.GoalNear(target.position.x, target.position.y, target.position.z, 2));}'
                },
                'retreat': {
                    'goal': '撤退到安全位置',
                    'reasoning': '生命值低，需要遠離危險',
                    'action_type': 'generate_code',
                    'code': 'const back = bot.entity.position.offset(-15, 0, 0); await bot.pathfinder.goto(new goals.GoalNear(back.x, back.y, back.z, 1));'
                },
                'rest': {
                    'goal': '休息觀察',
                    'reasoning': '等待並觀察環境',
                    'action_type': 'wait',
                    'code': ''
                }
            }
            
            # 獲取對應的行動
            decision = action_map[action].copy()
            decision['is_new_skill'] = False
            
            logger.info(f"💭 LLM Decision: {decision['goal']} (action: {action})")
            
            return decision
                
        except Exception as e:
            logger.warning(f"Failed to parse decision: {e}")
            return self._default_decision()
    
    def _load_system_prompt(self) -> str:
        """加載系統提示詞"""
        return """你是一個在 Minecraft 世界中生存的 AI 代理人。

你的核心能力：
1. 觀察環境：你能看到周圍的方塊、生物和玩家
2. 做出決策：根據情況選擇最合適的行動
3. 執行代碼：你可以生成並執行 JavaScript 代碼來完成任務
4. 學習進化：從成功和失敗中學習，不斷改進

你的生存目標：
1. 保持生命值（避免受傷和死亡）
2. 保持飽食度（尋找食物）
3. 收集資源（木頭、石頭、礦物等）
4. 製作工具（從木鎬到鑽石鎬）
5. 建造庇護所（保護自己免受怪物襲擊）
6. 探索世界（發現新的生物群系和資源）

決策原則：
- 優先保證安全（低血量時避免戰鬥）
- 循序漸進（先收集基礎資源再追求高級目標）
- 從簡單技能開始（先學會砍樹再學會挖礦）
- 記住過去的經驗（不要重複失敗的行為）

代碼生成規則：
- 使用 Mineflayer API
- 代碼要健壯（包含錯誤處理）
- 確保代碼是異步安全的
- 註釋清晰說明代碼意圖
"""
    
    def _default_decision(self) -> Dict[str, Any]:
        """返回默認決策（出錯時使用）"""
        return {
            'goal': 'Wait and observe',
            'reasoning': 'Decision making failed, waiting for next iteration',
            'action_type': 'wait',
            'is_new_skill': False
        }
