from flask import Flask, request, abort
from linebot import (LineBotApi, WebhookHandler)
from linebot.exceptions import (InvalidSignatureError)
from linebot.models import (MessageEvent, TextMessage, TextSendMessage,)

app = Flask(__name__)

line_bot_api = LineBotApi('X8H8tZp/fwqo7QXQxIYAzB9JFl5Rc7gGC8YGiVvoCMOCo+LXXsGJ49IsLX4x9uL66s7y6m03sbJQDKW9xQ0tTcpztuOdWjF0Z2Shf+CnpwVfYpZovZq/UC7IHQI1qZ8a0Pjx99uhV2Wtnis79+XREAdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('ef9543e4b95c520018a463fb79b6e9d9')

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

    url = 'https://api.netpie.io/feed/IOTROOM?apikey=vz8QtgHoM7EhWc7UdCPIuBVOTs4YKjZ2&granularity=10minute&since=1hour'

    if event.message.text=='Get token':
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=event.reply_token))
    elif event.message.text=='Get id':
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=event.source.user_id))
    elif event.message.text=='Get temp':
        response = urllib.request.urlopen(url).read()
        data = json.loads(response.decode('utf-8'))
        data = data["lastest_data"][1]["values"][0][1]
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text="temperature: "+str(data)))
    elif event.message.text=='Get humid':
        response = urllib.request.urlopen(url).read()
        data = json.loads(response.decode('utf-8'))
        data = data["lastest_data"][0]["values"][0][1]
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text="Humidity: "+str(data)))
    else :
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    app.run()
