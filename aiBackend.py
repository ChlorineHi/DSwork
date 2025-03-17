# 这个文件可以作为独立测试Gemini API的脚本

from google import genai
import logging
import json

# 配置日志
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("aiBackend")

# 替换为您的实际API密钥
API_KEY = "AIzaSyAPho0iby74AjaMjcweHZn8Wh4a7HAx87g"

# 创建客户端
client = genai.Client(api_key=API_KEY)

def test_gemini_simple():
    """测试简单的Gemini API调用"""
    logger.info("Testing simple Gemini API call...")
    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents="介绍一下故宫的历史",
        )
        
        logger.info(f"Response: {response.text[:100]}...")
        print(response.text)
        return True
    except Exception as e:
        logger.error(f"Error: {e}")
        return False

def test_gemini_chat():
    """测试Gemini聊天API调用"""
    logger.info("Testing Gemini chat API call...")
    try:
        # 创建一个简单的聊天历史
        contents = [
            {
                "role": "user",
                "parts": [{"text": "你好，请介绍一下故宫"}]
            }
        ]
        
        logger.debug(f"Request contents: {json.dumps(contents)}")
        
        # 使用简化的API调用
        response = client.models.generate_content(
            model="gemini-1.5-flash",
            contents=contents
        )
        
        logger.info(f"Response: {response.text[:100]}...")
        print("Chat response:")
        print(response.text)
        
        # 继续对话
        contents.append({
            "role": "model",
            "parts": [{"text": response.text}]
        })
        
        contents.append({
            "role": "user",
            "parts": [{"text": "故宫有哪些著名的建筑？"}]
        })
        
        logger.debug(f"Follow-up request contents: {json.dumps([{'role': c['role'], 'parts_length': len(c['parts'])} for c in contents])}")
        
        # 使用简化的API调用
        response2 = client.models.generate_content(
            model="gemini-1.5-flash",
            contents=contents
        )
        
        logger.info(f"Follow-up response: {response2.text[:100]}...")
        print("\nFollow-up response:")
        print(response2.text)
        
        return True
    except Exception as e:
        logger.error(f"Error in chat test: {e}")
        return False

def test_available_models():
    """测试可用的模型"""
    logger.info("Testing available models...")
    try:
        models = client.models.list()
        logger.info("Available models:")
        for model in models:
            logger.info(f"- {model.name}")
        return True
    except Exception as e:
        logger.error(f"Error listing models: {e}")
        return False

if __name__ == "__main__":
    print("=== Testing Gemini API ===")
    
    print("\n1. Testing available models:")
    test_available_models()
    
    print("\n2. Testing simple query:")
    test_gemini_simple()
    
    print("\n3. Testing chat functionality:")
    test_gemini_chat()