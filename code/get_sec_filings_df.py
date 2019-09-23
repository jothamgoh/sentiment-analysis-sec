
# coding: utf-8

# In[1]:


import edgar
import os
from pathlib2 import Path
import pandas as pd
import numpy as np
import requests
from tqdm import tqdm


# ## generate df with all companies and URLs

# In[2]:


def get_project_dir():
    try:
        project_dir = Path.cwd() / '/' / 'My Drive' / 'Jotham' / 'Personal Docs' / 'ML for finance' / 'SEC Sentiment Analysis' / 'sec-sentiment'
    except:
        project_dir = Path.cwd() / '/' / 'Volumes' / 'GoogleDrive' / 'My Drive' / 'Jotham' / 'Personal Docs' / 'ML for finance' / 'SEC Sentiment Analysis' / 'sec-sentiment'
    return project_dir


# In[3]:


os.chdir(os.path.join(get_project_dir(), 'sec-filings-index'))


# In[4]:


# filing_year = 2013   # choose year to get filings from
# edgar.download_index(os.getcwd(), filing_year)


# In[5]:


# Get list of all DFs 
table_list = []

for i in os.listdir():
    if i.endswith('.tsv'):
        table_list.append(pd.read_csv(i, sep='|', header=None, encoding='latin-1', parse_dates=[3], dtype={0: int}))


# In[6]:


# append all dfs into a single df

df = pd.DataFrame(columns=[0,1,2,3,4,5])   # downloaded file has 6 columns

for i in range(len(table_list)):
        df = pd.concat([df, table_list[i]], ignore_index=True, axis=0)

df.columns= ['cik', 'company_name', 'filing_type', 'filing_date', 'url', 'url2']


# ## Check if dataframe correctly generated

# In[7]:


count_list = []
for i in range(len(table_list)):
    count_list.append(len(table_list[i]))

if df.shape[0] == sum(count_list):
    print('df tallies with individual files. Total rows = {}'.format(df.shape[0]))
else:
    print('ERROR. df does not tally!!')


# ## download data

# In[8]:


def download_filings(cik_num_list, from_date='2014-01-01'):
    """Function to filter the appropriate filings and download them in the folder"""
    
    # filter df with company CIK,filing type (10-K and 10-Q) and date  
    df_filtered = df [(df['cik'].isin(cik_num_list)) & 
                      ((df['filing_type']=='10-K') | (df['filing_type'] == '10-Q')) & 
                      (df['filing_date'] > from_date)]
    
    company_names = df_filtered['company_name'].unique().tolist()
    
    # check if folders for each company already exists    
    sec_filings_dir = os.path.join(get_project_dir(), 'sec-filings-downloaded')  # dir to download SEC filingsa
    os.chdir(sec_filings_dir)

    for company in company_names:
        company_dir = os.path.join(sec_filings_dir, company)

        if not os.path.exists(company_dir):
            os.makedirs(company_dir)
            print('\n created dir: {}'.format(company))
        else:
            print('\n{} directory exists'.format(company))
            
        os.chdir(company_dir)
        
        # create company specific df to iterate over    
        df_filtered_co = df_filtered[df_filtered['company_name'] == company]  # get df with the company only
        df_filtered_co['filing_date'] = df_filtered_co['filing_date'].astype(str)   # convert to 'object' to name file

        for i in range(len(df_filtered_co)):
            url_prefix = 'https://www.sec.gov/Archives/'
            row = df_filtered_co.iloc[i,:]
            url = url_prefix + row['url']
            response = requests.get(url, stream=True)
            
            filing_name = row['filing_date'] + str('_') + row['filing_type']
            if os.path.isfile(filing_name):
                print('{} file already exists'.format(filing_name))
            else:
                print('Downloading: {}'.format(filing_name))
                with open('{}'.format(filing_name), 'wb') as handle:
                    for data in tqdm(response.iter_content()):
                        handle.write(data)
                        
    


# In[11]:


download_filings([1000045, 1000229, 1000230])

