# -*- coding: utf-8 -*-
"""
Created on Tue Aug  3 13:46:21 2021

@author: Prasad
"""

import pandas as pd
import numpy as np
import json
from pandas import json_normalize
data=[
{
"date": "2021-04-30",
"product_type": "EquityEuropeanOption",
"book": "FIA_Derivatives",
"trade_count": 16974
},
{
"date": "2021-04-30",
"product_type": "EquityEuropeanOption",
"book": "FIA_Derivatives123",
"trade_count": 2833
}
]
op={
"filters": [
{
"book": 
["FIA_Derivatives"],
"op": "IN"
},
{
"product_type": "EquityEuropeanOption",
"op": "EQ"
}
],
 "orderBy": [
{
"trade_count": "desc"
}
],
"pagination": {
"size": 200,
"offset": 0
}
}
def apply_criteria(data,op):
    #create DataFrame from JSON data
    data_df = pd.DataFrame(data)
    
    #in operations find out all filters,oderby and pagination
    filterby=[]
    orderby=[]
    pagination=[]
    #search for filters
    for each in op["filters"]:
        if(type(each)==dict):
            flag=0
            for key in each:
                if key.lower()!="op":
                    if(type(each[key])==list):
                        for every in each[key]:
                            flag+=1
                            filterby.append([key,every])
                    else:
                        flag+=1
                        filterby.append([key,each[key]])
                else:
                    for i in reversed(range(len(filterby)-flag,len(filterby))):
                        filterby[i].append(each[key])  
        else:
            filterby.append([each,op["filters"][each]])
    #search for oderby
    for each in op["orderBy"]:
        if(type(each)==dict):
            for key in each:
                if(type(each[key])==list):
                    for every in each[key]:
                        orderby.append([key,every])
                else:
                    orderby.append([key,each[key]])
        else:
            orderby.append([each,op["orderBy"][each]])
    #search for pagination
    for each in op["pagination"]:
        pagination.append([each,op["pagination"][each]])
    
    #Now apply each filter one by one using pandas methods        
    for each in filterby:
        if each[2].lower()=='eq':
            data_df= data_df[data_df[each[0]].eq(each[1])]
        if each[2].lower()=='ne':
            data_df= data_df[data_df[each[0]].ne(each[1])]
        if each[2].lower()=='le':
            data_df= data_df[data_df[each[0]].le(each[1])]
        if each[2].lower()=='lt':
            data_df= data_df[data_df[each[0]].lt(each[1])]
        if each[2].lower()=='ge':
            data_df= data_df[data_df[each[0]].ge(each[1])]
        if each[2].lower()=='gt':
            data_df= data_df[data_df[each[0]].gt(each[1])]
        if each[2].lower()=='in':
            data_df= data_df[data_df[each[0]].isin([each[1]])]
        if each[2].lower()=='nin':
            data_df= data_df[~data_df[each[0]].isin(each[1])]
    #Now sort the values using pandas method sort_values
    for each in orderby:
        flag=True
        if each[1].lower()=='desc':
            flag=False
        data_df.sort_values(by=[each[0]],ascending=flag)
    dict_df=data_df.to_dict('records')
    #return the output with matching criteria
    return [{k:v for k, v in i.items()} for i in dict_df]
d= apply_criteria(data,op)
print(d)