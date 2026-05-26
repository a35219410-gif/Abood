from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from config import r, Dev_Zaid

CATEGORIES = {
    "admin": {
        "emoji": "🛡️",
        "label": "الإدارة",
        "cmds": [
            ("تفعيل البوت", "تفعيل البوت في المجموعة"),
            ("تعطيل البوت", "تعطيل البوت في المجموعة"),
            ("كتم", "كتم عضو (رد على رسالته)"),
            ("رفع الكتم", "رفع الكتم عن عضو"),
            ("كتم المجموعة", "كتم جميع الأعضاء"),
            ("رفع كتم المجموعة", "رفع الكتم العام"),
            ("طرد", "طرد عضو من المجموعة"),
            ("حظر", "حظر عضو نهائياً"),
            ("رفع الحظر", "رفع الحظر عن عضو"),
            ("حظر عام", "حظر عام في كل المجموعات"),
            ("رفع الحظر العام", "رفع الحظر العام"),
            ("تعطيل التحذير", "إيقاف رسائل التحذير"),
            ("تفعيل التحذير", "تشغيل رسائل التحذير"),
        ]
    },
    "locks": {
        "emoji": "🔒",
        "label": "الأقفال",
        "cmds": [
            ("قفل الصوت", "منع إرسال الرسائل الصوتية"),
            ("قفل الفيديو", "منع إرسال الفيديو"),
            ("قفل الصور", "منع إرسال الصور"),
            ("قفل الستيكرات", "منع إرسال الستيكرات"),
            ("قفل الGIF", "منع إرسال الصور المتحركة"),
            ("قفل الملفات", "منع إرسال الملفات"),
            ("قفل الروابط", "منع إرسال الروابط"),
            ("قفل الهاشتاق", "منع الهاشتاقات"),
            ("قفل التاقات", "منع التاق @"),
            ("قفل الشتائم", "منع الألفاظ البذيئة"),
            ("قفل الطائفي", "منع الكلام الطائفي"),
            ("قفل الفارسي", "منع النص الفارسي"),
            ("قفل التحويل", "منع إعادة التوجيه"),
            ("قفل الانلاين", "منع الرسائل الانلاين"),
            ("قفل التعديل", "منع تعديل الرسائل"),
            ("قفل الكل", "قفل جميع الأنواع"),
            ("فتح الكل", "فتح جميع الأنواع"),
            ("الاقفال", "عرض حالة الأقفال"),
        ]
    },
    "ranks": {
        "emoji": "⭐",
        "label": "الرتب",
        "cmds": [
            ("رتبتي", "عرض رتبتك الحالية"),
            ("رفع مميز", "رفع عضو لرتبة مميز"),
            ("رفع ادمن", "رفع عضو لرتبة ادمن"),
            ("رفع المدير", "رفع عضو لرتبة مدير"),
            ("رفع المالك", "رفع عضو لرتبة مالك"),
            ("رفع المالك الاساسي", "رفع عضو لرتبة المالك الأساسي"),
            ("رفع Dev", "رفع عضو لرتبة Dev (مالك البوت فقط)"),
            ("تنزيل مميز", "تنزيل رتبة مميز"),
            ("تنزيل ادمن", "تنزيل رتبة ادمن"),
            ("تعطيل الرفع", "تعطيل نظام الرتب"),
            ("تفعيل الرفع", "تفعيل نظام الرتب"),
        ]
    },
    "welcome": {
        "emoji": "👋",
        "label": "الترحيب",
        "cmds": [
            ("تفعيل الترحيب", "تشغيل رسالة الترحيب"),
            ("تعطيل الترحيب", "إيقاف رسالة الترحيب"),
            ("تعيين الترحيب", "تخصيص رسالة الترحيب"),
            ("الترحيب", "عرض رسالة الترحيب الحالية"),
            ("القوانين", "عرض قوانين المجموعة"),
            ("تعيين القوانين", "تخصيص قوانين المجموعة"),
            ("حذف القوانين", "حذف قوانين المجموعة"),
        ]
    },
    "games": {
        "emoji": "🎮",
        "label": "الألعاب",
        "cmds": [
            ("النرد 🎲", "العب النرد واربح فلوساً"),
            ("فلوسي", "عرض رصيدك"),
            ("لعبة الكلمات", "لعبة ترتيب الكلمات"),
            ("تفعيل الالعاب", "تشغيل الألعاب"),
            ("تعطيل الالعاب", "إيقاف الألعاب"),
        ]
    },
    "download": {
        "emoji": "🎵",
        "label": "التحميل",
        "cmds": [
            ("يوت [اسم]", "البحث في يوتيوب"),
            ("صوت [رابط/اسم]", "تحميل صوت من يوتيوب"),
            ("فيديو [رابط/اسم]", "تحميل فيديو من يوتيوب"),
        ]
    },
    "fun": {
        "emoji": "🎊",
        "label": "المرح",
        "cmds": [
            ("رفع كيكه", "رفع كيكة لعضو (رد عليه)"),
            ("قائمة الكيك", "عرض قائمة الكيك"),
            ("صوّت [نص]", "تحويل النص لصوت"),
            ("التاريخ الهجري", "عرض التاريخ الهجري واليوم"),
            ("تفعيل المرح", "تشغيل أوامر المرح"),
            ("تعطيل المرح", "إيقاف أوامر المرح"),
        ]
    },
    "filters": {
        "emoji": "📋",
        "label": "الفلاتر",
        "cmds": [
            ("اضافة فلتر", "إضافة رد تلقائي لكلمة"),
            ("حذف فلتر", "حذف فلتر محدد"),
            ("الفلاتر", "عرض جميع الفلاتر"),
            ("حذف كل الفلاتر", "حذف جميع الفلاتر"),
        ]
    },
    "info": {
        "emoji": "🪪",
        "label": "المعلومات",
        "cmds": [
            ("ايدي", "عرض معلوماتك أو معلومات عضو"),
            ("ايدي المجموعة", "عرض ID المجموعة"),
            ("ping", "قياس سرعة البوت"),
        ]
    },
}

def main_menu_keyboard():
    buttons = []
    items = list(CATEGORIES.items())
    for i in range(0, len(items), 2):
        row = []
        key1, val1 = items[i]
        row.append(InlineKeyboardButton(f"{val1['emoji']} {val1['label']}", callback_data=f"help_{key1}"))
        if i + 1 < len(items):
            key2, val2 = items[i + 1]
            row.append(InlineKeyboardButton(f"{val2['emoji']} {val2['label']}", callback_data=f"help_{key2}"))
        buttons.append(row)
    return InlineKeyboardMarkup(buttons)

def category_keyboard(cat_key):
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("◀️ رجوع", callback_data="help_main")]
    ])

def build_category_text(cat_key, bot_name, key_symbol):
    cat = CATEGORIES[cat_key]
    lines = [f"{key_symbol} **{cat['emoji']} {cat['label']}**\n"]
    for cmd, desc in cat["cmds"]:
        lines.append(f"• `{cmd}` — {desc}")
    lines.append("\n☆")
    return "\n".join(lines)

@Client.on_message(filters.text & filters.group, group=99)
async def help_cmd(c, m: Message):
    if not m.from_user:
        return
    if not await r.get(f"{m.chat.id}:enable:{Dev_Zaid}"):
        return
    text = m.text.strip()
    name = await r.get(f"{Dev_Zaid}:BotName") or "رعد"
    if text.startswith(f"{name} "):
        text = text[len(name)+1:]
    if text != "الاوامر":
        return
    k = await r.get(f"{Dev_Zaid}:botkey") or "⇜"
    await m.reply(
        f"{k} **أهلاً! أنا {name}**\nاختر قسماً لعرض أوامره:\n\n☆",
        reply_markup=main_menu_keyboard()
    )

@Client.on_callback_query(filters.regex(r"^help_(.+)$"))
async def help_callback(c, cb: CallbackQuery):
    cat_key = cb.data.replace("help_", "")
    k = await r.get(f"{Dev_Zaid}:botkey") or "⇜"
    name = await r.get(f"{Dev_Zaid}:BotName") or "رعد"

    if cat_key == "main":
        await cb.message.edit(
            f"{k} **أهلاً! أنا {name}**\nاختر قسماً لعرض أوامره:\n\n☆",
            reply_markup=main_menu_keyboard()
        )
        return await cb.answer()

    if cat_key not in CATEGORIES:
        return await cb.answer("قسم غير موجود", show_alert=True)

    text = build_category_text(cat_key, name, k)
    await cb.message.edit(text, reply_markup=category_keyboard(cat_key))
    await cb.answer()
