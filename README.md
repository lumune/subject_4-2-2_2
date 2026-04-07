# subject_4-2-2_2
提出用課題

4-2-2 API連携実践課題

# 2. Zoom API


Zoom API（OAuth）を利用して、認証後にZoomミーティングを自動作成するPythonアプリです。  
ターミナルから会議内容を入力し、ミーティングID・パスワード・参加URLを取得できます。

---

## 🚀 機能

- OAuth認証によるZoom API連携
- アクセストークンの取得
- Zoomミーティングの自動作成
- 会議情報（ID / パスワード / URL）の出力
- ターミナル入力による会議内容の動的設定
- ローカルサーバーを使用した認証コードの自動取得（コピペ不要）
- 認証完了後、ブラウザに完了メッセージを表示（UX向上）

---

## 🛠 使用技術

- Python
- requests
- python-dotenv
- Zoom API（OAuth）
- http.server（ローカルサーバー）

---

## 📦 セットアップ方法

### ① リポジトリをクローン

``bash``
``git clone https://github.com/your-username/your-repo-name.git``
``cd your-repo-name``

### ② ライブラリをインストール

``bash``
``pip install requests python-dotenv``

### ③ .envファイルを作成
プロジェクト直下に .env ファイルを作成し、以下を記述してください。

``CLIENT_ID=あなたのClientID``
``CLIENT_SECRET=あなたのClientSecret``
``REDIRECT_URI=http://localhost:8000``

※ .env はGitHubにアップしないでください

---

## ▶️ 実行方法

``bash``
``python zoom_auto.py``

---

## 🔄 実行の流れ

1. ターミナルに表示されたURLをブラウザで開く
2. Zoomで「許可」をクリック
3. ブラウザに「認証成功」と表示される
4. ターミナルで会議情報を入力
5. Zoomミーティングが作成される

---

## 📎 注意事項

- .env ファイルは絶対に公開しないでください
- Zoom APIの設定（OAuthアプリ作成）が必要です
