import logging,time,psutil,platform
from pyrogram import Client,filters
from pyrogram.types import Message
from config import r,Dev_Zaid,OWNER_ID
from helpers.Ranks import dev_pls
ST=time.time()
@Client.on_message(filters.text&filters.private,group=1)
async def priv(c,m:Message):
    if not m.from_user: return
    uid=m.from_user.id;text=m.text.strip();k=await r.get(f"{Dev_Zaid}:botkey") or "⇜"
    if text.lower() in("ping","بينق"):
        import time as _t;s=_t.monotonic();rep=await m.reply(f"{k} ...")
        e=(_t.monotonic()-s)*1000;up=int(_t.time()-ST);h,r_=divmod(up,3600);mi,s_=divmod(r_,60)
        return await rep.edit(f"🏓 Pong!\n• السرعة: `{e:.0f}ms`\n• وقت التشغيل: `{h}h {mi}m {s_}s`\n☆")
    if text in("السيرفر","الهوست"):
        if not await dev_pls(uid,0): return await m.reply(f"{k} Dev فقط")
        cpu=psutil.cpu_percent(1);mem=psutil.virtual_memory();disk=psutil.disk_usage("/")
        return await m.reply(f"💻 السيرفر:\n• CPU: `{cpu}%`\n• RAM: `{mem.percent}%`\n• Disk: `{disk.percent}%`\n• OS: `{platform.system()}`\n☆")
    if text.startswith("اسم البوت "):
        if uid!=OWNER_ID and not await dev_pls(uid,0): return
        await r.set(f"{Dev_Zaid}:BotName",text[10:].strip());return await m.reply(f"{k} تم ✅")
    if text.startswith("مفتاح البوت "):
        if uid!=OWNER_ID and not await dev_pls(uid,0): return
        await r.set(f"{Dev_Zaid}:botkey",text[12:].strip());return await m.reply("تم ✅")
    if text.startswith("قناة البوت "):
        if uid!=OWNER_ID and not await dev_pls(uid,0): return
        ch=text[11:].strip().replace("@","");await r.set(f"{Dev_Zaid}:BotChannel",ch);return await m.reply(f"{k} تم: @{ch} ✅")
    if text.startswith(("قناة اجبارية ","قناة إجبارية ")):
        if uid!=OWNER_ID and not await dev_pls(uid,0): return
        ch=text.split(None,2)[2].strip().replace("@","");await r.set(f"forceChannel:{Dev_Zaid}",ch)
        return await m.reply(f"{k} تم: @{ch} ✅")
    if text=="الغاء القناة الاجبارية":
        if uid!=OWNER_ID and not await dev_pls(uid,0): return
        await r.delete(f"forceChannel:{Dev_Zaid}");return await m.reply(f"{k} تم ✅")
@Client.on_message(filters.text&filters.group,group=50)
async def grp_admin(c,m:Message):
    if not m.from_user: return
    if not await r.get(f"{m.chat.id}:enable:{Dev_Zaid}"): return
    text=m.text.strip();name=await r.get(f"{Dev_Zaid}:BotName") or "رعد"
    if text.startswith(f"{name} "): text=text[len(name)+1:]
    k=await r.get(f"{Dev_Zaid}:botkey") or "⇜"
    if text.lower()=="ping":
        import time as _t;s=_t.monotonic();rep=await m.reply(f"{k} ...")
        return await rep.edit(f"🏓 {(_t.monotonic()-s)*1000:.0f}ms\n☆")
    # الاوامر تعالج في help.py
