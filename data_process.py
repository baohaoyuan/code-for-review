

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
    file_name = mycsv[0:-4]

    df['Pre'] = 1
    df['Agree/Pre'] = df['PPAgree']/df['PreVisits']
    df['Post/Agree'] = df['PostStorefront']/df['PPAgree']
    df['Orders/Post'] = df['ThankYou(Hit)']/df['PostStorefront']
    cols = ['VerificationSuccessRate','ConversionRate','Pre','Agree/Pre','Post/Agree','Orders/Post']
    df[cols] = df[cols].round(2)    
    df = df.transpose()
    
    if os.path.exists(file_name+'_out.csv'):
        os.remove(file_name+'_out.csv')
    df.to_csv(file_name+'_out.csv', encoding='utf-8', sep=',')
    '''
    try:
        df.to_csv(file_name+'_out.csv', encoding='utf-8', sep=',')
    except FileExistsError:
        df.to_csv(file_name+'_out2.csv', encoding='utf-8', sep=',')
    '''

if __name__ == "__main__":
    for i in inFile:
        data_prep(i, col)