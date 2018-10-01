import sys

from flask import Flask, request

import receive
import reply

app = Flask(__name__)

print('Python version:', sys.version)


@app.route('/hello')
def hello():
    print('hello')
    return 'hello'


@app.route('/wx', methods=['GET', 'POST'])
def weixin():
    assert request.method == 'POST'
    webData = request.data
    print('WebData: ', webData)
    recMsg = receive.parse_xml(webData)
    if recMsg is None:
        print('Parse error')
        return 'success'
    if isinstance(recMsg, receive.Msg) and recMsg.MsgType == 'text':
        toUser = recMsg.FromUserName
        fromUser = recMsg.ToUserName
        text = recMsg.Content
        print('收到文本消息: "{}"'.format(text))
        content = "你好，谢谢你的消息！你的消息一共有{}个字".format(len(text))
        replyMsg = reply.TextMsg(toUser, fromUser, content)
        return replyMsg.send()
    else:
        print("暂且不处理")
        return "success"
