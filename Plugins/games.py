import asyncio,logging,random
from pyrogram import Client,filters
from pyrogram.types import Message
from config import r,Dev_Zaid
from helpers.Ranks import admin_pls,is_muted,get_text_after_name,isLockCommand
from helpers.games import get_emoji_bank,get_word_game_words
@Client.on_message(filters.text&filters.group,group=33)
async def games(c,m:Message):
    if not m.from_user: return
    if not await r.get(f"{m.chat.id}:enable:{Dev_Zaid}"): return
    if await r.get(f"{m.chat.id}:disableGames:{Dev_Zaid}"): return
    if await is_muted(m.from_user.id,m.chat.id): return
    text=await get_text_after_name(m.text,m.chat.id)
    if await isLockCommand(m.from_user.id,m.chat.id,text): return
    k=await r.get(f"{Dev_Zaid}:botkey") or "⇜";uid=m.from_user.id;cid=m.chat.id;mention=m.from_user.mention
    if text in("فلوسي","رصيدي"):
        fl=int(await r.get(f"{uid}:Floos") or 0)
        return await m.reply(f"「 {mention} 」\n{k} رصيدك: `{fl:,}` ريال {get_emoji_bank(fl)}\n☆")
    if text=="لعبة الكلمات":
        if await r.get(f"{cid}:wordgame:{Dev_Zaid}"):
            w=await r.get(f"{cid}:wordgame_word:{Dev_Zaid}");return await m.reply(f"{k} اللعبة جارية! ||{w}||")
        chosen=random.choice(get_word_game_words());sh=list(chosen);random.shuffle(sh)
        await r.set(f"{cid}:wordgame:{Dev_Zaid}",1,ex=120);await r.set(f"{cid}:wordgame_word:{Dev_Zaid}",chosen,ex=120)
        return await m.reply(f"{k} 🎮 لعبة الكلمات!\n\nرتّب: **{'  '.join(sh)}**\n\nعندك دقيقتين!")
    if await r.get(f"{cid}:wordgame:{Dev_Zaid}"):
        correct=await r.get(f"{cid}:wordgame_word:{Dev_Zaid}")
        if correct and text==correct:
            await r.delete(f"{cid}:wordgame:{Dev_Zaid}");await r.delete(f"{cid}:wordgame_word:{Dev_Zaid}")
            rw=random.randint(50,200);cur=int(await r.get(f"{uid}:Floos") or 0);await r.set(f"{uid}:Floos",cur+rw)
            return await m.reply(f"🎉 صح! {mention} عرف **{correct}**\nالجائزة: `{rw}` ريال 💸\n☆")
    if text=="تعطيل الالعاب":
        if not await admin_pls(uid,cid): return await m.reply(f"{k} الادمن فقط")
        await r.set(f"{cid}:disableGames:{Dev_Zaid}",1);return await m.reply(f"{k} تم ✅")
    if text=="تفعيل الالعاب":
        if not await admin_pls(uid,cid): return await m.reply(f"{k} الادمن فقط")
        await r.delete(f"{cid}:disableGames:{Dev_Zaid}");return await m.reply(f"{k} تم ✅")
@Client.on_message(filters.dice&filters.group,group=45)
async def dice(c,m:Message):
    if not m.from_user: return
    if await r.get(f"{m.chat.id}:disableGames:{Dev_Zaid}"): return
    if await is_muted(m.from_user.id,m.chat.id): return
    if m.dice.emoji=="🎲":
        k=await r.get(f"{Dev_Zaid}:botkey") or "⇜";uid=m.from_user.id
        await asyncio.sleep(3)  # FIX: كان time.sleep(3)
        if m.dice.value==6:
            cur=int(await r.get(f"{uid}:Floos") or 0);new=cur+100;await r.set(f"{uid}:Floos",new)
            return await m.reply(f"صح عليك فزت بالنرد ✔\n💸 فلوسك: `{new:,}` ريال\n☆")
        return await m.reply(f"{k} للأسف خسرت 😔")
