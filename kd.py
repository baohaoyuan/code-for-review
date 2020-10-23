#!/usr/bin/env python
# coding: utf-8

# In[7]:


import pandas as pd
import numpy as np
from scipy.stats import chi2_contingency
import os
import sqlite3 


# In[13]:


pip install xlrd


# In[8]:


os.getcwd()


# In[12]:


os.chdir('/Users/vn060tw/Downloads')


# In[14]:


df = pd.read_excel('sample_data.xlsx', sheet_name='Sheet1')


# In[15]:



df


# In[25]:


grp_df=df.groupby('home_loc').agg({'emplid':['nunique']})


# In[22]:


grp_df


# In[ ]:


#df.groupby('home_loc')['emplid'].count()


# In[26]:


emp_df=df.groupby('emplid').agg({'metric1_numer':['sum']})


# In[27]:


emp_df


# In[ ]:


df.groupby(['emplid','session','user_id'])['user_id'].count()


# In[29]:


df.iloc[:]


# In[30]:


emp = pd.read_excel('emplid_metrics.xlsx', sheet_name='emplid')


# In[31]:


emp


# In[33]:


emplid_df=emp.groupby('emplid').agg({'tota_metrics':['sum'],
                                   'total_denom':['sum']})


# In[ ]:


emplid_pct=


# In[35]:



c = emplid_df.to_csv('emplid_metrics', index = True) 


# In[ ]:





# In[34]:


emplid_df


# In[37]:


df['metric1'] = df['metric1_numer']/df['metric1_denom']


# In[39]:


df['metric2'] = df['metric2_numer']/df['metric2_denom']
df['metric3'] = df['metric3_numer']/df['metric3_denom']
df['metric4'] = df['metric4_numer']/df['metric4_denom']
df['metric5'] = df['metric5_numer']/df['metric5_denom']
df['metric6'] = df['metric6_numer']/df['metric6_denom']
df['metric7'] = df['metric7_numer']/df['metric7_denom']


# In[44]:


df2=df.iloc[:,[0,1,2,3,4,5,-7,-6,-5,-4,-3,-2,-1]]


# In[45]:


df2


# In[49]:


c = df2.to_csv('emplid_metrics_pct.csv', index = True) 


# In[50]:


df2_pct=df2.groupby('emplid').agg({'metric1':['mean'],
                                   'metric2':['mean'],
                                   'metric3':['mean'],
                                   'metric4':['mean'],
                                   'metric5':['mean'],
                                   'metric6':['mean'],
                                   'metric7':['mean']                             
                                })


# In[51]:


df2_pct


# In[52]:


df2_pct.to_csv('emplid_metrics_pct_2.csv', index = True) 


# In[ ]:





# In[ ]:




