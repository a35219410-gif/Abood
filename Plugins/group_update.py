import logging
from pyrogram import Client,filters
from pyrogram.types import Message
from config import r,Dev_Zaid
log=logging.getLogger("R3D.group")
@Client.on_message(filters.new_chat_members&filters.group,group=20)
async def bot_added(c,m:Message):
    me=await c.get_me()
    if not any(u.id==me.id for u in m.new_chat_members): return
    k=await r.get(f"{Dev_Zaid}:botkey") or "⇜";name=await r.get(f"{Dev_Zaid}:BotName") or "رعد"
    await m.reply(f"{k} مرحباً! أنا بوت {name}\n\nلتفعيلي: **تفعيل البوت**\nللأوامر: **الاوامر**\n☆")
