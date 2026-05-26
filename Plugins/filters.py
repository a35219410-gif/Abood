import logging
from pyrogram import Client,filters
from pyrogram.types import Message
from config import r,Dev_Zaid
from helpers.Ranks import admin_pls,owner_pls,is_muted
@Client.on_message(filters.group,group=24)
async def filter_h(c,m:Message):
    if not m.from_user: return
    if not await r.get(f"{m.chat.id}:enable:{Dev_Zaid}"): return
    if await is_muted(m.from_user.id,m.chat.id): return
    uid=m.from_user.id;cid=m.chat.id;text=m.text or "";k=await r.get(f"{Dev_Zaid}:botkey") or "⇜"
    if await r.get(f"{cid}:addFilter:{uid}{Dev_Zaid}"):
        if text=="الغاء": await r.delete(f"{cid}:addFilter:{uid}{Dev_Zaid}");return await m.reply(f"{k} إلغاء ✅")
        if not await r.get(f"{cid}:addFilterWord:{uid}{Dev_Zaid}"):
            await r.set(f"{cid}:addFilterWord:{uid}{Dev_Zaid}",text,ex=300);return await m.reply(f"{k} الكلمة: **{text}**\nأرسل الرد")
        trigger=await r.get(f"{cid}:addFilterWord:{uid}{Dev_Zaid}")
        await r.set(f"{cid}:Filter:{Dev_Zaid}:{trigger}",text)
        await r.delete(f"{cid}:addFilter:{uid}{Dev_Zaid}");await r.delete(f"{cid}:addFilterWord:{uid}{Dev_Zaid}")
        return await m.reply(f"{k} تم إضافة الفلتر ✅\nعند «{trigger}» سيظهر الرد")
    if await r.get(f"{cid}:delFilter:{uid}{Dev_Zaid}"):
        if text=="الغاء": await r.delete(f"{cid}:delFilter:{uid}{Dev_Zaid}");return await m.reply(f"{k} إلغاء ✅")
        key=f"{cid}:Filter:{Dev_Zaid}:{text}"
        if await r.get(key): await r.delete(key);await r.delete(f"{cid}:delFilter:{uid}{Dev_Zaid}");return await m.reply(f"{k} تم ✅")
        return await m.reply(f"{k} ما وجدت")
    if text in("إضافة فلتر","اضافة فلتر"):
        if not await admin_pls(uid,cid): return await m.reply(f"{k} الادمن فقط")
        await r.set(f"{cid}:addFilter:{uid}{Dev_Zaid}",1,ex=300);return await m.reply(f"{k} أرسل الكلمة المشغِّلة")
    if text=="حذف فلتر":
        if not await admin_pls(uid,cid): return await m.reply(f"{k} الادمن فقط")
        await r.set(f"{cid}:delFilter:{uid}{Dev_Zaid}",1,ex=300);return await m.reply(f"{k} أرسل اسم الفلتر")
    if text in("الفلاتر","قائمة الفلاتر"):
        keys=[]
        async for key in r.scan_iter(f"{cid}:Filter:{Dev_Zaid}:*"): keys.append(f"• {key.split(f'{cid}:Filter:{Dev_Zaid}:')[-1]}")
        if not keys: return await m.reply(f"{k} لا توجد فلاتر")
        return await m.reply(f"{k} الفلاتر:\n"+"\n".join(keys))
    if text=="حذف كل الفلاتر":
        if not await owner_pls(uid,cid): return await m.reply(f"{k} المالك فقط")
        async for key in r.scan_iter(f"{cid}:Filter:{Dev_Zaid}:*"): await r.delete(key)
        return await m.reply(f"{k} تم ✅")
    fr=await r.get(f"{cid}:Filter:{Dev_Zaid}:{text}")
    if fr: await m.reply(fr)
