import re
import requests as rq
import bs4
import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials

scope=['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name("credentials_key", scope)
gc = gspread.authorize(credentials)
#スコープで範囲指定⇨承認作業、APIv３は2020年9月終了⇨v4に書き直す必要あり。

SPREADSHEET_KEY=("SPREADSHEET_KEY")
worksheet = gc.open_by_key(SPREADSHEET_KEY).sheet1
#許可されたGoogleAPI変数"gc"を使い、データ出力先のスプレッドシートを特定する。

Keyword_list = ["パイソン"]
#複数検索したい場合は、検索したい文字列を＋で連結

url = "https://www.google.co.jp/webhp?gl=JP&num=10"
r = rq.get(url,params={"q":"Keyword_list"})
r.raise_for_status()   #200番台以上のエラーは中止
#Google接続後キーワードtop10検索、ちなみに"q"ではなく"num"を使うと1ページの情報を取得できる

soup=bs4.BeautifulSoup(r.content,"html.parser")
#htmlをパース(BeautifulSoupでデータ抽出する準備)

i=6
for a in soup.select("dic#search h3.r a"):
    url_list=re.sub(r"/url\?q=|&sa.*","",a.get("href"))
    worksheet.update_cell(i,6,url_list)
    i+=1
