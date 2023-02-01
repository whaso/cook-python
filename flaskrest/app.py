import time

from flask import Flask
from flask_restful import Resource, Api, reqparse
from flask_socketio import SocketIO, emit


app = Flask(__name__)

api = Api(app)
socketio = SocketIO(app)


class HelloWorld(Resource):
    def get(self):
        return {"hello": "World"}


@socketio.on('request_for_response',namespace='/testnamespace')
def give_response(data):
    value = data.get('param')
    print(f"param: {value}")
 
    #进行一些对value的处理或者其他操作,在此期间可以随时会调用emit方法向前台发送消息
    emit('response',{'code':'200','msg':'start to process...'})
 
    time.sleep(1)
    emit('response',{'code':'200','msg':'processed'})


api.add_resource(HelloWorld, "/")


if __name__ == "__main__":
    socketio.run(app)
