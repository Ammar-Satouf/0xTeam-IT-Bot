from telegram import ReplyKeyboardMarkup, KeyboardButton, Update
from telegram.ext import ContextTypes
from resources import resources, channel_ids, temporary_culture_doc
from datetime import datetime


# 📅 التحية حسب الوقت
def get_greeting():
    hour = datetime.now().hour
    if hour < 12:
        return "صباح الخير ☀"
    elif hour < 18:
        return "مساء النور 🌇"
    else:
        return "سهرة سعيدة 🌙"


# 🧭 القوائم
def main_menu_keyboard():
    return ReplyKeyboardMarkup(
        [
            [KeyboardButton("📘 المواد الدراسية")],
            [KeyboardButton("📤 آلية تقديم اعتراض")],
            [KeyboardButton("📩 تواصل معنا")],
            [KeyboardButton("🧠 عن البوت")],
            [KeyboardButton("📗 مقرر الثقافة المؤقت")],
        ],
        resize_keyboard=True,
        one_time_keyboard=True,
    )


def year_keyboard():
    return ReplyKeyboardMarkup(
        [
            [KeyboardButton("السنة الأولى")],
            [KeyboardButton("السنة الثانية")],
            [KeyboardButton("السنة الثالثة")],
            [KeyboardButton("السنة الرابعة")],
            [KeyboardButton("السنة الخامسة")],
            [KeyboardButton("🔙 رجوع"),
             KeyboardButton("🏠 القائمة الرئيسية")],
        ],
        resize_keyboard=True,
        one_time_keyboard=True,
    )


def term_keyboard():
    return ReplyKeyboardMarkup(
        [
            [KeyboardButton("الفصل الأول")],
            [KeyboardButton("الفصل الثاني")],
            [KeyboardButton("🔙 رجوع"),
             KeyboardButton("🏠 القائمة الرئيسية")],
        ],
        resize_keyboard=True,
        one_time_keyboard=True,
    )


def subjects_keyboard(subjects_list):
    buttons = [[KeyboardButton(sub)] for sub in subjects_list]
    buttons.append(
        [KeyboardButton("🔙 رجوع"),
         KeyboardButton("🏠 القائمة الرئيسية")])
    return ReplyKeyboardMarkup(buttons,
                               resize_keyboard=True,
                               one_time_keyboard=True)


def section_keyboard():
    return ReplyKeyboardMarkup(
        [
            [KeyboardButton("📘 القسم النظري")],
            [KeyboardButton("🧪 القسم العملي")],
            [KeyboardButton("🔙 رجوع"),
             KeyboardButton("🏠 القائمة الرئيسية")],
        ],
        resize_keyboard=True,
        one_time_keyboard=True,
    )


def content_type_keyboard():
    return ReplyKeyboardMarkup(
        [
            [KeyboardButton("📚 محاضرات Gate")],
            [KeyboardButton("📚 محاضرات الكميت")],
            [KeyboardButton("✍ محاضرات كتابة زميلنا / دكتور المادة")],
            [KeyboardButton("📄 ملخصات")],
            [KeyboardButton("❓ أسئلة دورات")],
            [KeyboardButton("📝 ملاحظات المواد")],
            [KeyboardButton("🔙 رجوع"),
             KeyboardButton("🏠 القائمة الرئيسية")],
        ],
        resize_keyboard=True,
        one_time_keyboard=True,
    )


# 🚀 البداية
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_first_name = update.effective_user.first_name or "طالبنا"
    greeting = get_greeting()

    await update.message.reply_text(
        f"{greeting}، يسعد يومك يا {user_first_name} 💫\n"
        "زيرو ✖ تيم معك دايمًا يا مبدع 🤍🚀\n"
        "اختر أحد الأقسام التالية:",
        reply_markup=main_menu_keyboard())
    context.user_data.clear()


# 📩 المعالجة
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if text in ["🏠 القائمة الرئيسية", "🔙 رجوع"]:
        await start(update, context)
        return

    if text == "📘 المواد الدراسية":
        await update.message.reply_text("اختر السنة الدراسية :",
                                        reply_markup=year_keyboard())
        return

    if text == "📤 آلية تقديم اعتراض":
        await update.message.reply_text(
            "📣 إعلان بخصوص الاعتراض على النتائج:\n\n"
            "بعد صدور النتائج، يُفتح باب تقديم طلبات الاعتراض لفترة محددة. آلية الاعترض كالتالي:\n"
            "1. التوجه إلى النافذة الواحدة للحصول على نموذج الاعتراض.\n"
            "2. تعبئة الطلب وإرفاق الطوابع.\n"
            "3. تقديمه لشعبة الشؤون لتوليد الرسوم.\n"
            "4. دفع الرسوم عبر مصرف أو سيريتل كاش.\n"
            "5. توقيع الطلب لدى المحاسب.\n"
            "6. إعادة الطلب للنافذة لاستكمال الإجراء.\n\n"
            "مع تمنياتنا بالتوفيق 🍀",
            reply_markup=main_menu_keyboard())
        return

    if text == "📩 تواصل معنا":
        await update.message.reply_text(
            "📨 تقدر تتواصل معنا لأي استفسار أو اقتراح:\n\n"
            "👨‍💻 المطور: @Ammarsa51\n"
            "🧑‍🏫 دعم المحتويات: @ghadeer_wanous\n"
            "📢 تابعنا: @zeroxxteam",
            reply_markup=main_menu_keyboard())
        return

    if text == "🧠 عن البوت":
        await update.message.reply_text(
            "📚 بوت تعليمي مقدم من فريق زيرو ✖ تيم، هدفه إيصال الملفات الدراسية بطريقة سهلة.\n"
            "نشتغل على دعم باقي السنوات وتحسين الأداء بشكل دوري.\n\n"
            "إذا كان عندك اقتراح، لا تتردد تتواصل معنا 🌟",
            reply_markup=main_menu_keyboard())
        return

    if text == "📗 مقرر الثقافة المؤقت":
        cid = channel_ids.get("komit")
        msg_id = temporary_culture_doc

        if not cid or not msg_id:
            await update.message.reply_text(
                "📗 لا يتوفر محتويات مقرر الثقافة حالياً.",
                reply_markup=main_menu_keyboard())
            return

        await context.bot.copy_message(chat_id=update.effective_chat.id,
                                       from_chat_id=cid,
                                       message_id=msg_id)
        await update.message.reply_text(
            "🎯 تم إرسال مقرر الثقافة المؤقت بنجاح.\nلا تنسَ تشارك البوت مع زملائك ❤",
            reply_markup=main_menu_keyboard())
        return

    if text in [
            "السنة الأولى",
            "السنة الثانية",
            "السنة الثالثة",
            "السنة الرابعة",
            "السنة الخامسة",
    ]:
        year_map = {
            "السنة الأولى": "1",
            "السنة الثانية": "2",
            "السنة الثالثة": "3",
            "السنة الرابعة": "4",
            "السنة الخامسة": "5",
        }
        context.user_data["year"] = year_map[text]
        await update.message.reply_text("اختر الفصل :",
                                        reply_markup=term_keyboard())
        return

    if text in ["الفصل الأول", "الفصل الثاني"]:
        term_map = {"الفصل الأول": "1", "الفصل الثاني": "2"}
        context.user_data["term"] = term_map[text]
        year = context.user_data.get("year")
        term = context.user_data.get("term")

        if year == "1" and term == "2":
            subjects = [
                " تحليل 2",
                "برمجة 2",
                "فيزياء انصاف نواقل",
                "جبر خطى",
                "لغة انجليزية 2",
            ]
            await update.message.reply_text(
                "اختر المادة :", reply_markup=subjects_keyboard(subjects))
        else:
            await update.message.reply_text("لا توجد مواد حالياً.",
                                            reply_markup=main_menu_keyboard())
        return

    subjects_list = [
        " تحليل 2",
        "برمجة 2",
        "فيزياء انصاف نواقل",
        "جبر خطى",
        "لغة انجليزية 2",
    ]
    if text in subjects_list:
        context.user_data["subject"] = text
        if text == "لغة انجليزية 2":
            context.user_data["section"] = "theoretical"
            await update.message.reply_text(
                "اختر نوع المحتويات :", reply_markup=content_type_keyboard())
        else:
            await update.message.reply_text("اختر القسم :",
                                            reply_markup=section_keyboard())
        return

    if text in ["📘 القسم النظري", "🧪 القسم العملي"]:
        context.user_data[
            "section"] = "theoretical" if text == "📘 القسم النظري" else "practical"
        await update.message.reply_text("اختر نوع المحتويات :",
                                        reply_markup=content_type_keyboard())
        return

    content_map = {
        "📚 محاضرات Gate": "gate",
        "📚 محاضرات الكميت": "komit",
        "✍ محاضرات كتابة زميلنا / دكتور المادة": "student_written",
        "📄 ملخصات": "summaries",
        "❓ أسئلة دورات": "exams",
        "📝 ملاحظات المواد": "notes",
    }

    if text in content_map:
        content_key = content_map[text]
        year = context.user_data.get("year")
        term = context.user_data.get("term")
        section = context.user_data.get("section")
        subject = context.user_data.get("subject")

        try:
            msgs = resources[year][term][section][subject][content_key]
        except KeyError:
            msgs = []

        if not msgs or all(id == 0 for id in msgs):
            await update.message.reply_text("لا توجد محتويات حالياً.",
                                            reply_markup=main_menu_keyboard())
            return

        cid = channel_ids.get(content_key)
        if not cid:
            await update.message.reply_text("تعذر الوصول لقناة المحتويات.",
                                            reply_markup=main_menu_keyboard())
            return

        for mid in msgs:
            if mid == 0:
                continue
            await context.bot.copy_message(chat_id=update.effective_chat.id,
                                           from_chat_id=cid,
                                           message_id=mid)

        await update.message.reply_text(
            "🎯 تم إرسال الملفات بنجاح!\nلا تنسَ أن تشارك البوت مع زملائك ❤",
            reply_markup=main_menu_keyboard())
        return

    await update.message.reply_text("❗ الرجاء اختيار خيار صحيح.",
     reply_markup=main_menu_keyboard())
