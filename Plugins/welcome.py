import logging
from datetime import datetime
import pytz
from pyrogram import Client,filters
from pyrogram.types import Message,ChatMemberUpdated
from pyrogram.enums import ChatMemberStatus
from config import r,Dev_Zaid
from helpers.Ranks import owner_pls,get_text_after_name,isLockCommand,is_muted
DW="لا تُسِئ اللفظ\n\nɴᴀᴍᴇ ⌯ {الاسم}\nᴜѕᴇʀɴᴀᴍᴇ ⌯ {اليوزر}\n𝖣𝖺𝗍𝖾 ⌯ {التاريخ}"
def fmt(tmpl,user,d):
    u=f"@{user.username}" if user.username else "لا يوزر"
    return tmpl.replace("{الاسم}",user.first_name or "").replace("{اليوزر}",u).replace("{التاريخ}",d).replace("{الايدي}",str(user.id))
@Client.on_chat_member_updated(filters.group)
async def welcome_new(c,u:ChatMemberUpdated):
    if not u.new_chat_member: return
    if not await r.get(f"{u.chat.id}:enable:{Dev_Zaid}"): return
    if not await r.get(f"{u.chat.id}:welcomeEnabled:{Dev_Zaid}"): return
    ns=u.new_chat_member.status;os_=u.old_chat_member.status if u.old_chat_member else None
    if ns not in{ChatMemberStatus.MEMBER,ChatMemberStatus.RESTRICTED}: return
    if os_ in{ChatMemberStatus.MEMBER,ChatMemberStatus.ADMINISTRATOR}: return
    user=u.new_chat_member.user
    if user.is_bot: return
    d=datetime.now(pytz.timezone("Asia/Riyadh")).strftime("%d/%m/%Y")
    tmpl=await r.get(f"{u.chat.id}:welcomeText:{Dev_Zaid}") or DW
    try: await c.send_message(u.chat.id,fmt(tmpl,user,d))
    except Exception as e: pass
@Client.on_message(filters.text&filters.group,group=29)
async def welcome_cmds(c,m:Message):
    if not m.from_user: return
    if not await r.get(f"{m.chat.id}:enable:{Dev_Zaid}"): return
    if await is_muted(m.from_user.id,m.chat.id): return
    text=await get_text_after_name(m.text,m.chat.id)
    if await isLockCommand(m.from_user.id,m.chat.id,text): return
    k=await r.get(f"{Dev_Zaid}:botkey") or "⇜";uid=m.from_user.id;cid=m.chat.id
    if text=="تفعيل الترحيب":
        if not await owner_pls(uid,cid): return await m.reply(f"{k} المالك فقط")
        await r.set(f"{cid}:welcomeEnabled:{Dev_Zaid}",1);return await m.reply(f"{k} تم تفعيل الترحيب ✅\n☆")
    if text=="تعطيل الترحيب":
        if not await owner_pls(uid,cid): return await m.reply(f"{k} المالك فقط")
        await r.delete(f"{cid}:welcomeEnabled:{Dev_Zaid}");return await m.reply(f"{k} تم ✅\n☆")
    if text=="الترحيب":
        tmpl=await r.get(f"{cid}:welcomeText:{Dev_Zaid}") or DW
        st="✅" if await r.get(f"{cid}:welcomeEnabled:{Dev_Zaid}") else "❌"
        return await m.reply(f"{k} الترحيب ({st}):\n\n{tmpl}\n\nالمتغيرات: {{الاسم}} {{اليوزر}} {{التاريخ}} {{الايدي}}")
    if text=="تعيين الترحيب":
        if not await owner_pls(uid,cid): return await m.reply(f"{k} المالك فقط")
        await r.set(f"{cid}:settingWelcome:{uid}{Dev_Zaid}",1,ex=120);return await m.reply(f"{k} أرسل رسالة الترحيب")
    if await r.get(f"{cid}:settingWelcome:{uid}{Dev_Zaid}"):
        if text=="الغاء": await r.delete(f"{cid}:settingWelcome:{uid}{Dev_Zaid}");return await m.reply(f"{k} إلغاء")
        await r.delete(f"{cid}:settingWelcome:{uid}{Dev_Zaid}");await r.set(f"{cid}:welcomeText:{Dev_Zaid}",text)
        return await m.reply(f"{k} تم تعيين الترحيب ✅\n☆")
    if text=="القوانين":
        rules=await r.get(f"{cid}:rules:{Dev_Zaid}")
        return await m.reply(f"📜 القوانين:\n\n{rules}" if rules else f"{k} لا توجد قوانين")
    if text=="تعيين القوانين":
        if not await owner_pls(uid,cid): return await m.reply(f"{k} المالك فقط")
        await r.set(f"{cid}:settingRules:{uid}{Dev_Zaid}",1,ex=300);return await m.reply(f"{k} أرسل القوانين")
    if await r.get(f"{cid}:settingRules:{uid}{Dev_Zaid}"):
        if text=="الغاء": await r.delete(f"{cid}:settingRules:{uid}{Dev_Zaid}");return await m.reply(f"{k} إلغاء")
        await r.delete(f"{cid}:settingRules:{uid}{Dev_Zaid}");await r.set(f"{cid}:rules:{Dev_Zaid}",text)
        return await m.reply(f"{k} تم تعيين القوانين ✅\n☆")
    if text=="حذف القوانين":
        if not await owner_pls(uid,cid): return await m.reply(f"{k} المالك فقط")
        await r.delete(f"{cid}:rules:{Dev_Zaid}");return await m.reply(f"{k} تم ✅")
