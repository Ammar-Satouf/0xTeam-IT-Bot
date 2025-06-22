import os
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
from datetime import datetime

# تحميل المتغيرات البيئية
load_dotenv()

# إعدادات الاتصال بقاعدة البيانات
MONGO_URI = os.getenv("MONGO_URI")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", "telegram_bot_db")

# إنشاء اتصال بـ MongoDB
mongo_client = AsyncIOMotorClient(MONGO_URI)
db = mongo_client[MONGO_DB_NAME]

# الوصول إلى الكولكشن الخاص بالمستخدمين المفعّلين للإشعارات
notified_collection = db["notified_users"]

# الوصول إلى كولكشن التقييمات والمراجعات
ratings_collection = db["content_ratings"]
reminders_collection = db["user_reminders"]


# دوال التعامل مع إشعارات التحديثات
async def load_notified_users():
    """إرجاع قائمة user_id من قاعدة البيانات"""
    try:
        cursor = notified_collection.find({}, {"_id": 0, "user_id": 1})
        users = []
        async for doc in cursor:
            users.append(doc["user_id"])
        return users
    except Exception as e:
        print(f"Database error in load_notified_users: {e}")
        return []


async def add_notified_user(user_id: int,
                            first_name: str = "",
                            last_name: str = ""):
    """إضافة user_id جديد مع الاسم الأول والأخير إذا غير موجود"""
    try:
        exists = await notified_collection.find_one({"user_id": user_id})
        if not exists:
            user_data = {
                "user_id": user_id,
                "first_name": first_name,
                "last_name": last_name
            }
            await notified_collection.insert_one(user_data)
            print(
                f"User ID {user_id} ({first_name} {last_name}) added successfully."
            )
            return True
        print(f"User ID {user_id} already exists.")
        return False
    except Exception as e:
        print(f"Database error in add_notified_user: {e}")
        return False


async def remove_notified_user(user_id: int):
    """حذف user_id من قاعدة البيانات"""
    try:
        result = await notified_collection.delete_one({"user_id": user_id})
        return result.deleted_count > 0
    except Exception as e:
        print(f"Database error in remove_notified_user: {e}")
        return False


async def is_user_notified(user_id: int):
    """فحص إذا كان المستخدم مفعل للإشعارات"""
    try:
        exists = await notified_collection.find_one({"user_id": user_id})
        return exists is not None
    except Exception as e:
        print(f"Database error in is_user_notified: {e}")
        return False


# دوال نظام التقييم والمراجعات
async def add_content_rating(user_id: int, content_id: str, rating: int, review: str = ""):
    """إضافة تقييم للمحتوى"""
    try:
        rating_data = {
            "user_id": user_id,
            "content_id": content_id,
            "rating": rating,
            "review": review,
            "timestamp": datetime.now()
        }
        await ratings_collection.insert_one(rating_data)
        return True
    except Exception as e:
        print(f"Database error in add_content_rating: {e}")
        return False

async def get_content_average_rating(content_id: str):
    """الحصول على متوسط التقييم للمحتوى"""
    try:
        pipeline = [
            {"$match": {"content_id": content_id}},
            {"$group": {
                "_id": "$content_id",
                "average_rating": {"$avg": "$rating"},
                "total_ratings": {"$sum": 1}
            }}
        ]
        result = await ratings_collection.aggregate(pipeline).to_list(1)
        if result:
            return result[0]["average_rating"], result[0]["total_ratings"]
        return 0, 0
    except Exception as e:
        print(f"Database error in get_content_average_rating: {e}")
        return 0, 0

async def get_content_reviews(content_id: str, limit: int = 5):
    """الحصول على مراجعات المحتوى"""
    try:
        cursor = ratings_collection.find(
            {"content_id": content_id, "review": {"$ne": ""}},
            {"_id": 0, "user_id": 1, "rating": 1, "review": 1, "timestamp": 1}
        ).sort("timestamp", -1).limit(limit)
        
        reviews = []
        async for doc in cursor:
            reviews.append(doc)
        return reviews
    except Exception as e:
        print(f"Database error in get_content_reviews: {e}")
        return []


# دوال نظام التذكيرات
async def add_user_reminder(user_id: int, reminder_type: str, content: str, reminder_date):
    """إضافة تذكير للمستخدم"""
    try:
        reminder_data = {
            "user_id": user_id,
            "type": reminder_type,
            "content": content,
            "reminder_date": reminder_date,
            "created_at": datetime.now(),
            "is_sent": False
        }
        await reminders_collection.insert_one(reminder_data)
        return True
    except Exception as e:
        print(f"Database error in add_user_reminder: {e}")
        return False

async def get_pending_reminders():
    """الحصول على التذكيرات المستحقة"""
    try:
        current_time = datetime.now()
        cursor = reminders_collection.find({
            "reminder_date": {"$lte": current_time},
            "is_sent": False
        })
        
        reminders = []
        async for doc in cursor:
            reminders.append(doc)
        return reminders
    except Exception as e:
        print(f"Database error in get_pending_reminders: {e}")
        return []

async def mark_reminder_sent(reminder_id):
    """تحديد التذكير كمرسل"""
    try:
        await reminders_collection.update_one(
            {"_id": reminder_id},
            {"$set": {"is_sent": True}}
        )
        return True
    except Exception as e:
        print(f"Database error in mark_reminder_sent: {e}")
        return False
