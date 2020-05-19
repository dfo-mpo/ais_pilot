#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd


# In[2]:


static = pd.read_csv("CCG_AIS_Static_Data_2018-05-01.csv")


# In[3]:


cs_countries = pd.read_csv("CallSignSeriesRanges-1cc49d48-935c-4514-9ba2-3aabef92c7aa.csv")

# In[5]:


cs_countries[cs_countries['Series'].str.contains("VGdd")].shape[0]

# In[20]:


static = static.drop_duplicates(["Region","Station_Location","AIS_Channel","AIS_Class","Message_Type","Repeat_Indicator","MMSI","IMO_number","Call_Sign","Vessel_Name","Type_of_Ship_and_Cargo","Dimension_to_Bow_meters","Dimension_to_Stern_meters","Dimension_to_Port_meters","Dimension_to_Starboard_meters","Vessel_Length_meters","Vessel_Width_meters","Draught_decimeters","Destination"], keep="last")


# In[54]:


def identify_country(cs_countries,cs):
    cs = cs[0:2]
    if cs.isalnum():
        match = cs_countries[(cs_countries['Series'].str[0:2]).str.match(str(cs))]
        if match.shape[0] != 0:
            return match["Allocated to"].iloc[0]
        else:
            return 'undefined'
    return 'undefined'


# In[55]:


static['country'] = static.apply(lambda x: identify_country(cs_countries, str(x['Call_Sign'])), axis=1)


# In[53]:


identify_country(cs_countries,'Z3Z')



