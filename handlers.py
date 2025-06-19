import os
from telegram import ReplyKeyboardMarkup, KeyboardButton, Update
from telegram.ext import ContextTypes
from datetime import datetime
from resources import resources, channel_ids, temporary_culture_doc
from db import load_notified_users, add_notified_user, is_user_notified


# 🧭 القوائم الرئيسية
def main_menu_keyboard():
    return ReplyKeyboardMarkup(
        [
            [KeyboardButton("📘 المواد الدراسية")],
            [KeyboardButton("📤 آلية تقديم اعتراض")],
            [KeyboardButton("📌 عن البوت ومن وراه؟")],
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


def get_greeting():
    hour = datetime.now().hour
    if hour < 12:
        return "صباح الخير ☀"
    elif hour < 18:
        return "مساء النور 🌇"
    else:
        return "سهرة سعيدة 🌙"


async def notify_update_to_users(bot):
    try:
        users = await load_notified_users()
        for user_id in users:
            try:
                await bot.send_message(
                    chat_id=user_id,
                    text="🔔 تم تحديث محتوى البوت بنجاح! يمكنك الآن استعراض المواد الجديدة.",
                )
            except Exception as e:
                print(f"Error notifying user {user_id}: {e}")
    except Exception as e:
        print(f"Database error in notify_update_to_users: {e}")
        user_data = {}


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    name = user.first_name or "صديقي"
    greeting = get_greeting()

    await update.message.reply_text(
        f"{greeting} {name}!\n\n"
        "أهلاً في بوت المواد الدراسية، اختر من القائمة أدناه ما ترغب بالوصول إليه:",
        reply_markup=main_menu_keyboard(),
    )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = update.message.text

    if text == "🏠 القائمة الرئيسية":
        user_data[user_id] = {}
        await start(update, context)
        return

    if text == "🔙 رجوع":
        if user_id not in user_data:
            user_data[user_id] = {}
            await start(update, context)
            return

        current = user_data[user_id]

        if "section" in current:
            del current["section"]
            await update.message.reply_text("اختر القسم المطلوب 👇", reply_markup=section_keyboard())
        elif "term" in current:
            del current["term"]
            await update.message.reply_text("اختر السنة الدراسية 👇", reply_markup=year_keyboard())
        elif "year" in current:
            del current["year"]
            await start(update, context)
        else:
            await start(update, context)
        return

    if text == "📘 المواد الدراسية":
        user_data[user_id] = {}
        await update.message.reply_text("اختر السنة الدراسية 👇", reply_markup=year_keyboard())
        return

    if text in ["السنة الأولى", "السنة الثانية", "السنة الثالثة", "السنة الرابعة", "السنة الخامسة"]:
        user_data[user_id] = {"year": text}
        await update.message.reply_text("اختر الفصل الدراسي 👇", reply_markup=term_keyboard())
        return

    if text in ["الفصل الأول ⚡", "الفصل الثاني 🔥"]:
        if user_id not in user_data or "year" not in user_data[user_id]:
            await start(update, context)
            return
        user_data[user_id]["term"] = text
        await update.message.reply_text("اختر القسم 👇", reply_markup=section_keyboard())
        return

    if text in ["📘 القسم النظري", "🧪 القسم العملي"]:
        if user_id not in user_data or "term" not in user_data[user_id]:
            await start(update, context)
            return
        user_data[user_id]["section"] = "theoretical" if "نظري" in text else "practical"

        year = user_data[user_id]["year"]
        term = user_data[user_id]["term"]
        section = user_data[user_id]["section"]

        subjects = list(resources.get(year, {}).get(term, {}).get(section, {}).keys())

        if not subjects:
            await update.message.reply_text("لا يوجد مواد بعد لهذا الفصل 😔", reply_markup=main_menu_keyboard())
            return

        await update.message.reply_text("اختر المادة 👇", reply_markup=subjects_keyboard(subjects))
        return

    # التكملة في الجزء الثالث (تشمل اختيار المادة، نوع المحتوى، وإرسال الملفات)
    year = user_data[user_id].get("year")
    term = user_data[user_id].get("term")
    section = user_data[user_id].get("section")

    if year and term and section:
        subjects = list(resources.get(year, {}).get(term, {}).get(section, {}).keys())

        if text in subjects:
            user_data[user_id]["subject"] = text

            types = list(
                resources[year][term][section][text].keys()
            )
            await update.message.reply_text("اختر نوع المحتوى المطلوب 👇", reply_markup=types_keyboard(types))
            return

        subject = user_data[user_id].get("subject")

        if subject and text in resources[year][term][section][subject]:
            files = resources[year][term][section][subject][text]
            channel_id = channel_ids.get((year, term), temporary_culture_doc)

            if files:
                for file_id in files:
                    try:
                        await context.bot.forward_message(
                            chat_id=update.effective_chat.id,
                            from_chat_id=channel_id,
                            message_id=file_id,
                        )
                    except Exception as e:
                        logging.error(f"فشل في إرسال الملف {file_id}: {e}")
                await update.message.reply_text("تم عرض الملفات ✅", reply_markup=main_menu_keyboard())
            else:
                await update.message.reply_text("لا يوجد ملفات حالياً لهذا النوع.", reply_markup=main_menu_keyboard())
            return

    await update.message.reply_text("لم أفهم هذا الأمر، الرجاء اختيار أمر من الأزرار 👇", reply_markup=main_menu_keyboard())
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.constants import ParseMode

def main_menu_keyboard():
    return ReplyKeyboardMarkup(
        [["الرجوع للقائمة الرئيسية 🔙"]], resize_keyboard=True
    )

def year_term_keyboard(years_terms):
    return ReplyKeyboardMarkup(
        [[f"{year} - {term}"] for year, term in years_terms],
        resize_keyboard=True,
    )

def section_keyboard():
    return ReplyKeyboardMarkup(
        [["نظري", "عملي"], ["الرجوع 🔙"]],
        resize_keyboard=True,
    )

def subjects_keyboard(subjects):
    keyboard = [subjects[i:i+2] for i in range(0, len(subjects), 2)]
    keyboard.append(["الرجوع 🔙"])
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

def types_keyboard(types):
    keyboard = [types[i:i+2] for i in range(0, len(types), 2)]
    keyboard.append(["الرجوع 🔙"])
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

def save_notified_user(user_id):
    try:
        with open("notified_users.json", "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        data = []

    if user_id not in data:
        data.append(user_id)
        with open("notified_users.json", "w") as f:
            json.dump(data, f)
            import logging
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
)
from telegram import Update

# إعدادات تسجيل الدخول (لو حبيت تظهر الأخطاء في الكونسول)
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


# دالة start: ترحيب المستخدم وبداية التفاعل
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


# دالة help (اختيارية لشرح البوت)
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "مرحباً! استخدم الأزرار لاختيار المواد أو تفعيل الإشعارات."
    )


# دالة رئيسية لتشغيل التطبيق
def main():
    application = ApplicationBuilder().token("YOUR_BOT_TOKEN").build()

    # تسجيل Handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # تشغيل البوت
    application.run_polling()


if __name__ == "__main__":
    main()
    # دالة لإزالة الإيموجي من بداية اسم المادة (للتأكد من اختيار المادة بدون رموز)
def strip_emoji(text: str) -> str:
    # تفترض الإيموجي مكونة من حرفين (يمكن تعديل حسب الحاجة)
    return text[2:] if len(text) > 2 else text


# دالة لاختيار المادة بعد السنة والفصل والقسم
async def choose_subject(update: Update, context: ContextTypes.DEFAULT_TYPE):
    year = context.user_data.get("year")
    term = context.user_data.get("term")
    if not year or not term:
        await update.message.reply_text(
            "الرجاء اختيار السنة والفصل أولاً.",
            reply_markup=main_menu_keyboard(),
        )
        return

    # تجميع كل المواد من القسم النظري والعملي بدون تكرار
    theoretical_subjects = list(resources.get(year, {}).get(term, {}).get("theoretical", {}).keys())
    practical_subjects = list(resources.get(year, {}).get(term, {}).get("practical", {}).keys())
    all_subjects_set = set(theoretical_subjects + practical_subjects)
    all_subjects = sorted(all_subjects_set)

    prefix = "⚡ " if term == "الفصل الأول" else "🔥 "
    subjects_with_prefix = [prefix + subj for subj in all_subjects]

    await update.message.reply_text(
        "اختر المادة:",
        reply_markup=subjects_keyboard(subjects_with_prefix),
    )


# دالة اختيار القسم (نظري أو عملي) للمادة المختارة
async def choose_section(update: Update, context: ContextTypes.DEFAULT_TYPE):
    subject = context.user_data.get("subject")
    year = context.user_data.get("year")
    term = context.user_data.get("term")

    if not subject or not year or not term:
        await update.message.reply_text(
            "حدث خطأ في اختيار المادة أو السنة أو الفصل، يرجى البدء من جديد.",
            reply_markup=main_menu_keyboard(),
        )
        context.user_data.clear()
        return

    available_sections = []
    if subject in resources.get(year, {}).get(term, {}).get("theoretical", {}):
        available_sections.append("theoretical")
    if subject in resources.get(year, {}).get(term, {}).get("practical", {}):
        available_sections.append("practical")

    if len(available_sections) == 1:
        context.user_data["section"] = available_sections[0]
        await update.message.reply_text(
            "اختر نوع المحتوى المطلوب:",
            reply_markup=content_type_keyboard(),
        )
    elif len(available_sections) > 1:
        await update.message.reply_text(
            "اختر القسم (نظري أو عملي):",
            reply_markup=section_keyboard(),
        )
    else:
        await update.message.reply_text(
            "لا تتوفر أقسام لهذه المادة حالياً.",
            reply_markup=main_menu_keyboard(),
        )
        context.user_data.clear()


# دالة إرسال الملفات المطلوبة للمستخدم بناء على الاختيارات
async def send_selected_content(update: Update, context: ContextTypes.DEFAULT_TYPE):
    year = context.user_data.get("year")
    term = context.user_data.get("term")
    section = context.user_data.get("section")
    subject = context.user_data.get("subject")
    content_type_map = {
        "📚 محاضرات Gate": "gate",
        "📚 محاضرات الكميت": "komit",
        "✍ محاضرات كتابة زميلنا / دكتور المادة": "student_written",
        "📄 ملخصات": "summaries",
        "❓ أسئلة دورات": "exams",
        "📝 ملاحظات المواد": "notes",
    }
    text = update.message.text

    if text not in content_type_map:
        await update.message.reply_text(
            "الرجاء اختيار نوع المحتوى من الأزرار المتاحة.",
            reply_markup=content_type_keyboard(),
        )
        return

    content_key = content_type_map[text]

    # التحقق من توفر البيانات
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
        "✅ تم إرسال الملفات المطلوبة.\nيمكنك اختيار مواد أخرى أو العودة للقائمة الرئيسية.",
        reply_markup=main_menu_keyboard(),
    )
    context.user_data.clear()
    # دالة التعامل مع أمر "تفعيل إشعارات التحديثات"
async def activate_notifications(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    try:
        from db import is_user_notified
        is_already_notified = await is_user_notified(user_id)

        if not is_already_notified:
            success = await add_notified_user(user_id)
            if success:
                await update.message.reply_text(
                    "✅ تم تفعيل إشعارات التحديثات بنجاح. ستتلقى تنبيهات عند تحديث محتوى البوت.",
                    reply_markup=main_menu_keyboard(),
                )
            else:
                await update.message.reply_text(
                    "⚠ حدث خطأ في تفعيل الإشعارات. يرجى المحاولة لاحقاً.",
                    reply_markup=main_menu_keyboard(),
                )
        else:
            await update.message.reply_text(
                "ℹ أنت مفعل الإشعارات سابقاً.",
                reply_markup=main_menu_keyboard(),
            )
    except Exception as e:
        print(f"Database error: {e}")
        await update.message.reply_text(
            "⚠ حدث خطأ في تفعيل الإشعارات. يرجى المحاولة لاحقاً.",
            reply_markup=main_menu_keyboard(),
        )


# دالة الإجراء للرجوع للخطوة السابقة أو القائمة الرئيسية
async def go_back(update: Update, context: ContextTypes.DEFAULT_TYPE):
    previous_step = context.user_data.get("previous_step")
    if previous_step:
        await previous_step(update, context)
    else:
        await start(update, context)


# دالة إرسال شرح اعتراض
async def send_objection_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
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


# دالة إرسال شرح "عن البوت ومن وراه؟"
async def send_about_bot(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📌 عن البوت ومن وراه؟\n\n"
        "أنا عمار سطوف [@ammarsa51]، مطوّر ومبرمج هذا البوت 🎯\n"
        "صمّمته لحتى يساعد الطلاب يوصلوا للمحتوى الدراسي بسهولة وسرعة، وبشكل منظم وواضح.\n\n"
        "🔧 بس البوت ما كان ليكون بهالشكل بدون الفريق الرائع يلي ساعدني:\n\n"
        "👩‍💻 جودي حاضري [@JoudyHadry]\n"
        "الداعمة الأساسية، اشتغلت على تجهيز المحتوى، تنظيم الملفات، ومتابعة التفاصيل. وجودها كان فرق حقيقي بكل خطوة تطوير.\n\n"
        "👨‍💼 غدير ونوس [@ghadeer_wanous]\n"
        "مساعد خفيف، ساعدني بأوقات مختلفة في ترتيب وتنظيم المحتوى، وكان دعمه إضافة لطيفة ضمن الفريق.\n\n"
        "---\n\n"
        "🚀 جزء من فريق 0x Team – فريق شبابي مهتم بالتطوير والتقنية، وهدفه تقديم حلول ذكية وعملية عبر تيليجرام وغيرها.\n"
        "تابعونا على تيليجرام: @zeroxxteam",
        reply_markup=main_menu_keyboard(),
    )


# دالة إرسال مقرر الثقافة المؤقت (محدد مسبقاً)
async def send_culture_doc(update: Update, context: ContextTypes.DEFAULT_TYPE):
    cid = channel_ids.get("komit")
    msg_id = temporary_culture_doc
    if cid and msg_id:
        try:
            await context.bot.copy_message(
                chat_id=update.effective_chat.id,
                from_chat_id=cid,
                message_id=msg_id,
                protect_content=True,
            )
        except Exception as e:
            print(f"Error sending culture document: {e}")
            await update.message.reply_text(
                "عذراً، حدث خطأ أثناء إرسال مقرر الثقافة. حاول مرة أخرى لاحقاً.",
                reply_markup=main_menu_keyboard(),
            )
    else:
        await update.message.reply_text(
            "مقرر الثقافة غير متوفر حالياً.",
            reply_markup=main_menu_keyboard(),
        )


# دالة التعامل مع الرسائل الواردة بشكل عام
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    # الأوامر الخاصة
    if text == "📚 المواد الدراسية":
        await choose_year(update, context)
        return
    elif text in ["الفصل الأول", "الفصل الثاني"]:
        context.user_data["term"] = text
        await choose_section_type(update, context)
        return
    elif text in ["نظري", "عملي"]:
        context.user_data["section_type"] = text
        await choose_subject(update, context)
        return
    elif text.startswith("⚡ ") or text.startswith("🔥 "):
        # اختيار المادة (مع إزالة الإيموجي)
        subject = strip_emoji(text)
        context.user_data["subject"] = subject
        await choose_section(update, context)
        return
    elif text in ["نظري", "عملي"]:
        context.user_data["section"] = "theoretical" if text == "نظري" else "practical"
        await update.message.reply_text(
            "اختر نوع المحتوى المطلوب:",
            reply_markup=content_type_keyboard(),
        )
        return
    elif text in [
        "📚 محاضرات Gate",
        "📚 محاضرات الكميت",
        "✍ محاضرات كتابة زميلنا / دكتور المادة",
        "📄 ملخصات",
        "❓ أسئلة دورات",
        "📝 ملاحظات المواد",
    ]:
        await send_selected_content(update, context)
        return
    elif text == "تفعيل إشعارات التحديثات":
        await activate_notifications(update, context)
        return
    elif text == "العودة للقائمة الرئيسية":
        context.user_data.clear()
        await start(update, context)
        return
    elif text == "اعتراض على النتائج":
        await send_objection_info(update, context)
        return
    elif text == "عن البوت ومن وراه؟":
        await send_about_bot(update, context)
        return
    elif text == "مقرر الثقافة المؤقت":
        await send_culture_doc(update, context)
        return
    else:
        await update.message.reply_text(
            "عذراً، لم أفهم الأمر. يرجى اختيار أحد الخيارات من القائمة.",
            reply_markup=main_menu_keyboard(),
        )
