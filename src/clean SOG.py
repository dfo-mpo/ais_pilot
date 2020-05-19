#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd

# In[4]:


dynamic = pd.read_csv("dynamic.csv")
dynamic = dynamic[dynamic.Speed_Over_Ground_SOG_knots != 0.0]

dynamic.to_csv("dynamic_clean_SOG.csv",index=False)