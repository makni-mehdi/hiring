import pandas as pd
from pandas import isna
import csv


# ----------------------------- Useful Functions -----------------------------
  
"""
This function allows to create a python dictionary where the keys are words and the respective value is a set of 
all companies whose name contains that word.
The key idea is that when we want to match a company from data_A we would only look at companies in data_B who share at least 
a word in the company name as A. This turned out to filter the data a lot and makes run very fast.
The last part here where we set a value of a key to set() is if the word has too many companies associated to it.
Such words include: 'la', 'le', 'de', 'et', 'les', etc. Those words are not useful for our filtering.
"""
def group_companies_by_word(data_name_decomposition):
    word_group = {}
    for i in range(len(data_name_decomposition)):
        for word in data_name_decomposition[i]:
            if word not in word_group:
                word_group[word] = {i}
            else:
                word_group[word].add(i) 
    for key in word_group:
        if len(word_group[key]) > len(data_name_decomposition)/200:
            word_group[key] = set()
    return word_group

"""
The score is going to be a ratio of score obtained from common features divided by the maximum score possible for a company in data_A
This is useful to match companies who have only name as a feature for example
"""
def overall_score(data_A, i):
    return 5  *  (not isna(data_A['Name Decomposition'][i])) + \
           10 *  (not isna(data_A['Phone Number'][i])) + \
           6  *  (not isna(data_A['Website'][i])) + \
                 (not isna(data_A['Country'][i])) + \
                 (not isna(data_A['Postal Code'][i]))
    

"""
Function for website data processing. In both datasets many companies that are a match
have different websites simply because of absence/presence of "www." or "https://" etc.
"""
def suffix_website(website):
    if isna(website): return website
    website = str(website)
    if website.startswith('https://'):
        website = website[8:]
    elif website.startswith('http://'):
        website = website[7:]
    if website.startswith('www.'):
        website = website[4:]
    return website

def suffix_phone(phone):
    if isna(phone): return phone
    phone = str(phone)
    phone = phone.replace(' ','').replace('-','')[-8:]
    return phone

def decompose_name(name):
    if isna(name): return name
    name_decompose = set(name.lower().replace('(', ' ').replace(')', ' ').split())
    return name_decompose

# ----------------------------- Scoring Functions -----------------------------

# Compute number of words that appear in both companies divided by length of longest name
def name_score(set_A, set_B):
    return len(set_A.intersection(set_B))/max(len(set_A),len(set_B))*3

# After having the suffix phone, we compute if it is equal or not
def phone_score(A, B):
    if isna(A) or isna(B): return 0
    return 10 if A == B else 0

# After having the suffix website, we compute if it is equal or not
def website_score(A, B):
    if isna(A) or isna(B): return 0
    return 6 if A == B else 0

# We check for location and penalize if it is different
def location_score(postal_A, country_A, postal_B, country_B):
    res = 0   
    if not isna(postal_A) and not isna(postal_B) and postal_A != postal_B:
        res -= 2
    if not isna(country_A) and not isna(country_B) and country_A != country_B:
        res -= 3
    return res        


def not_isna(value):
    return not isna(value)

def filtering(csv_file, header):
    data = pd.read_csv(csv_file, header = None)
    columns_keep = []
    for column in data:
        if data[column].apply(not_isna).sum() > 5:
            columns_keep.append(column)
    data = data[columns_keep]
    data.columns = header
    return data

"""
Suffix Phone: only consider the last 8 digits because some companies that are a match
have different phone numbers simply because of "+33 Phone Number" or "0 Phone Number"
Name Decomposition: A column that contains the words of the company name but in a set. 
We will use the Name Decomposition to make the algorithm much faster.
"""
def processing(data):
    data['Suffix Phone'] = data['Phone Number'].apply(suffix_phone)
    data['Suffix Website'] = data['Website']
    data['Suffix Website'] = data['Suffix Website'].apply(suffix_website)
    data['Name Decomposition'] = data['Company Name'].apply(decompose_name)
    data['Country'] = data['Country'].str.lower()
    return data


# ----------------------------- Matching Algorithm -----------------------------

def greedy_matching(data_A, data_B, graph_possbilities):
    with open('matches.csv', 'a') as matches_file:
        writer = csv.writer(matches_file)
        header = ['id A', 'id B', 'Name Decomposition A', 'Name Decomposition B', 'Suffix Phone A', 'Suffix Phone B', 'Suffix Website A', 'Suffix Website B', 'Matching Score']
        writer.writerows([header])
        for i in range(len(data_A)):
            possible_matches = set()
            for word in data_A['Name Decomposition'][i]:
                if word in graph_possbilities:
                    possible_matches = possible_matches.union(graph_possbilities[word])
            highest_score = overall_score(data_A, i)
            for j in possible_matches:
                score = name_score(data_A['Name Decomposition'][i], data_B['Name Decomposition'][j]) \
                                   + website_score(data_A['Suffix Website'][i], data_B['Suffix Website'][j]) \
                                   + phone_score(data_A['Suffix Phone'][i], data_B['Suffix Phone'][j]) \
                                   + location_score(data_A['Country'][i], data_A['Postal Code'][i], data_B['Country'][j], data_B['Postal Code'][j])
                ratio = score/highest_score
                if  ratio > 0.3:
                    writer.writerows([[data_A['id'][i], data_B['id'][j], data_A['Name Decomposition'][i], data_B['Name Decomposition'][j], data_A['Suffix Phone'][i], data_B['Suffix Phone'][j], data_A['Suffix Website'][i], data_B['Suffix Website'][j], min(ratio, 1)]])
