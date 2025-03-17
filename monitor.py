import subprocess
import time
import sys
import os
import signal
import logging

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("monitor.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("monitor")

def start_server():
    """启动Flask服务器"""
    logger.info("Starting Flask server...")
    # 使用Popen启动服务器，这样我们可以获取进程ID
    process = subprocess.Popen([sys.executable, "app.py"], 
                              stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE)
    logger.info(f"Server started with PID: {process.pid}")
    return process

def check_server_health(port=5000):
    """检查服务器健康状态"""
    try:
        import requests
        response = requests.get(f"http://localhost:{port}/api/health", timeout=5)
        if response.status_code == 200 and response.json().get("status") == "ok":
            logger.info("Server health check passed")
            return True
        else:
            logger.warning(f"Server returned unexpected response: {response.status_code}")
            return False
    except Exception as e:
        logger.error(f"Server health check failed: {e}")
        return False

def restart_server_if_needed(process):
    """如果需要，重启服务器"""
    if process.poll() is not None:
        # 进程已经结束
        logger.warning(f"Server process terminated with code: {process.returncode}")
        return start_server()
    
    if not check_server_health():
        # 服务器没有响应健康检查
        logger.warning("Server not responding to health checks, restarting...")
        try:
            # 尝试正常终止进程
            process.terminate()
            # 等待进程终止
            process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            # 如果进程没有及时终止，强制终止
            logger.warning("Server did not terminate gracefully, killing...")
            process.kill()
        
        # 启动新的服务器进程
        return start_server()
    
    return process

def monitor_server():
    """监控服务器并在需要时重启"""
    logger.info("Starting server monitor...")
    
    # 启动服务器
    server_process = start_server()
    
    try:
        # 每30秒检查一次服务器状态
        while True:
            time.sleep(30)
            server_process = restart_server_if_needed(server_process)
    except KeyboardInterrupt:
        logger.info("Monitor interrupted, shutting down server...")
        server_process.terminate()
        try:
            server_process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            server_process.kill()
        logger.info("Server shutdown complete")

if __name__ == "__main__":
    monitor_server() 