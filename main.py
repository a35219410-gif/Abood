import asyncio,logging
from pyrogram import Client
from config import BOT_TOKEN,API_ID,API_HASH,Dev_Zaid,r,DEFAULT_BOT_NAME,DEFAULT_BOT_CHANNEL
logging.basicConfig(level=logging.INFO,format="%(asctime)s %(name)s: %(message)s")
log=logging.getLogger("R3D")
async def init():
    if not await r.get(f"{Dev_Zaid}:botkey"): await r.set(f"{Dev_Zaid}:botkey","⇜")
    if not await r.get(f"{Dev_Zaid}:BotName"): await r.set(f"{Dev_Zaid}:BotName",DEFAULT_BOT_NAME)
    if not await r.get(f"{Dev_Zaid}:BotChannel"): await r.set(f"{Dev_Zaid}:BotChannel",DEFAULT_BOT_CHANNEL)
async def main():
    app=Client(name=f"{Dev_Zaid}_r3d",api_id=API_ID,api_hash=API_HASH,bot_token=BOT_TOKEN,plugins={"root":"Plugins"})
    await init()
    async with app:
        me=await app.get_me()
        log.info(f"Running: @{me.username}")
        await asyncio.Event().wait()
if __name__=="__main__":
    try: asyncio.run(main())
    except KeyboardInterrupt: pass
