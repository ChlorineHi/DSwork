from flask import jsonify
import os
from google import genai
import logging
import traceback
import json
import time
import random

# 配置日志
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("ai_guide_simple.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("ai_guide_simple")

# 设置API密钥
API_KEY = "AIzaSyby74AjaMjcweHZn8Wh4a7HAx87g"  # 您的API密钥

# 创建客户端
client = genai.Client(api_key=API_KEY)
logger.info("Initialized Gemini API client (simple version)")

# 预定义回复
FALLBACK_RESPONSES = [
    "故宫是中国明清两代的皇家宫殿，位于北京中轴线的中心，是世界上现存规模最大、保存最为完整的木质结构古建筑之一。",
    "太和殿是故宫中轴线上的主要建筑，是明清两代举行大典的地方。它是中国古代宫殿建筑的精华，象征着皇权的至高无上。",
    "午门是故宫南端的正门，是紫禁城的正门。它建于明永乐十八年(1420年)，是一座五开间的城楼，呈凹字形。",
    "故宫的著名建筑包括太和殿、中和殿、保和殿、乾清宫、交泰殿、坤宁宫、御花园等，每一处都有其独特的历史和文化价值。",
    "我很乐意为您介绍更多关于中国文化景区的信息。您对哪个景点特别感兴趣呢？",
    "中国有许多著名的文化景区，如北京的故宫、颐和园，西安的兵马俑，苏州的园林等。您想了解哪一个呢？"
]

def simple_chat_with_ai_guide(user_input):
    """简化版的AI导游对话功能"""
    logger.info(f"Received chat request (simple). User input: '{user_input}'")
    
    try:
        # 尝试调用Gemini API进行简单问答
        logger.info("Calling Gemini API with simple prompt...")
        
        prompt = f"""你是一位专业的中国文化景区虚拟导游，名叫'小文'。
        请用简洁、亲切的语气回答以下问题（200字以内）：
        
        问题：{user_input}
        """
        
        # 使用简化的API调用
        response = client.models.generate_content(
            model="gemini-1.5-flash",  # 使用更稳定的模型
            contents=prompt
        )
        
        # 获取回复
        ai_response = response.text
        logger.info(f"Received response from Gemini API: '{ai_response[:50]}...'")
        
        return {
            "response": ai_response,
            "conversation_id": str(int(time.time()))  # 简单版本不需要真正的会话ID
        }
    except Exception as e:
        error_msg = f"Error calling Gemini API (simple): {str(e)}"
        stack_trace = traceback.format_exc()
        logger.error(error_msg)
        logger.error(f"Stack trace: {stack_trace}")
        
        # 使用预定义回复
        fallback_response = random.choice(FALLBACK_RESPONSES)
        logger.info(f"Using fallback response: '{fallback_response[:30]}...'")
        
        return {
            "response": fallback_response,
            "conversation_id": str(int(time.time())),
            "fallback": True
        }

# API端点函数
def handle_ai_guide_chat_simple(request):
    """处理简化版AI导游聊天请求"""
    try:
        logger.info("Received API request to simple AI guide chat")
        data = request.json
        logger.debug(f"Request data: {data}")
        
        user_input = data.get("message", "")
        
        logger.info(f"Processing chat request: message='{user_input}'")
        
        result = simple_chat_with_ai_guide(user_input)
        
        logger.info("Sending response back to client")
        logger.debug(f"Response: {result}")
        
        return jsonify(result)
    except Exception as e:
        error_msg = f"Unexpected error in handle_ai_guide_chat_simple: {str(e)}"
        stack_trace = traceback.format_exc()
        logger.error(error_msg)
        logger.error(f"Stack trace: {stack_trace}")
        
        # 使用预定义回复
        fallback_response = random.choice(FALLBACK_RESPONSES)
        
        return jsonify({
            "response": fallback_response,
            "fallback": True
        }) 