import json
import os
from telegram import ReplyKeyboardMarkup, KeyboardButton, Update
from telegram.ext import ContextTypes
from resources import resources, channel_ids, temporary_culture_doc
from datetime import datetime

NOTIFIED_USERS_FILE = "notified_users.json"

# تحميل وحفظ قائمة المستخدمين المفعّلين للإشعارات
def load_notified_users():
    if os.path.exists(NOTIFIED_USERS_FILE):
        with open(NOTIFIED_USERS_FILE, "r") as f:
            return json.load(f)
    return []

def save_notified_users(user_ids):
    with open(NOTIFIED_USERS_FILE, "w") as f:
        json.dump(user_ids, f)

# إضافة زر تفعيل الإشعارات للقائمة الرئيسية
def main_menu_keyboard():
    return ReplyKeyboardMarkup(
        [
            [KeyboardButton("📘 المواد الدراسية")],
            [KeyboardButton("📤 آلية تقديم اعتراض")],
            [KeyboardButton("📩 تواصل معنا")],
            [KeyboardButton("🧠 عن البوت")],
            [KeyboardButton("📗 مقرر الثقافة المؤقت")],
            [KeyboardButton("🔔 تفعيل إشعارات التحديثات")],
        ],
        resize_keyboard=True,
        one_time_keyboard=True,
    )

def year_keyboard():
    return ReplyKeyboardMarkup(
        [
            [KeyboardButton("السنة الأولى"), KeyboardButton("السنة الثانية")],
            [KeyboardButton("السنة الثالثة"), KeyboardButton("السنة الرابعة")],
            [KeyboardButton("السنة الخامسة")],
            [KeyboardButton("🔙 رجوع"), KeyboardButton("🏠 القائمة الرئيسية")],
        ],
        resize_keyboard=True,
    )

def term_keyboard():
    return ReplyKeyboardMarkup(
        [
            [KeyboardButton("الفصل الأول ⚡"), KeyboardButton("الفصل الثاني 🔥")],
            [KeyboardButton("🔙 رجوع"), KeyboardButton("🏠 القائمة الرئيسية")],
        ],
        resize_keyboard=True,
    )

def section_keyboard():
    return ReplyKeyboardMarkup(
        [
            [KeyboardButton("📘 القسم النظري"), KeyboardButton("🧪 القسم العملي")],
            [KeyboardButton("🔙 رجوع"), KeyboardButton("🏠 القائمة الرئيسية")],
        ],
        resize_keyboard=True,
    )

def content_type_keyboard():
    return ReplyKeyboardMarkup(
        [
            [KeyboardButton("📚 محاضرات Gate"), KeyboardButton("📚 محاضرات الكميت")],
            [KeyboardButton("✍ محاضرات كتابة زميلنا / دكتور المادة")],
            [KeyboardButton("📄 ملخصات"), KeyboardButton("❓ أسئلة دورات")],
            [KeyboardButton("📝 ملاحظات المواد")],
            [KeyboardButton("🔙 رجوع"), KeyboardButton("🏠 القائمة الرئيسية")],
        ],
        resize_keyboard=True,
    )

def subjects_keyboard(subjects):
    keyboard = []
    for i in range(0, len(subjects), 2):
        row = [KeyboardButton(subjects[i])]
        if i + 1 < len(subjects):
            row.append(KeyboardButton(subjects[i + 1]))
        keyboard.append(row)

    keyboard.append([KeyboardButton("🔙 رجوع"), KeyboardButton("🏠 القائمة الرئيسية")])

    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

# التحية حسب الوقت
def get_greeting():
    hour = datetime.now().hour
    if hour < 12:
        return "صباح الخير ☀"
    elif hour < 18:
        return "مساء النور 🌇"
    else:
        return "سهرة سعيدة 🌙"

# إرسال إشعارات التحديثات للمستخدمين المفعّلين
async def notify_update_to_users(bot):
    users = load_notified_users()
    for user_id in users:
        try:
            await bot.send_message(chat_id=user_id, text="🔔 تم تحديث محتوى البوت بنجاح! يمكنك الآن استعراض المواد الجديدة.")
        except Exception as e:
            print(f"Error notifying user {user_id}: {e}")

# 🚀 البداية
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_first_name = update.effective_user.first_name or "طالبنا"
    greeting = get_greeting()

    await update.message.reply_text(
        f"{greeting}، يسعد يومك يا {user_first_name} 💫\n"
        "زيرو ✖ تيم معك دايمًا يا مبدع 🤍🚀\n"
        "اختر أحد الأقسام التالية:",
        reply_markup=main_menu_keyboard(),
    )
    context.user_data.clear()

# 📩 المعالجة الرئيسية
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    user_id = update.effective_user.id

    # تفعيل إشعارات التحديثات
    if text == "🔔 تفعيل إشعارات التحديثات":
        users = load_notified_users()
        if user_id not in users:
            users.append(user_id)
            save_notified_users(users)
            await update.message.reply_text(
                "✅ تم تفعيل إشعارات التحديثات بنجاح. ستتلقى تنبيهات عند تحديث محتوى البوت.",
                reply_markup=main_menu_keyboard(),
            )
        else:
            await update.message.reply_text(
                "ℹ أنت مفعل الإشعارات سابقاً.",
                reply_markup=main_menu_keyboard(),
            )
        return

    # رجوع أو القائمة الرئيسية
    if text == "🔙 رجوع":
        previous_step = context.user_data.get("previous_step")
        if previous_step:
            await previous_step(update, context)
        else:
            await start(update, context)
        return

    if text == "🏠 القائمة الرئيسية":
        await start(update, context)
        return

    # المواد الدراسية - بداية اختيار السنة
    if text == "📘 المواد الدراسية":
        context.user_data["previous_step"] = start
        await update.message.reply_text("اختر السنة الدراسية:", reply_markup=year_keyboard())
        return

    # آلية تقديم اعتراض
    if text == "📤 آلية تقديم اعتراض":
        context.user_data["previous_step"] = start
        await update.message.reply_text(
            "📣 إعلان بخصوص الاعتراض على النتائج:\n\n"
            "بعد صدور النتائج، يُفتح باب تقديم طلبات الاعتراض لفترة محددة. آلية الاعتراض كالتالي:\n"
            "1. التوجه إلى النافذة الواحدة للحصول على نموذج الاعتراض.\n"
            "2. تعبئة الطلب وإرفاق الطوابع.\n"
            "3. تقديمه لشعبة الشؤون لتوليد الرسوم.\n"
            "4. دفع الرسوم عبر مصرف أو سيريتل كاش.\n"
            "5. توقيع الطلب لدى المحاسب.\n"
            "6. إعادة الطلب للنافذة لاستكمال الإجراء.\n\n"
            "مع تمنياتنا بالتوفيق 🍀",
            reply_markup=main_menu_keyboard(),
        )
        return

    # تواصل معنا
    if text == "📩 تواصل معنا":
        context.user_data["previous_step"] = start
        await update.message.reply_text(
            "📨 تقدر تتواصل معنا لأي استفسار أو اقتراح:\n\n"
            "👨‍💻 المطور: @Ammarsa51\n"
            "🧑‍🏫 دعم المحتويات: @ghadeer_wanous\n"
            "📢 تابعنا: @zeroxxteam",
            reply_markup=main_menu_keyboard(),
        )
        return

    # عن البوت
    if text == "🧠 عن البوت":
        context.user_data["previous_step"] = start
        await update.message.reply_text(
            "📚 بوت تعليمي مقدم من فريق زيرو ✖ تيم، هدفه إيصال الملفات الدراسية بطريقة سهلة.\n"
            "نشتغل على دعم باقي السنوات وتحسين الأداء بشكل دوري.\n\n"
            "إذا كان عندك اقتراح، لا تتردد تتواصل معنا 🌟",
            reply_markup=main_menu_keyboard(),
        )
        return

    # مقرر الثقافة المؤقت
    if text == "📗 مقرر الثقافة المؤقت":
        context.user_data["previous_step"] = start
        cid = channel_ids.get("komit")
        msg_id = temporary_culture_doc

        if not cid or not msg_id:
            await update.message.reply_text(
                "📗 لا يتوفر محتويات مقرر الثقافة حالياً.",
                reply_markup=main_menu_keyboard(),
            )
            return

        await context.bot.copy_message(
            chat_id=update.effective_chat.id, from_chat_id=cid, message_id=msg_id, protect_content=True
        )
        await update.message.reply_text(
            "🎯 تم إرسال مقرر الثقافة المؤقت بنجاح.\nلا تنسَ تشارك البوت مع زملائك ❤",
            reply_markup=main_menu_keyboard(),
        )
        return

    # اختيار السنة الدراسية
    years_map = {
        "السنة الأولى": "السنة الأولى",
        "السنة الثانية": "السنة الثانية",
        "السنة الثالثة": "السنة الثالثة",
        "السنة الرابعة": "السنة الرابعة",
        "السنة الخامسة": "السنة الخامسة",
    }

    if text in years_map:
        context.user_data["year"] = text
        context.user_data["previous_step"] = lambda u, c: u.message.reply_text("اختر السنة الدراسية:", reply_markup=year_keyboard())
        await update.message.reply_text("اختر الفصل الدراسي:", reply_markup=term_keyboard())
        return

    # اختيار الفصل الدراسي
    term_map = {"الفصل الأول ⚡": "الفصل الأول", "الفصل الثاني 🔥": "الفصل الثاني"}
    if text in term_map:
        year = context.user_data.get("year")
        term = term_map[text]
        context.user_data["term"] = term
        context.user_data["previous_step"] = lambda u, c: u.message.reply_text("اختر الفصل الدراسي:", reply_markup=term_keyboard())

        if year not in resources or term not in resources[year]:
            await update.message.reply_text("لا توجد مواد لهذا الفصل.", reply_markup=main_menu_keyboard())
            return

        # جلب المواد من النظري والعملي مع دمج وإزالة التكرار
        theoretical_subjects = list(resources[year][term].get("theoretical", {}).keys())
        practical_subjects = list(resources[year][term].get("practical", {}).keys())

        all_subjects_set = set(theoretical_subjects + practical_subjects)
        all_subjects = sorted(all_subjects_set)

        prefix = "⚡ " if term == "الفصل الأول" else "🔥 "
        subjects = [prefix + subj for subj in all_subjects]

        if not subjects:
            await update.message.reply_text("لا توجد مواد لهذا الفصل.", reply_markup=main_menu_keyboard())
            return

        await update.message.reply_text("اختر المادة:", reply_markup=subjects_keyboard(subjects))
        return

    # دالة لإزالة الإيموجي من بداية اسم المادة
    def strip_emoji(text):
        return text[2:] if len(text) > 2 else text

    # جميع المواد في resources تحت السنة والفصل والقسمين
    year = context.user_data.get("year")
    term = context.user_data.get("term")
    if year and term:
        subjects_all = []
        for section_key in ["theoretical", "practical"]:
            subjects_all += list(resources.get(year, {}).get(term, {}).get(section_key, {}).keys())
        subjects_all_set = set(subjects_all)
    else:
        subjects_all_set = set()

    if strip_emoji(text) in subjects_all_set:
        subj_clean = strip_emoji(text)
        context.user_data["subject"] = subj_clean
        context.user_data["previous_step"] = lambda u, c: u.message.reply_text("اختر المادة:", reply_markup=subjects_keyboard(sorted(subjects_all_set)))

        # نتحقق الأقسام المتوفرة للمادة
        available_sections = []
        if subj_clean in resources.get(year, {}).get(term, {}).get("theoretical", {}):
            available_sections.append("theoretical")
        if subj_clean in resources.get(year, {}).get(term, {}).get("practical", {}):
            available_sections.append("practical")

        if len(available_sections) == 1:
            context.user_data["section"] = available_sections[0]
            await update.message.reply_text(
                "اختر نوع المحتوى المطلوب:",
                reply_markup=content_type_keyboard(),
            )
        else:
            await update.message.reply_text(
                "اختر القسم (نظري أو عملي):",
                reply_markup=section_keyboard(),
            )
        return

    # اختيار القسم
    if text == "📘 القسم النظري":
        context.user_data["section"] = "theoretical"
        await update.message.reply_text(
            "اختر نوع المحتوى المطلوب:",
            reply_markup=content_type_keyboard(),
        )
        return

    if text == "🧪 القسم العملي":
        context.user_data["section"] = "practical"
        await update.message.reply_text(
            "اختر نوع المحتوى المطلوب:",
            reply_markup=content_type_keyboard(),
        )
        return

    # اختيار نوع المحتوى
    content_type_map = {
        "📚 محاضرات Gate": "gate",
        "📚 محاضرات الكميت": "komit",
        "✍ محاضرات كتابة زميلنا / دكتور المادة": "student_written",
        "📄 ملخصات": "summaries",
        "❓ أسئلة دورات": "exams",
        "📝 ملاحظات المواد": "notes",
    }

    if text in content_type_map:
        content_key = content_type_map[text]
        year = context.user_data.get("year")
        term = context.user_data.get("term")
        section = context.user_data.get("section")
        subject = context.user_data.get("subject")

        if not all([year, term, section, subject]):
            await update.message.reply_text(
                "يبدو أن هناك خطأ في اختيارك. الرجاء البدء من جديد.",
                reply_markup=main_menu_keyboard(),
            )
            context.user_data.clear()
            return

        messages_list = resources.get(year, {}).get(term, {}).get(section, {}).get(subject, {}).get(content_key, [])

        if not messages_list or messages_list == [0]:
            await update.message.reply_text(
                "عذرًا، لا توجد ملفات متاحة لهذا المحتوى حالياً.",
                reply_markup=main_menu_keyboard(),
            )
            return

        channel_id = channel_ids.get(content_key)
        if not channel_id:
            await update.message.reply_text(
                "حدث خطأ في جلب القناة. الرجاء المحاولة لاحقاً.",
                reply_markup=main_menu_keyboard(),
            )
            return

        for msg_id in messages_list:
            try:
                await context.bot.copy_message(
                    chat_id=update.effective_chat.id,
                    from_chat_id=channel_id,
                    message_id=msg_id,
                    protect_content=True,
                )
            except Exception as e:
                print(f"Error sending message {msg_id} from {channel_id}: {e}")

        await update.message.reply_text(
            "✅ تم إرسال الملفات المطلوبة.\n"
            "يمكنك اختيار مواد أخرى أو العودة للقائمة الرئيسية.",
            reply_markup=main_menu_keyboard(),
        )
        context.user_data.clear()
        return

    # إذا لم يتعرف على النص
    await update.message.reply_text(
        "عذراً، لم أفهم طلبك. الرجاء استخدام الأزرار المتاحة.",
        reply_markup=main_menu_keyboard(),
    )
