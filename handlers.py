import os
from telegram import ReplyKeyboardMarkup, KeyboardButton, Update
from telegram.ext import ContextTypes
from resources import resources, channel_ids, temporary_culture_doc, practical_exam_schedule
from datetime import datetime
from db import load_notified_users, add_notified_user


# إضافة زر تفعيل الإشعارات للقائمة الرئيسية
def main_menu_keyboard():
    return ReplyKeyboardMarkup(
        [
            [KeyboardButton("🏛️ الأفرع الجامعية"), 
             KeyboardButton("📗 مقرر الثقافة المؤقت")],
            [KeyboardButton("🔍 البحث الذكي"), 
             KeyboardButton("🔔 تفعيل إشعارات التحديثات")],
            [KeyboardButton("⏰ التذكيرات الذكية"), 
             KeyboardButton("🌙 تغيير المظهر")],
            [KeyboardButton("👥 عن البوت والفريق"), 
             KeyboardButton("📤 آلية تقديم اعتراض")],
        ],
        resize_keyboard=True,
        one_time_keyboard=True,
    )


def university_branches_keyboard():
    return ReplyKeyboardMarkup(
        [
            [KeyboardButton("💻 الهندسة المعلوماتية"), 
             KeyboardButton("🏗️ الهندسة المعمارية")],
            [KeyboardButton("🚧 الهندسة المدنية"), 
             KeyboardButton("🏥 الهندسة الطبية")],
            [KeyboardButton("🔙 رجوع"),
             KeyboardButton("🏠 القائمة الرئيسية")],
        ],
        resize_keyboard=True,
    )


def informatics_menu_keyboard():
    return ReplyKeyboardMarkup(
        [
            [KeyboardButton("📘 المواد الدراسية"), 
             KeyboardButton("📅 برنامج الامتحان العملي")],
            [KeyboardButton("🔙 رجوع"),
             KeyboardButton("🏠 القائمة الرئيسية")],
        ],
        resize_keyboard=True,
    )


def year_keyboard():
    return ReplyKeyboardMarkup(
        [
            [KeyboardButton("السنة الأولى"),
             KeyboardButton("السنة الثانية")],
            [KeyboardButton("السنة الثالثة"),
             KeyboardButton("السنة الرابعة")],
            [KeyboardButton("السنة الخامسة")],
            [KeyboardButton("🔙 رجوع"),
             KeyboardButton("🏠 القائمة الرئيسية")],
        ],
        resize_keyboard=True,
    )


def specialization_keyboard():
    return ReplyKeyboardMarkup(
        [
            [
                KeyboardButton("هندسة البرمجيات"),
                KeyboardButton("الشبكات والنظم")
            ],
            [KeyboardButton("الذكاء الاصطناعي")],
            [KeyboardButton("🔙 رجوع"),
             KeyboardButton("🏠 القائمة الرئيسية")],
        ],
        resize_keyboard=True,
    )


def term_keyboard():
    return ReplyKeyboardMarkup(
        [
            [
                KeyboardButton("الفصل الأول ⚡"),
                KeyboardButton("الفصل الثاني 🔥")
            ],
            [KeyboardButton("🔙 رجوع"),
             KeyboardButton("🏠 القائمة الرئيسية")],
        ],
        resize_keyboard=True,
    )


def section_keyboard():
    return ReplyKeyboardMarkup(
        [
            [
                KeyboardButton("📘 القسم النظري"),
                KeyboardButton("🧪 القسم العملي")
            ],
            [KeyboardButton("🔙 رجوع"),
             KeyboardButton("🏠 القائمة الرئيسية")],
        ],
        resize_keyboard=True,
    )


def content_type_keyboard():
    return ReplyKeyboardMarkup(
        [
            [
                KeyboardButton("📚 محاضرات Gate"),
                KeyboardButton("📚 محاضرات الكميت")
            ],
            [KeyboardButton("✍ محاضرات كتابة زميلنا / دكتور المادة")],
            [KeyboardButton("📄 ملخصات"),
             KeyboardButton("❓ أسئلة دورات")],
            [KeyboardButton("📝 ملاحظات المواد"),
             KeyboardButton("⭐ تقييم المحتوى")],
            [KeyboardButton("📊 عرض التقييمات"),
             KeyboardButton("🤖 المساعد الذكي")],
            [KeyboardButton("🔙 رجوع"),
             KeyboardButton("🏠 القائمة الرئيسية")],
        ],
        resize_keyboard=True,
    )

def ai_assistant_keyboard():
    return ReplyKeyboardMarkup(
        [
            [KeyboardButton("💡 نصائح دراسية"), 
             KeyboardButton("📝 أسئلة تدريبية")],
            [KeyboardButton("📊 ملخص سريع"), 
             KeyboardButton("🎯 خطة دراسية")],
            [KeyboardButton("❓ سؤال حر")],
            [KeyboardButton("🔙 رجوع"),
             KeyboardButton("🏠 القائمة الرئيسية")],
        ],
        resize_keyboard=True,
    )

def rating_keyboard():
    return ReplyKeyboardMarkup(
        [
            [KeyboardButton("⭐ 1"), KeyboardButton("⭐⭐ 2"), 
             KeyboardButton("⭐⭐⭐ 3")],
            [KeyboardButton("⭐⭐⭐⭐ 4"), 
             KeyboardButton("⭐⭐⭐⭐⭐ 5")],
            [KeyboardButton("🔙 رجوع"),
             KeyboardButton("🏠 القائمة الرئيسية")],
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

    keyboard.append(
        [KeyboardButton("🔙 رجوع"),
         KeyboardButton("🏠 القائمة الرئيسية")])

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
    try:
        users = await load_notified_users()
        for user_id in users:
            try:
                await bot.send_message(
                    chat_id=user_id,
                    text=
                    "🔔 تم تحديث محتوى البوت بنجاح! يمكنك الآن استعراض المواد الجديدة."
                )
            except Exception as e:
                print(f"Error notifying user {user_id}: {e}")
    except Exception as e:
        print(f"Database error in notify_update_to_users: {e}")


# 🚀 البداية
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_first_name = update.effective_user.first_name or "طالبنا"
    user_id = update.effective_user.id
    greeting = get_greeting()

    welcome_text = (
        f"🌟 {greeting} يا {user_first_name}! أهلاً وسهلاً بك في منصتك التعليمية 🌟\n\n"
        "🏛️ مرحباً بك في البوت التعليمي الخاص بجامعة اللاذقية\n"
        "✨ مكانك الأمثل للحصول على كل ما تحتاجه في رحلتك الأكاديمية\n\n"
        "🎓 نوفر لك محتوى شامل لجميع الأفرع الهندسية:\n"
        "💻 الهندسة المعلوماتية • 🏗️ الهندسة المعمارية\n"
        "🚧 الهندسة المدنية • 🏥 الهندسة الطبية\n\n"
        "🚀 فريق 0x Team معك خطوة بخطوة نحو التفوق\n"
        "💡 مواد منظمة • ملخصات شاملة • امتحانات سابقة • نصائح دراسية\n\n"
        "📚 فريق SP_ITE ساعد في تقديم محتوى مواد كلية الهندسة المعلوماتية\n\n"
        "🎯 اختر فرعك من القائمة أدناه وابدأ رحلة التميز! 📚✨"
    )

    # تطبيق المظهر على النص
    themed_text = apply_theme_to_text(welcome_text, user_id, context)

    await update.message.reply_text(
        themed_text,
        reply_markup=main_menu_keyboard()
    )
    context.user_data.clear()


# المساعد الذكي المتطور
def ai_assistant_response(question, subject=None, free_text=None, user_context=None):
    """مساعد ذكي متطور للإجابة على الأسئلة الأكاديمية"""
    
    # قاعدة معرفة موسعة
    knowledge_base = {
        "برمجة": {
            "نصائح": "💻 نصائح متقدمة للبرمجة:\n\n🔥 المستوى المبتدئ:\n• ابدأ بـ Python أو C++ (حسب مادتك)\n• تعلم المفاهيم الأساسية: المتغيرات، الشروط، الحلقات\n• تدرب يومياً لمدة ساعة على الأقل\n\n🚀 المستوى المتقدم:\n• تعلم Algorithms و Data Structures\n• شارك في مسابقات البرمجة\n• ابني مشاريع شخصية\n\n💡 نصائح الامتحان:\n• حل 50+ مسألة قبل الامتحان\n• راجع أخطائك المتكررة\n• تدرب على كتابة الكود بدون IDE",
            
            "مشاكل": "🔧 حلول للمشاكل الشائعة:\n\n❌ مشكلة: 'لا أفهم الخوارزميات'\n✅ الحل: ابدأ بالرسم والمخططات التدفقية\n\n❌ مشكلة: 'أنسى syntax اللغة'\n✅ الحل: اكتب cheat sheet شخصي\n\n❌ مشكلة: 'لا أستطيع حل المسائل'\n✅ الحل: ابدأ بمسائل بسيطة وتدرج\n\n🎯 تذكر: البرمجة مهارة تحتاج ممارسة مستمرة!"
        },
        
        "رياضيات": {
            "نصائح": "📊 استراتيجية شاملة للرياضيات:\n\n📚 التحليل والجبر:\n• فهم المفاهيم قبل الحفظ\n• حل 10 تمارين يومياً\n• اربط المفاهيم ببعضها\n\n🔢 التطبيق العملي:\n• استخدم الآلة الحاسبة بذكاء\n• تعلم الاختصارات الرياضية\n• مارس الرسم البياني\n\n⚡ نصائح الامتحان:\n• ابدأ بالأسئلة السهلة\n• راجع حلولك مرتين\n• اكتب الخطوات بوضوح",
            
            "قوانين": "📋 أهم القوانين:\n\n🔸 التفاضل:\n• قاعدة السلسلة: (f(g(x)))' = f'(g(x)) × g'(x)\n• تفاضل اللوغاريتم: (ln(x))' = 1/x\n\n🔸 التكامل:\n• التكامل بالتعويض\n• التكامل بالأجزاء\n\n🔸 المصفوفات:\n• ضرب المصفوفات\n• المحدد والمعكوس"
        },
        
        "فيزياء": {
            "نصائح": "⚡ فيزياء فعالة:\n\n🎯 فهم المفاهيم:\n• اربط النظرية بالواقع\n• استخدم المحاكيات\n• ارسم المخططات\n\n🔬 المعادلات:\n• احفظ الوحدات جيداً\n• تأكد من الأبعاد\n• تدرب على المسائل التطبيقية",
            
            "قوانين": "⚡ قوانين أساسية:\n\n🔸 الكهرباء:\n• قانون أوم: V = I × R\n• قانون كيرشوف للتيار والجهد\n\n🔸 أنصاف النواقل:\n• معادلة ديود\n• خصائص الترانزستور"
        }
    }
    
    # تحليل السؤال الحر بذكاء
    if free_text:
        text_lower = free_text.lower()
        response = "🤖 المساعد الذكي:\n\n"
        
        # تحديد موضوع السؤال
        if any(word in text_lower for word in ["برمجة", "كود", "خوارزمية", "program"]):
            if "صعب" in text_lower or "مشكلة" in text_lower:
                response += knowledge_base["برمجة"]["مشاكل"]
            else:
                response += knowledge_base["برمجة"]["نصائح"]
        
        elif any(word in text_lower for word in ["رياضيات", "تحليل", "جبر", "تفاضل"]):
            if "قانون" in text_lower or "معادلة" in text_lower:
                response += knowledge_base["رياضيات"]["قوانين"]
            else:
                response += knowledge_base["رياضيات"]["نصائح"]
        
        elif any(word in text_lower for word in ["فيزياء", "كهرباء", "دارة"]):
            if "قانون" in text_lower:
                response += knowledge_base["فيزياء"]["قوانين"]
            else:
                response += knowledge_base["فيزياء"]["نصائح"]
        
        elif any(word in text_lower for word in ["امتحان", "دراسة", "مراجعة"]):
            response += "📚 نصائح عامة للامتحانات:\n\n1. 📅 ضع خطة دراسية واقعية\n2. 🎯 ركز على النقاط المهمة\n3. ⏰ اتبع نظام pomodoro للدراسة\n4. 💤 احصل على راحة كافية\n5. 🧘 تدرب على تقنيات الاسترخاء\n\n💡 تذكر: الثقة بالنفس نصف النجاح!"
        
        elif any(word in text_lower for word in ["وقت", "تنظيم", "جدول"]):
            response += "⏰ إدارة الوقت الذكية:\n\n📊 تقنية Pomodoro:\n• 25 دقيقة دراسة مركزة\n• 5 دقائق راحة\n• كرر 4 مرات ثم استراحة طويلة\n\n📅 التخطيط الأسبوعي:\n• حدد أولوياتك\n• اتبع قاعدة 80/20\n• اترك وقت للمراجعة\n\n🎯 نصائح إضافية:\n• استخدم تطبيقات التذكير\n• احتفظ بقائمة مهام يومية"
        
        else:
            response += f"💭 سؤالك: '{free_text}'\n\n🔍 دعني أحلل سؤالك...\n\n"
            response += "✨ نصائح عامة:\n• كن محدداً في أسئلتك\n• اطرح أسئلة حول مواضيع معينة\n• استخدم كلمات مفتاحية واضحة\n\n🎓 يمكنني مساعدتك في:\n• البرمجة والخوارزميات\n• الرياضيات والتحليل\n• الفيزياء والدارات\n• تنظيم الدراسة والامتحانات"
        
        return response
    
    # الأسئلة المحددة مسبقاً
    responses = {
        "نصائح دراسية": {
            "default": "🎓 نصائح دراسية ذكية:\n\n📚 تقنيات الدراسة:\n• Active Learning: لا تقرأ فقط، طبق\n• Spaced Repetition: راجع بفترات متباعدة\n• Feynman Technique: اشرح للآخرين\n\n🧠 تحسين التركيز:\n• اختر مكان هادئ\n• أغلق الإشعارات\n• استخدم الموسيقى الهادئة\n\n💪 تطوير الذات:\n• ضع أهداف قابلة للقياس\n• احتفل بالإنجازات الصغيرة\n• تعلم من الأخطاء"
        },
        
        "أسئلة تدريبية": {
            "default": "❓ أسئلة تدريبية متنوعة:\n\n🔸 برمجة:\n• اكتب خوارزمية للبحث الثنائي\n• ما الفرق بين Stack و Queue؟\n• شرح مفهوم Recursion\n\n🔸 رياضيات:\n• احسب نهاية دالة معطاة\n• حل نظام معادلات خطية\n• جد مشتقة دالة مركبة\n\n🔸 فيزياء:\n• حلل دارة كهربائية بسيطة\n• احسب التيار في مقاوم"
        }
    }
    
    # إرجاع الإجابة المناسبة
    if question in responses:
        return responses[question].get(subject, responses[question]["default"])
    
    return "🤖 مرحباً! أنا مساعدك الذكي المطور.\n\n💡 اسألني عن:\n• نصائح دراسية محددة\n• حل مشاكل أكاديمية\n• تنظيم الوقت والدراسة\n• أي موضوع دراسي\n\n✨ كلما كان سؤالك أكثر تحديداً، كانت إجابتي أكثر فائدة!"

# نظام البحث الذكي المحسن - يبحث فقط في المواد التي لها محتوى
def search_content(query):
    """البحث في المحتوى بالكلمات المفتاحية - يعرض فقط المواد التي لها محتوى"""
    from resources import resources, channel_ids
    results = []
    query_lower = query.lower()

    def has_content(subject_data):
        """فحص إذا كان للمادة محتوى فعلي"""
        for content_type, messages in subject_data.items():
            if isinstance(messages, list) and messages != [0] and len(messages) > 0:
                return True
        return False

    for year, year_data in resources.items():
        if year == "specializations":
            continue
        for term, term_data in year_data.items():
            if term == "specializations":
                continue
            if year in ["السنة الرابعة", "السنة الخامسة"]:
                for spec, spec_data in term_data.items():
                    if isinstance(spec_data, dict):
                        for section, section_data in spec_data.items():
                            if isinstance(section_data, dict):
                                for subject, subject_content in section_data.items():
                                    if has_content(subject_content):
                                        clean_subject = subject.replace("⚡ ", "").replace("🔥 ", "")
                                        if query_lower in clean_subject.lower():
                                            results.append({
                                                "year": year,
                                                "term": term,
                                                "specialization": spec,
                                                "section": section,
                                                "subject": clean_subject,
                                                "content_available": True
                                            })
            else:
                for section, section_data in term_data.items():
                    if isinstance(section_data, dict):
                        for subject, subject_content in section_data.items():
                            if has_content(subject_content):
                                clean_subject = subject.replace("⚡ ", "").replace("🔥 ", "")
                                if query_lower in clean_subject.lower():
                                    results.append({
                                        "year": year,
                                        "term": term,
                                        "section": section,
                                        "subject": clean_subject,
                                        "content_available": True
                                    })

    # إزالة النتائج المكررة
    unique_results = []
    seen = set()
    for result in results:
        key = f"{result['year']}-{result['term']}-{result.get('specialization', '')}-{result['section']}-{result['subject']}"
        if key not in seen:
            seen.add(key)
            unique_results.append(result)

    return unique_results

# نظام المظهر المحسن
user_themes = {}  # قاموس عالمي لحفظ المظاهر

def get_user_theme(user_id, context):
    """الحصول على مظهر المستخدم"""
    return user_themes.get(user_id, "light")

def set_user_theme(user_id, theme, context):
    """تعيين مظهر المستخدم"""
    user_themes[user_id] = theme
    context.user_data[f"theme_{user_id}"] = theme

def apply_theme_to_text(text, user_id, context):
    """تطبيق المظهر على النص"""
    theme = get_user_theme(user_id, context)
    if theme == "dark":
        # تطبيق المظهر المظلم
        themed_text = text.replace("🌟", "⭐").replace("☀", "🌙").replace("🌇", "🌃")
        themed_text = themed_text.replace("💡", "🔥").replace("✨", "⭐")
        themed_text = themed_text.replace("🎓", "🎯").replace("📚", "📖")
        return f"🌙 المظهر المظلم\n\n{themed_text}"
    else:
        return f"☀️ المظهر الفاتح\n\n{text}"

def theme_keyboard():
    return ReplyKeyboardMarkup(
        [
            [KeyboardButton("🌞 المظهر الفاتح"), 
             KeyboardButton("🌙 المظهر المظلم")],
            [KeyboardButton("🔙 رجوع"),
             KeyboardButton("🏠 القائمة الرئيسية")],
        ],
        resize_keyboard=True,
    )

# 📩 المعالجة الرئيسية
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    user_id = update.effective_user.id

    # البحث الذكي
    if text == "🔍 البحث الذكي":
        context.user_data["search_mode"] = True
        await update.message.reply_text(
            "🔍 نظام البحث الذكي المتطور\n\n"
            "💡 اكتب اسم المادة أو جزء منها للبحث عنها في جميع السنوات والتخصصات\n\n"
            "🎯 مثال: اكتب 'برمجة' للعثور على جميع مواد البرمجة\n"
            "📚 مثال: اكتب 'داتا' للعثور على مواد قواعد البيانات\n\n"
            "✨ البحث يشمل جميع السنوات والأقسام والتخصصات",
            reply_markup=ReplyKeyboardMarkup(
                [[KeyboardButton("🔙 رجوع"), KeyboardButton("🏠 القائمة الرئيسية")]],
                resize_keyboard=True
            )
        )
        return

    # تغيير المظهر
    if text == "🌙 تغيير المظهر":
        user_id = update.effective_user.id
        current_theme = get_user_theme(user_id, context)
        theme_emoji = "🌙" if current_theme == "light" else "🌞"

        await update.message.reply_text(
            f"🎨 إعدادات المظهر\n\n"
            f"المظهر الحالي: {theme_emoji} {current_theme}\n\n"
            "اختر المظهر المفضل لديك:",
            reply_markup=theme_keyboard()
        )
        return

    # معالجة اختيار المظهر
    if text in ["🌞 المظهر الفاتح", "🌙 المظهر المظلم"]:
        user_id = update.effective_user.id
        theme = "light" if text == "🌞 المظهر الفاتح" else "dark"
        set_user_theme(user_id, theme, context)

        theme_name = "الفاتح" if theme == "light" else "المظلم"
        emoji = "🌞" if theme == "light" else "🌙"

        themed_response = apply_theme_to_text(
            f"✅ تم تعيين المظهر {emoji} {theme_name} بنجاح!\n\n"
            "🎨 سيتم تطبيق المظهر الجديد على جميع الرسائل.\n"
            "🔄 يمكنك تغيير المظهر في أي وقت من القائمة الرئيسية.",
            user_id, context
        )

        await update.message.reply_text(
            themed_response,
            reply_markup=main_menu_keyboard()
        )
        return

    # معالجة البحث
    if context.user_data.get("search_mode"):
        if text in ["🔙 رجوع", "🏠 القائمة الرئيسية"]:
            context.user_data.pop("search_mode", None)
            if text == "🔙 رجوع":
                await update.message.reply_text(
                    "تم إلغاء البحث",
                    reply_markup=main_menu_keyboard()
                )
            else:
                await start(update, context)
            return

        # تنفيذ البحث
        results = search_content(text)

        if not results:
            await update.message.reply_text(
                f"❌ لم يتم العثور على نتائج للبحث: '{text}'\n\n"
                "💡 جرب البحث بكلمات أخرى أو تأكد من الإملاء",
                reply_markup=ReplyKeyboardMarkup(
                    [[KeyboardButton("🔙 رجوع"), KeyboardButton("🏠 القائمة الرئيسية")]],
                    resize_keyboard=True
                )
            )
            return

        # عرض النتائج
        response = f"🔍 نتائج البحث عن: '{text}'\n\n"
        response += f"📊 تم العثور على {len(results)} نتيجة:\n\n"

        # تجميع النتائج حسب السنة لعرض أفضل
        results_by_year = {}
        for result in results:
            year = result['year']
            if year not in results_by_year:
                results_by_year[year] = []
            results_by_year[year].append(result)

        count = 0
        for year in sorted(results_by_year.keys()):
            if count >= 15:  # عرض أول 15 نتيجة
                break
            response += f"🎓 {year}:\n"
            for result in results_by_year[year]:
                if count >= 15:
                    break
                count += 1
                response += f"  • 📚 {result['subject']} ✅\n"
                response += f"    📅 {result['term']}\n"
                if 'specialization' in result and result['specialization']:
                    response += f"    🔧 {result['specialization']}\n"
                response += f"    📖 {result['section']}\n"
                response += f"    💾 يحتوي على ملفات دراسية\n\n"

        if len(results) > 15:
            response += f"📋 ... و {len(results) - 15} نتيجة أخرى\n\n"

        response += "💡 اكتب كلمة أخرى للبحث مرة أخرى أو اضغط رجوع"

        # تطبيق المظهر على النص
        themed_response = apply_theme_to_text(response, user_id, context)

        await update.message.reply_text(
            themed_response,
            reply_markup=ReplyKeyboardMarkup(
                [[KeyboardButton("🔙 رجوع"), KeyboardButton("🏠 القائمة الرئيسية")]],
                resize_keyboard=True
            )
        )
        return

    # التذكيرات الذكية
    if text == "⏰ التذكيرات الذكية":
        await update.message.reply_text(
            "⏰ نظام التذكيرات الذكية\n\n"
            "🎯 هذه الميزة قيد التطوير!\n\n"
            "🔜 قريباً ستتمكن من:\n"
            "• تعيين تذكيرات للامتحانات\n"
            "• جدولة المراجعة الشخصية\n"
            "• إشعارات المواعيد المهمة\n"
            "• تذكيرات المهام الأكاديمية\n\n"
            "📅 ابقَ متابعاً للتحديثات!",
            reply_markup=main_menu_keyboard()
        )
        return

    # المساعد الذكي
    if text == "🤖 المساعد الذكي":
        context.user_data["ai_mode"] = True
        await update.message.reply_text(
            "🤖 المساعد الذكي التعليمي\n\n"
            "🎓 مرحباً! أنا مساعدك الذكي للدعم الأكاديمي\n\n"
            "💡 يمكنني مساعدتك في:\n"
            "• تقديم نصائح دراسية مخصصة\n"
            "• إنشاء أسئلة تدريبية\n"
            "• تقديم ملخصات سريعة\n"
            "• وضع خطط دراسية\n\n"
            "🎯 اختر ما تحتاجه:",
            reply_markup=ai_assistant_keyboard()
        )
        return

    # تقييم المحتوى
    if text == "⭐ تقييم المحتوى":
        subject = context.user_data.get("subject")
        if subject:
            context.user_data["rating_mode"] = True
            themed_response = apply_theme_to_text(
                f"⭐ تقييم المحتوى - {subject}\n\n"
                "🎯 ساعدنا في تحسين جودة المحتوى!\n"
                "📊 اختر تقييمك من 1 إلى 5 نجوم:\n\n"
                "⭐ 1 - ضعيف جداً\n"
                "⭐⭐ 2 - ضعيف\n"
                "⭐⭐⭐ 3 - متوسط\n"
                "⭐⭐⭐⭐ 4 - جيد\n"
                "⭐⭐⭐⭐⭐ 5 - ممتاز",
                user_id, context
            )
            await update.message.reply_text(
                themed_response,
                reply_markup=rating_keyboard()
            )
        else:
            await update.message.reply_text(
                "❌ يرجى اختيار مادة أولاً قبل التقييم",
                reply_markup=content_type_keyboard()
            )
        return

    # عرض التقييمات
    if text == "📊 عرض التقييمات":
        subject = context.user_data.get("subject")
        if subject:
            # إنشاء معرف فريد للمحتوى
            year = context.user_data.get("year", "")
            term = context.user_data.get("term", "")
            section = context.user_data.get("section", "")
            content_id = f"{year}-{term}-{section}-{subject}"
            
            try:
                from db import get_content_average_rating, get_content_reviews
                avg_rating, total_ratings = await get_content_average_rating(content_id)
                reviews = await get_content_reviews(content_id, 3)
                
                if total_ratings > 0:
                    stars = "⭐" * int(round(avg_rating))
                    response = f"📊 تقييمات المحتوى - {subject}\n\n"
                    response += f"⭐ المتوسط: {avg_rating:.1f}/5 {stars}\n"
                    response += f"👥 عدد المقيمين: {total_ratings}\n\n"
                    
                    if reviews:
                        response += "💬 بعض التعليقات:\n\n"
                        for i, review in enumerate(reviews, 1):
                            stars_review = "⭐" * review['rating']
                            response += f"{i}. {stars_review} - {review['review']}\n"
                    else:
                        response += "💭 لا توجد تعليقات بعد"
                else:
                    response = f"📊 تقييمات المحتوى - {subject}\n\n"
                    response += "🔍 لا توجد تقييمات لهذا المحتوى بعد\n"
                    response += "✨ كن أول من يقيم هذا المحتوى!"
                
                themed_response = apply_theme_to_text(response, user_id, context)
                await update.message.reply_text(
                    themed_response,
                    reply_markup=content_type_keyboard()
                )
                
            except Exception as e:
                print(f"Error getting ratings: {e}")
                await update.message.reply_text(
                    "❌ حدث خطأ في جلب التقييمات",
                    reply_markup=content_type_keyboard()
                )
        else:
            await update.message.reply_text(
                "❌ يرجى اختيار مادة أولاً لعرض التقييمات",
                reply_markup=content_type_keyboard()
            )
        return

    # معالجة المساعد الذكي
    if context.user_data.get("ai_mode"):
        if text in ["🔙 رجوع", "🏠 القائمة الرئيسية"]:
            context.user_data.pop("ai_mode", None)
            if text == "🔙 رجوع":
                await update.message.reply_text(
                    "🤖 شكراً لاستخدام المساعد الذكي!",
                    reply_markup=content_type_keyboard()
                )
            else:
                await start(update, context)
            return

        if text in ["💡 نصائح دراسية", "📝 أسئلة تدريبية"]:
            subject = context.user_data.get("subject", "")
            user_context = {
                "year": context.user_data.get("year"),
                "subject": subject,
                "user_id": user_id
            }
            response = ai_assistant_response(text, subject, None, user_context)
            themed_response = apply_theme_to_text(response, user_id, context)
            await update.message.reply_text(
                themed_response,
                reply_markup=ai_assistant_keyboard()
            )
            return

        if text == "📊 ملخص سريع":
            await update.message.reply_text(
                "📊 ملخص سريع:\n\n"
                "🎯 هذه الميزة قيد التطوير!\n"
                "🔜 قريباً ستحصل على ملخصات ذكية للمحاضرات",
                reply_markup=ai_assistant_keyboard()
            )
            return

        if text == "🎯 خطة دراسية":
            await update.message.reply_text(
                "🎯 خطة دراسية ذكية:\n\n"
                "📅 الأسبوع الأول:\n"
                "• يوم 1-2: مراجعة المفاهيم الأساسية\n"
                "• يوم 3-4: حل التمارين\n"
                "• يوم 5-6: مراجعة شاملة\n"
                "• يوم 7: راحة واسترخاء\n\n"
                "💡 خصص 2-3 ساعات يومياً للدراسة الفعالة",
                reply_markup=ai_assistant_keyboard()
            )
            return

        if text == "❓ سؤال حر":
            await update.message.reply_text(
                "❓ اسأل سؤالك:\n\n"
                "🤖 اكتب سؤالك وسأحاول الإجابة عليه!\n"
                "💡 مثال: 'كيف أحسن من مهاراتي في البرمجة؟'",
                reply_markup=ReplyKeyboardMarkup(
                    [[KeyboardButton("🔙 رجوع"), KeyboardButton("🏠 القائمة الرئيسية")]],
                    resize_keyboard=True
                )
            )
            context.user_data["free_question"] = True
            return

    # معالجة السؤال الحر
    if context.user_data.get("free_question"):
        if text not in ["🔙 رجوع", "🏠 القائمة الرئيسية"]:
            context.user_data.pop("free_question", None)

            # استخدام المساعد الذكي المطور للإجابة
            user_context = {
                "year": context.user_data.get("year"),
                "subject": context.user_data.get("subject"),
                "user_id": user_id
            }
            response = ai_assistant_response("", None, text, user_context)
            themed_response = apply_theme_to_text(response, user_id, context)

            await update.message.reply_text(
                themed_response,
                reply_markup=ai_assistant_keyboard()
            )
            return

    # معالجة التقييم
    if context.user_data.get("rating_mode"):
        rating_map = {
            "⭐ 1": 1, "⭐⭐ 2": 2, "⭐⭐⭐ 3": 3,
            "⭐⭐⭐⭐ 4": 4, "⭐⭐⭐⭐⭐ 5": 5
        }

        if text in rating_map:
            rating = rating_map[text]
            context.user_data["rating"] = rating
            context.user_data.pop("rating_mode", None)

            themed_response = apply_theme_to_text(
                f"✅ شكراً لك! تم تسجيل تقييمك: {text}\n\n"
                "📝 هل تريد إضافة تعليق على المحتوى؟ (اختياري)\n"
                "💭 اكتب تعليقك أو اضغط 'تخطي'\n\n"
                "💡 تعليقك سيساعد الطلاب الآخرين في اتخاذ قرار الدراسة من هنا",
                user_id, context
            )
            
            await update.message.reply_text(
                themed_response,
                reply_markup=ReplyKeyboardMarkup(
                    [
                        [KeyboardButton("⏭️ تخطي")],
                        [KeyboardButton("🔙 رجوع"), KeyboardButton("🏠 القائمة الرئيسية")]
                    ],
                    resize_keyboard=True
                )
            )
            context.user_data["review_mode"] = True
            return

    # معالجة التعليقات
    if context.user_data.get("review_mode"):
        if text == "⏭️ تخطي":
            # حفظ التقييم بدون تعليق
            try:
                subject = context.user_data.get("subject")
                rating = context.user_data.get("rating")
                year = context.user_data.get("year", "")
                term = context.user_data.get("term", "")
                section = context.user_data.get("section", "")
                content_id = f"{year}-{term}-{section}-{subject}"
                
                from db import add_content_rating
                await add_content_rating(user_id, content_id, rating, "")
                
                context.user_data.pop("review_mode", None)
                context.user_data.pop("rating", None)
                
                themed_response = apply_theme_to_text(
                    "✅ تم حفظ تقييمك بنجاح!\n"
                    "🙏 شكراً لمساهمتك في تحسين جودة المحتوى\n"
                    "📊 يمكنك الآن مشاهدة التقييمات من خيار 'عرض التقييمات'",
                    user_id, context
                )
                
                await update.message.reply_text(
                    themed_response,
                    reply_markup=content_type_keyboard()
                )
            except Exception as e:
                print(f"Error saving rating: {e}")
                await update.message.reply_text(
                    "❌ حدث خطأ في حفظ التقييم",
                    reply_markup=content_type_keyboard()
                )
            return
        elif text not in ["🔙 رجوع", "🏠 القائمة الرئيسية"]:
            # حفظ التقييم مع التعليق
            try:
                subject = context.user_data.get("subject")
                rating = context.user_data.get("rating")
                year = context.user_data.get("year", "")
                term = context.user_data.get("term", "")
                section = context.user_data.get("section", "")
                content_id = f"{year}-{term}-{section}-{subject}"
                
                from db import add_content_rating
                await add_content_rating(user_id, content_id, rating, text)
                
                context.user_data.pop("review_mode", None)
                context.user_data.pop("rating", None)
                
                themed_response = apply_theme_to_text(
                    "✅ تم حفظ تقييمك وتعليقك بنجاح!\n"
                    f"📊 تعليقك: {text}\n\n"
                    "🙏 شكراً لمساهمتك في تحسين جودة المحتوى\n"
                    "💡 تعليقك سيظهر للطلاب الآخرين ليساعدهم في اختيار المصادر",
                    user_id, context
                )
                
                await update.message.reply_text(
                    themed_response,
                    reply_markup=content_type_keyboard()
                )
            except Exception as e:
                print(f"Error saving rating with review: {e}")
                await update.message.reply_text(
                    "❌ حدث خطأ في حفظ التقييم والتعليق",
                    reply_markup=content_type_keyboard()
                )
            return

    # تفعيل إشعارات التحديثات
    if text == "🔔 تفعيل إشعارات التحديثات":
        try:
            from db import is_user_notified
            is_already_notified = await is_user_notified(user_id)

            if not is_already_notified:
                # جلب معلومات المستخدم
                first_name = update.effective_user.first_name or ""
                last_name = update.effective_user.last_name or ""

                success = await add_notified_user(user_id, first_name,
                                                  last_name)
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
        return

    # رجوع أو القائمة الرئيسية
    if text == "🔙 رجوع":
        # نحدد المرحلة الحالية بناء على البيانات المحفوظة
        year = context.user_data.get("year")
        specialization = context.user_data.get("specialization")
        term = context.user_data.get("term")
        subject = context.user_data.get("subject")
        section = context.user_data.get("section")
        current_step = context.user_data.get("current_step")
        in_branches = context.user_data.get("in_branches")
        in_informatics = context.user_data.get("in_informatics")

        print(
            f"Debug - Back button pressed. Data: year={year}, specialization={specialization}, term={term}, subject={subject}, section={section}, current_step={current_step}, in_branches={in_branches}, in_informatics={in_informatics}"
        )

        # إذا كان في مرحلة اختيار نوع المحتوى، يرجع للمرحلة السابقة
        if current_step == "content_type":
            # إذا كان القسم محدد، يرجع لاختيار القسم
            if section:
                context.user_data["current_step"] = "section"
                await update.message.reply_text(
                    "اختر القسم (نظري أو عملي):",
                    reply_markup=section_keyboard())
                return
            # إذا لم يكن محتاج قسم، يرجع للمواد
            else:
                context.user_data["current_step"] = "subject"

                # جلب المواد حسب السنة والتخصص
                if year in ["السنة الرابعة", "السنة الخامسة"]:
                    subjects_all = []
                    for section_key in ["theoretical", "practical"]:
                        subjects_all += list(
                            resources.get(year, {}).get(term, {}).get(
                                specialization, {}).get(section_key,
                                                        {}).keys())
                else:
                    subjects_all = []
                    for section_key in ["theoretical", "practical"]:
                        subjects_all += list(
                            resources.get(year,
                                          {}).get(term,
                                                  {}).get(section_key,
                                                          {}).keys())

                subjects_all_set = set(subjects_all)
                prefix = "⚡ " if term == "الفصل الأول" else "🔥 "
                subjects_with_emoji = [
                    prefix + subj for subj in sorted(subjects_all_set)
                ]

                await update.message.reply_text(
                    "اختر المادة:",
                    reply_markup=subjects_keyboard(subjects_with_emoji))
                return

        # إذا كان في مرحلة اختيار القسم، يرجع لاختيار المادة
        if current_step == "section":
            context.user_data["current_step"] = "subject"
            context.user_data.pop("section", None)

            # جلب المواد حسب السنة والتخصص
            if year in ["السنة الرابعة", "السنة الخامسة"]:
                subjects_all = []
                for section_key in ["theoretical", "practical"]:
                    subjects_all += list(
                        resources.get(year,
                                      {}).get(term,
                                              {}).get(specialization,
                                                      {}).get(section_key,
                                                              {}).keys())
            else:
                subjects_all = []
                for section_key in ["theoretical", "practical"]:
                    subjects_all += list(
                        resources.get(year, {}).get(term,
                                                    {}).get(section_key,
                                                            {}).keys())

            subjects_all_set = set(subjects_all)
            prefix = "⚡ " if term == "الفصل الأول" else "🔥 "
            subjects_with_emoji = [
                prefix + subj for subj in sorted(subjects_all_set)
            ]

            await update.message.reply_text(
                "اختر المادة:",
                reply_markup=subjects_keyboard(subjects_with_emoji))
            return

        # إذا كان في مرحلة اختيار المادة، يرجع لاختيار الفصل
        if current_step == "subject":
            context.user_data["current_step"] = "term"
            context.user_data.pop("subject", None)
            context.user_data.pop("section", None)

            await update.message.reply_text("اختر الفصل الدراسي:",
                                            reply_markup=term_keyboard())
            return

        # إذا كان في مرحلة اختيار الفصل، يرجع لاختيار التخصص أو السنة
        if current_step == "term":
            context.user_data.pop("term", None)

            # إذا كانت السنة الرابعة أو الخامسة، يرجع لاختيار التخصص
            if year in ["السنة الرابعة", "السنة الخامسة"]:
                context.user_data["current_step"] = "specialization"
                await update.message.reply_text(
                    "اختر التخصص:", reply_markup=specialization_keyboard())
                return
            else:
                context.user_data["current_step"] = "year"
                await update.message.reply_text("اختر السنة الدراسية:",
                                                reply_markup=year_keyboard())
                return

        # إذا كان في مرحلة اختيار التخصص، يرجع لاختيار السنة
        if current_step == "specialization":
            context.user_data["current_step"] = "year"
            context.user_data.pop("specialization", None)

            await update.message.reply_text("اختر السنة الدراسية:",
                                            reply_markup=year_keyboard())
            return

        # إذا كان في مرحلة اختيار السنة، يرجع لقائمة الهندسة المعلوماتية
        if current_step == "year":
            context.user_data.clear()
            context.user_data["in_informatics"] = True
            await update.message.reply_text(
                "🎓 الهندسة المعلوماتية\n\nاختر ما تريد:",
                reply_markup=informatics_menu_keyboard()
            )
            return

        # إذا كان في قائمة الهندسة المعلوماتية، يرجع للأفرع الجامعية
        if in_informatics:
            context.user_data.clear()
            context.user_data["in_branches"] = True
            await update.message.reply_text(
                "اختر الفرع الجامعي:",
                reply_markup=university_branches_keyboard()
            )
            return

        # إذا كان في قائمة الأفرع الجامعية، يرجع للقائمة الرئيسية
        if in_branches:
            context.user_data.clear()
            await start(update, context)
            return

        # إذا لم يكن في أي مرحلة محددة، يرجع للقائمة الرئيسية
        context.user_data.clear()
        await start(update, context)
        return

    if text == "🏠 القائمة الرئيسية":
        await start(update, context)
        return

    # الأفرع الجامعية
    if text == "🏛️ الأفرع الجامعية":
        context.user_data.clear()
        context.user_data["in_branches"] = True
        await update.message.reply_text(
            "اختر الفرع الجامعي:",
            reply_markup=university_branches_keyboard()
        )
        return

    # الهندسة المعلوماتية
    if text == "💻 الهندسة المعلوماتية":
        context.user_data["in_informatics"] = True
        context.user_data.pop("in_branches", None)
        await update.message.reply_text(
            "🎓 الهندسة المعلوماتية\n\nاختر ما تريد:",
            reply_markup=informatics_menu_keyboard()
        )
        return

    # الأفرع الأخرى
    if text in ["🏗️ الهندسة المعمارية", "🚧 الهندسة المدنية", "🏥 الهندسة الطبية"]:
        branch_name = text.split(" ", 1)[1]  # إزالة الإيموجي
        await update.message.reply_text(
            f"🔧 {branch_name}\n\nسنضيف محتوى لهذا الفرع في الأيام القادمة بإذن الله.\nتابعونا للحصول على التحديثات! 📚",
            reply_markup=university_branches_keyboard()
        )
        return

    # المواد الدراسية - بداية اختيار السنة
    if text == "📘 المواد الدراسية":
        # نحتفظ بحالة كوننا في الهندسة المعلوماتية
        in_informatics = context.user_data.get("in_informatics")
        context.user_data.clear()
        if in_informatics:
            context.user_data["in_informatics"] = True
        context.user_data["current_step"] = "year"
        await update.message.reply_text("اختر السنة الدراسية:",
                                        reply_markup=year_keyboard())
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

    # عن البوت والفريق
    if text == "👥 عن البوت والفريق":
        context.user_data["previous_step"] = start
        await update.message.reply_text(
            "👥 <b>عن البوت والفريق</b>\n\n"
            "🏛️ منصة تعليمية شاملة مصممة خصيصاً لطلاب جامعة اللاذقية\n\n"
            "🎯 نهدف إلى تقديم محتوى منظم وسهل الوصول لجميع الأفرع الهندسية، بما يسرّع عملية الدراسة والمراجعة ويوفر الوقت والجهد على الطلاب في رحلتهم الأكاديمية.\n\n"
            "🚀 <b>رؤيتنا:</b> تمكين المجتمع الطلابي من خلال أدوات تقنية متطورة تدعم التعلم والتفوق الأكاديمي\n\n"
            "💻 هذا العمل هو نتاج رؤية برمجية متقدمة وخبرة أكاديمية عميقة، أعدّه <a href=\"https://t.me/ammarsa51\">عمار سطوف</a> – مطوّر ومهندس برمجيات مختص في بناء الأنظمة التعليمية والتقنية المتقدمة.\n\n"
            "🤝 <b>فريق العمل:</b>\n"
            "• فريق <a href=\"https://t.me/zeroxxteam\">0x Team</a> - التطوير التقني والبرمجة\n"
            "• فريق SP_ITE - ساعد في تقديم محتوى مواد كلية الهندسة المعلوماتية\n\n"
            "🌟 نعمل معاً لخدمة الطلاب وتوفير بيئة تعليمية رقمية متميزة\n\n"
            "🔹 <i>Developed with passion and precision to support all Engineering students on their academic journey</i>\n\n"
            "© 2025 0x Team – جميع الحقوق محفوظة\n"
            "🔧 Designed & Developed by Ammar Satouf",
            reply_markup=main_menu_keyboard()
        )
        return
    # مقرر الثقافة المؤقت
    if text == "📗 مقرر الثقافة المؤقت":
        context.user_data["previous_step"] = start
        cid = channel_ids.get("komit1")  # تحديث للسنة الأولى
        msg_id = temporary_culture_doc

        if not cid or not msg_id:
            await update.message.reply_text(
                "📗 لا يتوفر محتويات مقرر الثقافة حالياً.",
                reply_markup=main_menu_keyboard(),
            )
            return

        await context.bot.copy_message(chat_id=update.effective_chat.id,
                                       from_chat_id=cid,
                                       message_id=msg_id,
                                       protect_content=True)
        await update.message.reply_text(
            "🎯 تم إرسال مقرر الثقافة المؤقت بنجاح.\nلا تنسَ تشارك البوت مع زملائك ❤",
            reply_markup=main_menu_keyboard(),
        )
        return

    # برنامج الامتحان العملي
    if text == "📅 برنامج الامتحان العملي":
        cid = channel_ids.get("exams1")  # قناة الامتحانات للسنة الأولى
        msg_id = practical_exam_schedule

        if not cid or not msg_id:
            await update.message.reply_text(
                "📅 لا يتوفر برنامج الامتحان العملي حالياً.",
                reply_markup=informatics_menu_keyboard(),
            )
            return

        await context.bot.copy_message(chat_id=update.effective_chat.id,
                                       from_chat_id=cid,
                                       message_id=msg_id,
                                       protect_content=True)
        await update.message.reply_text(
            "📅 تم إرسال برنامج الامتحان العملي بنجاح.\nبالتوفيق في امتحاناتك! 💪",
            reply_markup=informatics_menu_keyboard(),
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
        year = text
        context.user_data["year"] = year

        # إذا كانت السنة الرابعة أو الخامسة، نطلب اختيار التخصص
        if year in ["السنة الرابعة", "السنة الخامسة"]:
            context.user_data["current_step"] = "specialization"
            await update.message.reply_text(
                "اختر التخصص:", reply_markup=specialization_keyboard())
        else:
            context.user_data["current_step"] = "term"
            await update.message.reply_text("اختر الفصل الدراسي:",
                                            reply_markup=term_keyboard())
        return

    # اختيار التخصص (للسنة الرابعة والخامسة)
    specializations_map = {
        "هندسة البرمجيات": "هندسة البرمجيات",
        "الشبكات والنظم": "الشبكات والنظم",
        "الذكاء الاصطناعي": "الذكاء الاصطناعي",
    }

    if text in specializations_map:
        context.user_data["specialization"] = text
        context.user_data["current_step"] = "term"
        await update.message.reply_text("اختر الفصل الدراسي:",
                                        reply_markup=term_keyboard())
        return

    # اختيار الفصل الدراسي
    term_map = {
        "الفصل الأول ⚡": "الفصل الأول",
        "الفصل الثاني 🔥": "الفصل الثاني"
    }
    if text in term_map:
        year = context.user_data.get("year")
        specialization = context.user_data.get("specialization")
        term = term_map[text]
        context.user_data["term"] = term
        context.user_data["current_step"] = "subject"

        # التحقق من وجود المواد حسب السنة والتخصص
        if year in ["السنة الرابعة", "السنة الخامسة"]:
            if (year not in resources or term not in resources[year]
                    or specialization not in resources[year][term]):
                await update.message.reply_text(
                    "لا توجد مواد لهذا التخصص والفصل.",
                    reply_markup=term_keyboard())
                return

            # جلب المواد من النظري والعملي للتخصص المحدد
            theoretical_subjects = list(
                resources[year][term][specialization].get("theoretical",
                                                          {}).keys())
            practical_subjects = list(
                resources[year][term][specialization].get("practical",
                                                          {}).keys())
        else:
            if year not in resources or term not in resources[year]:
                await update.message.reply_text("لا توجد مواد لهذا الفصل.",
                                                reply_markup=term_keyboard())
                return

            # جلب المواد من النظري والعملي للسنوات العادية
            theoretical_subjects = list(resources[year][term].get(
                "theoretical", {}).keys())
            practical_subjects = list(resources[year][term].get(
                "practical", {}).keys())

        all_subjects_set = set(theoretical_subjects + practical_subjects)
        all_subjects = sorted(all_subjects_set)

        prefix = "⚡ " if term == "الفصل الأول" else "🔥 "
        subjects = [prefix + subj for subj in all_subjects]

        if not subjects:
            await update.message.reply_text("لا توجد مواد لهذا الفصل.",
                                            reply_markup=term_keyboard())
            return

        await update.message.reply_text(
            "اختر المادة:", reply_markup=subjects_keyboard(subjects))
        return

    # دالة لإزالة الإيموجي من بداية اسم المادة
    def strip_emoji(text):
        return text[2:] if len(text) > 2 else text

    # جميع المواد في resources تحت السنة والفصل والقسمين
    year = context.user_data.get("year")
    specialization = context.user_data.get("specialization")
    term = context.user_data.get("term")

    if year and term:
        subjects_all = []
        if year in ["السنة الرابعة", "السنة الخامسة"] and specialization:
            for section_key in ["theoretical", "practical"]:
                subjects_all += list(
                    resources.get(year,
                                  {}).get(term,
                                          {}).get(specialization,
                                                  {}).get(section_key,
                                                          {}).keys())
        else:
            for section_key in ["theoretical", "practical"]:
                subjects_all += list(
                    resources.get(year, {}).get(term, {}).get(section_key,
                                                              {}).keys())
        subjects_all_set = set(subjects_all)
    else:
        subjects_all_set = set()

    if strip_emoji(text) in subjects_all_set:
        subj_clean = strip_emoji(text)
        context.user_data["subject"] = subj_clean

        # نتحقق الأقسام المتوفرة للمادة
        available_sections = []

        if year in ["السنة الرابعة", "السنة الخامسة"]:
            subject_data = resources.get(year,
                                         {}).get(term,
                                                 {}).get(specialization, {})
        else:
            subject_data = resources.get(year, {}).get(term, {})

        if subj_clean in subject_data.get("theoretical", {}):
            available_sections.append("theoretical")
        if subj_clean in subject_data.get("practical", {}):
            available_sections.append("practical")

        if len(available_sections) == 1:
            context.user_data["section"] = available_sections[0]
            context.user_data["current_step"] = "content_type"
            await update.message.reply_text(
                "اختر نوع المحتوى المطلوب:",
                reply_markup=content_type_keyboard(),
            )
        else:
            context.user_data["current_step"] = "section"
            await update.message.reply_text(
                "اختر القسم (نظري أو عملي):",
                reply_markup=section_keyboard(),
            )
        return

    # اختيار القسم
    if text == "📘 القسم النظري":
        context.user_data["section"] = "theoretical"
        context.user_data["current_step"] = "content_type"
        await update.message.reply_text(
            "اختر نوع المحتوى المطلوب:",
            reply_markup=content_type_keyboard(),
        )
        return

    if text == "🧪 القسم العملي":
        context.user_data["section"] = "practical"
        context.user_data["current_step"] = "content_type"
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
        content_key_base = content_type_map[text]
        year = context.user_data.get("year")
        specialization = context.user_data.get("specialization")
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

        # تحديد مفتاح المحتوى حسب السنة والتخصص
        if year == "السنة الأولى":
            content_key = content_key_base + "1"
        elif year == "السنة الثانية":
            content_key = content_key_base + "2"
        elif year == "السنة الثالثة":
            content_key = content_key_base + "3"
        elif year in ["السنة الرابعة", "السنة الخامسة"]:
            year_num = "4" if year == "السنة الرابعة" else "5"
            spec_code = resources[year]["specializations"][specialization]
            content_key = content_key_base + year_num + spec_code

        # جلب البيانات حسب السنة والتخصص
        if year in ["السنة الرابعة", "السنة الخامسة"]:
            messages_list = resources.get(year, {}).get(term, {}).get(
                specialization,
                {}).get(section, {}).get(subject, {}).get(content_key, [])
        else:
            messages_list = resources.get(year, {}).get(term, {}).get(
                section, {}).get(subject, {}).get(content_key, [])

        if not messages_list or messages_list == [0]:
            await update.message.reply_text(
                "عذرًا، لا توجد ملفات متاحة لهذا المحتوى حالياً.",
                reply_markup=content_type_keyboard(),
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

        # البقاء في نفس مرحلة اختيار نوع المحتوى
        context.user_data["current_step"] = "content_type"

        await update.message.reply_text(
            "اختر نوع المحتوى المطلوب:",
            reply_markup=content_type_keyboard(),
        )
        return

    # إذا لم يتعرف على النص
    await update.message.reply_text(
        "عذراً، لم أفهم طلبك. الرجاء استخدام الأزرار المتاحة.",
        reply_markup=main_menu_keyboard(),
    )
