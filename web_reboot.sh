#!/bin/bash

echo '--------gunicorn process-----'
ps -ef |grep gunicorn|grep -v grep

echo -e '\n--------going to close------'
sleep 0.5
# ps -ef |grep wsgi_cmdbtest.ini|grep -v grep|awk 'NR==1{print $2}'|xargs kill -9
# kill -9 `ps -ef |grep  wsgi_use.ini|grep -v 'grep'| awk '{print $2}'`
pkill gunicorn

echo -e '\n--------check if the kill action is correct------'

sleep 1.5
gunicorn -c config/gunicorn.conf config.wsgi

echo -e '\n\033[42;1m----------started...------\033[0m'
sleep 1
ps -ef |grep gunicorn


echo -e '\n---------log----------'
tail -f /var/log/gunicorn_access.log