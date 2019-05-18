from flask import Flask, request, abort, jsonify
from linebot import (LineBotApi, WebhookHandler)
from linebot.exceptions import (InvalidSignatureError)
from linebot.models import (MessageEvent, TextMessage, TextSendMessage,)
from flask.logging import create_logger
import requests
import json
import datetime, pytz
tz = pytz.timezone('Asia/Bangkok')

app = Flask(__name__)
LOG = create_logger(app)

line_bot_api = LineBotApi('THIS IS A SECRET')
handler = WebhookHandler('THIS IS A SECRET')

@app.route("/")
def hello():
    return "Hello World"

def date_now():
    now1 = datetime.datetime.now(tz)
    month_name = 'x มกราคม กุมภาพันธ์ มีนาคม เมษายน พฤษภาคม มิถุนายน กรกฎาคม สิงหาคม กันยายน ตุลาคม พฤศจิกายน ธันวาคม'.split()[now1.month]
    thai_year = now1.year + 543
    time_str = now1.strftime('%H:%M:%S')
    return "%d %s %d %s"%(now1.day, month_name, thai_year, time_str) # 30 ตุลาคม 2560 20:45:30

# for test
@app.route("/test")
def test():
    r = requests.get(
      'https://bx.in.th/api/')
    data = r.json()
    command = "acn"
    today = date_now()
    message = "ข้อมูลปัจจุบัน ณ เวลา " + today + "\n"
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
    today = date_now()
    message = "ข้อมูลปัจจุบัน ณ เวลา " + today + "\n"
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
        message = "ไม่มีคำสั่งที่คุณพิมพ์มาตอนนี้เรามีแค่\n1.acn (all crypto now)\n2.tcn(thai crypto now)"
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=message))

if __name__ == "__main__":
    app.run()
