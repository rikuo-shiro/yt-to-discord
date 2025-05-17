# dummy_server.py - Webサービスとして動かす
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer

def run_dummy_server():
    class DummyHandler(BaseHTTPRequestHandler):
        def do_GET(self):
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"Bot is running")

    server = HTTPServer(('0.0.0.0', 10000), DummyHandler)
    server.serve_forever()

threading.Thread(target=run_dummy_server, daemon=True).start()




import pytchat
import requests
import re

# 🔧 あなたのライブ動画のID（URLの最後の部分）
VIDEO_ID = "https://www.youtube.com/watch?v=fTiSrW_ZMSw"

# 🔧 あなたのDiscord Webhook URL
DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1373269699248259163/VBpN7VszrXauuc2w-49k88ftrDMlE5DKtOvuyTKH60t5qX62ZT4YBDy-qKGjE1sR8gxs"


# # YouTubeチャットの監視スタート
# chat = pytchat.create(video_id=VIDEO_ID)

# print("✅ 監視開始：16桁の数列コメントを転送します")

# while chat.is_alive():
#     for c in chat.get().sync_items():
#         message = c.message.strip()
#         if re.fullmatch(r"\d{16}", message):
#             print(f"▶ 転送: {message}")
#             content = f"💬 **{c.author.name}**: {message}"
#             requests.post(DISCORD_WEBHOOK_URL, json={"content": content})




# チャット取得開始
chat = pytchat.create(video_id=VIDEO_ID)

# print("✅ 16桁数列を抽出して送信中...")

# while chat.is_alive():
#     for c in chat.get().sync_items():
#         message = c.message.strip()
        
#         # 16桁の数字をすべて抽出（複数あっても対応）
#         matches = re.findall(r"\d{16}", message)
        
#         if matches:
#             for match in matches:
#                 print(f"▶ 転送: {match}")
#                 # 数列だけを送信
#                 requests.post(DISCORD_WEBHOOK_URL, json={"content": match})









print("✅ ユーザー名と16桁数列を連携中...")

# 👤 前回の送信者を記録
last_author = None

while chat.is_alive():
    for c in chat.get().sync_items():
        message = c.message.strip()
        matches = re.findall(r"\d{16}", message)

        if matches:
            # 今回のコメント投稿者
            current_author = c.author.name

            # ① 違うユーザーなら：名前を先に送信
            if current_author != last_author:
                requests.post(DISCORD_WEBHOOK_URL, json={"content": f"👤 {current_author}"})
                last_author = current_author

            # ② 数列だけを順に送信
            for match in matches:
                requests.post(DISCORD_WEBHOOK_URL, json={"content": match})
                print(f"▶ {current_author}: {match}")



