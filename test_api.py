import requests
import json
import logging

# 配置日志
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("test_api")

def test_ai_guide_api():
    """测试AI导游API"""
    url = "http://localhost:5000/api/ai_guide/chat"
    
    # 第一条消息
    data = {
        "message": "你好，请介绍一下故宫"
    }
    
    logger.info(f"Sending first message: {data['message']}")
    
    try:
        response = requests.post(url, json=data)
        response.raise_for_status()  # 如果状态码不是200，抛出异常
        
        result = response.json()
        logger.info(f"Received response: {result['response'][:100]}...")
        print(f"AI: {result['response']}")
        
        # 获取对话ID
        conversation_id = result.get("conversation_id")
        logger.info(f"Conversation ID: {conversation_id}")
        
        # 发送第二条消息
        data = {
            "message": "故宫有哪些著名的建筑？",
            "conversation_id": conversation_id
        }
        
        logger.info(f"Sending second message: {data['message']}")
        
        response = requests.post(url, json=data)
        response.raise_for_status()
        
        result = response.json()
        logger.info(f"Received response: {result['response'][:100]}...")
        print(f"AI: {result['response']}")
        
        return True
    except Exception as e:
        logger.error(f"Error: {e}")
        return False

if __name__ == "__main__":
    print("Testing AI Guide API...")
    success = test_ai_guide_api()
    if success:
        print("Test completed successfully!")
    else:
        print("Test failed!") 