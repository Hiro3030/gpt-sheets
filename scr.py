# %%
import os
from dotenv import load_dotenv
import openai
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# %%
# APIキーの設定
load_dotenv()
openai.api_key = os.environ["OPENAI_API_KEY"]

response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "user", "content": "日本の上位50人の有名なYoutuberを教えてください（登録者が多い上位50人でも◯）。チャンネル名と登録者数、YoutubeのアカウントのURL、簡単な紹介をタブ区切りのフォーマットで教えてください。"},
    ],
)
print(response.choices[0]["message"]["content"].strip())

# %%

# %%
# Google Sheets APIを使用するための認証情報を取得する
scope = ["https://www.googleapis.com/auth/spreadsheets"]
creds = ServiceAccountCredentials.from_json_keyfile_name(
    "credential-service-account.json", scope)
sheet_id = os.environ["SHEET_ID"]
# Google Sheets APIを使用して、Googleスプレッドシートにアクセスする
client = gspread.authorize(creds)
sheet = client.open_by_key(sheet_id).sheet1

# シートの初期化
sheet.clear()

# タブ区切りの文字列データを読み込む
data = response.choices[0]["message"]["content"].strip()

# 文字列データをタブ区切りで分割し、Googleスプレッドシートに入力する
for i, row in enumerate(data.split("\n")):
    values = row.split("\t")
    sheet.insert_row(values, i + 1)
# %%
