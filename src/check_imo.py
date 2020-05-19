#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd

static = pd.read_csv("CCG_AIS_Static_Data_2018-05-01.csv")
#dynamic = pd.read_csv("dynamic.csv")

data_s = static



data_s = data_s.drop_duplicates(["Region","Station_Location","AIS_Channel","AIS_Class","Message_Type","Repeat_Indicator","MMSI","IMO_number","Call_Sign","Vessel_Name","Type_of_Ship_and_Cargo","Dimension_to_Bow_meters","Dimension_to_Stern_meters","Dimension_to_Port_meters","Dimension_to_Starboard_meters","Vessel_Length_meters","Vessel_Width_meters","Draught_decimeters","Destination"], keep="last")



data_s['IMO_number'] = data_s['IMO_number'].fillna(0)

data_s['IMO_number'] = data_s['IMO_number'].astype(int)



def getImoCheck(imo):
    """
    Check a given IMO number to make sure the check value is accurate and if the IMO is good. Accepts the 7-digit IMO number as an integer argument, and returs a boolean value where True indicates a good IMO.
    """
    # Set our return value.
    retVal = False
    
    # Running sum of the current digit times its position
    runningSum = 0
    
    # Multiplier for each position.
    multiplier = 0
        
    # This is used to create a value we can manipulate
    imo = str(imo)
    if len(imo) is not 7:
        return retVal
    
    for i in range(1, 7):
        # Compute our multiplier since range() can't go from 7 to 1.
        multiplier = (i - 8) * -1
        
        # Add the current digit times the multiplier for it to the sum.
        runningSum += int(imo[i-1]) * multiplier
        

    # Get the last digit of the running sum..
    imoCheck = runningSum % 10
    print(runningSum)
    
    # Get the last digit of the IMO, and check it against the computed IMO check value.
    #print(imo %10)
    if (int(imo) % 10) == imoCheck:
        retVal = True
    
    return retVal


imo = 9553402

getImoCheck(imo)


data_s["IMO_status"] = data_s.apply(lambda x: getImoCheck(x['IMO_number']), axis=1)


data_s.to_csv("static_verified_imo.csv",index=False)


