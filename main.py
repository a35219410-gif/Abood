import asyncio, logging, threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from pyrogram import Client
from config import BOT_TOKEN, API_ID, API_HASH, Dev_Zaid, r, DEFAULT_BOT_NAME, DEFAULT_BOT_CHANNEL

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(name)s: %(message)s")
log = logging.getLogger("R3D")

# سيرفر HTTP وهمي يخلي Render يعتقد أن الخدمة شغالة
class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is running!")
    def log_message(self, *args): pass

def run_http():
    server = HTTPServer(("0.0.0.0", 8080), Handler)
    server.serve_forever()

async def init():
    if not await r.get(f"{Dev_Zaid}:botkey"): await r.set(f"{Dev_Zaid}:botkey", "⇜")
    if not await r.get(f"{Dev_Zaid}:BotName"): await r.set(f"{Dev_Zaid}:BotName", DEFAULT_BOT_NAME)
    if not await r.get(f"{Dev_Zaid}:BotChannel"): await r.set(f"{Dev_Zaid}:BotChannel", DEFAULT_BOT_CHANNEL)

async def main():
    app = Client(
        name=f"{Dev_Zaid}_r3d",
        api_id=API_ID,
        api_hash=API_HASH,
        bot_token=BOT_TOKEN,
        plugins={"root": "Plugins"}
    )
    await init()
    async with app:
        me = await app.get_me()
        log.info(f"Running: @{me.username}")
        await asyncio.Event().wait()

if __name__ == "__main__":
    # شغّل HTTP في thread منفصل
    t = threading.Thread(target=run_http, daemon=True)
    t.start()
    log.info("HTTP server started on port 8080")
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
