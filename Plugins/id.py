import logging,random
from pyrogram import Client,filters
from pyrogram.types import Message
from config import r,Dev_Zaid
from helpers.Ranks import get_rank,get_text_after_name,isLockCommand,is_muted
from helpers.get_create import get_creation_date
from helpers.games import get_emoji_bank
TEMPS=["- ᴜѕᴇʀɴᴀᴍᴇ ➣ {اليوزر}\n- ᴍѕɢѕ ➣ {الرسائل}\n- ѕᴛᴀᴛѕ ➣ {الرتبه}\n- ɪᴅ ➣ {الايدي}\n{البايو}","• USE ➣ {اليوزر}\n• MSG ➣ {الرسائل}\n• STA ➣ {الرتبه}\n• iD ➣ {الايدي}\n{البايو}","⌁ NaMe ⇨ {الاسم}\n⌁ Use ⇨ {اليوزر}\n⌁ Msg ⇨ {الرسائل}\n⌁ Sta ⇨ {الرتبه}\n⌁ iD ⇨ {الايدي}\n{البايو}","- الايـدي || {الايدي}\n• الاسـم  || {الاسم}\n• المُعرف || {اليوزر}\n• الرُتبـه || {الرتبه}\n• الرسائل || {الرسائل}\n{البايو}"]
CMS=["تيكفه لاتكتب ايدي","يع","جبر","احلى من يكتب ايدي","ازق ايدي","للأسف ايديك تلوث بصري"]
@Client.on_message(filters.group,group=9)
async def count(c,m:Message):
    if m.from_user and not await is_muted(m.from_user.id,m.chat.id): await r.incr(f"{Dev_Zaid}{m.chat.id}:TotalMsgs:{m.from_user.id}")
@Client.on_message(filters.text&filters.group,group=11)
async def id_h(c,m:Message):
    if not m.from_user: return
    if not await r.get(f"{m.chat.id}:enable:{Dev_Zaid}"): return
    if await is_muted(m.from_user.id,m.chat.id): return
    text=await get_text_after_name(m.text,m.chat.id)
    if await isLockCommand(m.from_user.id,m.chat.id,text): return
    k=await r.get(f"{Dev_Zaid}:botkey") or "⇜";cid=m.chat.id
    if text=="ايدي":
        if random.random()<0.1: return await m.reply(random.choice(CMS))
        rep=m.reply_to_message;target=rep.from_user if rep and rep.from_user else m.from_user
        try: full=await c.get_users(target.id);bio=full.bio or ""
        except: bio=""
        msgs=int(await r.get(f"{Dev_Zaid}{cid}:TotalMsgs:{target.id}") or 0)
        rank=await get_rank(target.id,cid);uname=f"@{target.username}" if target.username else "لا يوزر"
        fl=int(await r.get(f"{target.id}:Floos") or 0);created=get_creation_date(target.id)
        tmpl=random.choice(TEMPS);bio_line=f"• البايو: {bio}" if bio else ""
        txt=tmpl.format(**{"اليوزر":uname,"الرسائل":f"{msgs:,}","الرتبه":rank,"الايدي":str(target.id),"الاسم":target.first_name or "","البايو":bio_line}).strip()
        return await m.reply(f"「 {target.mention} 」\n{k}\n{txt}\n• أُنشئ: {created}\n☆",disable_web_page_preview=True)
    if text in("ايدي المجموعة","ايدي الجروب"): return await m.reply(f"{k} معرّف المجموعة: `{cid}`\n☆")
