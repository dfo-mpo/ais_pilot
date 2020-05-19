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


# delete unwanted fields

del static['year']
del static['month']
del static['day']
del static['hour']
del static['minute']
del static['second']
del static['TimeZone']
del static['Repeat_Indicator']
del static['AIS_Channel']
del static['AIS_Class']
del static['Region']
del static['Station_Location']
del static['Message_Type']

static = static.drop_duplicates(subset='MMSI', keep='first')

dynamic = pd.read_csv("CCG_AIS_Dynamic_Data_2018-05-01.csv")


# delete message type as that can conflict with static when merging
del dynamic['Message_Type']


dynamic = dynamic.fillna(0)
dynamic['MMSI'] = dynamic['MMSI'].astype(np.int64)

l = pd.Series(list(set(static['MMSI']) & set(dynamic['MMSI'])))


m1 = pd.merge(static,dynamic, on='MMSI', how='inner')



df3['MMSI'].unique()


m1.to_csv("static_dynamic_combined.csv",index=False)

# generating origin and end positions 

origin_pos = df3.drop_duplicates(subset='MMSI', keep='first')


end_pos = df3.drop_duplicates(subset='MMSI', keep='last')


col_list = ['MMSI','Longitude_decimal_degrees','Latitude_decimal_degrees' ]
origin_pos = origin_pos[col_list]
end_pos = end_pos[col_list]


origin_pos = origin_pos.rename(columns={"Longitude_decimal_degrees": "long_org", "Latitude_decimal_degrees": "lat_org"})
end_pos = end_pos.rename(columns={"Longitude_decimal_degrees": "long_end", "Latitude_decimal_degrees": "lat_end"})


orig_end = pd.merge(origin_pos,end_pos,on='MMSI')


orig_end.to_csv("dynamic_static_orig_end_pos.csv",index=False)


# In[ ]:




