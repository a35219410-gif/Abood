import asyncio,logging,os,re
import yt_dlp
from pyrogram import Client,filters
from pyrogram.types import Message,InlineKeyboardMarkup,InlineKeyboardButton,CallbackQuery
from pyrogram.enums import ChatAction
from config import r,Dev_Zaid
from helpers.Ranks import admin_pls,is_muted
from helpers.utils import cleanup_file
log=logging.getLogger("R3D.dl")
YA={"format":"bestaudio/best","postprocessors":[{"key":"FFmpegExtractAudio","preferredcodec":"mp3","preferredquality":"192"}],"outtmpl":"%(id)s.%(ext)s","quiet":True,"no_warnings":True}
YV={"format":"best[height<=720]","outtmpl":"%(id)s.%(ext)s","quiet":True,"no_warnings":True}
URE=re.compile(r"(?i)\b((?:https?://|www\d{0,3}[.])[^\s()<>]+((?:\([^\s()<>]+\))|[^\s!()]))")

async def search_youtube(query, limit=4):
    """البحث في يوتيوب باستخدام yt-dlp"""
    try:
        opts = {
            "quiet": True,
            "no_warnings": True,
            "extract_flat": True,
            "default_search": f"ytsearch{limit}",
        }
        def _search():
            with yt_dlp.YoutubeDL(opts) as y:
                info = y.extract_info(f"ytsearch{limit}:{query}", download=False)
                return info.get("entries", [])
        return await asyncio.get_event_loop().run_in_executor(None, _search)
    except Exception as e:
        log.error(e)
        return []

async def dl_a(url):
    try:
        def _d():
            with yt_dlp.YoutubeDL(YA) as y:
                i=y.extract_info(url,download=True);return y.prepare_filename(i).replace(".webm",".mp3").replace(".m4a",".mp3")
        return await asyncio.get_event_loop().run_in_executor(None,_d)
    except Exception as e: log.error(e);return None

async def dl_v(url):
    try:
        def _d():
            with yt_dlp.YoutubeDL(YV) as y:
                i=y.extract_info(url,download=True);return y.prepare_filename(i),i
        return await asyncio.get_event_loop().run_in_executor(None,_d)
    except Exception as e: log.error(e);return None,None

@Client.on_message(filters.text&filters.group,group=32)
async def dl_handler(c,m:Message):
    if not m.from_user: return
    if not await r.get(f"{m.chat.id}:enable:{Dev_Zaid}"): return
    if await is_muted(m.from_user.id,m.chat.id): return
    text=m.text.strip();k=await r.get(f"{Dev_Zaid}:botkey") or "⇜";ch=await r.get(f"{Dev_Zaid}:BotChannel") or "yqyqy66"
    btn=InlineKeyboardMarkup([[InlineKeyboardButton("🎵",url=f"https://t.me/{ch}")]])
    if text.startswith("يوت "):
        if await r.get(f"{m.chat.id}:disableYT:{Dev_Zaid}"): return
        q=text[4:].strip()
        if not q: return await m.reply(f"{k} أرسل اسم الأغنية")
        rep=await m.reply(f"{k} جاري البحث 🔍")
        try:
            results = await search_youtube(q, limit=4)
            if not results: return await rep.edit(f"{k} ما وجدت نتائج")
            kb=[[InlineKeyboardButton(r.get("title","")[:40],callback_data=f"{m.from_user.id}GET{r.get('id','')}")] for r in results if r.get("id")]
            await rep.edit(f"{k} نتائج ~ {q}",reply_markup=InlineKeyboardMarkup(kb))
        except Exception as e: log.error(e);await rep.edit(f"{k} خطأ")
        return
    if text.startswith(("صوت ","mp3 ")):
        uq=text.split(None,1)[1].strip();urls=[m[0] for m in URE.findall(uq)]
        url=urls[0] if urls else f"ytsearch:{uq}";rep=await m.reply(f"{k} جاري التحميل 🎵")
        await c.send_chat_action(m.chat.id,ChatAction.UPLOAD_AUDIO)
        path=await dl_a(url)
        if not path or not os.path.exists(path): return await rep.edit(f"{k} فشل التحميل")
        try: await c.send_audio(m.chat.id,path,reply_markup=btn,reply_to_message_id=m.id);await rep.delete()
        except Exception as e: log.error(e);await rep.edit(f"{k} فشل")
        finally: cleanup_file(path)
        return
    if text.startswith(("فيديو ","mp4 ")):
        uq=text.split(None,1)[1].strip();urls=[m[0] for m in URE.findall(uq)]
        url=urls[0] if urls else f"ytsearch:{uq}";rep=await m.reply(f"{k} جاري التحميل 🎬")
        await c.send_chat_action(m.chat.id,ChatAction.UPLOAD_VIDEO)
        path,info=await dl_v(url)
        if not path or not os.path.exists(path): return await rep.edit(f"{k} فشل التحميل")
        cap=info.get("title","") if info else ""
        try: await c.send_video(m.chat.id,path,caption=cap,reply_markup=btn,reply_to_message_id=m.id);await rep.delete()
        except Exception as e: log.error(e);await rep.edit(f"{k} فشل")
        finally: cleanup_file(path)
        return

@Client.on_callback_query(filters.regex(r"^(\d+)GET(.+)$"))
async def yt_cb(c,cb:CallbackQuery):
    import re as _r;mat=_r.match(r"^(\d+)GET(.+)$",cb.data)
    if not mat: return await cb.answer("خطأ")
    if cb.from_user.id!=int(mat.group(1)): return await cb.answer("ليس بحثك!",show_alert=True)
    await cb.answer("جاري التحميل 🎵")
    url=f"https://www.youtube.com/watch?v={mat.group(2)}"
    k=await r.get(f"{Dev_Zaid}:botkey") or "⇜";ch=await r.get(f"{Dev_Zaid}:BotChannel") or "yqyqy66"
    btn=InlineKeyboardMarkup([[InlineKeyboardButton("🎵",url=f"https://t.me/{ch}")]])
    rep=await cb.message.edit(f"{k} جاري التحميل 🎵")
    path=await dl_a(url)
    if not path or not os.path.exists(path): return await rep.edit(f"{k} فشل")
    try: await c.send_audio(cb.message.chat.id,path,reply_markup=btn);await rep.delete()
    except Exception as e: log.error(e);await rep.edit(f"{k} فشل")
    finally: cleanup_file(path)
