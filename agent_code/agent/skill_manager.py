"""
Skill Manager - 技能管理器
負責技能的存儲、檢索和執行
"""

import os
import json
import logging
from typing import Dict, Any
from pathlib import Path

logger = logging.getLogger(__name__)


class SkillManager:
    """技能管理器 - 存儲和管理 AI 學會的技能"""
    
    def __init__(self, memory_manager):
        self.memory_manager = memory_manager
        self.skills_dir = Path('/app/skills')
        self.skills_dir.mkdir(exist_ok=True)
        
        # 加載已有技能
        self.skills = self._load_all_skills()
        
        logger.info(f"🎯 Skill Manager initialized with {len(self.skills)} skills")
    
    def save_skill(self, decision: Dict[str, Any], result: Dict[str, Any]):
        """
        保存成功執行的新技能
        
        Args:
            decision: 決策信息
            result: 執行結果
        """
        try:
            skill_name = decision.get('skill_name') or self._generate_skill_name(decision)
            
            skill_data = {
                'name': skill_name,
                'goal': decision.get('goal'),
                'code': decision.get('code'),
                'parameters': decision.get('parameters', {}),
                'description': decision.get('reasoning'),
                'success_count': 1,
                'failure_count': 0,
                'created_at': result.get('timestamp'),
                'last_used': result.get('timestamp')
            }
            
            # 保存到文件
            skill_file = self.skills_dir / f"{skill_name}.json"
            with open(skill_file, 'w', encoding='utf-8') as f:
                json.dump(skill_data, f, indent=2, ensure_ascii=False)
            
            # 加載到內存
            self.skills[skill_name] = skill_data
            
            logger.info(f"✅ Saved new skill: {skill_name}")
            
        except Exception as e:
            logger.error(f"Failed to save skill: {e}")
    
    def execute_skill(self, skill_name: str, parameters: Dict[str, Any], 
                     bot_controller) -> Dict[str, Any]:
        """
        執行已知技能
        
        Args:
            skill_name: 技能名稱
            parameters: 執行參數
            bot_controller: Bot 控制器
            
        Returns:
            執行結果
        """
        try:
            if skill_name not in self.skills:
                return {
                    'success': False,
                    'error': f'Skill not found: {skill_name}'
                }
            
            skill = self.skills[skill_name]
            code = skill['code']
            
            # 執行代碼
            result = bot_controller.execute_code(code)
            
            # 更新技能統計
            if result.get('success'):
                skill['success_count'] += 1
                skill['last_used'] = result.get('timestamp')
                self._save_skill_to_file(skill_name, skill)
            else:
                skill['failure_count'] += 1
            
            return result
            
        except Exception as e:
            logger.error(f"Failed to execute skill {skill_name}: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def get_skill_list(self) -> list:
        """獲取所有技能列表"""
        return [
            {
                'name': name,
                'goal': skill['goal'],
                'success_count': skill['success_count'],
                'failure_count': skill['failure_count']
            }
            for name, skill in self.skills.items()
        ]
    
    def _load_all_skills(self) -> Dict[str, Dict]:
        """從文件加載所有技能"""
        skills = {}
        
        try:
            for skill_file in self.skills_dir.glob('*.json'):
                with open(skill_file, 'r', encoding='utf-8') as f:
                    skill_data = json.load(f)
                    skills[skill_data['name']] = skill_data
            
            logger.info(f"Loaded {len(skills)} skills from disk")
            
        except Exception as e:
            logger.error(f"Failed to load skills: {e}")
        
        return skills
    
    def _save_skill_to_file(self, skill_name: str, skill_data: Dict):
        """保存單個技能到文件"""
        try:
            skill_file = self.skills_dir / f"{skill_name}.json"
            with open(skill_file, 'w', encoding='utf-8') as f:
                json.dump(skill_data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            logger.error(f"Failed to save skill to file: {e}")
    
    def _generate_skill_name(self, decision: Dict[str, Any]) -> str:
        """生成技能名稱"""
        goal = decision.get('goal', 'unknown_skill')
        # 移除空格和特殊字符
        name = goal.lower().replace(' ', '_').replace('-', '_')
        # 限制長度
        name = name[:50]
        return name
