import logging
from pyrogram import Client,filters
from pyrogram.types import Message
from config import r,Dev_Zaid
from helpers.Ranks import admin_pls,owner_pls,get_text_after_name
LM={"قفل الصوت":"lockVoice","قفل الفيديو":"lockVideo","قفل الصور":"lockPhoto","قفل الستيكرات":"lockStickers","قفل الGIF":"lockAnimations","قفل الملفات":"lockFiles","قفل الصوتيات":"lockAudios","قفل الروابط":"lockUrls","قفل الهاشتاق":"lockHashtags","قفل التاقات":"lockTags","قفل الشتائم":"lockSpam","قفل الطائفي":"lockSHTM","قفل الفارسي":"lockPersian","قفل التحويل":"lockForward","قفل الانلاين":"lockInline","قفل الاشعارات":"lockNot","قفل التعديل":"lockEdit","قفل تعديل الميديا":"lockEditM","قفل الاضافات":"lockaddContacts"}
UM={k.replace("قفل","فتح"):v for k,v in LM.items()}
@Client.on_message(filters.text&filters.group,group=5)
async def locks(c,m:Message):
    if not m.from_user: return
    if not await r.get(f"{m.chat.id}:enable:{Dev_Zaid}"): return
    text=await get_text_after_name(m.text,m.chat.id)
    k=await r.get(f"{Dev_Zaid}:botkey") or "⇜";uid=m.from_user.id;cid=m.chat.id
    if text in LM:
        if not await admin_pls(uid,cid): return await m.reply(f"{k} الادمن فقط")
        lk=f"{cid}:{LM[text]}:{Dev_Zaid}"
        if await r.get(lk): return await m.reply(f"{k} القفل مُفعّل أصلاً")
        await r.set(lk,1);return await m.reply(f"{k} تم القفل 🔒\n☆")
    if text in UM:
        if not await admin_pls(uid,cid): return await m.reply(f"{k} الادمن فقط")
        await r.delete(f"{cid}:{UM[text]}:{Dev_Zaid}");return await m.reply(f"{k} تم الفتح 🔓\n☆")
    if text=="قفل الكل":
        if not await owner_pls(uid,cid): return await m.reply(f"{k} المالك فقط")
        async with r.pipeline() as p: [p.set(f"{cid}:{v}:{Dev_Zaid}",1) for v in LM.values()];await p.execute()
        return await m.reply(f"{k} تم قفل كل شيء 🔒\n☆")
    if text=="فتح الكل":
        if not await owner_pls(uid,cid): return await m.reply(f"{k} المالك فقط")
        async with r.pipeline() as p: [p.delete(f"{cid}:{v}:{Dev_Zaid}") for v in LM.values()];await p.execute()
        return await m.reply(f"{k} تم فتح كل شيء 🔓\n☆")
    if text in("الاقفال","الأقفال"):
        lines=[f"{k} حالة الأقفال:"]
        for cmd,lv in LM.items():
            st="🔒" if await r.get(f"{cid}:{lv}:{Dev_Zaid}") else "🔓"
            lines.append(f"• {cmd.replace('قفل ','')}: {st}")
        return await m.reply("\n".join(lines))
