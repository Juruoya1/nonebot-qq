from nonebot import on_message
from nonebot.adapters.onebot.v11 import MessageEvent, Bot
from nonebot.params import EventMessage
import aiohttp
import os
import json
from typing import Dict

# 存储对话历史
conversations: Dict[str, list] = {}

# 匹配所有消息
ai = on_message(priority=10)

@ai.handle()
async def handle_ai(bot: Bot, event: MessageEvent):
    # 获取消息内容
    msg = event.get_plaintext().strip()
    
    # 检查是否以 # 开头
    if not msg.startswith('#'):
        return
    
    # 去掉 # 号
    question = msg[1:].strip()
    if not question:
        await ai.finish("❌ 你想问什么？")
        return
    
    # 获取会话ID（群聊或私聊）
    if event.group_id:
        session_id = f"group_{event.group_id}"
    else:
        session_id = f"private_{event.user_id}"
    
    # 发送"正在思考"
    await ai.send("🤔 小深正在思考中...")
    
    # 调用DeepSeek API
    answer = await call_deepseek(question, session_id)
    
    # 发送回复
    await ai.finish(f"🤖 {answer}")

async def call_deepseek(question: str, session_id: str) -> str:
    """调用DeepSeek API"""
    api_key = os.environ.get('DEEPSEEK_API_KEY')
    if not api_key:
        return "❌ 未配置API Key"
    
    # 获取对话历史
    history = conversations.get(session_id, [])
    
    # 构建消息列表
    messages = [
        {"role": "system", "content": "你是一个友好的QQ机器人，回答简洁有趣，可以用表情符号。"}
    ]
    
    # 添加最近3轮对话
    for msg in history[-3:]:
        messages.append(msg)
    
    # 添加当前问题
    messages.append({"role": "user", "content": question})
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                'https://api.deepseek.com/v1/chat/completions',
                headers={
                    'Authorization': f'Bearer {api_key}',
                    'Content-Type': 'application/json'
                },
                json={
                    'model': 'deepseek-chat',
                    'messages': messages,
                    'temperature': 0.7,
                    'max_tokens': 1000
                },
                timeout=30
            ) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    answer = data['choices'][0]['message']['content']
                    
                    # 保存到历史
                    conversations.setdefault(session_id, [])
                    conversations[session_id].append({"role": "user", "content": question})
                    conversations[session_id].append({"role": "assistant", "content": answer})
                    
                    # 保持历史不超过10条
                    if len(conversations[session_id]) > 10:
                        conversations[session_id] = conversations[session_id][-10:]
                    
                    return answer
                else:
                    error = await resp.text()
                    return f"❌ API错误: {resp.status}"
    except Exception as e:
        return f"❌ 请求失败: {str(e)}"
