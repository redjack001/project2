# -*- coding: utf-8 -*-
"""
Created on Thu Aug 27 11:10:59 2020

It is in AML1 to generate new set of synthesized data.
This syntheization would be different... as it will start from building by account number.

@author: legomate
"""
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

import pandas as pd
import numpy as np
import random
import datetime
from datetime import timedelta
import time
import csv

pd.options.display.float_format = '{:.2f}'.format

#df = pd.DataFrame(trax, columns=['Trx Date', 'Account No', 'Currency', 'Amount', 'Functional Amount', 'Withdrawal or Deposit', 'Trx ID', 'Product', 'Product Number', 'Attr 1', 'Attr 2', 'Attr 3'])

#parameters
clients = 150
start_date = datetime.date(2015, 1, 1)
end_date = datetime.date(2020, 8, 17)
ac_open_date = datetime.date(2014, 5, 2)
ac_open_enddate = datetime.date(2020, 7, 31)
arbitrary_number = 9000
m = 200 #max number of trx per clients
bias = 2.0
num = 250


handler_list = ['0001', '0002', '0003', '0004', '0005', '0006', '0007', '0008', '0009', '0010', '0011', '0012', '0013', '0014', '0015', '0016', '0017', '0018']
product_list = ['bond', 'stock', 'options', 'futures', 'cash']

HKD_USD = 'HKD_USD.csv'
USD_CNY = 'USD_CNY.csv'


def ac_number_generator(clients, ac_open_date, ac_open_enddate):
    ac = random.sample(range(1, 60000), clients)

    ac_list = []

    for i in range(0,len(ac)):
        ac[i] = 1000000000+ac[i]
        x = random.choice(['A','B','C'])
        ac[i] = str(ac[i])
        ac[i] = x + ac[i][1::]
        ac_list.append(ac[i])
        
    #print(ac_list)
    l = len(ac_list)
    
    randomlist = []
    
    for i in range(0,5):
        n = random.randint(0,l)
        randomlist.append(n)
    
    #print(l)
    
    r_datelist = []
    
    for j in range (0,l):
        time_between_dates = ac_open_enddate - ac_open_date
        days_between_dates = time_between_dates.days
        random_number_of_days = random.randrange(days_between_dates)
        random_date = start_date + timedelta(days=random_number_of_days) 
        
        if random_date.weekday() >= 5:
            random_date = random_date - timedelta(random.randint(0,4)) 
        
        r_datelist.append(random_date)
    
    #print (r_datelist)
       
    df = pd.DataFrame(list(zip(ac_list, r_datelist)), columns=['ac_no','ac_open_date'])
    #print (df)
    
    df.to_csv('acct_list.csv', index=False)
    return df


def random_dates(start_date, end_date, m):
    
    r_datelist = []
    
    for j in range (0,m):
        time_between_dates = end_date - start_date
        days_between_dates = time_between_dates.days
        
        if days_between_dates > 2:
            random_number_of_days = random.randrange(days_between_dates)
            random_date = start_date + timedelta(days=random_number_of_days) 
        else:
            random_number_of_days = random.randrange(2)
            random_date = start_date + timedelta(days=random_number_of_days)          
        
        if random_date.weekday() >= 5:
            random_date = random_date - timedelta(random.randint(0,4)) 
        
        r_datelist.append(random_date)    
    
    #print (r_datelist)
    
    
    return r_datelist


def curr_random():
    n = np.random.gamma(1, 2.0) 
    if n > 2:
        p = 2
    else:
        p = int(n)
    curr_list = ['USD','HKD','CNY']
    gr3 = curr_list[p]
    return gr3


def g_random(arbitrary_number):
    n = np.random.gamma(1, 2.0) * 5
    gr = round(n,2)*arbitrary_number
    return gr

def g_random3(bias, r_list):
    n = np.random.gamma(1, bias) 
    l = len(r_list)
    
    if int(n) > l-1:
        p = l-1
    else:
        p = int(n)

    gr3 = r_list[p]
    return gr3


#function to open CSV files
def open_csv(file):
    
    data = pd.read_csv(file)
    data['Date'] = pd.to_datetime(data['Date'])
    
    #print (data.head)
    #print (data.dtypes)
    return data

#function to open forex CSV & convert to dataframe
def forex_csv(f):
    
    nfile = 'HKD_'+f+'.csv'
    df_f1 = open_csv(nfile)
    
    df_f = df_f1[['Date', 'Adj Close']].copy()

    return df_f

#create data by account number
def create_data(i, m, bias, r_list, arbitrary_number, end_date):
    #['Trx Date', 'Account No', 'Currency', 'Amount', 'Functional Amount', 'Withdrawal or Deposit', 'Trx ID', 'Product', 'Product Number', 'Attr 1', 'Attr 2', 'Attr 3'])
    
    #m is the length of the list
    
    #read account list:
    client = pd.read_csv('acct_list.csv')    
    
    ac_number = client['ac_no'].iloc[i] #get an account number
    #print(ac_number)
    
    ac_open_date = client['ac_open_date'].iloc[i] #get open date
    #print(ac_open_date)

    
    n = random.randint(0, m) #get number of trax for this client
    
    ac_list = [ac_number]*m   
    ac_date_list = [ac_open_date]*m
    curr_list = []
    trx_list = []
    pdt_list = []
    
    #put currency, trx amount & product type in
    for i in range(0,n):
        a = curr_random();
        curr_list.append(a)
    
    for z in range(0,n):
        zz = g_random(arbitrary_number)
        trx_list.append(zz)
        
    for v in range(0,n):
        vv = g_random3(bias, r_list)
        pdt_list.append(vv)

    #for d in range(0,n):
    ac_open_date = datetime.datetime.strptime(ac_open_date, '%d/%m/%Y').date()
    r_datelist = random_dates(ac_open_date, end_date, n)
   

    df = pd.DataFrame(list(zip(ac_list, ac_date_list, curr_list, r_datelist, trx_list, pdt_list)), columns=['AC_no','AC_open_date', 'Curr', 'Trx_Date', 'Trx_Amt', 'Product'])
    df['AC_open_date'] = pd.to_datetime(df['AC_open_date'])
    df['Trx_Date'] = pd.to_datetime(df['Trx_Date'])
    df['Date'] = df['Trx_Date'].copy()
    
    #filter the df
    
    df2 = df.groupby('Curr')['Trx_Amt'].nunique()
    d2_list = list(df2.index) #list of unique values of the dataframe
        
    list_df = []
    
    #match forex list with the currency
    for i in d2_list:
        #it's to filter non-HKD transactions
        if not i == 'HKD':
            df_tmp = df[df['Curr']== i]           
            df_f = forex_csv(i) #pick the right currency file
            df_tmp2 = pd.merge(df_tmp, df_f, on ='Date', how ='inner') 
            print('df_tmp2')
            print(type(df_tmp2))
            list_df.append(df_tmp2)
            
        else:
            df_tmp_hkd = df[df['Curr']==i] #it should be HKD
            df_tmp_hkd['Adj Close'] = 1
            df_tmp_hkd['Adj Close'].astype(float)
            print('df_tmp_hkd')
            print(type(df_tmp_hkd))
            list_df.append(df_tmp_hkd)           
    

    if len(list_df) > 0:    
        df_final = pd.concat(list_df, ignore_index=True)
        print ('df_final:')
        print (df_final.head)
    
        df_final = df_final.rename(columns={"Adj Close": "Exchange Rate"})
        df_final['Functional_Amt'] = df_final['Trx_Amt']*df_final['Exchange Rate']
        df_final1 = df_final.sort_values('Trx_Date', ascending=True).copy()
        df_final2 = df_final1.reset_index(drop=True)
        df_final2 = df_final.drop(['Date'], axis=1)
        
        return df_final2 
        
    else:
        pass

   

#ac_list = ac_number_generator(clients, ac_open_date, ac_open_enddate)
#random_dates(start_date, end_date, 5)

#open_csv(HKD_USD)

#df_final = create_data(0, 100, bias, product_list, 20000, end_date)
#print(df_final.head)


def create_all(bias, num, product_list, end_date):

    client = pd.read_csv('acct_list.csv')    
    #print(client.shape)
    print(client.shape[0])

    num_ac = client.shape[0]

    pd_ac_list = []
    
    i = 0

    for zzz in range(0,num_ac):
        df_final = create_data(zzz, num, bias, product_list, 12000, end_date)
        pd_ac_list.append(df_final)
        print(i)
        i = i+1
        
    
    df_all = pd.concat(pd_ac_list, ignore_index=True)

    return df_all


df_xx = create_all(bias, num, product_list, end_date)
print(df_xx.head)

df_xx.to_csv('df_xx.csv', index=False, header=True)

