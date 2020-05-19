#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd 
pd.options.mode.chained_assignment = None  # default='warn
pd.options.display.max_columns = None
import numpy as np


# In[2]:


static = pd.read_csv("CCG_AIS_Static_Data_2018-05-01.csv)


# In[3]:


static = static.drop_duplicates(["Station_Location","MMSI","IMO_number","Destination"], keep="last")


# In[4]:


del static['year']
del static['month']
del static['day']


# In[5]:


del static['hour']
del static['minute']
del static['second']
del static['TimeZone']


# In[6]:


del static['Repeat_Indicator']
del static['AIS_Channel']
del static['AIS_Class']


# In[7]:


static = static.drop_duplicates(subset='MMSI', keep='first')


# In[8]:


del static['Region']
del static['Station_Location']


# In[9]:


del static['Message_Type']


# In[10]:


static


# In[11]:


dynamic = pd.read_csv("CCG_AIS_Dynamic_Data_2018-05-01.csv")


# In[12]:


del dynamic['Message_Type']


# In[13]:


dynamic = dynamic.fillna(0)


# In[13]:


dynamic['MMSI'] = dynamic['MMSI'].astype(np.int64)


# In[14]:


dynamic


# In[14]:


l = pd.Series(list(set(static['MMSI']) & set(dynamic['MMSI'])))


# In[15]:


m1 = pd.merge(static,dynamic, on='MMSI', how='inner')
m1


# In[19]:


merged = m1[m1['MMSI']==316014014]
merged


# In[17]:


df3['MMSI'].unique()


# In[16]:


m1.to_csv("static_dynamic_combined.csv",index=False)


# In[19]:


# create first and last positions


# In[20]:


origin_pos = df3.drop_duplicates(subset='MMSI', keep='first')


# In[21]:


origin_pos


# In[24]:


end_pos = df3.drop_duplicates(subset='MMSI', keep='last')


# In[25]:


end_pos


# In[27]:


col_list = ['MMSI','Longitude_decimal_degrees','Latitude_decimal_degrees' ]
origin_pos = origin_pos[col_list]
end_pos = end_pos[col_list]


# In[34]:


origin_pos = origin_pos.rename(columns={"Longitude_decimal_degrees": "long_org", "Latitude_decimal_degrees": "lat_org"})
end_pos = end_pos.rename(columns={"Longitude_decimal_degrees": "long_end", "Latitude_decimal_degrees": "lat_end"})


# In[35]:


orig_end = pd.merge(origin_pos,end_pos,on='MMSI')


# In[43]:


orig_end.head(60)


# In[44]:


orig_end.to_csv("orig_end_pos.csv",index=False)


# In[37]:


merg = pd.merge(df3,orig_end,on='MMSI')


# In[40]:


merg.head(60)


# In[39]:


merg.to_csv("dynamic_static_orig_end_pos.csv",index=False)


# In[ ]:




