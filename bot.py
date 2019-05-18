from flask import Flask, request, abort, jsonify
from linebot import (LineBotApi, WebhookHandler)
from linebot.exceptions import (InvalidSignatureError)
from linebot.models import (MessageEvent, TextMessage, TextSendMessage,)
from flask.logging import create_logger
import requests
import json
from datetime import datetime

app = Flask(__name__)
LOG = create_logger(app)

line_bot_api = LineBotApi('zg8vZk9ia6rij/KY90Lh40+3TCbqujTeujhNXrGXy/LH6epuuF27rdV6HSLr6F8vJmUFds1LkXD9OS8ctQn23UpiaCpKf/SLVLQSicjljBIvTokhv17eCNBrFF9pbYoZNsT/Xo/a3WaA6poP1SIt6gdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('32e5d95ef00636497e243caae6e97f2f')

@app.route("/")
def hello():
    return "Hello World"

def keyfunc(tup):
    key, d = tup
    return d["pairing_id"]


# for test
@app.route("/test")
def test():
    r = requests.get(
      'https://bx.in.th/api/')
    data = r.json()
    command = "acn"
    today = date.today()
    month = today.month < 10 and "0" + str(today.month) or str(today.month)
    message = "ข้อมูลปัจจุบัน ณ เวลา " + str(today.day) + "/" + month + "/" + str(today.year) + "\n"
    if command == "tcn":
        filterData = [v for v in data.values() if "THB" in v.values()]
        for value in sorted(filterData, key = lambda name: name['pairing_id']):
            message += str(value['pairing_id']) + ": " + value['primary_currency'] + " to " + value['secondary_currency'] + " = " + str(value['last_price']) + "\n"
    elif command == "acn":
        for value in sorted(data.values(), key = lambda name: name['pairing_id']):
            message += str(value['pairing_id']) + ": " + value['primary_currency'] + " to " + value['secondary_currency'] + " = " + str(value['last_price']) + "\n"
    # for key, value in sort_data:
    # return jsonify(r.json())
    print(message)
    return "ok"

@app.route("/webhook", methods=['POST'])
def webhook():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    LOG.debug("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'
    

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    r = requests.get(
      'https://bx.in.th/api/')
    data = r.json()
    command = event.message.text
    today = datetime.now()
    hourMinuteSecond = today.strftime('%H:%M:%S')
    month = today.month < 10 and "0" + str(today.month) or str(today.month)
    year = today.year + 543
    message = "ข้อมูลปัจจุบัน ณ เวลา " + str(today.day) + "/" + month + "/" + str(year) + " " + hourMinuteSecond + "\n"
    if command == "tcn":
        filterData = [v for v in data.values() if "THB" in v.values()]
        for value in sorted(filterData, key = lambda name: name['pairing_id']):
            message += str(value['pairing_id']) + ": " + value['primary_currency'] + " to " + value['secondary_currency'] + " = " + str(value['last_price']) + "\n"
    elif command == "acn":
        for value in sorted(data.values(), key = lambda name: name['pairing_id']):
            message += str(value['pairing_id']) + ": " + value['primary_currency'] + " to " + value['secondary_currency'] + " = " + str(value['last_price']) + "\n"
    elif command == "รักเค้าไหม":
        message = "รักดิมากด้วย <3"
    elif command == "ตอแหลไหม":
        message = "มากที่สุดเหมือนกัน :)"
    else:
        message = "ไม่มีคำสั่งที่คุณพิมพ์มาตอนนี้เรามีแค่\n1. acn (all crypto now)\n2.tcn(thai crypto now)"
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=message))

if __name__ == "__main__":
    app.run()