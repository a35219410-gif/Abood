import os
import redis.asyncio as aioredis
from dotenv import load_dotenv
load_dotenv()
BOT_TOKEN=os.getenv("BOT_TOKEN","")
API_ID=int(os.getenv("API_ID","0"))
API_HASH=os.getenv("API_HASH","")
OWNER_ID=int(os.getenv("OWNER_ID","0"))
DEFAULT_BOT_NAME=os.getenv("BOT_NAME","رعد")
DEFAULT_BOT_CHANNEL=os.getenv("BOT_CHANNEL","yqyqy66")
REDIS_HOST=os.getenv("REDIS_HOST","localhost")
REDIS_PORT=int(os.getenv("REDIS_PORT","6379"))
REDIS_DB=int(os.getenv("REDIS_DB","0"))
REDIS_PASSWORD=os.getenv("REDIS_PASSWORD",None)
r=aioredis.Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    db=REDIS_DB,
    password=REDIS_PASSWORD,
    decode_responses=True,
    ssl=True
)
Dev_Zaid=BOT_TOKEN.split(":")[0] if BOT_TOKEN else "0"
if not BOT_TOKEN: raise ValueError("BOT_TOKEN missing")
if not API_ID: raise ValueError("API_ID missing")
if not OWNER_ID: raise ValueError("OWNER_ID missing")
