import os
import threading
import nonebot
from nonebot.adapters.onebot.v11 import Adapter as OneBotV11Adapter
from flask import Flask
from dotenv import load_dotenv

load_dotenv()

# 初始化 NoneBot
nonebot.init()

# 注册适配器
driver = nonebot.get_driver()
driver.register_adapter(OneBotV11Adapter)
nonebot.load_plugins("plugins")

# Flask 用不同端口
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot Running"

def run_nonebot():
    # 修改 NoneBot 端口
    os.environ['PORT'] = '8081'  # 让 NoneBot 用 8081
    nonebot.run()

def run_flask():
    port = int(os.environ.get('FLASK_PORT', 8080))
    app.run(host='0.0.0.0', port=port)

if __name__ == '__main__':
    # 分别启动在不同端口
    threading.Thread(target=run_nonebot, daemon=True).start()
    threading.Thread(target=run_flask).start()  # 主线程运行 Flask
