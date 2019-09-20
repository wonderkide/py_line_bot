from flask import Flask, request, abort
from linebot import (LineBotApi, WebhookHandler)
from linebot.exceptions import (InvalidSignatureError)
from linebot.models import (MessageEvent, TextMessage, TextSendMessage, ImageMessage, ImageSendMessage, )

import line_channel_setting
import json

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
        TextSendMessage(text=event.message.type))


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    #user = line_bot_api.get_profile(event.user_id)
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.source.user_id))
    #line_bot_api.push_message(
    #    event.source.user_id,
    #    ImageSendMessage(original_content_url='https://hoodline.imgix.net/uploads/story/image/579057/..destination_photo_url..RIOA-sky.jpg.jpg', preview_image_url='https://hoodline.imgix.net/uploads/story/image/579057/..destination_photo_url..RIOA-sky.jpg.jpg'))
'''

@handler.add(MessageEvent)
def handle_message(event, destination):
    if event.message.type == 'text':
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=event.message.text))
    elif event.message.type == 'image':
        #img = line_bot_api.get_message_content(event.message.id)
        if event.message.content_provider.type == 'line':
            message_content = line_bot_api.get_message_content(event.message.id)
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=event.message.content_provider.type))

            
            with open('test.jpg', 'wb') as fd:
                for chunk in message_content.iter_content():
                    fd.write(chunk)

        line_bot_api.reply_message(
            event.reply_token,
            #ImageSendMessage(original_content_url=img.original_content_url, preview_image_url=img.preview_image_url))
            TextSendMessage(text=event.message.content_provider.type))


if __name__ == "__main__":
    app.run()