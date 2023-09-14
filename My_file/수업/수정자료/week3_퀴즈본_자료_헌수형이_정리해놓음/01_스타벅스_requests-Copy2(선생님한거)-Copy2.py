#!/usr/bin/env python
# coding: utf-8

# ### [requests] 스타벅스 매장 위치 데이터 크롤링하기
# - https://syudal.tistory.com/entry/Crawling-%EC%8A%A4%ED%83%80%EB%B2%85%EC%8A%A4-%EB%A7%A4%EC%9E%A5-%EC%9C%84%EC%B9%98-%EB%8D%B0%EC%9D%B4%ED%84%B0-%ED%81%AC%EB%A1%A4%EB%A7%81%ED%95%98%EA%B8%B0

# In[1]:


import math
import random
import requests
import pandas as pd


# In[2]:


chars = "0123456789ABCDEFGHIKLMNOPQRSTUVWXYZ";
string_length = 10;
randomstring = '';
for i in range(0, string_length):
    rnum = int(math.floor(random.random() * len(chars)));
    randomstring += chars[rnum : rnum+1];
randomstring


# In[3]:


def randomString():
    chars = "0123456789ABCDEFGHIKLMNOPQRSTUVWXYZ";
    string_length = 10;
    randomstring = '';
    for i in range(0, string_length):
        rnum = int(math.floor(random.random() * len(chars)));
        randomstring += chars[rnum : rnum+1];
    
    return randomstring


# In[4]:


url = 'https://www.starbucks.co.kr/store/getGugunList.do'
gugunlist = [[]]

for i in range(1, 18):
    datas = {
                'sido_cd': str(i).zfill(2)
            }
    response = requests.post(url, data=datas).json()


# In[5]:


url = 'https://www.starbucks.co.kr/store/getGugunList.do'
gugunlist = [[]]
for i in range(1, 18): #17개의 시군구를 담음
    datas = {
        'sido_cd': str(i).zfill(2)
    }
    response = requests.post(url, data=datas).json()

    for j in range(0, len(response['list'])):
        gugunlist[i-1].append(response['list'][j])

    gugunlist.append([])


# In[6]:


gugunlist[0]


# In[7]:


def getGugunList():
    url = 'https://www.starbucks.co.kr/store/getGugunList.do'
    gugunlist = [[]]
    for i in range(1, 18): #17개의 시군구를 담음
        datas = {
            'sido_cd': str(i).zfill(2)
        }
        response = requests.post(url, data=datas).json()

        for j in range(0, len(response['list'])):
            gugunlist[i-1].append(response['list'][j])

        gugunlist.append([])
    return gugunlist


# In[8]:


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
    return response;


# In[9]:


Gugun = getGugunList()


# In[10]:


Gugun


# In[11]:


result = []


# In[12]:


#for i in range(0, 1):
#    for j in range(0, 1):
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


# In[13]:


Store[0]


# In[14]:


selectdata = pd.DataFrame(result)


# In[15]:


selectdata#[selectdata['s_name']=='역삼이마트']['defaultimage'].values


# In[ ]:





# In[16]:


# selectdata.to_csv("data/starbucks.csv")


# ## 방법2. csv_to_table(교재 10.5.1 참고)

# In[24]:


import pandas as pd
import pymysql


# In[25]:


# df=pd.read_csv('data/starbucks.csv')


# In[26]:


# df.info()


# In[27]:


# df['gugun_name'].isnull().sum()
df['gugun_name']


# In[28]:


# df[df['gugun_name'].isnull()]
df=df.fillna(value='')
df[df['sido_name']=='세종']
df


# In[29]:


for i in df.columns:
    i = df[f"{i}"]
    print(i)


# In[30]:


sido_name = df['sido_name']
gugun_name = df['gugun_name']
sido_code = df['sido_code']
gugun_code = df['gugun_code']
addr = df['addr']
doro_address = df['doro_address']
s_code = df['s_code']
s_name = df['s_name']
open_dt = df['open_dt']
lat = df['lat']
lot = df['lot']
s_biz_code = df['s_biz_code']
store_area_code = df['store_area_code']
out_distance = df['out_distance']
defaultimage = df['defaultimage']


# In[33]:


config = {
    'host' : '127.0.0.1',
    'user' : 'root',
    'password' : '1234',
    'database' : 'work',
    'port' : 3306,
    'charset' : 'utf8',
    'use_unicode' : True
}
conn = pymysql.connect(**config)
cursor = conn.cursor()
    
# table 조회
cursor.execute("show tables")
tables = cursor.fetchall()

sql = """create table star_tab(
    sido_name TEXT NULL,
    gugun_name TEXT NULL,
    s_name TEXT NULL,    
    doro_address TEXT NULL,
    open_dt BIGINT(20) NULL DEFAULT NULL
    )"""
cursor.execute(sql)


# In[34]:


for i in range(0,len(df)):
    sql = """insert into star_tab(sido_name, gugun_name, s_name, doro_address, open_dt)             values(%s, %s, %s, %s, %s)"""
    val = (df.iloc[i,0], df.iloc[i,1], df.iloc[i,2], df.iloc[i,3], df.iloc[i,4])
    cursor.execute(sql,val)
    conn.commit()


# In[35]:


cursor.execute("select * from star_tab")
rows = cursor.fetchall()
rows


# In[36]:


if rows : # 레코드 있는 경우 : 레코드 조회
    for row in rows :
        for i in range(0,len(rows[0])):
            print(f"{row[i]}", end = ' ')
        print(f"\n")
    print('전체 레코드 수 : ', len(rows))
    
else : # 레코드 없는 경우 : 레코드 추가
    len_df = len(df) 
    print(f"{len_df} : 레코드 추가")
    for i in range(0, len(df)):
        sql = """INSERT ignore INTO star_tab         (sido_code, gugun_code, s_code, doro_address, open_dt)         VALUES (%s, %s, %s, %s, %s)"""
        val = (df.iloc[i,0], df.iloc[i,1], df.iloc[i,2], df.iloc[i,3],
               df.iloc[i,4])
        cursor.execute(sql, val)
        conn.commit()


# In[37]:


cursor.close()
conn.close() 


# In[38]:


#     addr TEXT NULL,
#     s_code BIGINT(20) NULL DEFAULT NULL,
#     sido_code BIGINT(20) NULL DEFAULT NULL,
#     lat DOUBLE NULL DEFAULT NULL,
#     lot DOUBLE NULL DEFAULT NULL,
#     gugun_code BIGINT(20) NULL DEFAULT NULL,
#     s_biz_code BIGINT(20) NULL DEFAULT NULL,
#     store_area_code TEXT NULL,
#     out_distance DOUBLE NULL DEFAULT NULL,
#     defaultimage TEXT NULL


# In[40]:


# get_ipython().system('where python')


# In[ ]:




