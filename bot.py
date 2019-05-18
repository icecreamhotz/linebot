from flask import Flask, request, abort, jsonify
from linebot import (LineBotApi, WebhookHandler)
from linebot.exceptions import (InvalidSignatureError)
from linebot.models import (MessageEvent, TextMessage, TextSendMessage,)
from flask.logging import create_logger
import requests
import json

app = Flask(__name__)
LOG = create_logger(app)

line_bot_api = LineBotApi('THIS IS A SECRET')
handler = WebhookHandler('THIS IS A SECRET')

@app.route("/")
def hello():
    return "Hello World"

# for test
@app.route("/test")
def test():

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
    command = event.message.text
    r = requests.get(
      'https://superheroapi.com/api/2531207266924281/search/' + command)
    data = r.json()
    message = ""
    if data['response'] == "success":
        for item in data['results']:
            message += "ชื่อในวงการ: " + item['name']
            message += "\nชื่อจริง: " + item['biography']['full-name']
            message += "\nเพศ: " + item['appearance']['gender']
            message += "\nส่วนสูง: " + item['appearance']['height'][1]
            message += "\nน้ำหนัก: " + item['appearance']['weight'][1]
            message += "\nสถานที่เกิด: " + item['biography']['place-of-birth']
            message += "\nเผ่าพันธ์: " + item['appearance']['race']
            message += "\nความฉลาด: " + item['powerstats']['intelligence']
            message += "\nความแข็งแรง: " + item['powerstats']['strength']
            message += "\nความไว: " + item['powerstats']['speed']
            message += "\nความทนทาน: " + item['powerstats']['durability']
            message += "\nพลังการต่อสู้: " + item['powerstats']['power']
            message += "\nทักษะการต่อสู้: " + item['powerstats']['combat']
            message += "\nสื่อที่ตีพิมพ์: " + item['biography']['publisher']
            message += "\n-----------------------\n"
    else:
        message = "ไม่พบข้อมูลของตัวละคร " + command + "\n*หมายเหตุ เว้นวรรคมีผลกับการค้นหาเช่น captain america, iron man ตัวเล็กตัวใหญ่ไม่มีผล"
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=message))

if __name__ == "__main__":
    app.run()
