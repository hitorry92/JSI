import math
import random
import requests
import pandas as pd



def randomString():
    chars = "0123456789ABCDEFGHIKLMNOPQRSTUVWXYZ"
    string_length = 10
    randomstring = ''
    for i in range(0, string_length):
        rnum = int(math.floor(random.random() * len(chars)))
        randomstring += chars[rnum : rnum+1]
    
    return randomstring

rands = randomString()
print(rands)

def getGugunList():
    url = 'https://www.starbucks.co.kr/store/getGugunList.do'
    gugunlist = [[]]
    for i in range(1, 18): #17개의 시군구를 담음
        datas = {
            'sido_cd': str(i).zfill(2) # f'{i:02d}'
        }
        response = requests.post(url, data=datas).json()

        for j in range(0, len(response['list'])):
            gugunlist[i-1].append(response['list'][j])

        gugunlist.append([])
    return gugunlist

def getStore(p_gugun_cd, p_sido_cd):
    randomStr = randomString()
    url = 'https://www.starbucks.co.kr/store/getStore.do?r=' + randomStr
    datas = {
        'P10': 0,
        'P20': 0,
        'P30': 0,
        'P40': 0,
        'P50': 0,
        'P60': 0,
        'P70': 0,
        'P80': 0,
        'P90': 0,
        'T01': 0,
        'T03': 0,
        'T05': 0,
        'T09': 0,
        'T10': 0,
        'T12': 0,
        'T21': 0,
        'T22': 0,
        'T27': 0,
        'T30': 0,
        'T36': 0,
        'T43': 0,
        'T48': 0,
        'all_store': 0,
        'iend': "100",
        'in_biz_cd': "",
        'in_biz_cds': 0,
        'in_distance': 0,
        'in_scodes': 0,
        'ins_lat': 37.0,
        'ins_lng': 126.0,
        'isError': True,
        'new_bool': 0,
        'p_gugun_cd': p_gugun_cd,
        'p_sido_cd': p_sido_cd,
        'rndCod': randomStr,
        'searchType': "C",
        'search_text': "",
        'set_date': "",
        'whcroad_yn': 0  
    }
    response = requests.post(url, data=datas).json()
    return response

Gugun = getGugunList()
Gugun

result = []
for i in range(0, len(Gugun)):
    for j in range(0, len(Gugun[i])):
        Store = getStore(Gugun[i][j]['gugun_cd'], Gugun[i][j]['gugun_cd'][0:2])
        Store = Store['list']
        for k in range(0, len(Store)):
            savedata = {
                'sido_name': Store[k]['sido_name'],
                'gugun_name': Store[k]['gugun_name'],
                'sido_code': Store[k]['sido_code'],
                'gugun_code': Store[k]['gugun_code'],
                'addr': Store[k]['addr'],
                'doro_address': Store[k]['doro_address'],
                's_code': Store[k]['s_code'],
                's_name': Store[k]['s_name'],
                'open_dt': Store[k]['open_dt'],
                'lat': Store[k]['lat'],
                'lot': Store[k]['lot'],
                's_biz_code': Store[k]['s_biz_code'],
                'store_area_code': Store[k]['store_area_code'],
                'out_distance': Store[k]['out_distance'],
                'defaultimage': 'http://image.istarbucks.co.kr'+Store[k]['defaultimage']
            }
            result.append(savedata)

selectdata = pd.DataFrame(result)

import pymysql
import mariadb
# from sqlalchemy import create_engine

conn = mariadb.connect(
        user="root",
        password="1234",
        host="127.0.0.1",
        port=3306,
        database="work"
)

cursor = conn.cursor()

# query = "CREATE TABLE starbucks (sido_name text, gugun_name text, sido_code text, gugun_code text, addr text,\
#        doro_address text, s_code varchar(10), s_name text, open_dt text, lat text, lot text, s_biz_code text,\
#        store_area_code text, out_distance text, defaultimage text, primary key (s_code))"
# cursor.execute(query)
# conn.commit()

# for idx, row in selectdata.iterrows():
#     query_insert = """INSERT INTO starbucks \
#                    (sido_name, gugun_name, sido_code, gugun_code, addr, doro_address, s_code, s_name, open_dt, lat, lot, s_biz_code, store_area_code, out_distance, defaultimage)\
#                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
#     values = (
#         row['sido_name'],
#         row['gugun_name'],
#         row['sido_code'],
#         row['gugun_code'],
#         row['addr'],
#         row['doro_address'],
#         row['s_code'],
#         row['s_name'],
#         row['open_dt'],
#         row['lat'],
#         row['lot'],
#         row['s_biz_code'],
#         row['store_area_code'],
#         row['out_distance'],
#         row['defaultimage']
#     )
#     cursor.execute(query_insert, values)
# conn.commit()

for idx, row in selectdata.iterrows():
    query_update = """INSERT IGNORE INTO starbucks \
                   (sido_name, gugun_name, sido_code, gugun_code, addr, doro_address, s_code, s_name, open_dt, lat, lot, s_biz_code, store_area_code, out_distance, defaultimage)\
                   VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
    values = (
        row['sido_name'],
        row['gugun_name'],
        row['sido_code'],
        row['gugun_code'],
        row['addr'],
        row['doro_address'],
        row['s_code'],
        row['s_name'],
        row['open_dt'],
        row['lat'],
        row['lot'],
        row['s_biz_code'],
        row['store_area_code'],
        row['out_distance'],
        row['defaultimage']
    )
    cursor.execute(query_update, values)
conn.commit()
conn.close()
