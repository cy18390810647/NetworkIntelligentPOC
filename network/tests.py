# -*- coding: utf-8 -*-
from django.test import TestCase
import ConfigParser

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
    print 'options of [file]:', cp.options('file')
    print 'fileUrl of file:', cp.get('file', 'fileUrl')

    print 'options of [esAddress]:', cp.options('esAddress')
    print 'port of esAddress:', cp.get('esAddress', 'port')
    print 'ip of esAddress:', cp.get('esAddress', 'ip')


test_reader();