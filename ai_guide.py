from flask import jsonify
import os
from google import genai
from typing import List, Dict, Any
import json
import time
import logging
import traceback
import uuid
import threading

# 配置日志
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("ai_guide.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("ai_guide")

# 设置API密钥
API_KEY = "AIzaSyAPho0iby74AjaMjcweHZn8Wh4a7HAx87g"  # 您的API密钥

# 创建客户端
try:
    client = genai.Client(api_key=API_KEY)
    logger.info("Initialized Gemini API client")
except Exception as e:
    logger.error(f"Error initializing Gemini API client: {e}")
    logger.error(traceback.format_exc())

# 初始化对话历史
conversation_history = {}

# 景点信息数据库
spots_info = {
    "故宫": "故宫，又名紫禁城，是中国明清两代的皇家宫殿，位于北京中轴线的中心。它是世界上现存规模最大、保存最为完整的木质结构古建筑之一。",
    "颐和园": "颐和园，是中国清朝时期的皇家园林，位于北京西北郊。它是保存最完整的一座皇家行宫御苑，被誉为'皇家园林博物馆'。",
    "圆明园": "圆明园，清代著名的皇家园林，位于北京西北郊，与颐和园毗邻。它由圆明园、长春园和万春园组成，被誉为'万园之园'。",
    "午门": "午门是故宫南端的正门，是紫禁城的正门。它建于明永乐十八年(1420年)，是一座五开间的城楼，呈凹字形。",
    "太和殿": "太和殿是故宫中轴线上的主要建筑，是明清两代举行大典的地方。它是中国古代宫殿建筑的精华，象征着皇权的至高无上。",
    "乾清宫": "乾清宫是内廷的中心建筑，是皇帝居住和处理政务的地方。它建于明永乐十八年(1420年)，是紫禁城内最重要的宫殿之一。",
    "御花园": "御花园位于紫禁城北部，是一座供皇帝和后妃游玩休息的皇家园林。园内假山叠石，花木扶疏，布局精巧。",
    "珍宝馆": "珍宝馆位于故宫西北角，原为雍和宫，现为收藏和展示皇家珍宝的场所。馆内珍藏了大量明清两代的宫廷珍宝。"
}

# 路线推荐数据库
routes_info = {
    "午门_太和殿": "从午门出发，沿着中轴线向北步行约10分钟即可到达太和殿。",
    "太和殿_乾清宫": "从太和殿出发，穿过中和殿、保和殿，继续向北步行约5分钟即可到达乾清宫。",
    "乾清宫_御花园": "从乾清宫出发，向北步行约3分钟即可到达御花园。",
    "太和殿_珍宝馆": "从太和殿出发，向西北方向步行约10分钟即可到达珍宝馆。",
    "乾清宫_珍宝馆": "从乾清宫出发，向西北方向步行约7分钟即可到达珍宝馆。",
    "御花园_珍宝馆": "从御花园出发，向西步行约5分钟即可到达珍宝馆。"
}

# 添加一个辅助函数来查询路线
def get_route_info(start, end):
    """获取从起点到终点的路线信息"""
    key = f"{start}_{end}"
    reverse_key = f"{end}_{start}"
    
    if key in routes_info:
        return routes_info[key]
    elif reverse_key in routes_info:
        # 如果找到反向路线，稍微修改描述
        reverse_info = routes_info[reverse_key]
        return f"您可以按照反向路线: {reverse_info}"
    else:
        return f"从{start}到{end}的路线建议：请咨询景区地图或工作人员。"

def get_system_prompt():
    """获取系统提示"""
    return """你是一位专业的中国文化景区虚拟导游，名叫'小文'。你熟悉中国各大文化景区的历史、文化和景点信息。
    
    你的回答应该：
    1. 准确、简洁、富有文化底蕴
    2. 使用礼貌、亲切的语气
    3. 适当融入中国传统文化元素
    4. 回答长度控制在200字以内
    
    当游客询问特定景点的信息时，你可以查询以下景点数据库：
    {spots_info}
    
    当游客询问如何从一个景点到另一个景点时，你可以查询以下路线数据库（格式为"起点_终点"）：
    {routes_info}
    
    当游客询问与景区无关的问题时，礼貌地将话题引回到景区相关内容。
    """

def create_conversation(conversation_id=None):
    """创建或获取对话"""
    logger.debug(f"Creating/retrieving conversation with ID: {conversation_id}")
    
    if conversation_id and conversation_id in conversation_history:
        logger.debug(f"Found existing conversation with ID: {conversation_id}")
        return conversation_history[conversation_id]
    
    # 创建新对话
    new_id = str(int(time.time()))
    logger.info(f"Creating new conversation with ID: {new_id}")
    
    # 确保景点信息和路线信息可以正确序列化为JSON
    spots_info_json = json.dumps(spots_info, ensure_ascii=False)
    routes_info_json = json.dumps(routes_info, ensure_ascii=False)
    
    system_prompt = get_system_prompt().format(
        spots_info=spots_info_json,
        routes_info=routes_info_json
    )
    logger.debug(f"System prompt length: {len(system_prompt)} characters")
    
    conversation_history[new_id] = {
        "id": new_id,
        "messages": [
            {
                "role": "system",
                "parts": [system_prompt]
            }
        ],
        "created_at": time.time()
    }
    return conversation_history[new_id]

def chat_with_ai_guide(user_input, conversation_id=None):
    """与AI导游对话"""
    logger.info(f"Received chat request. User input: '{user_input}', Conversation ID: {conversation_id}")
    
    # 获取或创建对话
    conversation = create_conversation(conversation_id)
    
    # 准备消息内容
    contents = []
    
    try:
        # 添加系统提示
        system_message = next((msg for msg in conversation["messages"] if msg["role"] == "system"), None)
        if system_message:
            logger.debug("Adding system message to contents")
            contents.append({
                "role": "user",
                "parts": [{"text": f"[SYSTEM INSTRUCTION] {system_message['parts'][0]}"}]
            })
        
        # 添加历史消息（除了系统消息）
        history_count = 0
        for msg in conversation["messages"]:
            if msg["role"] != "system":
                history_count += 1
                logger.debug(f"Adding history message ({msg['role']}): {msg['parts'][0][:30]}...")
                contents.append({
                    "role": msg["role"] if msg["role"] != "model" else "assistant",
                    "parts": [{"text": msg["parts"][0]}]
                })
        
        logger.debug(f"Added {history_count} history messages")
        
        # 添加用户当前消息
        logger.debug(f"Adding current user message: {user_input}")
        contents.append({
            "role": "user",
            "parts": [{"text": user_input}]
        })
        
        # 更新对话历史中的用户消息
        conversation["messages"].append({
            "role": "user",
            "parts": [user_input]
        })
        
        logger.info("Calling Gemini API...")
        logger.debug(f"Request contents structure: {json.dumps([{'role': c['role'], 'parts_length': len(c['parts'])} for c in contents])}")
        
        # 尝试不同的模型
        models_to_try = ["gemini-1.5-flash", "gemini-1.5-pro", "gemini-pro"]
        last_error = None
        
        for model in models_to_try:
            try:
                logger.info(f"Trying model: {model}")
                # 调用Gemini API - 使用简化的参数
                response = client.models.generate_content(
                    model=model,
                    contents=contents
                )
                
                # 获取回复
                ai_response = response.text
                logger.info(f"Received response from Gemini API ({model}): '{ai_response[:50]}...'")
                
                # 添加AI回复到对话历史
                conversation["messages"].append({
                    "role": "model",
                    "parts": [ai_response]
                })
                
                # 清理过长的对话历史（保留系统消息和最近10条消息）
                if len(conversation["messages"]) > 11:  # 系统提示 + 10条消息
                    logger.debug("Trimming conversation history")
                    conversation["messages"] = [conversation["messages"][0]] + conversation["messages"][-10:]
                
                return {
                    "response": ai_response,
                    "conversation_id": conversation["id"]
                }
            except Exception as e:
                logger.warning(f"Error with model {model}: {str(e)}")
                last_error = e
                continue
        
        # 如果所有模型都失败
        if last_error:
            raise last_error
        else:
            raise Exception("All models failed but no error was captured")
            
    except Exception as e:
        error_msg = f"Error calling Gemini API: {str(e)}"
        stack_trace = traceback.format_exc()
        logger.error(error_msg)
        logger.error(f"Stack trace: {stack_trace}")
        
        # 尝试获取更详细的错误信息
        error_details = ""
        if hasattr(e, 'details'):
            error_details = f"\nDetails: {e.details}"
            logger.error(f"Error details: {error_details}")
        
        return {
            "response": f"抱歉，我遇到了一些技术问题，请稍后再试。\n错误信息：{str(e)}{error_details}",
            "conversation_id": conversation["id"],
            "error": True
        }

# 清理旧对话（超过1小时的对话）
def cleanup_old_conversations():
    """清理旧对话"""
    current_time = time.time()
    to_delete = []
    
    for conv_id, conv in conversation_history.items():
        if current_time - conv["created_at"] > 3600:  # 1小时
            to_delete.append(conv_id)
    
    for conv_id in to_delete:
        logger.info(f"Cleaning up old conversation: {conv_id}")
        del conversation_history[conv_id]

# 定期清理旧对话
def start_cleanup_thread():
    """启动清理线程"""
    threading.Timer(1800, start_cleanup_thread).start()  # 每30分钟清理一次
    cleanup_old_conversations()

# 启动清理线程
start_cleanup_thread()

# API端点函数
def handle_ai_guide_chat(request):
    """处理AI导游聊天请求"""
    try:
        logger.info("Received API request to /api/ai_guide/chat")
        data = request.json
        logger.debug(f"Request data: {data}")
        
        user_input = data.get("message", "")
        conversation_id = data.get("conversation_id")
        
        logger.info(f"Processing chat request: message='{user_input}', conversation_id={conversation_id}")
        
        result = chat_with_ai_guide(user_input, conversation_id)
        
        logger.info("Sending response back to client")
        logger.debug(f"Response: {result}")
        
        return jsonify(result)
    except Exception as e:
        error_msg = f"Unexpected error in handle_ai_guide_chat: {str(e)}"
        stack_trace = traceback.format_exc()
        logger.error(error_msg)
        logger.error(f"Stack trace: {stack_trace}")
        
        return jsonify({
            "response": f"服务器内部错误，请稍后再试。\n错误信息：{str(e)}",
            "error": True
        }) 