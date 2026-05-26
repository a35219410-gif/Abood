from config import r,Dev_Zaid,OWNER_ID
async def _chk(keys):
    for k in keys:
        if await r.get(k): return True
    return False
async def get_rank(uid,cid):
    if str(uid)==Dev_Zaid: return "البوت"
    if uid==OWNER_ID: return "Dev🎖️"
    if await r.get(f"{uid}:rankDEV2:{Dev_Zaid}"): return "Dev²🎖"
    if await r.get(f"{uid}:rankDEV:{Dev_Zaid}"): return "Myth🎖️"
    if await r.get(f"{uid}:gban:{Dev_Zaid}"): return "محظور عام"
    if await r.get(f"{uid}:mute:{Dev_Zaid}"): return "محظور عام"
    for rk,df,nk in [(f"{cid}:rankGOWNER:{uid}{Dev_Zaid}","المالك الاساسي",f"{cid}:RankGowner:{Dev_Zaid}"),(f"{cid}:rankOWNER:{uid}{Dev_Zaid}","المالك",f"{cid}:RankOwner:{Dev_Zaid}"),(f"{cid}:rankMOD:{uid}{Dev_Zaid}","المدير",f"{cid}:RankMod:{Dev_Zaid}"),(f"{cid}:rankADMIN:{uid}{Dev_Zaid}","ادمن",f"{cid}:RankAdm:{Dev_Zaid}"),(f"{cid}:rankPRE:{uid}{Dev_Zaid}","مميز",f"{cid}:RankPre:{Dev_Zaid}")]:
        if await r.get(rk): return (await r.get(nk)) or df
    return (await r.get(f"{cid}:RankMem:{Dev_Zaid}")) or "عضو"
async def admin_pls(uid,cid):
    if str(uid)==Dev_Zaid or uid==OWNER_ID: return True
    return await _chk([f"{uid}:rankDEV2:{Dev_Zaid}",f"{uid}:rankDEV:{Dev_Zaid}",f"{cid}:rankGOWNER:{uid}{Dev_Zaid}",f"{cid}:rankOWNER:{uid}{Dev_Zaid}",f"{cid}:rankMOD:{uid}{Dev_Zaid}",f"{cid}:rankADMIN:{uid}{Dev_Zaid}"])
async def mod_pls(uid,cid):
    if str(uid)==Dev_Zaid or uid==OWNER_ID: return True
    return await _chk([f"{uid}:rankDEV2:{Dev_Zaid}",f"{uid}:rankDEV:{Dev_Zaid}",f"{cid}:rankGOWNER:{uid}{Dev_Zaid}",f"{cid}:rankOWNER:{uid}{Dev_Zaid}",f"{cid}:rankMOD:{uid}{Dev_Zaid}"])
async def owner_pls(uid,cid):
    if str(uid)==Dev_Zaid or uid==OWNER_ID: return True
    return await _chk([f"{uid}:rankDEV2:{Dev_Zaid}",f"{uid}:rankDEV:{Dev_Zaid}",f"{cid}:rankGOWNER:{uid}{Dev_Zaid}",f"{cid}:rankOWNER:{uid}{Dev_Zaid}"])
async def gowner_pls(uid,cid):
    if str(uid)==Dev_Zaid or uid==OWNER_ID: return True
    return await _chk([f"{uid}:rankDEV2:{Dev_Zaid}",f"{uid}:rankDEV:{Dev_Zaid}",f"{cid}:rankGOWNER:{uid}{Dev_Zaid}"])
async def dev_pls(uid,cid):
    if str(uid)==Dev_Zaid or uid==OWNER_ID: return True
    return await _chk([f"{uid}:rankDEV2:{Dev_Zaid}",f"{uid}:rankDEV:{Dev_Zaid}"])
async def devp_pls(uid,cid): return await dev_pls(uid,cid)
async def pre_pls(uid,cid): return await admin_pls(uid,cid) or bool(await r.get(f"{cid}:rankPRE:{uid}{Dev_Zaid}"))
async def is_muted(uid,cid): return bool(await r.get(f"{uid}:mute:{cid}{Dev_Zaid}") or await r.get(f"{uid}:mute:{Dev_Zaid}"))
async def get_text_after_name(text,cid):
    name=await r.get(f"{Dev_Zaid}:BotName") or "رعد"
    if text.startswith(f"{name} "): text=text[len(name)+1:]
    c=await r.get(f"{cid}:Custom:{cid}{Dev_Zaid}&text={text}")
    if c: text=c
    g=await r.get(f"Custom:{Dev_Zaid}&text={text}")
    if g: text=g
    return text
async def isLockCommand(uid,cid,text): return text.startswith(("تفعيل ","تعطيل ","قفل ","فتح ","رفع ","كتم"))
BAD_WORDS={"كس","كسمك","عير","خرا بالله","عير بالله","شرموط","شرموطه","ابن الكحبه","فرخ","طيزك","يا ابن الخول","المتناك","ابن الخول","ابن العرص","منايك","متناك","زبك","عرص","زبي","خول","لبوه","منيوك","متناكه","يا عرص","يا خول","قحبه","القحبه","شراميط","العلق","الشرموطه","قاحب"}
SECTARIAN_WORDS={"يا علي","يا حسين","ياعلي","ياحسين","علي ولي الله","عائشه زانيه","عائشة زانية","خرب ربك","خرب الله","يلعن ربك","يلعن الله","ربنا علي","علي الله"}
def contains_bad_word(text,ws): t=text.lower();return any(w in t for w in ws)
