import os
import threading
import time
import requests
import nonebot
from nonebot.adapters.onebot.v11 import Adapter as OneBotV11Adapter
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 初始化 NoneBot
nonebot.init()

# 注册适配器
driver = nonebot.get_driver()
driver.register_adapter(OneBotV11Adapter)

# 加载插件
nonebot.load_plugins("plugins")

def keep_alive():
    """保活函数 - 不用 Flask，直接发请求"""
    # 从环境变量获取你的服务地址
    railway_url = os.environ.get('RAILWAY_URL')
    if not railway_url:
        print("❌ 未设置 RAILWAY_URL 环境变量")
        return
    
    print(f"📡 保活线程启动，监控地址: {railway_url}")
    
    while True:
        time.sleep(240)  # 4分钟
        try:
            # 给自己发请求保活
            response = requests.get(
                f"{railway_url}/",
                timeout=5,
                headers={'User-Agent': 'KeepAlive/1.0'}
            )
            print(f"💓 心跳正常 - {time.strftime('%Y-%m-%d %H:%M:%S')} - 状态码: {response.status_code}")
        except Exception as e:
            print(f"⚠️ 心跳异常: {e}")

if __name__ == '__main__':
    print("="*50)
    print("🤖 AI QQ机器人启动中...")
    print("="*50)
    
    # 启动保活线程
    alive_thread = threading.Thread(target=keep_alive, daemon=True)
    alive_thread.start()
    print("✅ 保活线程已启动")
    
    # 检查环境变量
    if os.environ.get('DEEPSEEK_API_KEY'):
        print("✅ DeepSeek API Key 已配置")
    else:
        print("❌ 未配置 DeepSeek API Key")
    
    if os.environ.get('RAILWAY_URL'):
        print(f"✅ RAILWAY_URL 已配置")
    else:
        print("❌ 未配置 RAILWAY_URL")
    
    print("="*50)
    print("📝 使用 # 触发AI对话")
    print("="*50)
    
    # 运行 NoneBot
    nonebot.run()
