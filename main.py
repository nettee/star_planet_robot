import sys

from flask import Flask, request

import chatter
import receive
import reply

app = Flask(__name__)

print('Python version:', sys.version)

chatter.train()
print('Chatter training done.')


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
        content = chatter.get_response(text)
        print('返回消息: "{}"'.format(content))
        replyMsg = reply.TextMsg(toUser, fromUser, content)
        return replyMsg.send()
    else:
        print("暂且不处理")
        return "success"
