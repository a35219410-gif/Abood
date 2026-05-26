import asyncio,logging
from pyrogram import Client,filters
from pyrogram.types import Message,InlineKeyboardMarkup,InlineKeyboardButton
from pyrogram.enums import ChatMemberStatus
from pyrogram.errors import UserNotParticipant,FloodWait
from config import r,Dev_Zaid
from helpers.Ranks import admin_pls,pre_pls,BAD_WORDS,SECTARIAN_WORDS,contains_bad_word
from helpers.utils import find_urls,contains_persian
log=logging.getLogger("R3D.all")
@Client.on_message(filters.group,group=-1111111111)
async def check_force(c,m:Message):
    if not m.from_user or not m.text: return m.continue_propagation()
    text=m.text;name=await r.get(f"{Dev_Zaid}:BotName") or "رعد"
    if text.startswith(f"{name} "): text=text[len(name)+1:]
    if not(any(text.startswith(p) for p in("تفعيل ","تعطيل ","قفل ","فتح ")) or text in("ايدي","الاوامر")): return m.continue_propagation()
    force=await r.get(f"forceChannel:{Dev_Zaid}")
    if not force or await r.get(f"disableSubscribe:{Dev_Zaid}"): return m.continue_propagation()
    if await r.get(f"inDontCheck:{Dev_Zaid}"): return m.continue_propagation()
    username=force.replace("@","")
    try:
        member=await c.get_chat_member(username,m.from_user.id)
        if member.status in{ChatMemberStatus.LEFT,ChatMemberStatus.BANNED}: raise UserNotParticipant
    except FloodWait as e: await asyncio.sleep(e.value);return m.continue_propagation()
    except UserNotParticipant:
        btn=InlineKeyboardMarkup([[InlineKeyboardButton("اضغط هنا",url=f"https://t.me/{username}")]])
        await m.reply(f"انضم للقناة @{username} لاستخدام البوت",reply_markup=btn)
        await r.set(f"inDontCheck:{Dev_Zaid}",1,ex=10);return m.stop_propagation()
    except Exception as e: log.warning(e);return m.continue_propagation()
    return m.continue_propagation()
@Client.on_message(filters.group,group=27)
async def guard(c,m:Message):
    if not await r.get(f"{m.chat.id}:enable:{Dev_Zaid}"): return
    if m.sender_chat: uid=m.sender_chat.id;mention=m.sender_chat.title;is_admin=is_pre=False
    elif m.from_user: uid=m.from_user.id;mention=m.from_user.mention;is_admin=await admin_pls(uid,m.chat.id);is_pre=await pre_pls(uid,m.chat.id)
    else: return
    k=await r.get(f"{Dev_Zaid}:botkey") or "⇜";sw=not await r.get(f"{m.chat.id}:disableWarn:{Dev_Zaid}");wcd=f"{Dev_Zaid}:inWARN:{uid}{m.chat.id}"
    async def warn(r_):
        await m.delete()
        if sw and not await r.get(wcd): await r.set(wcd,1,ex=60);await m.reply(f"「 {mention} 」\n{k} ممنوع {r_}\n☆",disable_web_page_preview=True)
    if await r.get(f"{m.chat.id}:lockNot:{Dev_Zaid}") and m.service: await m.delete();return
    if await r.get(f"{m.chat.id}:lockVoice:{Dev_Zaid}") and m.voice and not is_admin: await warn("الصوتيات");return
    if await r.get(f"{m.chat.id}:lockVideo:{Dev_Zaid}") and m.video and not is_admin: await warn("الفيديو");return
    if await r.get(f"{m.chat.id}:lockPhoto:{Dev_Zaid}") and m.photo and not is_admin: await warn("الصور");return
    if await r.get(f"{m.chat.id}:lockStickers:{Dev_Zaid}") and m.sticker and not is_admin: await warn("الستيكرات");return
    if await r.get(f"{m.chat.id}:lockAnimations:{Dev_Zaid}") and m.animation and not is_admin: await warn("GIF");return
    if await r.get(f"{m.chat.id}:lockFiles:{Dev_Zaid}") and m.document and not m.animation and not is_admin: await warn("الملفات");return
    if await r.get(f"{m.chat.id}:lockAudios:{Dev_Zaid}") and m.audio and not is_admin: await warn("الصوتيات");return
    if await r.get(f"{m.chat.id}:lockForward:{Dev_Zaid}") and m.forward_date and not is_admin: await warn("التحويل");return
    if await r.get(f"{m.chat.id}:lockInline:{Dev_Zaid}") and m.via_bot and not is_admin: await warn("الانلاين");return
    if m.text:
        t=m.text
        if await r.get(f"{m.chat.id}:lockUrls:{Dev_Zaid}") and find_urls(t) and not is_admin: await warn("الروابط");return
        if await r.get(f"{m.chat.id}:lockHashtags:{Dev_Zaid}") and "#" in t and not is_admin: await warn("الهاشتاقات");return
        if await r.get(f"{m.chat.id}:lockTags:{Dev_Zaid}") and "@" in t and not is_admin: await warn("التاقات");return
        if await r.get(f"{m.chat.id}:lockSpam:{Dev_Zaid}") and contains_bad_word(t,BAD_WORDS) and not is_pre: await warn("الشتائم");return
        if await r.get(f"{m.chat.id}:lockSHTM:{Dev_Zaid}") and contains_bad_word(t,SECTARIAN_WORDS) and not is_admin: await warn("الطائفي");return
        if await r.get(f"{m.chat.id}:lockPersian:{Dev_Zaid}") and contains_persian(t) and not is_admin: await warn("الفارسي");return
@Client.on_edited_message(filters.group,group=27)
async def guard_edit(c,m:Message):
    if not await r.get(f"{m.chat.id}:enable:{Dev_Zaid}"): return
    uid=m.from_user.id if m.from_user else(m.sender_chat.id if m.sender_chat else None)
    if not uid: return
    mention=m.from_user.mention if m.from_user else "?"
    is_admin=await admin_pls(uid,m.chat.id);k=await r.get(f"{Dev_Zaid}:botkey") or "⇜"
    sw=not await r.get(f"{m.chat.id}:disableWarn:{Dev_Zaid}");wcd=f"{Dev_Zaid}:inWARN:{uid}{m.chat.id}"
    async def warn(r_):
        await m.delete()
        if sw and not await r.get(wcd): await r.set(wcd,1,ex=60);await m.reply(f"「 {mention} 」\n{k} ممنوع {r_}\n☆",disable_web_page_preview=True)
    if await r.get(f"{m.chat.id}:lockEdit:{Dev_Zaid}") and m.text and not is_admin: await warn("التعديل")
    if await r.get(f"{m.chat.id}:lockEditM:{Dev_Zaid}") and m.media and not is_admin: await warn("تعديل الميديا")
