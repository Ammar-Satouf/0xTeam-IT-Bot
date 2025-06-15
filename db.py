import os
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", "telegram_bot_db")

# إنشاء اتصال بـ MongoDB
mongo_client = AsyncIOMotorClient(MONGO_URI)
db = mongo_client[MONGO_DB_NAME]

# الوصول إلى الكولكشن
notified_collection = db["notified_users"]


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


async def add_notified_user(user_id: int):
    """إضافة user_id جديد إذا غير موجود"""
    try:
        exists = await notified_collection.find_one({"user_id": user_id})
        if not exists:
            await notified_collection.insert_one({"user_id": user_id})
            print(f"User ID {user_id} added successfully.")
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
