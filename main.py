# -*- coding: utf-8 -*-
# filename: main.py

from flask import app, request

import receive
import reply

@app.route('/wx', methods=['POST'])
def weixin():
    assert request.method == 'POST'
    try:
        webData = request.data
        print "Handle Post webdata is ", webData
        recMsg = receive.parse_xml(webData)
        if isinstance(recMsg, receive.Msg) and recMsg.MsgType == 'text':
            toUser = recMsg.FromUserName
            fromUser = recMsg.ToUserName
            content = "你好，谢谢你的消息！你的消息一共有" + str(len(recMsg.Content)) + "个字"
            replyMsg = reply.TextMsg(toUser, fromUser, content)
            return replyMsg.send()
        else:
            print "暂且不处理"
            return "success"
    except Exception as e:
        return e
