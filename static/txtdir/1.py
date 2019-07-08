# -*- coding:utf-8 -*-
# @File  : demo1.py
# @Author: zlx
# @Date  : 2019/7/2
# @Desc  : 机器学习
import paramiko
import time
import os
import yaml
from threading import *


def verification_ssh(host, username, password, cmds, port=22):
    s = paramiko.Transport(host, int(port))
    s.connect(username=username, password=password)
    time.sleep(0.1)
    chan = s.open_session()
    chan.settimeout(15)
    chan.get_pty()
    chan.invoke_shell()
    for cmd in cmds:
        print(cmd)
        chan.send(str(cmd) + "\n")
        time.sleep(1)
    time.sleep(3)
    strz = chan.recv(65535)
    #print strz
    # f = open("D:\\t.txt", "w")
    # f.write(chan.recv(65535).decode('ascii'))
    # f.close()
    s.close()


def load_config(path):
    """
    将指定路径下的配置文件信息加载到对象中
    """
    # 判断是否存在配置文件，如果不存在返回None
    if not os.path.exists(path):
        return False
    fp = None
    try:
        fp = open(path)
        configs = fp.read()
    except Exception as e:
        if None is not fp:
            fp.close()
        return False
    if None is not fp:
        fp.close()
    # 使用ymal文件方式载入配置文件，生成字典
    try:
        config_dict = yaml.load(configs)
        return config_dict
    except Exception as e:
        print(e)
        return False


if __name__ == '__main__':
    # 配置文件的路径
    config_dir = r'..\NetworkIntelligentPOC\static\txtdir\conf.yml'
    conf_dict = load_config(path=config_dir)
    print(conf_dict)
    if conf_dict:
        conf_list = conf_dict['List']
        for conf in conf_list:
            username = conf['username']
            host = conf['host']
            pwd = conf['pwd']
            cmds = conf['cmds']
            t = Thread(target=verification_ssh(host, str(username), str(pwd), cmds))
            t.start()
            print (host+"自动化配置执行完毕...")
    else:
        print ("获取配置文件出错！")
