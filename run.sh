#!/bin/sh
/usr/sbin/uwsgi --ini ttt.ini  --cache2 name=mycache,items=100
