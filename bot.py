#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import yaml
import json
from pathlib import Path
import nonebot
from nonebot.adapters.onebot.v11 import Adapter as OneBotV11Adapter

# 加载环境变量
from dotenv import load_dotenv
load_dotenv()

# 初始化NoneBot
nonebot.init()

# 注册适配器
driver = nonebot.get_driver()
driver.register_adapter(OneBotV11Adapter)

# 加载插件（会自动加载plugins目录下的插件）
nonebot.load_plugins("plugins")

# 创建Flask应用用于保活
from flask import Flask
app = Flask(__name__)

@app.route('/')
def home():
    return "NoneBot QQ Robot is running with DeepSeek!"

@app.route('/health')
def health():
    return "OK", 200

if __name__ == '__main__':
    # 启动NoneBot
    import threading
    threading.Thread(target=nonebot.run, daemon=True).start()
    
    # 启动Flask
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
