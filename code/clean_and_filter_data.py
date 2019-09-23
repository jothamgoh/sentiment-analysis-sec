
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import nltk
import os
from pathlib2 import Path
import re
import shutil


# In[2]:


def get_project_dir():
    try:
        project_dir = Path.cwd() / '/' / 'My Drive' / 'Jotham' / 'Personal Docs' / 'ML for finance' / 'SEC Sentiment Analysis' / 'sec-sentiment'
    except:
        project_dir = Path.cwd() / '/' / 'Volumes' / 'GoogleDrive' / 'My Drive' / 'Jotham' / 'Personal Docs' / 'ML for finance' / 'SEC Sentiment Analysis' / 'sec-sentiment'
    return project_dir


# In[3]:


def clean_filing(input_filename, filing_type, output_filename):
    """
    Cleans a 10-K or 10-Q filing. All arguments take strings as input
    input_filename: name of the file to be cleaned
    filing_type: either 10-K or 10-Q
    outuput_filename: name of output file
    """
    
    # open file and get rid of all lines 
    with open (input_filename, 'r') as f:
        data = f.read().replace('\n', ' ')
    
    # get text in between the appropriate 10-K tags
    search_10k = re.search("(?s)(?m)<TYPE>{}.*?(</TEXT>)".format(filing_type), data)
    try:
        data_processed = search_10k.group(0)
    
        # delete formatting text used to identify 10-K section as its not relevant
        data_processed = re.sub(pattern="((?i)<TYPE>).*?(?=<)", repl='', string=data_processed)

        # Five more formatting tags are deleted
        data_processed = re.sub(pattern="((?i)<SEQUENCE>).*?(?=<)", repl='', string=data_processed)
        data_processed = re.sub(pattern="((?i)<FILENAME>).*?(?=<)", repl='', string=data_processed)
        data_processed = re.sub(pattern="((?i)<DESCRIPTION>).*?(?=<)", repl='', string=data_processed)
        data_processed = re.sub(pattern="(?s)(?i)<head>.*?</head>", repl='', string=data_processed)
        data_processed = re.sub(pattern="(?s)(?i)<(table).*?(</table>)", repl='', string=data_processed)

        # Tags each section of the financial statement with prefix '°Item' for future analysis
        data_processed = re.sub(pattern="(?s)(?i)(?m)> +Item|>Item|^Item", repl=">Â°Item", string=data_processed, count=0)

        # Removes all HTML tags
        data_processed = re.sub(pattern="(?s)<.*?>", repl=" ", string=data_processed, count=0)

        # Replaces all Unicode strings
        data_processed = re.sub(pattern="&(.{2,6});", repl=" ", string=data_processed, count=0)

        # Replaces multiple spaces with a single space
        data_processed = re.sub(pattern="(?s) +", repl=" ", string=data_processed, count=0)

        with open(output_filename, 'w') as output:
            output.write(data_processed)
            
    except BaseException as e:
        print('{} could not be cleaned. Exception: {}'.format(input_filename, e))
        pass


# In[4]:


def clean_all_filings():
    """Clean all filings in sec-filings directory"""
    
    project_dir = get_project_dir()
    company_list = os.listdir(os.path.join(project_dir, 'sec-filings-downloaded'))  

    for company in company_list:
        company_dir = os.path.join(project_dir, 'sec-filings-downloaded', company)
        os.chdir(company_dir) # abs path to each company directory
        
        print('***Cleaning: {}***'.format(company))
        for file in os.listdir():  # iterate through all files in the respective company directory
            
            # cleaning files
            if file.startswith('cleaned'): 
                continue
            
            if file.endswith('10-K'): filing_type = '10-K'
            else: filing_type = '10-Q'
            
            if file.endswith('10-K') or file.endswith('10-Q'):
                clean_filing(input_filename=file, filing_type=filing_type, output_filename='cleaned_' + str(file))
                print('{} filing cleaned'.format(file))


# In[5]:


def rename_10_Q_filings():
    """Rename 10Q filigns to include the quarter of the filing in the filing name"""
    
    project_dir = get_project_dir()
    company_list = os.listdir(os.path.join(project_dir, 'sec-filings-downloaded'))  
    
    for company in company_list:
        company_dir = os.path.join(project_dir, 'sec-filings-downloaded', company)
        os.chdir(company_dir)
        
        print('***{}***'.format(company))
        for file in os.listdir():
            if file.startswith('cleaned_filings') or file.startswith('cleaned_Q'): 
                continue
                
            if file.startswith('cleaned') and file.endswith('10-Q'):
                get_date = file[8:18]
                get_year = file[8:12]
                get_month = int(file[13:15])

                if get_month >= 1 and get_month <= 5:
                    filing_quarter = 'Q1'
                elif get_month >= 6 and get_month <= 8:
                    filing_quarter = 'Q2'
                else:
                    filing_quarter = 'Q3'

                os.rename(file, ('cleaned_'+str(filing_quarter)+'_'+str(get_date)+'_'+'10-Q'))
                print('{} renamed'.format(file))
            
            else:
                print('{} not renamed'.format(file))


# In[6]:


def move_10k_10q_to_folder():
    """Move filings to the appropriate folders in each company directory"""
    
    company_list = os.listdir(os.path.join(get_project_dir(), 'sec-filings-downloaded'))  

    for company in company_list:    
        # make directory of cleaned files
        cleaned_files_dir = os.path.join(get_project_dir(), 'sec-filings-downloaded', company, 'cleaned_filings')
        if not os.path.exists(cleaned_files_dir): os.makedirs(cleaned_files_dir)
        
        company_dir = os.path.join(get_project_dir(), 'sec-filings-downloaded', company)
        os.chdir(company_dir) # abs path to each company directory    
        
        print('***{}***'.format(company))
        for file in os.listdir():
            if file.startswith('cleaned_filings'): continue  # cleaned_filings directory
            if file.startswith('clean') and (file.endswith('10-Q') or file.endswith('10-K')):
                try:
                    shutil.move(os.path.join(company_dir, file), os.path.join(cleaned_files_dir, file))
                    print('{} moved to cleaned files folder'.format(file))
                except Exception as e:
                    os.remove(os.path.join(cleaned_files_dir, file))
                    shutil.move(os.path.join(company_dir, file), os.path.join(cleaned_files_dir, file))
                    print('{} moved to cleaned files folder'.format(file))


# In[16]:


clean_all_filings()


# In[17]:


rename_10_Q_filings()


# In[18]:


move_10k_10q_to_folder()

