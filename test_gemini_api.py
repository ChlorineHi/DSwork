from google import genai
import logging
import json

# 配置日志
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("test_gemini_api")

# 替换为您的实际API密钥
API_KEY = "AIzaSyAPho0iby74AjaMjcweHZn8Wh4a7HAx87g"

def test_simple_query():
    """测试简单查询"""
    try:
        # 创建客户端
        client = genai.Client(api_key=API_KEY)
        logger.info("Successfully created client")
        
        # 简单文本查询
        response = client.models.generate_content(
            model="gemini-1.5-flash",
            contents="介绍一下故宫的历史"
        )
        
        logger.info(f"Response: {response.text[:100]}...")
        print(f"Simple query response:\n{response.text}\n")
        return True
    except Exception as e:
        logger.error(f"Error in simple query: {e}")
        return False

def test_chat_query():
    """测试聊天查询"""
    try:
        # 创建客户端
        client = genai.Client(api_key=API_KEY)
        
        # 聊天格式查询
        contents = [
            {
                "role": "user",
                "parts": [{"text": "你好，请介绍一下故宫"}]
            }
        ]
        
        response = client.models.generate_content(
            model="gemini-1.5-flash",
            contents=contents
        )
        
        logger.info(f"Response: {response.text[:100]}...")
        print(f"Chat query response:\n{response.text}\n")
        return True
    except Exception as e:
        logger.error(f"Error in chat query: {e}")
        return False

if __name__ == "__main__":
    print("=== Testing Gemini API ===")
    
    print("\n1. Testing simple query:")
    test_simple_query()
    
    print("\n2. Testing chat query:")
    test_chat_query() 