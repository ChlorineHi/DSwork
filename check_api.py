from google import genai
import logging
import sys

# 配置日志
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("check_api")

def check_api_key(api_key):
    """检查API密钥是否有效"""
    try:
        client = genai.Client(api_key=api_key)
        logger.info("Successfully created client with provided API key")
        return client
    except Exception as e:
        logger.error(f"Error creating client: {e}")
        return None

def check_models(client):
    """检查可用的模型"""
    try:
        models = client.models.list()
        logger.info("Available models:")
        for model in models:
            logger.info(f"- {model.name}")
        return models
    except Exception as e:
        logger.error(f"Error listing models: {e}")
        return []

def test_simple_generation(client, model_name):
    """测试简单的文本生成"""
    try:
        logger.info(f"Testing model: {model_name}")
        # 使用简化的API调用
        response = client.models.generate_content(
            model=model_name,
            contents="你好，请用一句话介绍一下故宫"
        )
        logger.info(f"Response: {response.text}")
        return True
    except Exception as e:
        logger.error(f"Error generating content with {model_name}: {e}")
        return False

if __name__ == "__main__":
    if len(sys.argv) > 1:
        api_key = sys.argv[1]
    else:
        api_key = "AIzaSyAPho0iby74AjaMjcweHZn8Wh4a7HAx87g"  # 默认使用您的API密钥
    
    logger.info(f"Checking API key: {api_key[:5]}...{api_key[-3:]}")
    
    client = check_api_key(api_key)
    if not client:
        logger.error("API key check failed")
        sys.exit(1)
    
    models = check_models(client)
    if not models:
        logger.error("No models available")
        sys.exit(1)
    
    # 测试不同的模型
    models_to_test = [
        "gemini-2.0-flash",
        "gemini-1.5-flash",
        "gemini-1.5-pro",
        "gemini-pro"
    ]
    
    success = False
    for model in models_to_test:
        if test_simple_generation(client, model):
            logger.info(f"Successfully tested {model}")
            success = True
            break
    
    if not success:
        logger.error("All model tests failed")
        sys.exit(1)
    
    logger.info("API key and model checks completed successfully") 