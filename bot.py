import os
import threading
from pathlib import Path
import nonebot
from nonebot.adapters.onebot.v11 import Adapter as OneBotV11Adapter
from flask import Flask
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

# Flask 用于保活
app = Flask(__name__)

@app.route('/')
def home():
    return "NoneBot QQ Robot is running!"

@app.route('/health')
def health():
    return "OK", 200

def run_nonebot():
    """运行 NoneBot"""
    nonebot.run()

if __name__ == '__main__':
    # 启动 NoneBot 在后台线程
    bot_thread = threading.Thread(target=run_nonebot, daemon=True)
    bot_thread.start()
    
    # 启动 Flask
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
