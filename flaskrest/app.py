import requests

from flask import Flask
from flask_restful import Resource, Api, reqparse
from flask_socketio import SocketIO, emit



app = Flask(__name__)

api = Api(app)
socketio = SocketIO(app)


class HelloWorld(Resource):
    def get(self):
        return {"hello": "World"}


@socketio.on('request_for_response', namespace='/testnamespace')
def give_response(data):
    msg = data.get('param')
    print(f"param: {msg}")
    headers = {
        "Authorization": "Bearer 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"
    }
    payload = {
        "model": "gpt-3.5-turbo",
        "messages": [{"role": "user", "content": f"{msg}"}]
    }

    resp = requests.post("https://api.openai.com/v1/chat/completions",
                         json=payload,
                         headers=headers,
                         proxies={"http": "http://127.0.0.1:7890",
                                  "https": "http://127.0.0.1:7890"},
                         verify=False)
    if resp.status_code != 200:
        pass
    print(f"response: {resp.json()}")
    for i in resp.json()["choices"]:
        emit("response", {"code": 200, "msg": i["message"]["content"]})

    # 进行一些对value的处理或者其他操作,在此期间可以随时会调用emit方法向前台发送消息
    # emit('response', {'code': '200', 'msg': 'start to process...'})

    # time.sleep(1)
    # emit('response', {'code': '200', 'msg': 'processed'})


api.add_resource(HelloWorld, "/")


if __name__ == "__main__":
    # http://168.168.78.172:5000/static/index.html
    socketio.run(app)
