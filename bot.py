from flask import Flask, request, abort
from linebot import (LineBotApi, WebhookHandler)
from linebot.exceptions import (InvalidSignatureError)
from linebot.models import (MessageEvent, TextMessage, TextSendMessage, ImageMessage, ImageSendMessage, )

import line_channel_setting

app = Flask(__name__)

line_bot_api = LineBotApi(line_channel_setting.token)
handler = WebhookHandler(line_channel_setting.secret)

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/webhook", methods=['POST'])
def webhook():
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
    
'''
@handler.add(MessageEvent, message=ImageMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        ImageSendMessage(even.message.original_content_url, even.message.preview_image_url))
'''

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    #user = line_bot_api.get_profile(event.user_id)
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.source.userId))
    #line_bot_api.push_message(
    #    event.user_id,
    #    ImageSendMessage(original_content_url='https://hoodline.imgix.net/uploads/story/image/579057/..destination_photo_url..RIOA-sky.jpg.jpg', preview_image_url='https://hoodline.imgix.net/uploads/story/image/579057/..destination_photo_url..RIOA-sky.jpg.jpg'))



if __name__ == "__main__":
    app.run()