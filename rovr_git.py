#!/usr/bin/env python
# coding: utf-8

import os
import pandas as pd
import numpy as np
import datetime
import requests
import json
from dateutil import tz

start_dt=(datetime.datetime.utcnow()+ datetime.timedelta(days=1)).strftime('%Y-%m-%d')

end_dt=(datetime.datetime.utcnow()+ datetime.timedelta(days=1)).strftime('%Y-%m-%d')

ts=datetime.datetime.utcnow().strftime("%m%d_%H%M")

dir='/app/bbb_test/'

col_names=['postcode_sector', 'sub_pc', 'store_from', 'store_to', 'lat','lon']
str_api=pd.read_csv(dir+'/input/str_post_lat_lon.csv',skiprows=1,names=col_names)
str_api.head()
str_api.columns

str_data=pd.DataFrame(str_api)

str_test=str_data.head(20)

strList = [] #empty list
for i, r in str_data.iterrows(): 
    mylist = [r.store_from, r.store_to, r.customer_lat, r.customer_lon]
    strList.append(mylist)

strList[0]

strList[0][3]


#store1 payload file
store_1=[0]*len(str_test)
for i in range(len(str_test)): 
    with open (dir+'/input/req.json','r') as r_data:
        store_1=json.load(r_data)                  
        store_1['payload']['startDate']=start_dt
        store_1['payload']['endDate']=end_dt
        store_1['payload']['deliveryStartPointExternalId']=strList[i][0]
        store_1['payload']['customerInfo']['customerAddress']['latitude']=strList[i][2]
        store_1['payload']['customerInfo']['customerAddress']['longitude']=strList[i][3]
        fn=str(strList[i][0])+'_'+str(ts)+'_'+str(strList[i][2])+'_'+str(strList[i][3])
    #with open(dir+'/input/request_file'+fn+'_s1.json', 'w') as p:
       #json.dump(store_1, p)        

#store 1 API calls

import requests
api_url = 'http://asda.rovr-api.prod.walmart.com/rovr-app/services/customer/slot/view'
headers = {'content-type': 'application/json' }

re1 = []
for i in range(len(str_test)):
    r1 = requests.post(api_url, json=store_1, headers = headers)
    #re.append({'store_id':store_1['payload']['deliveryStartPointExternalId']})
    re1.append(r1.json())
    a='_'+str(strList[i][0])+'_'+str(ts)+'_'+str(strList[i][2])+'_'+str(strList[i][3])
    with open(dir+'/output/res'+a+'_s1.json', 'w') as df:
        json.dump(re1, df)
    del re1[:] 

#####store 2 payload

store_2=[0]*len(str_test)
for i in range(len(str_test)): 
    with open (dir+'/input/req.json','r') as r_data:
        store_2=json.load(r_data)                  
        store_2['payload']['startDate']=start_dt
        store_2['payload']['endDate']=end_dt
        store_2['payload']['deliveryStartPointExternalId']=strList[i][1]
        store_2['payload']['customerInfo']['customerAddress']['latitude']=strList[i][2]
        store_2['payload']['customerInfo']['customerAddress']['longitude']=strList[i][3]
        fn=str(strList[i][1])+'_'+str(ts)+'_'+str(strList[i][2])+'_'+str(strList[i][3])
    #with open(dir+'/input/request_file'+fn+'_s2.json', 'w') as p:
       #json.dump(store_2, p)        

#store 2 API calls

import requests
api_url = 'http://asda.rovr-api.prod.walmart.com/rovr-app/services/customer/slot/view'
headers = {'content-type': 'application/json' }

re2 = []
for i in range(len(str_test)):
    r2 = requests.post(api_url, json=store_2, headers = headers)
    #re.append({'store_id':store_2['payload']['deliveryStartPointExternalId']})
    re2.append(r2.json())
    a='_'+str(strList[i][1])+'_'+str(ts)+'_'+str(strList[i][2])+'_'+str(strList[i][3])
    with open(dir+'/output/res'+a+'_s2.json', 'w') as df:
        json.dump(re2, df)
    del re2[:] 
 ########################  
 ##test one output 
with open (dir+'/output/res_4850_1106_2345_53.112935_-3.044629_s2.json','r') as r_data:
        da=json.load(r_data)

da[0]['payload']['slotDays'][0]['slots'][0]['startDateTime']
da[0]['payload']['slotDays'][0]['slots'][0]['endDateTime']
da[0]['payload']['slotDays'][0]['slots'][0]['status']
dataa = []
for i in range(len(da)):
    for j in range(len(da[i]['payload']['slotDays'])):
        for k in range(len(da[i]['payload']['slotDays'][j]['slots'])):
            #printing data for the values in that interval(startDataTime, endDataTime, status)
            #print(da[i]['payload']['slotDays'][j]['slots'][k]['startDateTime'],",",da[i]['payload']['slotDays'][j]['slots'][k]['endDateTime'],",",da[i]['payload']['slotDays'][j]['slots'][k]['status'])
            dataa.append(da[i]['payload']['slotDays'][j]['slots'][k]['startDateTime']+","+da[i]['payload']['slotDays'][j]['slots'][k]['endDateTime']+","+da[i]['payload']['slotDays'][j]['slots'][k]['status'])
print(dataa)

with open('listfile.txt', 'w') as filehandle:
    filehandle.writelines("%s\n" % place for place in dataa)
df=pd.read_csv('listfile.txt')
df.columns=['startDateTime','endDateTime','status']

os.getcwd()
os.chdir('/Users/aaa/Documents/bbb/output')
os.listdir()
for i in os.listdir():
    print(i)
dir='/Users/aaa/Documents/bbb'
with open (dir+'/output/res_4850_1106_2345_53.112935_-3.044629_s2.json','r') as r_data:
        da=json.load(r_data)
print(json.dumps(da,sort_keys=False, indent=4))

da[0]['payload']['slotDays'][0]['slots'][0]['startDateTime']
da[0]['payload']['slotDays'][0]['slots'][0]['endDateTime']
da[0]['payload']['slotDays'][0]['slots'][0]['status']

file='res_4135_1106_2145_53.770617_-0.310399_s1.json'
#print (file.find('_42'))
#print(file.split('_'))
'''fs=file.split('_')
print(file.split('_')[1])

hm=fs[len(fs)-4].split('.')[0]
print(fs[1]+'_'+fs[2]+'_'+hm)

store_time=file.split('_')[1]+'_'+file.split('_')[2]
lat_lon=file.split('_')[4]+'_'+file.split('_')[5]
print(lat_lon)
f=store_time+'_'+lat_lon+'_'+fs[len(fs)-1].split('.')[0]
print(f)


for file in os.listdir():
    fs=file.split('_')
    f=fs[1]+'_'+fs[2]+'_'+fs[3]+'_'+fs[4]+'_'+fs[5]+'_'+fs[len(fs)-1].split('.')[0]
    print(f)'''

x='res_4157_1106_2330_53.596835_-2.341542_s2.json'
with open (x,'r') as re_data:
        dat=json.load(re_data) 
        for i in range(len(dat)):
            for j in range(len(dat[i]['payload']['slotDays'])):
                for k in range(len(dat[i]['payload']['slotDays'][j]['slots'])):
            #printing data for the values in that interval(startDataTime, endDataTime, status)
            #print(da[i]['payload']['slotDays'][j]['slots'][k]['startDateTime'],",",da[i]['payload']['slotDays'][j]['slots'][k]['endDateTime'],",",da[i]['payload']['slotDays'][j]['slots'][k]['status'])
                    dia.append(dat[i]['payload']['slotDays'][j]['slots'][k]['startDateTime']+","+dat[i]['payload']['slotDays'][j]['slots'][k]['endDateTime']+","+dat[i]['payload']['slotDays'][j]['slots'][k]['status'])
        print(dia)

dr='/Users/aaa/Documents/bbb/output/' 
dia = []
for x in os.listdir(dr):
    if x.endswith('.json'):
        fs=x.split('_')
        fs=x.split('_')
        f=fs[1]+','+fs[2]+','+fs[3]+','+fs[4]+','+fs[5]+','+fs[len(fs)-1].split('.')[0]
        with open (dr+x,'r') as re_data:
            dat=json.load(re_data) 
            for i in range(len(dat)):
                for j in range(len(dat[i]['payload']['slotDays'])):
                    for k in range(len(dat[i]['payload']['slotDays'][j]['slots'])):
            #printing data for the values in that interval(startDataTime, endDataTime, status)
            #print(da[i]['payload']['slotDays'][j]['slots'][k]['startDateTime'],",",da[i]['payload']['slotDays'][j]['slots'][k]['endDateTime'],",",da[i]['payload']['slotDays'][j]['slots'][k]['status'])
                        dia.append(dat[i]['payload']['slotDays'][j]['slots'][k]['startDateTime']+","
                                   +dat[i]['payload']['slotDays'][j]['slots'][k]['endDateTime']+","
                                   +dat[i]['payload']['slotDays'][j]['slots'][k]['status']+","+f)
print(dia[0])


with open('res_d.csv', 'w') as fi:
    fi.writelines("%s\n" % place for place in dia)
df=pd.read_csv('res_d.csv')
df.columns=['startDateTime','endDateTime','status','store','req_dt','req_ts','lat','lon','store_type']
 
df.head()
df_s1 = df[df.store_type=='s1'] 
print(df_s1.shape)


df_s2 = df[df.store_type=='s2'] 
print(df_s2.shape)

res1=pd.DataFrame(pd.merge(df_s1,df_s2,on=['startDateTime','endDateTime','req_dt','req_ts','lat','lon']))

type(res1)

final=pd.DataFrame(pd.merge(res1,str_test,on=['store_1','store_2','lat','lon']))


res1.columns=['startDateTime','endDateTime','status_1','store_1','req_dt','req_ts','lat','lon','store_type_1','status_2','store_2','store_type_2']
d=res1[(res1['status_1']=="UNAVAILABLE") & (res1['status_2']=="UNAVAILABLE")]

result=res1[(res1['status_1']=="UNAVAILABLE") & (res1['status_2']=="AVAILABLE")]

result.to_csv('s1unavailabe_s2availabe.csv', encoding='utf-8', index=False) 

result.dtypes

ffinal=pd.DataFrame(pd.merge(result,str_test,on=['store_1','store_2','lat','lon']))
final.shape
#df_4213.to_csv('str_4213_1.csv', encoding='utf-8', index=False)

n= int(10e6)



df_s1 = df[ (df.store_type=='s1')& (df.status=='UNAVAILABLE')]
print(df_s1.shape)



