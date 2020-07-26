#coding=utf-8

import requests
import demjson
import lib.util as util
import time
import sys
from agileutil.queue import UniMemQueue
from lib.config import Config

msgQueue = None

def initMsgQueue():
    global msgQueue
    if msgQueue != None: return
    msgQueue = UniMemQueue()
    if msgQueue == None: 
        print('init msg queue failed')
        sys.exit(1)

def sendDDMsg(ddrotUrl = '', msg = '', timeout = 10):
    util.disable_requests_warn()
    headers = {'Content-Type' : 'application/json'}
    params = {
        'msgtype' : 'text', 
        'text' : {'content' : msg },
    }
    data = demjson.encode(params)
    r = requests.post(url = ddrotUrl, headers=headers, data=data, timeout = timeout, verify=False)
    print('send msg:', msg, ddrotUrl, r.status_code, r.text)
    return r.status_code, r.text

def defaultSendDDMsg(msg):
    conf = Config("./config.json")
    if not conf.isOK(): return
    return sendDDMsg(conf.reload().data['notifyUrl'], msg, 10)

def safeSendDDMsg(ddrotUrl = '', msg = '', timeout = 10):
    code = output = None
    try:
        code, output = sendDDMsg(ddrotUrl, msg, timeout)
    except Exception as ex:
        print('safeSendDDMsg exception:' + str(ex))
        pass
    return code, output

def asyncSendMsg(msg):
    if msg == '': return
    print('asyncSendMsg')
    msgQueue.push(msg)

def asyncMsgConsume(sleepIntval = 60):
    while 1:
        time.sleep(sleepIntval)
        totalMsg = ''
        while 1:
            msg = msgQueue.pop()
            if msg == None: break
            totalMsg = totalMsg + msg + "\n\n"
        if totalMsg == '': continue
        defaultSendDDMsg(totalMsg)
        print('send once---------------------------------------')