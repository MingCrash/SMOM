# -*- encoding: utf-8 -*-
# Author: MingCrash

import time,re
from lxml.etree import _Element

def get_localformattime():
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())

# def get_localtime_withformat(format):
#     return time.strftime(format, time.localtime())

def get_localtimestamp():
    return int(time.time())

#time.localtime 将时间戳转化成日期结构对象
#1555923627 -> 2019-04-22
def get_makedtime(format,timestamp):
    return time.strftime(format, time.localtime(int(timestamp)))

#{key1:value1,key2:value2} -> key1=value1&key2=value2
def getUrlWithPars(dict):
    str = []
    for i in dict.keys():
        tmp = '{key}={val}'.format(key=i, val=dict[i])
        str.append(tmp)
    return '&'.join(str)

def compare_time(time1,time2):
    partten = [
        '%Y-%m-%d %H:%M:%S',
        '%Y-%m-%d %H:%M',
        '%Y-%m-%d %H',
        '%Y-%m-%d',
        '%Y.%m.%d %H:%M:%S',
        '%Y.%m.%d %H:%M',
        '%Y.%m.%d %H',
        '%Y.%m.%d',
        '%Y/%m/%d %H:%M:%S',
        '%Y/%m/%d %H:%M',
        '%Y/%m/%d %H',
        '%Y/%m/%d',
        '%Y年%m月%d日 %H:%M:%S',
        '%Y年%m月%d日 %H:%M',
        '%Y年%m月%d日 %H',
        '%Y年%m月%d日',
    ]
    s_time = None
    e_time = None
    for i in partten:
        try:
            s_time = time.mktime(time.strptime(time1,i))
        except:
            continue
        break
    for i in partten:
        try:
            e_time = time.mktime(time.strptime(time2, i))
        except:
            continue
        break
    return int(s_time) - int(e_time)

#Published on Feb 24, 2019  -> 2019-02-24
#Streamed live on Feb 24, 2019  -> 2019-02-24
def formatTime(input):
    partten = [
        'Published on %b %d, %Y',
        'Published on %b %d,%Y',
        'Premiered %b %d, %Y',
        'Premiered %b %d,%Y',
        'Streamed live on %b %d, %Y',
        'Streamed live on %b %d,%Y',
        'Started streaming on %b %d, %Y',
        '上线日期：%Y年%m月%d日',
        '%Y年%m月%d日发布',
        '首播时间：%Y年%m月%d日',
        '直播开始日期：%Y年%m月%d日',
        '首播开始于 %Y年%m月%d日',
    ]
    for i in partten:
        try:
            s_time = time.mktime(time.strptime(input,i))
            input = get_makedtime('%Y-%m-%d', s_time)
        except:
            continue
        break

    return input

#{'key':'value'} -> ['key:value']
def dict2list(dict):
    tmp = []
    for key in dict.keys():
        str = '{k}:{v}'.format(k=key, v=dict[key])
        tmp.append(str)
    return tmp

#['abcd','edfg','hijk'] -> 'abcdefghijk'
def list2str(input=None,property=None):
    tmp = ''
    if len(input) == 0:return ''
    for i in input:
        if isinstance(i,_Element):
            if property == 'text':
                tmp = tmp + str(i.text) + ' '
            else:
                tmp = tmp + str(i.get(property)) + ' '
        else:
            tmp = tmp + str(i) + ' '
    return tmp

def extract2list(input=None,property=None):
    tmp = []
    if len(input) == 0: return None
    for i in input:
        if isinstance(i,_Element):
            if property == 'text':
                tmp.append(str(i.text))
            else:
                tmp.append(str(i.get(property)))
    return tmp

#02-07-2019 -> 2-7-2019
def replaceNum(time):
    map = {
        '01-': '1-',
        '02-': '2-',
        '03-': '3-',
        '04-': '4-',
        '05-': '5-',
        '06-': '6-',
        '07-': '7-',
        '08-': '8-',
        '09-': '9-',
    }
    for i in re.findall('0\d-',time):
        time = re.sub(i, map[i], time)
    return time

#4.5K -> 4500.0
def replaceUnit(input):
    if re.search('([\d.]*)[Kk]',input):
        return float(re.findall('([\d.]*)[Kk]',input)[0])*1000

    return input

# r = re.search('\d{10,}',1550000000021)
# print(r)