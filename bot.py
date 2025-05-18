# --- Renderの無料Webサービス対策用 ダミーWebサーバー ---
import threading
import os
from http.server import BaseHTTPRequestHandler, HTTPServer

def run_dummy_server():
    port = int(os.environ.get("PORT", 8000))  # Renderから渡されるポートを取得
    class DummyHandler(BaseHTTPRequestHandler):
        def do_GET(self):
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"Bot is running")

    server = HTTPServer(('0.0.0.0', port), DummyHandler)
    print(f"🌐 ダミーWebサーバー起動中（ポート: {port}）", flush=True)
    server.serve_forever()

threading.Thread(target=run_dummy_server, daemon=True).start()




import requests
import pytchat
import time
import re
import threading

# ========= 設定 =========
# API_KEY = ""
CHANNEL_ID = "UCd9lL57C8re9eQ5k1Hb0E0w"
# DISCORD_WEBHOOK_URL = ""


API_KEY = os.getenv("API_KEY")
# CHANNEL_ID = os.getenv("CHANNEL_ID")
DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")

# ========== 状態管理 ==========
user_latest_codes = {}
current_code_batch = {}
last_author = None
last_message_was_code = False

# ========== キーワード ==========
keywords_reset = r"(解除|再申請|船員|船長)"
keywords_hit = r"(通過|通った|通ってる|通ってます|擬似)"

# ========== 関数定義 ==========

def get_live_video_id():
    try:
        url = (
            f"https://www.googleapis.com/youtube/v3/search?"
            f"part=snippet&channelId={CHANNEL_ID}&type=video&eventType=live&key={API_KEY}"
        )
        resp = requests.get(url)
        if resp.status_code != 200:
            print(f"❌ APIエラー {resp.status_code}: {resp.text}", flush=True)
            return None

        data = resp.json()
        items = data.get("items", [])
        if items:
            video_id = items[0]["id"]["videoId"]
            print(f"✅ ライブ検出: {video_id}", flush=True)
            return video_id
        else:
            print("🔍 ライブなし（items 空）", flush=True)

    except Exception as e:
        print(f"❌ get_live_video_idで例外発生: {e}", flush=True)

    return None


def send_discord(msg):
    try:
        requests.post(DISCORD_WEBHOOK_URL, json={"content": msg})
    except:
        print("⚠ Discord送信失敗")

def monitor_chat(video_id):
    global last_author, last_message_was_code
    chat = pytchat.create(video_id=video_id)
    print("🎥 ライブ開始検出！",flush=True)
    send_discord(f"🚨 ライブ開始:https://www.youtube.com/watch?v={video_id}")

    while chat.is_alive():
        for c in chat.get().sync_items():
            author = c.author.name
            message = c.message.strip()
            codes = re.findall(r"\d{16}", message)

            if codes:
                if author != last_author:
                    send_discord(f"👤 {author}")
                    last_author = author
                for code in codes:
                    send_discord(code)
                    current_code_batch.setdefault(author, []).append(code)
                last_message_was_code = True

            else:
                if last_message_was_code and author in current_code_batch:
                    user_latest_codes[author] = current_code_batch[author]
                    current_code_batch[author] = []
                    last_message_was_code = False

                # if re.search(keywords_reset, message):
                #     if author in user_latest_codes:
                #         codes = "\n".join(user_latest_codes[author])
                #         send_discord(f"🔁 {author} の再申請対象コード:\n{codes}")

                # if re.search(keywords_hit, message):
                #     if author in user_latest_codes:
                #         codes = "\n".join(user_latest_codes[author])
                #         send_discord(f"🎉 {author} の当コード:\n{codes}")

# ========== メインループ ==========
# def main():
#     print("🔍 ライブ配信を監視中...")
#     detected = False
#     while True:
#         if not detected:
#             video_id = get_live_video_id()
#             if video_id:
#                 detected = True
#                 monitor_chat(video_id)
#         time.sleep(1500)


def main():
    print("🔍 ライブ配信を監視中...", flush=True)
    

    while True:
        print(f"PORT環境変数の値: {os.environ.get('PORT')}", flush=True)
        print(f"🕒 チェック開始: {time.strftime('%Y-%m-%d %H:%M:%S')}", flush=True)
        video_id = get_live_video_id()

        if video_id:
            monitor_chat(video_id)
            print("📴 ライブ配信が終了、再監視へ戻る", flush=True)
        else:
            print("⚠ 検出できず。25分後に再試行", flush=True)

        time.sleep(1500)




if __name__ == "__main__":
    main()








