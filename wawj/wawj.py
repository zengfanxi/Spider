# -*- coding:utf-8 -*-
import requests
import time
import json
import pandas as pd
from bs4 import BeautifulSoup
import re
import os
import random
from tqdm import tqdm
from fake_useragent import UserAgent
import warnings
warnings.filterwarnings('ignore')

# 配置方法详见：https://github.com/Python3WebSpider/ProxyPool
#设置代理，每次随机从redis中拿
PROXY_POOL_URL = 'http://localhost:5555/random'
def get_proxy():
    try:
        response = requests.get(PROXY_POOL_URL)
        if response.status_code == 200:
            return response.text
    except ConnectionError:
        return None

proxies = {"http": str(get_proxy()),
           "https": str(get_proxy())
          }

# 初始化两个空列表用以存储数据
data_1 = list()
data_2 = list()
# 初始化要爬取的url框架
url = 'https://m.5i5j.com/hz/zufang/index-n'

# 设置header头
ua = UserAgent()

headers = {
            'accept': 'application/json, text/javascript, */*; q=0.01',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9',
            'cache-control': 'no-cache',
            'cookie': '',
            'pragma': 'no-cache',
            'referer': 'https://m.5i5j.com/hz/zufang/index',
            'user-agent': ua.firefox,
            'x-requested-with': 'XMLHttpRequest',
        }

# 循环开始

for i in tqdm(range(1,400)):
    url_ = url + str(i)
#     r = requests.get(url_, headers= headers)
#     info = r.json()
#     house = info['houses']
#     time.sleep(2)
    r = requests.get(url_, headers= headers, proxies=proxies)
    if r.status_code != 301:
        proxies = {"http": str(get_proxy()),
           "https": str(get_proxy())
          }
        r = requests.get(url_, headers= headers, proxies=proxies)
        if r.status_code == 301:
            info = r.json()
            house = info['houses']
        else:
            print(u'更换的代理失败，请重试！')
            break
    else:
        info = r.json()
        house = info['houses']
        time.sleep(random.randint(1,3))

    if house:
        for j in range(len(house)):
            price = house[j]['_source']['price'] # 价格
            updatetimestr = house[j]['_source']['updatetimestr'] # 更新时间
            pre_price = house[j]['_source']['pre_price'] # 价格字段2（可能多余）
            livingroom = house[j]['_source']['livingroom'] # 卧室数量--不一定对（可能多余）
            buildingfloor = house[j]['_source']['buildingfloor'] # 当前楼层--不一定对（可能多余）
            heading = house[j]['_source']['heading'] # 朝向
            housestate = house[j]['_source']['housestate'] # 上架状态
            floorPositionStr = house[j]['_source']['floorPositionStr'] # 楼层特点
            qyname = house[j]['_source']['qyname'] # 区域名称
            buildage_cn = house[j]['_source']['buildage_cn'] # 建造年份
            housetitle = house[j]['_source']['housetitle'] # 房子标题
            housesid = house[j]['_source']['housesid'] # 房源id
            subwaylines = house[j]['_source']['subwaylines'] # 地铁线路
            subwaystations = house[j]['_source']['subwaystations'] # 地铁线路1
            decoratelevel = house[j]['_source']['decoratelevel'] # 装修级别
            toilet = house[j]['_source']['toilet'] # 卫生间数量
            jtcx = house[j]['_source']['jtcx'] # 交通出行特点
            zbpt = house[j]['_source']['zbpt'] # 周边配套特点
            pay = house[j]['_source']['pay'] # 租赁方式（押一付三等）
            buildyear = house[j]['_source']['buildyear'] # 建造年份
            contacttime = house[j]['_source']['contacttime'] # 看房时间
            tagwall = house[j]['_source']['tagwall'] # 标签墙
            toilet_cn = house[j]['_source']['toilet_cn'] # 卫生间数量2
            houseallfloor = house[j]['_source']['houseallfloor'] # 房源总楼层数
            buildage = house[j]['_source']['buildage'] # 构造年份2（int）
            memo2 = house[j]['_source']['memo2'] # 备忘录2
            decoratelevelid = house[j]['_source']['decoratelevelid'] # 装修级别（int）
            floorPositionId = house[j]['_source']['floorPositionId'] # 楼层（int）
            fyld = house[j]['_source']['fyld'] # 房源亮点
            bedroom_cn = house[j]['_source']['bedroom_cn'] # 卧室数（str）
            sqname = house[j]['_source']['sqname'] # 区域名称2
            rentmodename = house[j]['_source']['rentmodename'] # 租赁类型
            memo1 = house[j]['_source']['memo1'] # 标签2
            memo5 = house[j]['_source']['memo5'] # 标签3
            memo3 = house[j]['_source']['memo3'] # 标签4
            bedroom = house[j]['_source']['bedroom'] # 卧室数量
            communityname = house[j]['_source']['communityname'] # 小区名称
            hxjs = house[j]['_source']['hxjs'] # 户型介绍
            xqxx = house[j]['_source']['xqxx'] # 小区信息
            area = house[j]['_source']['area'] # 面积
            bookin_time = house[j]['_source']['bookin_time'] # bookin_time
            floorType = house[j]['_source']['floorType'] # 楼层特点
            livingroom_cn = house[j]['_source']['livingroom_cn'] # 厅数
            memo4 = house[j]['_source']['memo4'] # 标签5
            location = house[j]['_source']['location'] # 地理位置经纬度
            data_1 = [price,updatetimestr,pre_price,livingroom,buildingfloor,
                      heading,housestate,floorPositionStr,qyname,buildage_cn,
                      housetitle,housesid,subwaylines,subwaystations,decoratelevel,
                      toilet,jtcx,zbpt,pay,buildyear,contacttime,tagwall,toilet_cn,
                      houseallfloor,buildage,memo2,decoratelevelid,floorPositionId,
                      fyld,bedroom_cn,sqname,rentmodename,memo1,memo5,memo3,bedroom,
                      communityname,hxjs,xqxx,area,bookin_time,floorType,livingroom_cn,
                      memo4,location]
            data_2.append(data_1)
    else:
        print('第%d次请求中被阻断!' %(i))
        break

# 将爬取的数据整理到df
# 知识点：list-->array-->dataframe
import numpy as np
columns = ['price','updatetimestr','pre_price','livingroom','buildingfloor',
           'heading','housestate','floorPositionStr','qyname','buildage_cn',
           'housetitle','housesid','subwaylines','subwaystations','decoratelevel',
           'toilet','jtcx','zbpt','pay','buildyear','contacttime','tagwall','toilet_cn',
           'houseallfloor','buildage','memo2','decoratelevelid','floorPositionId',
           'fyld','bedroom_cn','sqname','rentmodename','memo1','memo5','memo3','bedroom',
           'communityname','hxjs','xqxx','area','bookin_time','floorType','livingroom_cn',
           'memo4','location']
wawj_ = pd.DataFrame(np.array(data_2), columns = columns)
# 数据导出备份
wawj_.to_csv('.../data.csv',index = False,encoding = 'utf-8',header = True)
