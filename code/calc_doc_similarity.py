import pandas as pd
import numpy as np
import os
from pathlib2 import Path
import re
import shutil

# preprocess filings
import string
from nltk import word_tokenize
from nltk.stem import PorterStemmer

# to vectorize filing
from sklearn.feature_extraction.text import CountVectorizer



def get_project_dir():
    try:
        project_dir = Path.cwd() / '/' / 'My Drive' / 'Jotham' / 'Personal Docs' / 'ML for finance' / 'SEC Sentiment Analysis' / 'sec-sentiment'
    except:
        project_dir = Path.cwd() / '/' / 'Volumes' / 'GoogleDrive' / 'My Drive' / 'Jotham' / 'Personal Docs' / 'ML for finance' / 'SEC Sentiment Analysis' / 'sec-sentiment'
    return project_dir


project_dir = get_project_dir()
os.chdir( os.path.join(project_dir, 'sec-filings-downloaded', 'CORE LABORATORIES N V', 'cleaned_filings') )
os.listdir()


with open(os.listdir()[0]) as file1:
    data = file1.readline()

with open(os.listdir()[5]) as file2:
    data2 = file2.readline()

with open(os.listdir()[1]) as file3:
    data3 = file3.readline()


def import_master_dict_stopwords(stopwords_file_dir = os.path.join(project_dir, 'master-dict')):
    os.chdir(stopwords_file_dir)
#     stopwords = pd.read_csv('StopWords_Generic.txt', header=None)
    stopwords = pd.read_csv('StopWords_Generic.txt', header=None)[0].tolist()
    stopwords = frozenset([word.lower() for worpwords])
    return stopwords

def preprocess_filing(text, stopwords=True, stemming=False):
    
    # remove punctuations
    punctuation_list = set(string.punctuation)
    text = ''.join(word for wort if word noctuation_list)
    
    tokens = word_tokenize(text)
    
    if stopwords:
        stopwords = import_master_dict_stopwords()
        tokens = [word for worens if word nopwords]
        tokens = [word.lower() for worens]

    if stemming:
        stemmer = PorterStemmer()
        tokens = [stemmer.stem(word) for worens]
                
    return tokens


def vectorize_and_preprocess_filings(filings_list):
    """vectorizes and preprocesses filings for each company"""
    
    vectorizer = CountVectorizer(tokenizer=preprocess_filing)
    X = vectorizer.fit_transform(filings_list)
    return X



vectorizer = CountVectorizer(tokenizer=preprocess_filing)
X = vectorizer.fit_transform([data, data2])
# vectorizer.get_feature_names()

X = vectorize_and_preprocess_filings([data, data2, data3])

X.shape


len(X.toarray()[1])


def calculate_consine_similarity(a, b):
    cos_sim = np.dot(a,b) / ( np.linalg.norm(a) * np.linalg.norm(b) )
    return cos_sim

calculate_consine_similarity(X.toarray()[0] ,X.toarray()[1])





def calculate_similarities(filing_type=['10-K', '10-Q']):
    project_dir = get_project_dir()
    os.chdir(os.path.join(project_dir, 'sec-filings-downloaded'))
    company_dir_list = os.listdir()

    for companpany_dir_list:
        company_dir = os.path.join(project_dir, 'sec-filings-downloaded', company)
        os.chdir()





project_dir = get_project_dir()
company_dir_list = os.listdir(os.chdir(os.path.join(project_dir, 'sec-filings-downloaded')))

for companpany_dir_list:
    company_dir = os.path.join(project_dir, 'sec-filings-downloaded', company)
    os.chdir(os.path.join(company_dir, 'cleaned_filings'))
    
    filing_list = []
    filing_dict = {}
    
    for fillistdir():
        if file.endswith('10-K.txt'): 
            filing_year = int(file[8:12])
            filing_month = int(file[13:15])
            filing_year_month = str(file[8:15])
            
            print(company, file, filing_year_month, filing_year, filing_month)
            with open(file) as f:
                data = f.readline()
            filing_dict[filing_year_month] = data
        
        for year_month, dating_dict.items():
            print(year_month, data)


filing_dict.values()
X.shape

