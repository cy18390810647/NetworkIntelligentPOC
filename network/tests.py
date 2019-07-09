# -*- coding: utf-8 -*-
from django.test import TestCase
import ConfigParser
import os

# Create your tests here.

print("123")


# 读取配置文件样例
def test_reader():
    """
    读取配置文件样例
    :return:
    """
    cp = ConfigParser.SafeConfigParser()
    cp.read('myapp.conf')

    print os.path.abspath(os.path.dirname(__file__))
    print 'options of [file]:', cp.options('file')
    print 'fileUrl of file:', cp.get('file', 'fileUrl')
    log_file_path = cp.get('file', 'fileUrl')
    print 'options of [esAddress]:', cp.options('esAddress')
    print 'port of esAddress:', cp.get('esAddress', 'port')
    print 'ip of esAddress:', cp.get('esAddress', 'ip')

    curPath = os.path.abspath(os.path.dirname(__file__))
    rootPath = curPath[:curPath.find("NetworkIntelligentPOC\\") + len("NetworkIntelligentPOC\\")]  # 获取myProject，也就是项目的根路径
    print rootPath+log_file_path

test_reader();