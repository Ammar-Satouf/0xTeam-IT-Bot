import os
from telegram import ReplyKeyboardMarkup, KeyboardButton, Update
from telegram.ext import ContextTypes
from resources import resources, channel_ids, practical_exam_schedule, exam_schedules_channels, exam_schedules_messages
from datetime import datetime
from db import load_notified_users, add_notified_user
from telegram.constants import ParseMode



# دالة للتحقق من صحة القناة
async def check_channel_access(context, channel_id):
    """التحقق من قدرة البوت على الوصول للقناة"""
    try:
        chat = await context.bot.get_chat(channel_id)
        return True, None
    except Exception as e:
        return False, str(e)


# إضافة زر تفعيل الإشعارات للقائمة الرئيسية
def main_menu_keyboard():
    return ReplyKeyboardMarkup(
        [
            [
                KeyboardButton("🏛️ الأفرع الجامعية"),
                KeyboardButton("🔍 البحث الذكي")
            ],
            [
                KeyboardButton("📅 برامج الامتحانات"),
                KeyboardButton("🔔 تفعيل إشعارات التحديثات")
            ],
            [
                KeyboardButton("⏰ التذكيرات الذكية"),
                KeyboardButton("🌙 تغيير المظهر")
            ],
            [
                KeyboardButton("🤖 المساعد الذكي"),
                KeyboardButton("👥 عن البوت والفريق")
            ],
            [
                KeyboardButton("📤 آلية تقديم اعتراض")
            ],
        ],
        resize_keyboard=True,
        one_time_keyboard=True,
    )


def university_branches_keyboard():
    return ReplyKeyboardMarkup(
        [
            [
                KeyboardButton("💻 الهندسة المعلوماتية"),
                KeyboardButton("🏗️ الهندسة المعمارية")
            ],
            [
                KeyboardButton("🚧 الهندسة المدنية"),
                KeyboardButton("🏥 الهندسة الطبية")
            ],
            [KeyboardButton("🔙 رجوع"),
             KeyboardButton("🏠 القائمة الرئيسية")],
        ],
        resize_keyboard=True,
    )


def informatics_menu_keyboard():
    return ReplyKeyboardMarkup(
        [
            [
                KeyboardButton("📘 المواد الدراسية")
            ],
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
            [
                KeyboardButton("📝 ملاحظات المواد"),
                KeyboardButton("⭐ تقييم المحتوى")
            ],
            [KeyboardButton("📊 عرض التقييمات")],
            [KeyboardButton("🔙 رجوع"),
             KeyboardButton("🏠 القائمة الرئيسية")],
        ],
        resize_keyboard=True,
    )


def ai_assistant_keyboard():
    return ReplyKeyboardMarkup(
        [
            [KeyboardButton("🔙 رجوع"),
             KeyboardButton("🏠 القائمة الرئيسية")],
        ],
        resize_keyboard=True,
    )


def exam_schedules_keyboard():
    return ReplyKeyboardMarkup(
        [
            [
                KeyboardButton("💻 هندسة معلوماتية"),
                KeyboardButton("🏗️ هندسة معمارية")
            ],
            [
                KeyboardButton("🚧 هندسة مدنية"),
                KeyboardButton("🏥 هندسة طبية")
            ],
            [KeyboardButton("🔙 رجوع"),
             KeyboardButton("🏠 القائمة الرئيسية")],
        ],
        resize_keyboard=True,
    )


def informatics_exam_types_keyboard():
    return ReplyKeyboardMarkup(
        [
            [
                KeyboardButton("📝 برنامج الامتحان النظري"),
                KeyboardButton("🧪 برنامج الامتحان العملي")
            ],
            [KeyboardButton("🔙 رجوع"),
             KeyboardButton("🏠 القائمة الرئيسية")],
        ],
        resize_keyboard=True,
    )


def rating_keyboard():
    return ReplyKeyboardMarkup(
        [
            [
                KeyboardButton("⭐ 1"),
                KeyboardButton("⭐⭐ 2"),
                KeyboardButton("⭐⭐⭐ 3")
            ],
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
        "🎯 اختر فرعك من القائمة أدناه وابدأ رحلة التميز! 📚✨")

    # تطبيق المظهر على النص
    themed_text = apply_theme_to_text(welcome_text, user_id, context)

    await update.message.reply_text(themed_text,
                                    reply_markup=main_menu_keyboard())
    context.user_data.clear()


# المساعد الذكي المتطور - مشابه لـ GPT-4
def ai_assistant_response(question,
                          subject=None,
                          free_text=None,
                          user_context=None):
    """مساعد ذكي متطور للإجابة على الأسئلة الأكاديمية - مشابه لـ ChatGPT-4"""

    # قاعدة معرفة شاملة ومتقدمة
    knowledge_base = {
        "برمجة": {
            "أساسيات":
            "💻 أساسيات البرمجة المتقدمة:\n\n🎯 المفاهيم الجوهرية:\n• Object-Oriented Programming (OOP)\n• Data Structures & Algorithms\n• Design Patterns\n• Clean Code Principles\n\n🔥 لغات البرمجة:\n• Python: للذكاء الاصطناعي والتطوير السريع\n• C++: للأداء العالي والنظم\n• JavaScript: لتطوير الويب\n• Java: للتطبيقات المؤسسية\n\n🚀 مسار التعلم:\n1. تعلم المنطق البرمجي\n2. اختر لغة أساسية\n3. تطبيق مشاريع عملية\n4. دراسة الخوارزميات\n5. تعلم الأنماط التصميمية",
            "خوارزميات":
            "🧠 الخوارزميات والهياكل:\n\n📊 خوارزميات الترتيب:\n• Bubble Sort: O(n²) - بسيط للتعلم\n• Quick Sort: O(n log n) - فعال عملياً\n• Merge Sort: O(n log n) - مستقر\n\n🔍 خوارزميات البحث:\n• Linear Search: O(n)\n• Binary Search: O(log n) - للمصفوفات المرتبة\n• Hash Tables: O(1) average case\n\n🌳 هياكل البيانات:\n• Arrays & Linked Lists\n• Stacks & Queues\n• Trees & Graphs\n• Hash Tables & Heaps",
            "مشاريع":
            "🛠️ أفكار مشاريع برمجية:\n\n🔰 مستوى مبتدئ:\n• آلة حاسبة متقدمة\n• نظام إدارة المهام\n• لعبة Tic-Tac-Toe\n• محول الوحدات\n\n🔥 مستوى متوسط:\n• نظام إدارة المكتبة\n• تطبيق طقس\n• محرر نصوص بسيط\n• لعبة Snake\n\n🚀 مستوى متقدم:\n• نظام إدارة قواعد البيانات\n• تطبيق ويب متكامل\n• محرك بحث مصغر\n• تطبيق ذكاء اصطناعي",
            "نصائح":
            "💡 نصائح الخبراء:\n\n🎯 للمبتدئين:\n• ابدأ بحل مشاكل صغيرة يومياً\n• اقرأ كود الآخرين وافهمه\n• لا تخف من الأخطاء، تعلم منها\n• استخدم Git من البداية\n\n🔥 للمتقدمين:\n• اكتب كود نظيف ومقروء\n• تعلم التطوير بالاختبارات (TDD)\n• شارك في مشاريع Open Source\n• ابني portfolio قوي\n\n🏆 للاحتراف:\n• تخصص في مجال معين\n• تعلم أساسيات DevOps\n• طور مهارات التواصل\n• ابقَ مطلعاً على التقنيات الجديدة"
        },
        "رياضيات": {
            "تحليل":
            "📐 التحليل الرياضي:\n\n🔢 النهايات:\n• تعريف النهاية الرسمي (ε-δ)\n• قوانين النهايات الأساسية\n• نهايات في اللانهاية\n• النهايات من جانب واحد\n\n📊 التفاضل:\n• تعريف المشتقة هندسياً وفيزيائياً\n• قواعد التفاضل الأساسية\n• تفاضل الدوال المعكوسة\n• تطبيقات التفاضل في الفيزياء\n\n∫ التكامل:\n• التكامل كعكس التفاضل\n• طرق التكامل المختلفة\n• التكامل المحدد وتطبيقاته\n• حساب المساحات والأحجام",
            "جبر":
            "🔢 الجبر الخطي:\n\n📋 المصفوفات:\n• العمليات الأساسية على المصفوفات\n• المحدد وخصائصه\n• المصفوفة المعكوسة\n• حل أنظمة المعادلات الخطية\n\n🎯 الفضاءات الشعاعية:\n• التركيبات الخطية\n• الاستقلال الخطي\n• الأساس والبعد\n• التحويلات الخطية\n\n🔍 القيم والأشعة الذاتية:\n• تعريف وحساب القيم الذاتية\n• التطبيقات في الفيزياء\n• قطرنة المصفوفات",
            "احصاء":
            "📊 الإحصاء والاحتمالات:\n\n🎲 الاحتمالات:\n• الاحتمال الكلاسيكي والتكراري\n• الاحتمال المشروط\n• قانون الاحتمال الكلي\n• نظرية بايز\n\n📈 الإحصاء الوصفي:\n• مقاييس النزعة المركزية\n• مقاييس التشتت\n• التمثيل البياني للبيانات\n• تحليل الارتباط\n\n🔬 الإحصاء الاستنتاجي:\n• فترات الثقة\n• اختبار الفرضيات\n• تحليل الانحدار\n• تحليل التباين"
        },
        "فيزياء": {
            "كلاسيكية":
            "⚛️ الفيزياء الكلاسيكية:\n\n🚀 الميكانيك:\n• قوانين نيوتن للحركة\n• حفظ الطاقة والزخم\n• الحركة الدائرية والتذبذبية\n• الجاذبية وقوانين كبلر\n\n⚡ الكهرومغناطيسية:\n• قانون كولوم والمجال الكهربائي\n• قانون جاوس وتطبيقاته\n• المقاومة وقانون أوم\n• المجال المغناطيسي وقانون أمبير\n\n🌊 الموجات والصوت:\n• خصائص الموجات\n• التداخل والحيود\n• تأثير دوبلر\n• الرنين والتطبيقات",
            "حديثة":
            "🔬 الفيزياء الحديثة:\n\n⚛️ الفيزياء الذرية:\n• نموذج بور للذرة\n• الأطياف الذرية\n• التأثير الكهروضوئي\n• إشعاع الجسم الأسود\n\n🌌 فيزياء الكم:\n• مبدأ الشك لهايزنبرغ\n• معادلة شرودنغر\n• ازدواجية الموجة-الجسيم\n• التشابك الكمي\n\n🚀 النسبية:\n• النسبية الخاصة\n• تمدد الزمن وتقلص الطول\n• معادلة أينشتاين E=mc²\n• النسبية العامة والجاذبية",
            "تطبيقية":
            "🔧 الفيزياء التطبيقية:\n\n💻 الإلكترونيات:\n• الدوائر المتكاملة\n• الترانزستورات والديودات\n• المضخمات العملياتية\n• المعالجات الدقيقة\n\n📡 الاتصالات:\n• موجات الراديو والميكروويف\n• الألياف البصرية\n• الأقمار الاصطناعية\n• الشبكات اللاسلكية\n\n⚕️ الفيزياء الطبية:\n• الأشعة السينية والتصوير\n• العلاج الإشعاعي\n• الرنين المغناطيسي\n• الليزر في الطب"
        },
        "هندسة": {
            "معلوماتية":
            "💻 الهندسة المعلوماتية:\n\n🌐 هندسة البرمجيات:\n• دورة حياة تطوير البرمجيات (SDLC)\n• الأنماط التصميمية (Design Patterns)\n• الهندسة المعمارية للبرمجيات\n• إدارة المشاريع البرمجية\n\n🔗 الشبكات والنظم:\n• بروتوكولات الشبكة (TCP/IP, HTTP, DNS)\n• أمان الشبكات والتشفير\n• إدارة النظم والخوادم\n• الحوسبة السحابية\n\n🤖 الذكاء الاصطناعي:\n• التعلم الآلي (Machine Learning)\n• الشبكات العصبية (Neural Networks)\n• معالجة اللغة الطبيعية (NLP)\n• رؤية الحاسوب (Computer Vision)",
            "عامة":
            "🏗️ الهندسة العامة:\n\n📐 الرياضيات الهندسية:\n• التحليل العددي\n• المعادلات التفاضلية\n• الإحصاء التطبيقي\n• نظرية التحكم\n\n🔬 العلوم الأساسية:\n• الفيزياء التطبيقية\n• الكيمياء الهندسية\n• علم المواد\n• الديناميكا الحرارية\n\n⚙️ التصميم الهندسي:\n• CAD وCAM\n• التحليل بالعناصر المحدودة\n• الرسم الهندسي\n• إدارة المشاريع الهندسية"
        },
        "دراسة": {
            "طرق":
            "📚 طرق الدراسة الفعالة:\n\n🎯 تقنيات التعلم النشط:\n• تقنية Pomodoro (25 دقيقة + 5 راحة)\n• تقنية Feynman (اشرح بكلمات بسيطة)\n• Mind Mapping للربط بين المفاهيم\n• Active Recall (استذكار نشط)\n\n📝 أساليب التلخيص:\n• Cornell Note-Taking System\n• SQ3R Method (Survey, Question, Read, Recite, Review)\n• تلخيص بالكلمات المفتاحية\n• إنشاء بطاقات المراجعة\n\n🧠 تحسين الذاكرة:\n• Spaced Repetition\n• ربط المعلومات الجديدة بالمعروفة\n• استخدام الحواس المتعددة\n• النوم الكافي (7-8 ساعات)",
            "تنظيم":
            "⏰ تنظيم الوقت والدراسة:\n\n📅 التخطيط الاستراتيجي:\n• تحديد الأهداف قصيرة وطويلة المدى\n• إنشاء جدول دراسي واقعي\n• تخصيص وقت للمراجعة\n• التوازن بين العمل والراحة\n\n🎯 إدارة الأولويات:\n• مصفوفة أيزنهاور (هام/عاجل)\n• قانون 80/20 (باريتو)\n• تقسيم المهام الكبيرة\n• تجنب التسويف\n\n💡 تحسين البيئة الدراسية:\n• إزالة المشتتات\n• إضاءة وتهوية مناسبة\n• مكان دراسة ثابت\n• أدوات دراسية منظمة",
            "امتحانات":
            "📋 استراتيجيات الامتحانات:\n\n🎯 التحضير للامتحان:\n• مراجعة شاملة للمنهج\n• حل امتحانات سابقة\n• تحديد النقاط الضعيفة\n• الحصول على راحة كافية\n\n⏱️ إدارة وقت الامتحان:\n• قراءة الأسئلة بعناية\n• البدء بالأسئلة السهلة\n• تخصيص وقت لكل سؤال\n• ترك وقت للمراجعة النهائية\n\n🧘 إدارة القلق:\n• تقنيات التنفس العميق\n• التفكير الإيجابي\n• التصور الذهني للنجاح\n• الثقة بالتحضير"
        }
    }

    # تحليل السؤال الحر بذكاء متقدم (مشابه لـ GPT-4)
    if free_text:
        text_lower = free_text.lower()
        response = "🤖 المساعد الذكي المتطور:\n\n"

        # تحليل متقدم للسؤال
        programming_keywords = [
            "برمجة", "كود", "خوارزمية", "program", "coding", "algorithm",
            "python", "c++", "java", "javascript"
        ]
        math_keywords = [
            "رياضيات", "تحليل", "جبر", "تفاضل", "تكامل", "مصفوفة", "معادلة",
            "نهاية", "مشتقة"
        ]
        physics_keywords = [
            "فيزياء", "كهرباء", "دارة", "موجة", "طاقة", "قوة", "سرعة", "تسارع",
            "مقاومة"
        ]
        engineering_keywords = [
            "هندسة", "تصميم", "شبكات", "ذكاء اصطناعي", "معلوماتية", "مشروع"
        ]
        study_keywords = [
            "دراسة", "امتحان", "مراجعة", "تعلم", "حفظ", "فهم", "تذكر"
        ]
        time_keywords = ["وقت", "تنظيم", "جدول", "إدارة", "تخطيط", "أولويات"]

        # تحديد المجال الرئيسي للسؤال
        if any(word in text_lower for word in programming_keywords):
            if any(word in text_lower for word in ["مشروع", "فكرة", "تطبيق"]):
                response += knowledge_base["برمجة"]["مشاريع"]
            elif any(word in text_lower
                     for word in ["خوارزمية", "algorithm", "ترتيب", "بحث"]):
                response += knowledge_base["برمجة"]["خوارزميات"]
            elif any(word in text_lower
                     for word in ["أساسيات", "تعلم", "بداية"]):
                response += knowledge_base["برمجة"]["أساسيات"]
            else:
                response += knowledge_base["برمجة"]["نصائح"]

        elif any(word in text_lower for word in math_keywords):
            if any(word in text_lower
                   for word in ["تحليل", "تفاضل", "تكامل", "نهاية"]):
                response += knowledge_base["رياضيات"]["تحليل"]
            elif any(word in text_lower
                     for word in ["جبر", "مصفوفة", "معادلة", "نظام"]):
                response += knowledge_base["رياضيات"]["جبر"]
            elif any(word in text_lower
                     for word in ["إحصاء", "احتمال", "توزيع"]):
                response += knowledge_base["رياضيات"]["احصاء"]
            else:
                response += knowledge_base["رياضيات"]["تحليل"]

        elif any(word in text_lower for word in physics_keywords):
            if any(word in text_lower
                   for word in ["كلاسيكية", "نيوتن", "حركة", "قوة"]):
                response += knowledge_base["فيزياء"]["كلاسيكية"]
            elif any(word in text_lower
                     for word in ["حديثة", "كم", "ذرة", "نسبية"]):
                response += knowledge_base["فيزياء"]["حديثة"]
            elif any(word in text_lower
                     for word in ["تطبيق", "إلكترونيات", "طبية"]):
                response += knowledge_base["فيزياء"]["تطبيقية"]
            else:
                response += knowledge_base["فيزياء"]["كلاسيكية"]

        elif any(word in text_lower for word in engineering_keywords):
            if any(word in text_lower
                   for word in ["معلوماتية", "برمجيات", "شبكات", "ذكاء"]):
                response += knowledge_base["هندسة"]["معلوماتية"]
            else:
                response += knowledge_base["هندسة"]["عامة"]

        elif any(word in text_lower for word in study_keywords):
            if any(word in text_lower for word in ["امتحان", "اختبار", "قلق"]):
                response += knowledge_base["دراسة"]["امتحانات"]
            elif any(word in text_lower
                     for word in ["طريقة", "أسلوب", "تقنية"]):
                response += knowledge_base["دراسة"]["طرق"]
            else:
                response += knowledge_base["دراسة"]["طرق"]

        elif any(word in text_lower for word in time_keywords):
            response += knowledge_base["دراسة"]["تنظيم"]

        # أسئلة محددة ومتقدمة
        elif "كيف" in text_lower and "تعلم" in text_lower:
            response += "🎓 دليل التعلم الذكي:\n\n📚 خطوات التعلم الفعال:\n1. 🎯 حدد هدفك بوضوح\n2. 🗺️ ضع خطة تعلم مرحلية\n3. 📖 ابدأ بالأساسيات\n4. 🔄 طبق ما تتعلمه فوراً\n5. 🤝 شارك معرفتك مع الآخرين\n6. 📊 قيّم تقدمك باستمرار\n\n💡 قاعدة 70-20-10:\n• 70% تعلم من التطبيق العملي\n• 20% تعلم من الآخرين\n• 10% تعلم نظري\n\n🧠 تقنيات التعلم المتقدمة:\n• Interleaving: تبديل المواضيع\n• Elaboration: ربط المعلومات\n• Generation: إنتاج إجابات قبل رؤيتها"

        elif "صعب" in text_lower or "مشكلة" in text_lower:
            response += "💪 حل المشاكل الأكاديمية:\n\n🎯 استراتيجية حل المشاكل:\n1. 🔍 حدد المشكلة بوضوح\n2. 🧩 قسمها لأجزاء صغيرة\n3. 🔄 جرب حلول مختلفة\n4. 📚 ابحث عن مصادر إضافية\n5. 🤝 اطلب المساعدة عند الحاجة\n6. ✅ تحقق من الحل\n\n🧠 تقنيات التفكير النقدي:\n• اسأل 'لماذا' 5 مرات\n• فكر بالعكس\n• استخدم القياس والتشبيه\n• اربط المعرفة الجديدة بالقديمة\n\n💡 عندما تواجه صعوبة:\n• خذ استراحة وعد لاحقاً\n• اشرح المشكلة لشخص آخر\n• ابحث عن أمثلة مشابهة\n• لا تتردد في طلب المساعدة"

        else:
            # تحليل ذكي للسؤال العام
            response += f"💭 تحليل ذكي لسؤالك: '{free_text}'\n\n"

            # تحديد نوع السؤال
            if "ما" in text_lower or "what" in text_lower.lower():
                response += "🔍 سؤال تعريفي - يبحث عن معلومات\n"
            elif "كيف" in text_lower or "how" in text_lower:
                response += "⚙️ سؤال إجرائي - يبحث عن طريقة\n"
            elif "لماذا" in text_lower or "why" in text_lower:
                response += "🤔 سؤال تحليلي - يبحث عن سبب\n"
            elif "متى" in text_lower or "when" in text_lower:
                response += "📅 سؤال زمني - يبحث عن توقيت\n"

            response += "\n💡 لتحسين إجابتي، يمكنك:\n"
            response += "• تحديد المجال: (برمجة، رياضيات، فيزياء، إلخ)\n"
            response += "• إضافة تفاصيل أكثر\n"
            response += "• ذكر مستواك الأكاديمي\n"
            response += "• تحديد ما تريد تحقيقه\n\n"
            response += "🎓 المجالات التي أتقنها:\n"
            response += "• 💻 البرمجة والخوارزميات\n"
            response += "• 📐 الرياضيات والتحليل\n"
            response += "• ⚛️ الفيزياء والعلوم\n"
            response += "• 🏗️ الهندسة والتقنية\n"
            response += "• 📚 طرق الدراسة والتعلم\n"
            response += "• ⏰ إدارة الوقت والتنظيم"

        # إضافة نصيحة ذكية في النهاية
        response += "\n\n🌟 نصيحة ذكية: التعلم رحلة وليس وجهة، استمتع بكل خطوة!"

        return response

    # الأسئلة المحددة مسبقاً
    responses = {
        "نصائح دراسية": {
            "default":
            "🎓 نصائح دراسية ذكية:\n\n📚 تقنيات الدراسة:\n• Active Learning: لا تقرأ فقط، طبق\n• Spaced Repetition: راجع بفترات متباعدة\n• Feynman Technique: اشرح للآخرين\n\n🧠 تحسين التركيز:\n• اختر مكان هادئ\n• أغلق الإشعارات\n• استخدم الموسيقى الهادئة\n\n💪 تطوير الذات:\n• ضع أهداف قابلة للقياس\n• احتفل بالإنجازات الصغيرة\n• تعلم من الأخطاء"
        },
        "أسئلة تدريبية": {
            "default":
            "❓ أسئلة تدريبية متنوعة:\n\n🔸 برمجة:\n• اكتب خوارزمية للبحث الثنائي\n• ما الفرق بين Stack و Queue؟\n• شرح مفهوم Recursion\n\n🔸 رياضيات:\n• احسب نهاية دالة معطاة\n• حل نظام معادلات خطية\n• جد مشتقة دالة مركبة\n\n🔸 فيزياء:\n• حلل دارة كهربائية بسيطة\n• احسب التيار في مقاوم"
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
            if isinstance(messages,
                          list) and messages != [0] and len(messages) > 0:
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
                                for subject, subject_content in section_data.items(
                                ):
                                    if has_content(subject_content):
                                        clean_subject = subject.replace(
                                            "⚡ ", "").replace("🔥 ", "")
                                        if query_lower in clean_subject.lower(
                                        ):
                                            results.append({
                                                "year":
                                                year,
                                                "term":
                                                term,
                                                "specialization":
                                                spec,
                                                "section":
                                                section,
                                                "subject":
                                                clean_subject,
                                                "content_available":
                                                True
                                            })
            else:
                for section, section_data in term_data.items():
                    if isinstance(section_data, dict):
                        for subject, subject_content in section_data.items():
                            if has_content(subject_content):
                                clean_subject = subject.replace("⚡ ",
                                                                "").replace(
                                                                    "🔥 ", "")
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


def apply_theme_to_text(text, user_id, context):
    """تطبيق المظهر على النص"""
    theme = get_user_theme(user_id, context)
    if theme == "dark":
        # تطبيق المظهر المظلم
        themed_text = text.replace("🌟", "⭐").replace("☀️",
                                                     "🌙").replace("🌇", "🌃")
        themed_text = themed_text.replace("💡", "🔥").replace("✨", "⭐")
        themed_text = themed_text.replace("🎓", "🎯").replace("📚", "📖")
        themed_text = themed_text.replace("🌞", "🌙").replace("☀", "🌙")
        return f"🌙 {themed_text}"
    else:
        return f"☀️ {text}"


def theme_keyboard():
    return ReplyKeyboardMarkup(
        [
            [
                KeyboardButton("🌞 المظهر الفاتح"),
                KeyboardButton("🌙 المظهر المظلم")
            ],
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
        search_message = "🔍 نظام البحث الذكي المتطور\n\n💡 اكتب اسم المادة أو جزء منها للبحث عنها في جميع السنوات والتخصصات\n\n🎯 مثال: اكتب 'برمجة' للعثور على جميع مواد البرمجة\n📚 مثال: اكتب 'داتا' للعثور على مواد قواعد البيانات\n\n✨ البحث يشمل جميع السنوات والأقسام والتخصصات"

        themed_message = apply_theme_to_text(search_message, user_id, context)

        await update.message.reply_text(
            themed_message,
            reply_markup=ReplyKeyboardMarkup([[
                KeyboardButton("🔙 رجوع"),
                KeyboardButton("🏠 القائمة الرئيسية")
            ]],
                                             resize_keyboard=True))
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
            reply_markup=theme_keyboard())
        return

    # معالجة اختيار المظهر
    if text in ["🌞 المظهر الفاتح", "🌙 المظهر المظلم"]:
        user_id = update.effective_user.id
        theme = "light" if text == "🌞 المظهر الفاتح" else "dark"
        set_user_theme(user_id, theme, context)

        theme_name = "الفاتح" if theme == "light" else "المظلم"
        emoji = "🌞" if theme == "light" else "🌙"

        base_message = f"✅ تم تعيين المظهر {theme_name} بنجاح!\n\n🎨 سيتم تطبيق المظهر الجديد على جميع الرسائل.\n🔄 يمكنك تغيير المظهر في أي وقت من القائمة الرئيسية."

        if theme == "dark":
            response_message = f"🌙 {base_message}"
        else:
            response_message = f"☀️ {base_message}"

        await update.message.reply_text(response_message,
                                        reply_markup=main_menu_keyboard())
        return

    # معالجة البحث
    if context.user_data.get("search_mode"):
        if text in ["🔙 رجوع", "🏠 القائمة الرئيسية"]:
            context.user_data.pop("search_mode", None)
            if text == "🔙 رجوع":
                await update.message.reply_text(
                    "تم إلغاء البحث", reply_markup=main_menu_keyboard())
            else:
                await start(update, context)
            return

        # تنفيذ البحث
        results = search_content(text)

        if not results:
            await update.message.reply_text(
                f"❌ لم يتم العثور على نتائج للبحث: '{text}'\n\n"
                "💡 جرب البحث بكلمات أخرى أو تأكد من الإملاء",
                reply_markup=ReplyKeyboardMarkup([[
                    KeyboardButton("🔙 رجوع"),
                    KeyboardButton("🏠 القائمة الرئيسية")
                ]],
                                                 resize_keyboard=True))
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
            reply_markup=ReplyKeyboardMarkup([[
                KeyboardButton("🔙 رجوع"),
                KeyboardButton("🏠 القائمة الرئيسية")
            ]],
                                             resize_keyboard=True))
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
            reply_markup=main_menu_keyboard())
        return

    # المساعد الذكي
    if text == "🤖 المساعد الذكي":
        context.user_data["ai_mode"] = True
        await update.message.reply_text(
            "🤖 المساعد الذكي المتطور - GPT Style\n\n"
            "🧠 مرحباً! أنا مساعدك الذكي المتطور للدعم الأكاديمي\n"
            "✨ مدرب على أحدث تقنيات الذكاء الاصطناعي\n\n"
            "🎯 قدراتي المتقدمة:\n"
            "• 💻 شرح المفاهيم البرمجية المعقدة\n"
            "• 📐 حل المسائل الرياضية خطوة بخطوة\n"
            "• ⚛️ تبسيط النظريات الفيزيائية\n"
            "• 🏗️ تقديم حلول هندسية إبداعية\n"
            "• 📚 وضع خطط دراسية شخصية\n"
            "• 🎓 تحليل الأسئلة وتقديم إجابات شاملة\n\n"
            "💡 أمثلة على أسئلة يمكنني الإجابة عليها:\n"
            "🔹 'اشرح لي الخوارزميات بطريقة بسيطة'\n"
            "🔹 'كيف أتقن التفاضل والتكامل؟'\n"
            "🔹 'ما أفضل طريقة لحفظ المعادلات الفيزيائية؟'\n"
            "🔹 'كيف أنظم وقتي بين المواد المختلفة؟'\n"
            "🔹 'اقترح لي مشاريع برمجية للتدرب'\n\n"
            "🚀 اكتب سؤالك الآن وسأقدم لك إجابة تفصيلية ومفيدة:",
            reply_markup=ai_assistant_keyboard())
        return

    # معالجة أمر /start من القائمة
    if text == "/start":
        await start(update, context)
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
                "⭐⭐⭐⭐⭐ 5 - ممتاز", user_id, context)
            await update.message.reply_text(themed_response,
                                            reply_markup=rating_keyboard())
        else:
            await update.message.reply_text(
                "❌ يرجى اختيار مادة أولاً قبل التقييم",
                reply_markup=content_type_keyboard())
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
                avg_rating, total_ratings = await get_content_average_rating(
                    content_id)
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

                themed_response = apply_theme_to_text(response, user_id,
                                                      context)
                await update.message.reply_text(
                    themed_response, reply_markup=content_type_keyboard())

            except Exception as e:
                print(f"Error getting ratings: {e}")
                await update.message.reply_text(
                    "❌ حدث خطأ في جلب التقييمات",
                    reply_markup=content_type_keyboard())
        else:
            await update.message.reply_text(
                "❌ يرجى اختيار مادة أولاً لعرض التقييمات",
                reply_markup=content_type_keyboard())
        return

    # معالجة المساعد الذكي
    if context.user_data.get("ai_mode"):
        if text in ["🔙 رجوع", "🏠 القائمة الرئيسية"]:
            context.user_data.pop("ai_mode", None)
            if text == "🔙 رجوع":
                await update.message.reply_text(
                    "🤖 شكراً لاستخدام المساعد الذكي!",
                    reply_markup=main_menu_keyboard())
            else:
                await start(update, context)
            return

        # معالجة أي سؤال مباشرة
        if text not in ["🔙 رجوع", "🏠 القائمة الرئيسية"]:
            # استخدام المساعد الذكي المطور للإجابة
            user_context = {
                "year": context.user_data.get("year"),
                "subject": context.user_data.get("subject"),
                "user_id": user_id
            }
            response = ai_assistant_response("", None, text, user_context)
            themed_response = apply_theme_to_text(response, user_id, context)

            await update.message.reply_text(
                themed_response, reply_markup=ai_assistant_keyboard())
            return

    # معالجة التقييم
    if context.user_data.get("rating_mode"):
        rating_map = {
            "⭐ 1": 1,
            "⭐⭐ 2": 2,
            "⭐⭐⭐ 3": 3,
            "⭐⭐⭐⭐ 4": 4,
            "⭐⭐⭐⭐⭐ 5": 5
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
                user_id, context)

            await update.message.reply_text(
                themed_response,
                reply_markup=ReplyKeyboardMarkup(
                    [[KeyboardButton("⏭️ تخطي")],
                     [
                         KeyboardButton("🔙 رجوع"),
                         KeyboardButton("🏠 القائمة الرئيسية")
                     ]],
                    resize_keyboard=True))
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
                    user_id, context)

                await update.message.reply_text(
                    themed_response, reply_markup=content_type_keyboard())
            except Exception as e:
                print(f"Error saving rating: {e}")
                await update.message.reply_text(
                    "❌ حدث خطأ في حفظ التقييم",
                    reply_markup=content_type_keyboard())
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
                    user_id, context)

                await update.message.reply_text(
                    themed_response, reply_markup=content_type_keyboard())
            except Exception as e:
                print(f"Error saving rating with review: {e}")
                await update.message.reply_text(
                    "❌ حدث خطأ في حفظ التقييم والتعليق",
                    reply_markup=content_type_keyboard())
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
                reply_markup=informatics_menu_keyboard())
            return

        # إذا كان في قائمة اختيار نوع الامتحان، يرجع لقائمة الأفرع في برامج الامتحانات
        if context.user_data.get("selected_branch"):
            context.user_data.pop("selected_branch", None)
            await update.message.reply_text(
                "📅 برامج الامتحانات\n\nاختر الفرع الجامعي لعرض برامج امتحاناته:",
                reply_markup=exam_schedules_keyboard())
            return

        # إذا كان في قائمة برامج الامتحانات، يرجع للقائمة الرئيسية
        if context.user_data.get("in_exam_schedules"):
            context.user_data.clear()
            await start(update, context)
            return

        # إذا كان في قائمة الهندسة المعلوماتية، يرجع للأفرع الجامعية
        if in_informatics:
            context.user_data.clear()
            context.user_data["in_branches"] = True
            await update.message.reply_text(
                "اختر الفرع الجامعي:",
                reply_markup=university_branches_keyboard())
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
            "اختر الفرع الجامعي:", reply_markup=university_branches_keyboard())
        return

    # الهندسة المعلوماتية
    if text == "💻 الهندسة المعلوماتية":
        context.user_data["in_informatics"] = True
        context.user_data.pop("in_branches", None)
        await update.message.reply_text(
            "🎓 الهندسة المعلوماتية\n\nاختر ما تريد:",
            reply_markup=informatics_menu_keyboard())
        return

    # الأفرع الأخرى
    if text in [
            "🏗️ الهندسة المعمارية", "🚧 الهندسة المدنية", "🏥 الهندسة الطبية"
    ]:
        branch_name = text.split(" ", 1)[1]  # إزالة الإيموجي
        await update.message.reply_text(
            f"🔧 {branch_name}\n\nسنضيف محتوى لهذا الفرع في الأيام القادمة بإذن الله.\nتابعونا للحصول على التحديثات! 📚",
            reply_markup=university_branches_keyboard())
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
            "🏛 منصة تعليمية شاملة مصممة خصيصاً لطلاب جامعة اللاذقية\n\n"
            "🎯 نهدف إلى تقديم محتوى منظم وسهل الوصول لجميع الأفرع الهندسية، بما يسرّع عملية الدراسة والمراجعة ويوفر الوقت والجهد على الطلاب في رحلتهم الأكاديمية.\n\n"
            "🚀 <b>رؤيتنا:</b> تمكين المجتمع الطلابي من خلال أدوات تقنية متطورة تدعم التعلم والتفوق الأكاديمي\n\n"
            "💻 هذا العمل هو نتاج رؤية برمجية متقدمة وخبرة أكاديمية عميقة، أعدّه <a href=\"https://t.me/ammarsa51\">عمار سطوف</a> – مطوّر ومهندس برمجيات مختص في بناء الأنظمة التعليمية والتقنية المتقدمة.\n\n"
            "🤝 <b>فريق العمل:</b>\n"
            "• <a href=\"https://t.me/zeroxxteam\">0x Team</a> - التطوير التقني والبرمجة\n"
            "• فريق SP_ITE - ساعد في تقديم محتوى مواد كلية الهندسة المعلوماتية\n\n"
            "🌟 نعمل معاً لخدمة الطلاب وتوفير بيئة تعليمية رقمية متميزة\n\n"
            "🔹 <i>Developed with passion and precision to support all Engineering students on their academic journey</i>\n\n"
            "© 2025 <a href=\"https://t.me/zeroxxteam\">0x Team</a> – جميع الحقوق محفوظة\n"
            "🔧 Designed & Developed by <a href=\"https://t.me/ammarsa51\">Ammar Satouf</a>",
            reply_markup=main_menu_keyboard(),
            parse_mode=ParseMode.HTML)
        return
    

    # برامج الامتحانات
    if text == "📅 برامج الامتحانات":
        context.user_data.clear()
        context.user_data["in_exam_schedules"] = True
        await update.message.reply_text(
            "📅 برامج الامتحانات\n\nاختر الفرع الجامعي لعرض برامج امتحاناته:",
            reply_markup=exam_schedules_keyboard())
        return

    # معالجة اختيار الأفرع في برامج الامتحانات
    if context.user_data.get("in_exam_schedules"):
        if text == "💻 هندسة معلوماتية":
            context.user_data["selected_branch"] = "informatics"
            await update.message.reply_text(
                "💻 برامج امتحانات الهندسة المعلوماتية\n\nاختر نوع الامتحان:",
                reply_markup=informatics_exam_types_keyboard())
            return
        elif text in ["🏗️ هندسة معمارية", "🚧 هندسة مدنية", "🏥 هندسة طبية"]:
            branch_name = text.split(" ", 1)[1]
            await update.message.reply_text(
                f"📅 {branch_name}\n\n🔧 برامج امتحانات هذا الفرع قيد التحضير.\nسيتم إضافتها قريباً بإذن الله! 📚",
                reply_markup=exam_schedules_keyboard())
            return

    # معالجة اختيار نوع الامتحان للهندسة المعلوماتية
    if context.user_data.get("selected_branch") == "informatics":
        if text == "📝 برنامج الامتحان النظري":
            channel_id = exam_schedules_channels.get("informatics_theoretical_exam")
            msg_id = exam_schedules_messages.get("informatics_theoretical_exam")
            
            if not channel_id or not msg_id:
                await update.message.reply_text(
                    "📝 لا يتوفر برنامج الامتحان النظري حالياً.",
                    reply_markup=informatics_exam_types_keyboard())
                return

            try:
                await context.bot.copy_message(
                    chat_id=update.effective_chat.id,
                    from_chat_id=channel_id,
                    message_id=msg_id,
                    protect_content=True)
                await update.message.reply_text(
                    "📝 تم إرسال برنامج الامتحان النظري بنجاح.\nبالتوفيق في امتحاناتك! 💪",
                    reply_markup=informatics_exam_types_keyboard())
            except Exception as e:
                await update.message.reply_text(
                    f"❌ حدث خطأ في جلب برنامج الامتحان النظري.\nتأكد من إضافة البوت للقناة المخصصة.",
                    reply_markup=informatics_exam_types_keyboard())
            return

        elif text == "🧪 برنامج الامتحان العملي":
            channel_id = exam_schedules_channels.get("informatics_practical_exam")
            msg_id = exam_schedules_messages.get("informatics_practical_exam")
            
            if not channel_id or not msg_id:
                await update.message.reply_text(
                    "🧪 لا يتوفر برنامج الامتحان العملي حالياً.",
                    reply_markup=informatics_exam_types_keyboard())
                return

            try:
                await context.bot.copy_message(
                    chat_id=update.effective_chat.id,
                    from_chat_id=channel_id,
                    message_id=msg_id,
                    protect_content=True)
                await update.message.reply_text(
                    "🧪 تم إرسال برنامج الامتحان العملي بنجاح.\nبالتوفيق في امتحاناتك! 💪",
                    reply_markup=informatics_exam_types_keyboard())
            except Exception as e:
                await update.message.reply_text(
                    f"❌ حدث خطأ في جلب برنامج الامتحان العملي.\nتأكد من إضافة البوت للقناة المخصصة.",
                    reply_markup=informatics_exam_types_keyboard())
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
        if text.startswith("⚡ ") or text.startswith("🔥 "):
            return text[2:]
        return text

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

        # التحقق من وجود الرسائل
        if not messages_list or messages_list == [0]:
            await update.message.reply_text(
                f"عذرًا، لا توجد ملفات متاحة لـ{text} في مادة {subject} حالياً.",
                reply_markup=content_type_keyboard(),
            )
            return

        # التحقق من وجود القناة
        channel_id = channel_ids.get(content_key)
        if not channel_id:
            await update.message.reply_text(
                f"حدث خطأ في العثور على قناة المحتوى لـ{content_key}. الرجاء المحاولة لاحقاً.",
                reply_markup=content_type_keyboard(),
            )
            return

        print(f"Debug - Sending content: subject={subject}, content_key={content_key}, channel_id={channel_id}, messages={messages_list}")

        # إرسال الرسائل
        sent_count = 0
        failed_count = 0
        error_details = []
        
        for msg_id in messages_list:
            try:
                await context.bot.copy_message(
                    chat_id=update.effective_chat.id,
                    from_chat_id=channel_id,
                    message_id=msg_id,
                    protect_content=True,
                )
                sent_count += 1
            except Exception as e:
                failed_count += 1
                print(f"Error sending message {msg_id} from channel {channel_id}: {e}")

        # إظهار نتيجة الإرسال
        if sent_count > 0:
            result_message = f"✅ تم إرسال {sent_count} ملف بنجاح"
            if failed_count > 0:
                result_message += f" (فشل إرسال {failed_count} ملف)"
            result_message += f"\n📚 {text} - {subject}"
        else:
            result_message = f"❌ حدث خطأ في الوصول للملفات\n\n🔢 رقم الخطأ: 26A\n📞 يرجى التواصل مع المطور للمساعدة في حلها"

        # البقاء في نفس مرحلة اختيار نوع المحتوى
        context.user_data["current_step"] = "content_type"

        await update.message.reply_text(
            result_message + "\n\nاختر نوع المحتوى المطلوب:",
            reply_markup=content_type_keyboard(),
        )
        return

    # إذا لم يتعرف على النص
    await update.message.reply_text(
        "عذراً، لم أفهم طلبك. الرجاء استخدام الأزرار المتاحة.",
        reply_markup=main_menu_keyboard(),
    )
