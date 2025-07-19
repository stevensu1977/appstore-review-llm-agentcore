#!/usr/bin/env python3
"""
App Reviews AgentCore Service - Simplified Version

基于 Option A: SDK Integration 的简化实现
专注于核心的应用评论分析功能
"""

import os
import json
from datetime import datetime
from typing import Dict, Any

# AgentCore SDK 导入
from bedrock_agentcore.runtime import BedrockAgentCoreApp

# Strands 和业务逻辑导入
from strands import Agent, tool
from google_play_scraper import search, Sort, reviews
import logging

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 初始化 AgentCore 应用
app = BedrockAgentCoreApp()

# ============================================================================
# 工具函数 - 保持与原版本相同
# ============================================================================

class DateTimeEncoder(json.JSONEncoder):
    """JSON 编码器"""
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super().default(obj)

@tool
def get_google_app_id(app_name: str) -> str:
    """
    Find Google Play Store AppID by app name.
    """
    try:
        result = search(app_name, lang="en", country="us", n_hits=1)
        if len(result) > 0:
            return result[0]['appId']
        else:
            return None
    except Exception as e:
        logger.error(f"Error in get_google_app_id: {e}")
        return None

@tool
def get_google_play_app_review(app_id: str, country: str = "us", rank: int = -1) -> list:
    """
    Get app reviews from Google Play Store.
    """
    try:
        filter_score = None
        if rank > 0 and rank < 6:
            filter_score = rank
        
        result, _ = reviews(
            app_id,
            lang='en',
            country="us" if country == "" else country,
            sort=Sort.NEWEST,
            count=100,
            filter_score_with=filter_score
        )
        
        # 保存评论到文件
        save_review(app_id, result)
        
        return [{"username": review["userName"], "content": review["content"], "score": review["score"]} for review in result]
    except Exception as e:
        logger.error(f"Error in get_google_play_app_review: {e}")
        return []

def save_review(app_id, data):
    """Save reviews to a JSON file."""
    try:
        os.makedirs("output", exist_ok=True)
        with open(f"output/{app_id}.json", "w", encoding="utf-8") as file:
            json.dump(data, file, cls=DateTimeEncoder, ensure_ascii=False, indent=4)
        logger.info(f"Reviews saved for app_id: {app_id}")
    except Exception as e:
        logger.error(f"Error saving reviews: {e}")

# ============================================================================
# 全局 Agent 初始化
# ============================================================================

# 初始化 Strands Agent
try:
    agent = Agent(
        tools=[get_google_app_id, get_google_play_app_review],
        model="us.anthropic.claude-3-7-sonnet-20250219-v1:0"
    )
    logger.info("Strands Agent initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize Strands Agent: {e}")
    agent = None

# ============================================================================
# 核心业务逻辑
# ============================================================================

def analyze_app_reviews_core(store: str, app_name: str, country: str = "us", rank: int = -1):
    """
    核心分析逻辑 - 基于原有 analyze_app_reviews 函数
    """
    if not agent:
        raise Exception("Strands Agent not available")
    
    logger.info(f"Starting analysis for app: {app_name}, store: {store}")
    
    # 获取app ID
    if store == 'Google Play':
        app_id_message = f"Find the Google Play Store app ID for the app named '{app_name}'."
        app_id_result = agent(app_id_message)
        
        app_id = str(app_id_result).strip()
        
        # 如果返回的不是有效的app ID，尝试直接调用工具
        if not app_id or "I'll help you find" in app_id:
            app_id = get_google_app_id(app_name)
    else:
        app_id = app_name
    
    logger.info(f"Found app ID: {app_id}")
    
    # 获取应用评论
    reviews_message = f"""
    Get app reviews from {store} for the app with ID '{app_id}' in country '{country}'.
    If rank is specified ({rank}), filter reviews by that score.
    """
    
    reviews_result = agent(reviews_message)
    
    # 分析评论
    analysis_message = f"""
    Analyze the following app reviews from {store}, app_id: {app_id}, country: {country}.
    
    {reviews_result}
    
    Your task:
    1. Identify common issues mentioned in the reviews (e.g., price issues, network issues, game content issues)
    2. Calculate the percentage for each review score (1-5 stars)
    3. Summarize the overall sentiment
    4. Format your response in markdown
    5. Translate your analysis to Chinese
    """
    
    analysis_result = agent(analysis_message)
    
    return app_id, str(analysis_result)

# ============================================================================
# AgentCore 入口点
# ============================================================================

@app.entrypoint
def invoke(payload):
    """
    AgentCore 主入口点
    
    根据 Option A: SDK Integration 的标准实现
    """
    try:
        logger.info(f"Received request: {payload}")
        
        # 解析输入
        prompt = payload.get("prompt", "")
        app_name = payload.get("app_name", "")
        store = payload.get("store", "Google Play")
        country = payload.get("country", "us")
        rank = payload.get("rank", -1)
        
        # 如果有 prompt，优先处理 prompt
        if prompt:
            # 尝试从 prompt 中提取应用名称
            if "analyze" in prompt.lower() and "app" in prompt.lower():
                # 简单的提取逻辑，可以根据需要改进
                words = prompt.split()
                for i, word in enumerate(words):
                    if word.lower() in ["app", "application"] and i + 1 < len(words):
                        app_name = words[i + 1].strip('"\'')
                        break
                
                if not app_name:
                    return {"error": "Could not extract app name from prompt. Please specify app_name parameter."}
        
        # 如果没有应用名称，返回错误
        if not app_name:
            return {"error": "app_name is required. Please provide either 'app_name' parameter or include it in 'prompt'."}
        
        # 执行分析
        app_id, analysis_result = analyze_app_reviews_core(store, app_name, country, rank)
        
        # 返回结果
        result = {
            "result": analysis_result,
            "app_id": app_id,
            "app_name": app_name,
            "store": store,
            "country": country,
            "timestamp": datetime.now().isoformat()
        }
        
        logger.info(f"Analysis completed for app: {app_name}")
        return result
        
    except Exception as e:
        logger.error(f"Error in invoke: {e}")
        return {"error": str(e), "timestamp": datetime.now().isoformat()}

# ============================================================================
# 应用启动
# ============================================================================

if __name__ == "__main__":
    logger.info("Starting App Reviews AgentCore service...")
    logger.info(f"Agent available: {agent is not None}")
    app.run()
