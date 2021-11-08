#! /usr/bin/python3
'''
@Author: Shuying Li <libunko@qq.com>
@Date: 2020-02-14 16:16:53
@LastEditTime: 2020-06-28 12:42:03
@LastEditors: Shuying Li <libunko@qq.com>
@Description: 
@FilePath: /v2ray_cli/v2ray_cli.py
'''

import os
import configparser
import time

import requests

from subscribe import Subscribe
# -*- coding:utf-8 -*-
import json
import os
import subprocess
import sys
import sys
import logging
import time
import traceback
import logging.handlers
import time
from datetime import datetime
logging.getLogger().setLevel(logging.NOTSET)
logging.getLogger('urllib3.connectionpool').setLevel(logging.WARNING)
logging.getLogger('web3.providers.HTTPProvider').setLevel(logging.WARNING)
logging.getLogger('web3.RequestManager').setLevel(logging.WARNING)

formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
h1 = logging.StreamHandler(sys.stdout)
h1.setFormatter(formatter)
h1.setLevel(logging.DEBUG)
logging.getLogger().addHandler(h1)
h2 = logging.handlers.RotatingFileHandler(
    filename='v2rayclilog.log', maxBytes=(1048576*5), backupCount=7
)
h2.setFormatter(formatter)
h2.setLevel(logging.DEBUG)
logging.getLogger().addHandler(h2)


cfg_pathname = "./cfg.conf"
json_template_pathname = "./config.json.template"
os.environ["https_proxy"] = ""
os.environ["http_proxy"] = ""

def chk_node_ok():
    try:
        http_proxy = "http://127.0.0.1:1081"
        https_proxy = "https://127.0.0.1:1081"
        proxyDict = {
            "http": http_proxy,
            "https": https_proxy,
        }

        res = requests.get("http://ip4.me/", proxies=proxyDict)
        #res = requests.get("https://www.youtube.com/", proxies=proxyDict)
        if res.status_code==200:
            # pos1 = res.content.find(r'Monospace" size=+3')
            # if pos1!=-1:
            #     print(res.content[pos1:pos1+50])
            # else:
            #     print(res.content)
            return True

    except:
        strexct = "except {}".format(traceback.format_exc())
        logging.info(strexct)

def check_next_node_signal():
    if os.path.isfile('/tmp/proxy_nextnode'):
        os.system("rm -rf  /tmp/proxy_nextnode")
        return True

def go_next(nexttime=30):
    '''

    :param nexttime: minutes
    :return:
    '''
    waitsec=nexttime*60
    while waitsec:
        waitsec= waitsec -1
        if check_next_node_signal():
            return
        time.sleep(1)

def start():
    cfg = configparser.ConfigParser()
    cfg.read(cfg_pathname, encoding='UTF-8')

    if cfg["subscribe"]["url"] == "":
        url = input("Please Enter The Subscription Address: ")
        cfg["subscribe"] = {"url": url}
        with open(cfg_pathname, 'w') as cfg_file:
            cfg.write(cfg_file)
    else:
        url = cfg["subscribe"]["url"]
    sub = Subscribe(url, json_template_pathname)
    while 1:
        try:
            sub.update()
            time.sleep(3)
            ok = chk_node_ok()
            if not ok:
                print("node is not available ,update next")
                continue
            logging.info("find succ node, wait next time update")

            go_next()
        except KeyboardInterrupt:
            sys.exit(0)
        except:
            strexct = "except {}".format(traceback.format_exc())
            logging.info(strexct)

if __name__=="__main__":
    start()