

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np 
import os

os.chdir('/Users/yuli/Downloads/')
cwd = os.getcwd()
print("Current working directory: {0}".format(os.getcwd()))


#print("hello"[:-3])

inFile = ['TY - Alipay Daily Summary.csv', 'TY - Alipay Daily Summary  - Desktop.csv',
          'TY - Alipay Daily Summary  - MOW.csv']
          
col = ['Day','PreVisits', 'PPAgree', 'PostStorefront','ThankYou(Hit)','VerificationSuccessRate',
                     'ConversionRate','PPDecline','PPAgreeOrDecline','AuthSuccessRate','MinutesPerPage']


def data_prep(mycsv, col):
    visit = pd.read_csv(mycsv, skiprows = 15,names = col, delimiter = ',',index_col=False)  
    df = visit.iloc[:,:7]
    df.iloc[[5,6]].round(2)
    df['Post/Agree'] = df['PostStorefront']/df['PPAgree']
    df['Agree/Pre'] = df['PPAgree']/df['PreVisits']
    df['Orders/Post'] = df['ThankYou(Hit)']/df['PostStorefront']
    df = df.transpose()
    if os.path.exists(mycsv[0:-4]+'_out.csv'):
        df.to_csv(mycsv[0:-4]+'_out2.csv', encoding='utf-8', sep=',')
    if os.path.exists(mycsv[0:-4]+'_out2.csv'):
        df.to_csv(mycsv[0:-4]+'_out2.csv', encoding='utf-8', sep=',')
    if os.path.exists(mycsv[0:-4]+'_out2.csv'):
        df.to_csv(mycsv[0:-4]+'_out3.csv', encoding='utf-8', sep=',')       
    '''
    try:
        df.to_csv(mycsv[0:-4]+'_out.csv', encoding='utf-8', sep=',')
    except FileExistsError:
        df.to_csv(mycsv[0:-4]+'_out2.csv', encoding='utf-8', sep=',')
    '''

for i in inFile:
    data_prep(i, col)