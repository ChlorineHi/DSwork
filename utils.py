import functools
import traceback
import logging
from flask import jsonify

logger = logging.getLogger("utils")

def api_error_handler(f):
    """API错误处理装饰器"""
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            error_msg = f"API错误: {str(e)}"
            stack_trace = traceback.format_exc()
            logger.error(error_msg)
            logger.error(f"堆栈跟踪: {stack_trace}")
            
            return jsonify({
                "error": True,
                "response": f"服务器内部错误，请稍后再试。\n错误信息：{str(e)}",
                "fallback": True
            }), 500
    
    return wrapper 