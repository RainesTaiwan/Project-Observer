"""
Logger Utility - 日誌配置
"""

import logging
import sys
from pathlib import Path
from datetime import datetime


def setup_logger(name: str = 'agent', log_level: str = 'INFO') -> logging.Logger:
    """
    設置日誌記錄器
    
    Args:
        name: Logger 名稱
        log_level: 日誌級別
        
    Returns:
        配置好的 Logger
    """
    # 創建日誌目錄
    log_dir = Path('/app/logs')
    log_dir.mkdir(exist_ok=True)
    
    # 生成日誌文件名（帶時間戳）
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    log_file = log_dir / f'agent_{timestamp}.log'
    
    # 配置 Logger
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, log_level.upper()))
    
    # 清除現有的 handlers
    logger.handlers.clear()
    
    # 控制台 Handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_formatter = logging.Formatter(
        '%(asctime)s | %(levelname)-8s | %(message)s',
        datefmt='%H:%M:%S'
    )
    console_handler.setFormatter(console_formatter)
    
    # 文件 Handler
    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)
    file_formatter = logging.Formatter(
        '%(asctime)s | %(name)s | %(levelname)-8s | %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    file_handler.setFormatter(file_formatter)
    
    # 添加 Handlers
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    
    return logger
