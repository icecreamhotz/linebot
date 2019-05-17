from flask import Flask, request, abort
from linebot import (LineBotApi, WebhookHandler)
from linebot.exceptions import (InvalidSignatureError)
from linebot.models import (MessageEvent, TextMessage, TextSendMessage,)

app = Flask(__name__)

line_bot_api = LineBotApi('zg8vZk9ia6rij/KY90Lh40+3TCbqujTeujhNXrGXy/LH6epuuF27rdV6HSLr6F8vJmUFds1LkXD9OS8ctQn23UpiaCpKf/SLVLQSicjljBIvTokhv17eCNBrFF9pbYoZNsT/Xo/a3WaA6poP1SIt6gdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('32e5d95ef00636497e243caae6e97f2f')

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


if __name__ == "__main__":
    app.run()