#!/bin/sh
find . -name '*.py' | xargs yapf -i
rm -f ./nohup.out
find . -name '__pycache__' | xargs rm -rf
find . -name '*.pyc' | xargs rm -f
ret=`ps -ef | grep stock  | awk '{print $2}' | xargs kill -9 > /dev/null 2>&1`
ret=`ps -ef | grep stock_api  | awk '{print $2}' | xargs kill -9 > /dev/null 2>&1`
echo "app exit"
nohup python3 stock.py > ./nohup.out 2>&1 &
echo "app start"
nohup python3 stock_api.py > ./nohup.out 2>&1 &
ps -ef | grep 'stock'