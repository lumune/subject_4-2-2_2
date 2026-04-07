import os
import requests
from urllib.parse import urlencode
from dotenv import load_dotenv
from datetime import datetime
from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib

load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REDIRECT_URI = os.getenv("REDIRECT_URI")


# ① 認証URL生成
def get_auth_url():
    params = {
        "response_type": "code",
        "client_id": CLIENT_ID,
        "redirect_uri": REDIRECT_URI
    }
    url = f"https://zoom.us/oauth/authorize?{urlencode(params)}"
    return url


# ② code → access_token
def get_access_token(code):
    url = "https://zoom.us/oauth/token"
    data = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": REDIRECT_URI
    }

    response = requests.post(
        url,
        auth=(CLIENT_ID, CLIENT_SECRET),
        data=data
    )

    res_json = response.json()

    if "access_token" not in res_json:
        print("❌ トークン取得エラー:", res_json)
        return None

    return res_json["access_token"]


# ③ 会議作成
def create_meeting(access_token):
    url = "https://api.zoom.us/v2/users/me/meetings"

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    # 👇 ターミナル入力
    topic = input("会議タイトルを入力して👇: ")
    start_time = input("開始時間を入力（例: 2026-04-02 15:00）: ")
    duration = input("会議時間（分）を入力（例: 60）: ")

    try:
        dt = datetime.strptime(start_time, "%Y-%m-%d %H:%M")
    except ValueError:
        print("❌ 日時の形式が違うよ！（例: 2026-04-02 15:00）")
        return

    zoom_time = dt.strftime("%Y-%m-%dT%H:%M:%SZ")

    data = {
        "topic": topic,
        "type": 2,
        "start_time": zoom_time,
        "duration": int(duration),
        "timezone": "Asia/Tokyo"
    }

    response = requests.post(url, headers=headers, json=data)
    meeting = response.json()

    if "id" not in meeting:
        print("❌ 会議作成エラー:", meeting)
        return

    print("\n🎉 会議作成成功！")
    print("Meeting ID:", meeting.get("id"))
    print("Password:", meeting.get("password"))
    print("Join URL:", meeting.get("join_url"))


# ④ OAuth受け取りサーバー（修正版）
class OAuthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        query = urllib.parse.urlparse(self.path).query
        params = urllib.parse.parse_qs(query)

        if "code" in params:
            code = params["code"][0]
            print("\n✅ code取得成功:", code)

            # 👇 先にブラウザへレスポンス返す（重要）
            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write("認証成功！ターミナルに戻ってください。".encode("utf-8"))

            # 👇 そのあと処理
            token = get_access_token(code)
            if token:
                create_meeting(token)


def run_server():
    server = HTTPServer(("localhost", 8000), OAuthHandler)
    print("\n🚀 サーバー起動：http://localhost:8000")
    server.handle_request()


# 実行
if __name__ == "__main__":
    print("① このURLを開いて認証して👇\n")
    print(get_auth_url())

    print("\n② 認証後、自動で処理されます...")
    run_server()