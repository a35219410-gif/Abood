import logging
from pyrogram import Client,filters
from pyrogram.types import Message
from config import r,Dev_Zaid,OWNER_ID
from helpers.Ranks import admin_pls,mod_pls,owner_pls,gowner_pls,dev_pls,get_rank,get_text_after_name,isLockCommand
RK={"مميز":"rankPRE","ادمن":"rankADMIN","المدير":"rankMOD","المالك":"rankOWNER","المالك الاساسي":"rankGOWNER"}
RQ={"rankPRE":admin_pls,"rankADMIN":mod_pls,"rankMOD":owner_pls,"rankOWNER":gowner_pls,"rankGOWNER":dev_pls}
@Client.on_message(filters.text&filters.group,group=7)
async def ranks(c,m:Message):
    if not m.from_user: return
    if not await r.get(f"{m.chat.id}:enable:{Dev_Zaid}"): return
    text=await get_text_after_name(m.text,m.chat.id)
    if await isLockCommand(m.from_user.id,m.chat.id,text): return
    k=await r.get(f"{Dev_Zaid}:botkey") or "⇜";uid=m.from_user.id;cid=m.chat.id
    if text=="رتبتي": return await m.reply(f"「 {m.from_user.mention} 」\n{k} رتبتك: {await get_rank(uid,cid)}\n☆")
    rep=m.reply_to_message;t=rep.from_user if rep and rep.from_user else None
    for rn,rk in RK.items():
        if text==f"رفع {rn}" and t:
            if not await RQ[rk](uid,cid): return await m.reply(f"{k} ما عندك صلاحية رفع {rn}")
            await r.set(f"{cid}:{rk}:{t.id}{Dev_Zaid}",1)
            return await m.reply(f"「 {t.mention} 」\n{k} تم الرفع إلى {rn} | {await get_rank(t.id,cid)}\n☆")
        if text==f"تنزيل {rn}" and t:
            if not await RQ[rk](uid,cid): return await m.reply(f"{k} ما عندك صلاحية تنزيل {rn}")
            await r.delete(f"{cid}:{rk}:{t.id}{Dev_Zaid}")
            return await m.reply(f"「 {t.mention} 」\n{k} تم تنزيل {rn}\n☆")
    if text=="رفع Dev" and t:
        if uid!=OWNER_ID: return await m.reply(f"{k} مالك البوت فقط")
        await r.set(f"{t.id}:rankDEV:{Dev_Zaid}",1);return await m.reply(f"「 {t.mention} 」\n{k} تم الرفع إلى Dev🎖️\n☆")
    if text=="تنزيل Dev" and t:
        if uid!=OWNER_ID: return await m.reply(f"{k} مالك البوت فقط")
        await r.delete(f"{t.id}:rankDEV:{Dev_Zaid}");return await m.reply(f"「 {t.mention} 」\n{k} تم تنزيل Dev\n☆")
    if text=="تعطيل الرفع":
        if not await owner_pls(uid,cid): return await m.reply(f"{k} المالك فقط")
        await r.set(f"{cid}:disableRanks:{Dev_Zaid}",1);return await m.reply(f"{k} تم ✅")
    if text=="تفعيل الرفع":
        if not await owner_pls(uid,cid): return await m.reply(f"{k} المالك فقط")
        await r.delete(f"{cid}:disableRanks:{Dev_Zaid}");return await m.reply(f"{k} تم ✅")
