from pathlib import Path
import requests
import pandas as pd
import os
from dotenv import load_dotenv

env_path = Path("..") / ".env"
load_dotenv(dotenv_path=env_path)

# APIのURL
URL = "https://www.reinfolib.mlit.go.jp/ex-api/external/XIT001"
# APIのKEY
KEY = os.getenv("REINFOLIB_CLIENT_API")
# API専用のheader 及び param設定
headers = {"Ocp-Apim-Subscription-Key": KEY}

# --- このコードを使用するサンプル ---
if __name__ == "__main__":
    print("APIキーを読み込んでいます...")

    # 関数を呼び出してAPIキーを変数に保存
    API_KEY = load_api_key()

    if API_KEY:
        print("APIキーの読み込みに成功しました。")
        # セキュリティのため、キーの一部のみを出力
        print(f"   読み込んだキー（先頭4文字）: {API_KEY[:4]}****")

        # これで、このAPI_KEY変数を使ってAPIリクエストを送信できます。
        # 例: headers = {'Ocp-Apim-Subscription-Key': API_KEY}
    else:
        print(
            "APIキーの読み込みに失敗しました。上記のエラーメッセージを確認してください。"
        )
