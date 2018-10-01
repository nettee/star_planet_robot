#!/usr/bin/env python3

import time

import requests

url = 'http://127.0.0.1/wx'

def send_message(text):

    template = """<xml>
<ToUserName><![CDATA[{ToUserName}]]></ToUserName>
<FromUserName><![CDATA[{FromUserName}]]></FromUserName>
<CreateTime>{CreateTime}</CreateTime>
<MsgType><![CDATA[text]]></MsgType>
<Content><![CDATA[{Content}]]></Content>
<MsgId>{MsgId}</MsgId>
</xml>
"""

    msg = template.format(ToUserName='Alice',
                          FromUserName='Bob',
                          CreateTime=int(time.time()),
                          Content=text,
                          MsgId=1)
    requests.post(url, data=msg)


if __name__ == '__main__':

    send_message('hello')