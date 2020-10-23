#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os
import pandas as pd
import numpy as np
import datetime
import requests
import json
from dateutil import tz


# In[3]:


now=datetime.datetime.utcnow().strftime('%Y-%m-%d')


# In[4]:


start_dt=(datetime.datetime.utcnow()+ datetime.timedelta(days=1)).strftime('%Y-%m-%d')


# In[5]:


end_dt=(datetime.datetime.utcnow()+ datetime.timedelta(days=1)).strftime('%Y-%m-%d')


# In[6]:


start_dt


# In[7]:


end_dt


# In[10]:


ts=datetime.datetime.utcnow().strftime("%m%d_%H%M")


# In[11]:


ts


# In[ ]:





# In[12]:


dir=os.getcwd()


# In[13]:


print(os.getcwd())


# In[14]:


os.chdir('/Users/vn060tw/Documents/crossover')


# In[15]:


os.listdir(os.getcwd())


# In[16]:


col_names=['postcode_sector', 'sub_pc', 'store_1', 'store_2', 'lat','lon','row_cnt']


# In[17]:


dir='/Users/vn060tw/Documents/crossover'


# In[18]:


str_api=pd.read_csv(dir+'/input/str_post_lat_lon.csv',skiprows=1,names=col_names)


# In[19]:


str_api.head()


# In[20]:


str_api.columns


# In[21]:


str_data=pd.DataFrame(str_api)


# In[274]:


for index, row in str_api.head(n=2).iterrows():
     print(index, row)


# In[22]:


for column in str_data[['store_1', 'store_2','lat','lon']]:
   # Select column contents by column name using [] operator
   columnSeriesObj = str_data[column]
   print('Colunm Name : ', column)
   print('Column Contents : ', columnSeriesObj.values)


# In[23]:


str_test=str_data.head(20)

str_test

strList = [] #empty list
for i, r in str_test.iterrows(): 
    mylist = [r.store_1, r.store_2, r.lat, r.lon]
    strList.append(mylist)

strList[0]


# In[25]:


strList[1][2]


# In[26]:


strList


# In[284]:


str_test


# In[27]:


strList[1][3]


# In[29]:


strList[0][3]


# In[28]:


strList[0][3]
'''with open (dir+'/req.json','r') as r1_data:
    da=json.load(r1_data)'''              


# In[30]:


da['payload']['customerInfo']['customerAddress']['latitude']
da['payload']['customerInfo']['customerAddress']['longitude']


# In[343]:


d=[0] * len(str_test)


# In[31]:


print(str(strList[1][0])+'_'+str(ts)+'_'+str(strList[1][2])+'_'+str(strList[1][3]))


# In[419]:


str(strList[0][1])+'_'+str(ts)+'_'+str(strList[0][2])+'_'+str(strList[0][3])


# In[420]:


str(strList[1][1])+'_'+str(ts)+'_'+str(strList[1][2])+'_'+str(strList[1][3])


# In[400]:


del d2


# In[427]:


strList


# In[413]:


strList[1][0]


# In[373]:


strList[1][0]


# In[32]:


#store payload file
d=[0]*len(str_test)
for j in range(len(str_test)): 
    with open (dir+'/input/req.json','r') as r_data:
        d[j]=json.load(r_data)                  
        d[j]['payload']['startDate']=start_dt
        d[j]['payload']['endDate']=end_dt
        d[j]['payload']['deliveryStartPointExternalId']=strList[j][1]
        d[j]['payload']['customerInfo']['customerAddress']['latitude']=strList[j][2]
        d[j]['payload']['customerInfo']['customerAddress']['longitude']=strList[j][3]
        fn='_'+str(strList[j][1])+'_'+str(strList[j][2])+'_'+str(strList[j][3])
    with open(dir+'/request_file'+fn+'.json', 'w') as p:
       json.dump(d[j], p)        


# In[36]:


d[0]


# In[38]:


import requests
api_url = 'http://asda.rovr-api.prod.walmart.com/rovr-app/services/customer/slot/view'
headers = {'content-type': 'application/json' }


# '''ra = []
# for i in range(len(str_test)):
#     r = requests.post(api_url, json=d[i], headers = headers)
#     #ra.append({'store_id':d[i]['payload']['deliveryStartPointExternalId']})   
#     ra.append(r.json())
#     with open("/Users/vn060tw/Documents/crossover/request_result"+str(d[i]['payload']['deliveryStartPointExternalId'])+".json", "w") as df:
#         json.dump(ra, df)'''

# In[39]:


#Working
re = []
for i in range(len(str_test)):
    r = requests.post(api_url, json=d[i], headers = headers)
    #re.append({'store_id':d[i]['payload']['deliveryStartPointExternalId']})
    re.append(r.json())
    a='_'+str(strList[i][1])+'_'+str(ts)+'_'+str(strList[i][2])+'_'+str(strList[i][3])
    with open(dir+'/res'+a+'.json', 'w') as df:
        json.dump(re, df)
    re.clear()
    


# In[40]:


res = []
for i in range(len(str_test)):
    a='_'+str(strList[i][1])+'_'+str(ts)+'_'+str(strList[i][2])+'_'+str(strList[i][3])
    fn=str(strList[i][0])+'_'+str(strList[i][2])+'_'+str(strList[i][3])
    print(a+' '+fn)
    res.clear()


# import os
# import datetime
# import requests
# import json
# 
# dir='/app/crossover_test'
# r_dir=dir+'/results'
# 
# # set start and end date to UTC time
# now=datetime.datetime.utcnow().strftime('%Y-%m-%d')
# 
# 
# start_dt=(datetime.datetime.utcnow()+ datetime.timedelta(days=1)).strftime('%Y-%m-%d')
# 
# 
# end_dt=(datetime.datetime.utcnow()+ datetime.timedelta(days=2)).strftime('%Y-%m-%d')
# 
# 
# ts=datetime.datetime.utcnow().strftime("%m%d_%H%M")
# 
# # list of test store ids
# 
# str_test=['4766','4213']
# 
# # read the payload file (req.json)
# 
# d=[0] * len(str_test)
# for j in range(len(str_test)): 
#     with open (dir+'/req.json','r') as r_data:
#         d[j]=json.load(r_data)                  
#         d[j]['payload']['startDate']=start_dt
#         d[j]['payload']['endDate']=end_dt
#         d[j]['payload']['deliveryStartPointExternalId']=str_test[j]        
#  #   with open(dir+'/request_fill'+str(j)+'.json', 'w') as p:
#  #      json.dump(d[j], p)
# # API call
# import requests
# api_url = 'http://asda.rovr-api.prod.walmart.com/rovr-app/services/customer/slot/view'
# headers = {'content-type': 'application/json' }
# 
# 
# #write the output
# re = []
# for i in range(len(str_test)):
#     r = requests.post(api_url, json=d[i], headers = headers)
#     #re.append({'store_id':d[i]['payload']['deliveryStartPointExternalId']})
#     re.append(r.json())
#     a='_'+str(str_test[i])+'_'+str(ts)
#     with open(r_dir+'/res'+a+'.json', 'w') as df:
#         json.dump(re, df)
#     del re[:] #python2
# 
# re = []
# for i in range(len(str_test)):
#     r = requests.post(api_url, json=d[i], headers = headers)
#     #re.append({'store_id':d[i]['payload']['deliveryStartPointExternalId']})
#     re.append(r.json())
#     a='_'+str(str_test[i])+'_'+str(ts)
#     with open(dir+'/res'+a+'.json', 'w') as df:
#         json.dump(re, df)
#     re.clear() #python3

# In[6]:


os.getcwd()

os.chdir('/Users/vn060tw/Documents/crossover')


# In[9]:


dir='/Users/vn060tw/Documents/crossover'


# In[22]:


with open (dir+'/output/res_4850_1106_2345_53.112935_-3.044629_s2.json','r') as r_data:
        da=json.load(r_data)


# In[442]:


print(json.dumps(da,sort_keys=False, indent=4))


# In[23]:


da[0]['payload']


# In[24]:


da[0]['payload']['slotDays'][0]['slots']


# In[25]:


da[0]['payload']['slotDays'][0]['slots'][0]['startDateTime']


# In[26]:


da[0]['payload']['slotDays'][0]['slots'][0]['endDateTime']


# In[27]:


da[0]['payload']['slotDays'][0]['slots'][0]['status']


# In[30]:


os.chdir('/Users/vn060tw/Documents/crossover/output')


# In[31]:


os.listdir()


# In[32]:


for i in os.listdir('/Users/vn060tw/Documents/crossover/output'):
    print(i)


# In[20]:


file='res_4135_1106_2145_53.770617_-0.310399_s1.json'
#print (file.find('_42'))
#print(file.split('_'))
fs=file.split('_')
print(file.split('_')[1]+file.split('_')[2])


# In[21]:


fs


# In[15]:


store_time=file.split('_')[1]+'_'+file.split('_')[2]


# In[16]:


lat_lon=file.split('_')[4]+'_'+file.split('_')[5]
print(lat_lon)


# In[17]:


f=store_time+'_'+lat_lon+'_'+fs[len(fs)-1].split('.')[0]
print(f)


# In[33]:


for file in os.listdir():
    fs=file.split('_')
    f=fs[1]+'_'+fs[2]+'_'+fs[3]+'_'+fs[4]+'_'+fs[5]+'_'+fs[len(fs)-1].split('.')[0]
    print(f)


# In[291]:


dr='/Users/vn060tw/Documents/crossover/output/' 
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
    


# In[292]:


dia[0:100]


# In[293]:


with open('res_d.csv', 'w') as fi:
    fi.writelines("%s\n" % place for place in dia)
df=pd.read_csv('res_d.csv')
df.columns=['startDateTime','endDateTime','status','store','req_dt','req_ts','lat','lon','store_type']
    


# In[294]:


df.head()


# In[295]:


df.shape


# In[296]:


df_s1 = df[df.store_type=='s1']
print(df_s1.shape)

#df[(df.salary >= 30000) & (df.year == 2017)]


# In[297]:


df_s2 = df[df.store_type=='s2'] 
print(df_s2.shape)


# In[39]:


#df_4213.to_csv('str_4213_1.csv', encoding='utf-8', index=False)


# In[298]:


res1=pd.DataFrame(pd.merge(df_s1,df_s2,on=['startDateTime','endDateTime','req_dt','req_ts','lat','lon']))


# In[299]:


type(res1)


# In[300]:


res1.dtypes


# In[301]:


res1.head()


# In[302]:


res1.columns=['startDateTime','endDateTime','status_1','store_1','req_dt','req_ts','lat','lon',
              'store_type_1','status_2','store_2','store_type_2']


# In[303]:


res1.head()


# In[304]:


all_re=pd.DataFrame(pd.merge(res1,str_test,on=['store_1','store_2','lat','lon']))


# In[256]:


all_re.to_csv('all.csv', encoding='utf-8', index=False)


# In[ ]:


df.dtypes


# In[255]:


all_re.shape


# In[220]:


final.head(20)


# In[ ]:





# In[192]:


d=res1[(res1['status_1']=="UNAVAILABLE") & (res1['status_2']=="UNAVAILABLE")]


# In[193]:


d.shape


# In[70]:


d.head()


# In[194]:


result=res1[(res1['status_1']=="UNAVAILABLE") & (res1['status_2']=="AVAILABLE")]


# In[195]:


result.shape


# In[196]:


result.to_csv('s1unavailabe_s2availabe.csv', encoding='utf-8', index=False)


# In[215]:


all_re=pd.DataFrame(pd.merge(res1,str_test,on=['store_1','store_2','lat','lon']))


# In[216]:


all_re.to_csv('all.csv', encoding='utf-8', index=False)


# In[217]:


all_re.shape


# In[204]:


str_test


# In[205]:


result


# In[168]:


result.dtypes


# In[210]:


result.lon.head()


# In[211]:


str_test.lat.head()


# In[212]:


final=pd.DataFrame(pd.merge(result,str_test,on=['store_1','store_2','lat','lon']))


# In[213]:


final.head()


# In[208]:


final.shape


# In[214]:


final.to_csv('final.csv', encoding='utf-8', index=False)

