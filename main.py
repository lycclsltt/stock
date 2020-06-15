#coding=utf-8
from lib.config import Config
from lib.watcher import Watcher
import sys
import multiprocessing
import time
import gevent
import gevent.monkey
gevent.monkey.patch_all()

def run(stock, notifyUrl):
    print('stock2',stock)
    watcher = Watcher(stock['code'], buyPriceList=stock['buyPriceList'], salePriceList=stock['salePriceList'], notifyUrl=notifyUrl)
    watcher.start()

if __name__ == '__main__':
    conf = Config("./config.json")
    if not conf.isOK():
        print('conf has syntax error')
        sys.exit()
    taskList = []
    for stock in conf.reload().data['stockList']:
        t = gevent.spawn(run, stock, conf.reload().data['notifyUrl'])
        taskList.append(t)
    gevent.joinall(taskList)