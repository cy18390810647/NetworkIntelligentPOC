# -*- coding: utf-8 -*-
from django.http import HttpResponse
import json
import time
from django.shortcuts import render
import re
# from elasticsearch import Elasticsearch
from django.views.decorators.csrf import csrf_exempt
import os


@csrf_exempt
def group_conf(request):
    res_data = json.loads(request.body)
    str = ("List:"+'\n')
    for i in res_data['data'][0]['info']:
        host = i['address']
        username = i['username']
        pwd = i['password']
        str1 = (
           "  - host: {}".format(host)+'\n'
           "    username: {}".format(username)+'\n'
           "    pwd: {}".format(pwd)+'\n'
           "    cmds:"+'\n'
           "      - enable"+'\n'
           "      - 123456"+'\n'
           "      - configure terminal"+'\n'
           "      - interface FastEthernet1/0"+'\n'
           "      - ip address 192.168.2.1 255.255.255.0"+'\n'
           "      - no shutdown"+'\n'
           "      - exit"+'\n'
           "      - ip route 192.168.3.0 255.255.255.0 192.168.2.2"+'\n'
           "      - exit"+'\n'
           "      - wr"+'\n'
        )
        str = str+str1
    with open('../NetworkIntelligentPOC/network/conf.yml', 'w+')as f:
        f.write(str)
    os.system(r"python ..\NetworkIntelligentPOC\static\txtdir\1.py")
    res = {"res": True}
    return HttpResponse(json.dumps(res))


@csrf_exempt
def ip_conf(request):
    print(2)
    res = {"res": True}
    return HttpResponse(json.dumps(res))


def index(request):

    return render(request, 'network.html')


def index1(request):

    return render(request, 'network1.html')


def es(list_data, name):
    """
    数据处理
    :param list_data:
    :return:
    """
    res_list = []
    for data in list_data:
        if len(res_list) == 0:
            res_list.append(data)
        else:
            num = 0
            for res_data in res_list:
                num = num + 1
                if res_data[name] == data[name]:
                    break
                elif num == len(res_list):
                    res_list.append(data)
    return res_list


@csrf_exempt
def test(request):
    res_data = json.loads(request.body)
    sel_name = res_data['sel_name']
    sel_source_region = res_data['sel_source_region']
    sel_destination_area = res_data['sel_destination_area']
    sel_source_ip = res_data['sel_source_ip']
    sel_source_port = res_data['sel_source_port']
    sel_destination_ip = res_data['sel_destination_ip']
    sel_tcp_flag = res_data['sel_tcp_flag']
    sel_destination_port = res_data['sel_destination_port']
    try:
        start_time = int(time.mktime(time.strptime(str(res_data['date_time'][0]), "%Y-%m-%d %H:%M:%S")))
        end_time = int(time.mktime(time.strptime(str(res_data['date_time'][1]), "%Y-%m-%d %H:%M:%S")))

    except Exception as e:
        start_time = 0
        end_time = 0
    try:
        start_time1 = int(time.mktime(time.strptime(str(res_data['date_time1'][0]), "%Y-%m-%d %H:%M:%S")))
        end_time1 = int(time.mktime(time.strptime(str(res_data['date_time1'][1]), "%Y-%m-%d %H:%M:%S")))
    except Exception as e:
        start_time1 = 0
        end_time1 = 0
    data_list = []  # 数据列表
    data_list1 = []
    # es_obj = Elasticsearch(['192.168.1.152:9200'])
    # query = {'query': {'match_all': {}}}  # 查找所有文档
    # all_Doc = es_obj.search(body=query, index='alarm_2019.02.11')
    with open(r'..\NetworkIntelligentPOC\static\txtdir\syslog.txt', 'r') as log_data:
        for line in log_data:
            ss = re.findall(r' for (.+) to ', line)  # 匹配每一行中的for和to
            if len(ss) > 0:
                # 大于0则匹配存在，然后取数据
                data_time = int(time.mktime(time.strptime (str(line[5:25]), "%b %d %Y %H:%M:%S")))
                for_str = re.findall(r' for (.+?):', line)[0]  # 取for和:之间的参数，贪婪取
                to_str = str.lower(re.findall(r' to (.+?):', line)[0])  # 取to和:之间的参数，贪婪取
                name = line[line.rfind('connection', 1)-4:line.rfind('connection', 1)-1]  # 取connection前面的协议字符串
                # 进行数据整理，并计数
                # 匹配前台来的数据和日志数据是否相等，若为空则是匹配所有
                if name == sel_name or sel_name == '':
                    if sel_source_region == '' or for_str == sel_source_region:
                        if (sel_destination_area == '' or sel_destination_area == to_str) and to_str.find(' ') == -1:
                            if start_time <= data_time <= end_time or start_time == 0 and end_time == 0:
                                log_dic = {
                                    "source_region": for_str,
                                    "destination_area": to_str,
                                    "name": name,
                                    "num": 1,
                                }
                                if len(data_list) == 0:
                                    data_list.append(log_dic)
                                list_num = 0
                                for data in data_list:
                                    list_num = list_num+1
                                    if data['source_region'] == for_str and data['destination_area'] == to_str:
                                        data["num"] += 1
                                        break
                                    elif len(data_list) == list_num:
                                        data_list.append (log_dic)
            ss1 = re.findall(r' [(]no connection[)] (.+) flags ', line)
            if len(ss1) > 0:
                name = re.findall(r'%(.+?):', line)
                data_time = int(time.mktime(time.strptime(str(line[5:25]), "%b %d %Y %H:%M:%S")))
                data_time1 = line[5:25]
                source_ip = re.findall(r' from (.+?)/', line)[0]
                source_port = re.findall(r'/(.+?) to ', line)[0]
                destination_ip = re.findall(r' to (.+?)/', line)[0]
                tcp_flag = re.findall(r' flags (.+?) on', line)[0]
                destination_port = re.findall(r'/(.+?)/(.+?) flags ', line)[0][1]
                if source_ip == sel_source_ip or sel_source_ip == '':
                    if sel_source_port == '' or source_port == sel_source_port:
                        if sel_destination_ip == '' or sel_destination_ip == destination_ip:
                            if start_time1 <= data_time <= end_time1 or start_time1 == 0 and end_time1 == 0:
                                if sel_tcp_flag == '' or sel_tcp_flag == tcp_flag:
                                    if sel_destination_port == '' or sel_destination_port == destination_port:
                                        res_dic = {
                                            "name":name,
                                            "data_time":data_time1,
                                            "source_ip": source_ip,
                                            "source_port": source_port,
                                            "destination_ip": destination_ip,
                                            "tcp_flag": tcp_flag,
                                            "destination_port": destination_port
                                        }
                                        data_list1.append(res_dic)
    source_region_List = es(data_list, 'source_region')
    destination_area_List = es(data_list, 'destination_area')
    name_List = es(data_list, 'name')
    source_ip_List = es(data_list1, 'source_ip')
    source_port_List = es(data_list1, 'source_port')
    destination_ip_List = es(data_list1, 'destination_ip')
    tcp_flag_List = es(data_list1, 'tcp_flag')
    destination_port_List = es(data_list1, 'destination_port')
    res = {
        "res":data_list,
        "res1":data_list1,
        "source_region_List": source_region_List,
        "destination_area_List": destination_area_List,
        "name_List": name_List,
        "source_ip_List": source_ip_List,
        "source_port_List": source_port_List,
        "destination_ip_List": destination_ip_List,
        "tcp_flag_List": tcp_flag_List,
        "destination_port_List": destination_port_List
    }
    return HttpResponse(json.dumps(res))

