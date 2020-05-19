#!/usr/bin/env python
# coding: utf-8

# # Destination Cleaning-Matching Approach
# ##### 14th May 2020 - DFO Tiger Team

# In[1]:


import editdistance # using this external package, finds the levenshtein distance
import pandas as pd
from IPython.display import Image


# ## With reference to the standard list of port names (World Port Index), we find the best word match for each AIS destination.
# #### Each AIS Destination name is compared to the port names in WPI.

# calculate confidence degree between two words
def conf_deg(dest,port):
    try:
        ratio = editdistance.eval(dest,port)/len(dest)
    except ZeroDivisionError:
        ratio = 2
    return (1 - (ratio))


# Destination fix algorithm 


def dest_fix(ports,dest):
    deg = []
    for p in ports:
        #print(conf_deg(dest,p))
        deg.append(conf_deg(dest,p))
    # get highest conf degree 
    max_deg = max(deg)
    print('degree= ' + str(max_deg))
    i = deg.index(max_deg)

    if (max_deg == 1):
        dest = dest # keep as is, perfect match
    if (max_deg<1 and max_deg >0.25):
        dest = ports[i] # switch port name to standard one
    if (max_deg<0.25 and max_deg >0):
        dest = 'other'
    if (max_deg < 0):
        dest = 'undefined'
    
    print(" \n - Matched port name: " + dest)
    return dest


# ## Small Example

# In[8]:


# assume this is World Port Index
ports = ['vancouver','havana','victoria','panama']
# destination name 
dest = 'fancouver'


# In[9]:


dest_fix(ports,dest)


# In[10]:


# if name of destination is = 'Toronto'
dest = 'Toronto'
dest_fix(ports,dest)


# In[11]:


# might consider increasing the threshold value a little 


# ### What's Left to apply this on the AIS Destination Field?
# #### 1. Cleaning data from any special characters, spaces or numbers *( done but not shown here )* 
# #### 2. Access to the World Port Index Reference List/database

# In[12]:


# wpi-raw.csv : world port index
wpi = pd.read_csv("wpi-raw.csv")
wpi['portName'] = wpi['portName'].fillna('')
wpi


# In[34]:


dest_fix(wpi['portName'],'C@@@@@@@@AT')


# In[15]:


p = wpi['portName'].notnull() 
#type(p)
#p.where(p == False)
p


# In[35]:


static = pd.read_csv("CCG_AIS_Static_Data_2018-05-01.csv")


# In[42]:


static['Destination'] = static['Destination'].fillna('')


# In[49]:


static = static.drop_duplicates(["Region","Station_Location","AIS_Channel","AIS_Class","Message_Type","Repeat_Indicator","MMSI","IMO_number","Call_Sign","Vessel_Name","Type_of_Ship_and_Cargo","Dimension_to_Bow_meters","Dimension_to_Stern_meters","Dimension_to_Port_meters","Dimension_to_Starboard_meters","Vessel_Length_meters","Vessel_Width_meters","Draught_decimeters","Destination"], keep="last")

# In[75]:


static['New Destination'] = static.apply(lambda x: dest_fix(wpi['portName'],x['Destination']), axis=1)


# In[55]:


static


# In[76]:


dest_correct = static[['Destination', 'New Destination']]


# In[77]:


dest_correct.to_csv("corrected_destination.csv",index=False)


# In[78]:


d = dest_correct[dest_correct['New Destination'] == 'undefined']


# In[81]:


d.shape[0] # number of records with undefined 


# In[82]:


o = dest_correct[dest_correct['New Destination'] == 'other']
o.shape[0] # number of records with other


# In[ ]:




