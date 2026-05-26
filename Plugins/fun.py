import asyncio,logging,random
from gtts import gTTS
from pyrogram import Client,filters
from pyrogram.types import Message
from config import r,Dev_Zaid
from helpers.Ranks import admin_pls,get_text_after_name,isLockCommand,is_muted
from helpers.utils import cleanup_file
@Client.on_message(filters.text&filters.group,group=34)
async def fun(c,m:Message):
    if not m.from_user: return
    if await r.get(f"{m.chat.id}:disableFun:{Dev_Zaid}"): return
    if not await r.get(f"{m.chat.id}:enable:{Dev_Zaid}"): return
    if await is_muted(m.from_user.id,m.chat.id): return
    text=await get_text_after_name(m.text,m.chat.id)
    if await isLockCommand(m.from_user.id,m.chat.id,text): return
    k=await r.get(f"{Dev_Zaid}:botkey") or "⇜";uid=m.from_user.id;cid=m.chat.id
    rep=m.reply_to_message;t=rep.from_user if rep and rep.from_user else None
    if text in("رفع كيك","رفع كيكه","رفع كيكة") and t:
        if await r.sismember(f"{Dev_Zaid}:CakeList:{cid}",t.id): return await m.reply(f"「 {t.mention} 」\n{k} رُفعت له كيكة من قبل 🍰\n☆")
        await r.sadd(f"{Dev_Zaid}:CakeList:{cid}",t.id);await r.set(f"{Dev_Zaid}:CakeName:{t.id}",t.first_name or "")
        return await m.reply(f"「 {t.mention} 」\n{k} ابشر رفعتله كيكة 🍰\n☆")
    if text in("رفع كيك","رفع كيكه","رفع كيكة"): return await m.reply(f"{k} رد على رسالة شخص")
    if text in("قائمة الكيك","كيكات"):
        mbs=await r.smembers(f"{Dev_Zaid}:CakeList:{cid}")
        if not mbs: return await m.reply(f"{k} قائمة الكيك فارغة!")
        lines=[f"{k} 🍰 قائمة الكيك:"]
        for mid in mbs: lines.append(f"• {await r.get(f'{Dev_Zaid}:CakeName:{mid}') or mid}")
        return await m.reply("\n".join(lines))
    if text in("حذف كيك","حذف كيكه","حذف كيكة") and t:
        if await r.sismember(f"{Dev_Zaid}:CakeList:{cid}",t.id):
            await r.srem(f"{Dev_Zaid}:CakeList:{cid}",t.id);await r.delete(f"{Dev_Zaid}:CakeName:{t.id}")
            return await m.reply(f"「 {t.mention} 」\n{k} تم الحذف ✅\n☆")
    if text.startswith("صوّت "):
        phrase=text[5:].strip()
        if not phrase: return await m.reply(f"{k} أرسل النص")
        if len(phrase)>200: return await m.reply(f"{k} النص طويل (الحد 200)")
        import os;path=f"tts_{uid}_{cid}.mp3"
        try:
            await asyncio.get_event_loop().run_in_executor(None,lambda:gTTS(text=phrase,lang="ar",slow=False).save(path))
            await c.send_voice(cid,path,reply_to_message_id=m.id)
        except: await m.reply(f"{k} فشل")
        finally: cleanup_file(path)
        return
    if text in("التاريخ الهجري","اليوم"):
        try:
            from hijri_converter import Gregorian;from datetime import date
            today=date.today();h=Gregorian(today.year,today.month,today.day).to_hijri()
            days=["الاثنين","الثلاثاء","الأربعاء","الخميس","الجمعة","السبت","الأحد"]
            months=["","محرم","صفر","ربيع الأول","ربيع الثاني","جمادى الأولى","جمادى الآخرة","رجب","شعبان","رمضان","شوال","ذو القعدة","ذو الحجة"]
            return await m.reply(f"📅 التاريخ:\n• الميلادي: {today.strftime('%d/%m/%Y')}\n• الهجري: {h.day} {months[h.month]} {h.year} هـ\n• اليوم: {days[today.weekday()]}")
        except: return await m.reply(f"{k} خطأ")
    if text=="تعطيل المرح":
        if not await admin_pls(uid,cid): return await m.reply(f"{k} الادمن فقط")
        await r.set(f"{cid}:disableFun:{Dev_Zaid}",1);return await m.reply(f"{k} تم 😐")
    if text=="تفعيل المرح":
        if not await admin_pls(uid,cid): return await m.reply(f"{k} الادمن فقط")
        await r.delete(f"{cid}:disableFun:{Dev_Zaid}");return await m.reply(f"{k} تم 😄")
