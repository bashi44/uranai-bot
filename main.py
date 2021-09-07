# インポートするライブラリ
from flask import Flask, request, abort
from linebot import (
   LineBotApi, WebhookHandler
)
from linebot.exceptions import (
   InvalidSignatureError
)
from linebot.models import (
   FollowEvent, MessageEvent, TextMessage, TextSendMessage, ImageMessage, ImageSendMessage, TemplateSendMessage, ButtonsTemplate, PostbackTemplateAction, MessageTemplateAction, URITemplateAction
)
import os
import json

# jsonファイルを開き、データを取得する
json_open = open('save.json', 'r')
json_load = json.load(json_open)

# 軽量なウェブアプリケーションフレームワーク:Flask
app = Flask(__name__)
#環境変数からLINE Access Tokenを設定
LINE_CHANNEL_ACCESS_TOKEN = os.environ["LINE_CHANNEL_ACCESS_TOKEN"]
#環境変数からLINE Channel Secretを設定
LINE_CHANNEL_SECRET = os.environ["LINE_CHANNEL_SECRET"]
line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)
@app.route("/callback", methods=['POST'])
def callback():
   # get X-Line-Signature header value
   signature = request.headers['X-Line-Signature']
   # get request body as text
   body = request.get_data(as_text=True)
   app.logger.info("Request body: " + body)
   # handle webhook body
   try:
       handler.handle(body, signature)
   except InvalidSignatureError:
       abort(400)
   return 'OK'
# MessageEvent
@handler.add(MessageEvent,message=TextMessage)
def handle_message(event):
   # 送信されたメッセージに応じたデータをjsonファイルから返す
   your_msg = event.message.text
   for value in json_load:
      if value == your_msg:
         name = json_load[your_msg][0]['name']
         rank = json_load[your_msg][1]['rank']
         message = json_load[your_msg][2]['message']
         my_msg = name + '\n' + rank + '\n' + message 
         break
      else:
         my_msg = '申し訳ございません。\n星座名は『ひらがな+座』で送信してください。\n例：おひつじ座'
   line_bot_api.reply_message(event.reply_token,TextSendMessage(text=my_msg))
if __name__ == "__main__":
   port = int(os.getenv("PORT"))
   app.run(host="0.0.0.0", port=port)