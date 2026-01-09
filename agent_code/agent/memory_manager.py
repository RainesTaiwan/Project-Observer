"""
Memory Manager - 記憶管理器
使用向量數據庫存儲和檢索 AI 的經驗
"""

import os
import json
import logging
from typing import Dict, Any, List
from datetime import datetime
import chromadb
from chromadb.config import Settings

logger = logging.getLogger(__name__)


class MemoryManager:
    """記憶管理器 - AI 的海馬迴"""
    
    def __init__(self):
        # 連接到 ChromaDB
        chroma_host = os.getenv('CHROMA_HOST', 'chromadb')
        chroma_port = os.getenv('CHROMA_PORT', '8000')
        
        self.client = chromadb.HttpClient(
            host=chroma_host,
            port=int(chroma_port)
        )
        
        # 創建或獲取集合
        self.experience_collection = self.client.get_or_create_collection(
            name="ai_experiences",
            metadata={"description": "AI agent's learning experiences"}
        )
        
        self.failure_collection = self.client.get_or_create_collection(
            name="ai_failures",
            metadata={"description": "Failed attempts and lessons learned"}
        )
        
        logger.info("💾 Memory Manager connected to ChromaDB")
    
    def query_similar_situations(self, observation: Dict[str, Any], top_k: int = 3) -> List[str]:
        """
        根據當前觀察查詢相似的過去經驗
        
        Args:
            observation: 當前觀察
            top_k: 返回最相似的 k 個記憶
            
        Returns:
            相關記憶的文本列表
        """
        try:
            # 構建查詢文本
            query_text = self._observation_to_text(observation)
            
            # 查詢向量數據庫
            results = self.experience_collection.query(
                query_texts=[query_text],
                n_results=top_k
            )
            
            if results['documents'] and len(results['documents'][0]) > 0:
                return results['documents'][0]
            else:
                return []
                
        except Exception as e:
            logger.error(f"Failed to query memories: {e}")
            return []
    
    def store_experience(self, observation: Dict[str, Any], decision: Dict[str, Any], 
                        result: Dict[str, Any]):
        """
        存儲一次成功的經驗
        
        Args:
            observation: 當時的觀察
            decision: 做出的決策
            result: 執行結果
        """
        try:
            # 構建文檔
            doc_text = f"""
情況: {self._observation_to_text(observation)}
決策: {decision.get('goal')}
行動: {decision.get('action_type')}
結果: 成功 - {result.get('message', 'N/A')}
"""
            
            # 存儲到向量數據庫
            doc_id = f"exp_{datetime.now().timestamp()}"
            
            self.experience_collection.add(
                documents=[doc_text],
                ids=[doc_id],
                metadatas=[{
                    'timestamp': datetime.now().isoformat(),
                    'goal': decision.get('goal', ''),
                    'success': True
                }]
            )
            
            logger.info(f"💾 Stored successful experience: {doc_id}")
            
        except Exception as e:
            logger.error(f"Failed to store experience: {e}")
    
    def store_failure(self, error_context: Dict[str, Any], improvement: str):
        """
        存儲失敗案例和改進建議
        
        Args:
            error_context: 錯誤上下文
            improvement: 改進建議
        """
        try:
            decision = error_context['decision']
            result = error_context['result']
            
            doc_text = f"""
失敗案例:
目標: {decision.get('goal')}
行動: {decision.get('action_type')}
錯誤: {result.get('error')}
改進建議: {improvement}
"""
            
            doc_id = f"fail_{datetime.now().timestamp()}"
            
            self.failure_collection.add(
                documents=[doc_text],
                ids=[doc_id],
                metadatas=[{
                    'timestamp': error_context['timestamp'],
                    'goal': decision.get('goal', ''),
                    'error': result.get('error', '')[:200]  # 限制長度
                }]
            )
            
            logger.info(f"💾 Stored failure lesson: {doc_id}")
            
        except Exception as e:
            logger.error(f"Failed to store failure: {e}")
    
    def get_statistics(self) -> Dict[str, int]:
        """獲取記憶統計信息"""
        try:
            return {
                'total_experiences': self.experience_collection.count(),
                'total_failures': self.failure_collection.count()
            }
        except:
            return {'total_experiences': 0, 'total_failures': 0}
    
    def _observation_to_text(self, observation: Dict[str, Any]) -> str:
        """將觀察轉換為文本描述"""
        return f"""
生命值: {observation.get('health', 0)}/20
飢餓值: {observation.get('food', 0)}/20
時間: {observation.get('time_of_day', 'unknown')}
附近實體數量: {len(observation.get('nearby_entities', []))}
背包物品數量: {len(observation.get('inventory', []))}
"""
