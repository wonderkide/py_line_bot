from flask import Flask, request, abort
from linebot import (LineBotApi, WebhookHandler)
from linebot.exceptions import (InvalidSignatureError)
from linebot.models import (MessageEvent, TextMessage, TextSendMessage, ImageMessage, ImageSendMessage, )

app = Flask(__name__)

line_bot_api = LineBotApi('L4nfx9rvGHa4wm09LHokrFpTvS9zD5G8DzlYd8R1hIFiUsCOdU8fyZC/TT5sKjcK+fs+7EE5WKqjKVyxFCCSgCeJope5wS07yuY86Rsmm/B69GasZJjU7EWu97xLEUW1VTeg+B3kW8+bbG63CiU2fAdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('954e358c46fc39d8e061a44dd918de4f')

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
    

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))

@handler.add(MessageEvent, message=ImageMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        ImageSendMessage(even.message.preview_image_url))

if __name__ == "__main__":
    app.run()