import logging
from pyrogram import Client,filters
from pyrogram.types import Message
from config import r,Dev_Zaid
from helpers.Ranks import admin_pls,mod_pls,owner_pls,dev_pls,get_rank,get_text_after_name,isLockCommand
log=logging.getLogger("R3D.mute")
@Client.on_message(filters.text&filters.group,group=14)
async def mutes(c,m:Message):
    if not m.from_user: return
    if not await r.get(f"{m.chat.id}:enable:{Dev_Zaid}"): return
    if await r.get(f"{m.chat.id}:mute:{Dev_Zaid}") and not await admin_pls(m.from_user.id,m.chat.id): return
    if await r.get(f"{m.from_user.id}:mute:{m.chat.id}{Dev_Zaid}"): return
    if await r.get(f"{m.from_user.id}:mute:{Dev_Zaid}"): return
    text=await get_text_after_name(m.text,m.chat.id)
    if await isLockCommand(m.from_user.id,m.chat.id,text): return
    k=await r.get(f"{Dev_Zaid}:botkey") or "⇜";uid=m.from_user.id;cid=m.chat.id
    async def reply(msg): return await m.reply(msg)
    rep=m.reply_to_message
    t=rep.from_user if rep and rep.from_user else None
    if text=="كتم" and t:
        if not await admin_pls(uid,cid): return await reply(f"{k} الادمن فقط")
        if await admin_pls(t.id,cid): return await reply(f"{k} ما اقدر اكتم ادمن")
        await r.set(f"{t.id}:mute:{cid}{Dev_Zaid}",1)
        return await reply(f"「 {t.mention} 」\n{k} تم الكتم | الرتبه: {await get_rank(t.id,cid)}\n☆")
    if text=="رفع الكتم" and t:
        if not await admin_pls(uid,cid): return await reply(f"{k} الادمن فقط")
        await r.delete(f"{t.id}:mute:{cid}{Dev_Zaid}")
        return await reply(f"「 {t.mention} 」\n{k} تم رفع الكتم ✅\n☆")
    if text in("كتم المجموعة","كتم الجروب"):
        if not await owner_pls(uid,cid): return await reply(f"{k} المالك فقط")
        await r.set(f"{cid}:mute:{Dev_Zaid}",1);return await reply(f"{k} تم كتم المجموعة 🔇\n☆")
    if text in("رفع كتم المجموعة","رفع كتم الجروب"):
        if not await owner_pls(uid,cid): return await reply(f"{k} المالك فقط")
        await r.delete(f"{cid}:mute:{Dev_Zaid}");return await reply(f"{k} تم رفع الكتم 🔊\n☆")
    if text=="طرد" and t:
        if not await admin_pls(uid,cid): return await reply(f"{k} الادمن فقط")
        if await admin_pls(t.id,cid): return await reply(f"{k} ما اقدر أطرد ادمن")
        try: await c.ban_chat_member(cid,t.id);await c.unban_chat_member(cid,t.id);return await reply(f"「 {t.mention} 」\n{k} تم الطرد 👋\n☆")
        except Exception as e: return await reply(f"{k} فشل: {e}")
    if text=="حظر" and t:
        if not await mod_pls(uid,cid): return await reply(f"{k} المدير فقط")
        if await admin_pls(t.id,cid): return await reply(f"{k} ما اقدر أحظر ادمن")
        try: await c.ban_chat_member(cid,t.id);await r.set(f"{t.id}:ban:{cid}{Dev_Zaid}",1);return await reply(f"「 {t.mention} 」\n{k} تم الحظر 🚫\n☆")
        except Exception as e: return await reply(f"{k} فشل: {e}")
    if text=="رفع الحظر" and t:
        if not await mod_pls(uid,cid): return await reply(f"{k} المدير فقط")
        try: await c.unban_chat_member(cid,t.id);await r.delete(f"{t.id}:ban:{cid}{Dev_Zaid}");return await reply(f"「 {t.mention} 」\n{k} تم رفع الحظر ✅\n☆")
        except Exception as e: return await reply(f"{k} فشل: {e}")
    if text=="حظر عام" and t:
        if not await dev_pls(uid,cid): return await reply(f"{k} Dev فقط")
        await r.set(f"{t.id}:gban:{Dev_Zaid}",1);return await reply(f"「 {t.mention} 」\n{k} حظر عام 🚫\n☆")
    if text=="رفع الحظر العام" and t:
        if not await dev_pls(uid,cid): return await reply(f"{k} Dev فقط")
        await r.delete(f"{t.id}:gban:{Dev_Zaid}");return await reply(f"「 {t.mention} 」\n{k} تم رفع الحظر العام ✅\n☆")
    if text=="تفعيل البوت":
        if not await owner_pls(uid,cid): return await reply(f"{k} المالك فقط")
        await r.set(f"{cid}:enable:{Dev_Zaid}",1);return await reply(f"{k} تم تفعيل البوت ✅\n☆")
    if text=="تعطيل البوت":
        if not await owner_pls(uid,cid): return await reply(f"{k} المالك فقط")
        await r.delete(f"{cid}:enable:{Dev_Zaid}");return await reply(f"{k} تم تعطيل البوت ✅\n☆")
    if text=="تعطيل التحذير":
        if not await owner_pls(uid,cid): return await reply(f"{k} المالك فقط")
        await r.set(f"{cid}:disableWarn:{Dev_Zaid}",1);return await reply(f"{k} تم ✅")
    if text=="تفعيل التحذير":
        if not await owner_pls(uid,cid): return await reply(f"{k} المالك فقط")
        await r.delete(f"{cid}:disableWarn:{Dev_Zaid}");return await reply(f"{k} تم ✅")
