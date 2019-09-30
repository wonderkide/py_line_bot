from flask import Flask, request, abort, render_template
from linebot import (LineBotApi, WebhookHandler)
from linebot.exceptions import (InvalidSignatureError)
from linebot.models import (MessageEvent, TextMessage, TextSendMessage, ImageMessage, ImageSendMessage, )

import line_channel_setting
import json

from PIL import Image
#from flask import Flask, render_template
import os

PEOPLE_FOLDER = os.path.join('static', 'test')



app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = PEOPLE_FOLDER

line_bot_api = LineBotApi(line_channel_setting.token)
handler = WebhookHandler(line_channel_setting.secret)

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/img")
def img():
    #full_filename = os.path.join(app.config['UPLOAD_FOLDER'], 'test.jpg')
    #return render_template("/test.html", user_image = full_filename)
    #image = Image.open('test.jpg')
    #image.show()
    message_content = line_bot_api.get_message_content(10657411630414)
    with open('img/'+ str(10657411630414) +'.jpg', 'wb') as fd:
                for chunk in message_content.iter_content():
                    fd.write(chunk)
    return 'gg';

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

        with open('file.txt', 'a') as fd:
                for chunk in message_content.iter_content():
                    fd.write('Hello\n')
    elif event.message.type == 'image':
        #img = line_bot_api.get_message_content(event.message.id)
        if event.message.content_provider.type == 'line':
            message_content = line_bot_api.get_message_content(event.message.id)
            #line_bot_api.push_message(event.source.user_id,TextSendMessage(text=event.message.id))
            #line_bot_api.reply_message(
            #    event.reply_token,
            #    TextSendMessage(text=event.message.content_provider.type))

            
            with open('img/'+ str(event.source.user_id) + '_' + str(event.message.id) +'.jpg', 'wb') as fd:
                for chunk in message_content.iter_content():
                    fd.write(chunk)
            
        '''
        line_bot_api.reply_message(
            event.reply_token,
            #ImageSendMessage(original_content_url=img.original_content_url, preview_image_url=img.preview_image_url))
            TextSendMessage(text=event.message.content_provider.type))
        '''


if __name__ == "__main__":
    app.run()