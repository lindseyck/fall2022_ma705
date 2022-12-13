# -*- coding: utf-8 -*-
"""
Created on Mon Dec  5 19:00:05 2022

@author: LKOSINSKI
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd

#Pull records for American paintings on view
amer_url = "https://collections.mfa.org/collections/314108/american-paintings/objects/images?filter=onview%3Atrue#filters"

headers = {"User-Agent" : "Chrome"}

amer_req = requests.get(amer_url, headers=headers)
amer_req.raise_for_status()

amer_req.text

amer = BeautifulSoup(amer_req.text, "html.parser")

#Extract titles
amer_title_list_dupe = []

for i in amer.find_all('a', class_=""):
    try:
        title = i.get('title')
        if title is not None and title != 'Sign in':
            amer_title_list_dupe.append(title)
    except:
        pass

#Remove title duplicates
amer_title_list = []

for item in amer_title_list_dupe:
    if item not in amer_title_list:
        amer_title_list.append(item)

#Extract artists
amer_artist_list = []

for i in amer.find_all('div', class_='primaryMaker text-wrap'):
    artist = i.text
    amer_artist_list.append(artist)

#Extract URLs
amer_url_list_dupe = []

for i in amer.select('a'):
    amer_url = 'https://collections.mfa.org' + i.get('href')
    if 'object' in amer_url:
        amer_url_list_dupe.append(amer_url)

#Remove URL duplicates
amer_url_list = []

for item in amer_url_list_dupe:
    if item not in amer_url_list:
        amer_url_list.append(item)

#Remove irrelevant URLs
amer_url_list = amer_url_list[1:-1]

#Extract object ID
obj_id_list = []

for i in amer.find_all('div', {'class': 'result item grid-item col-lg-2 col-md-3 col-sm-4 col-xs-12'}):
    obj_id = i['data-emuseum-id']
    obj_id_list.append(obj_id)

#Create dataframe for American paintings on view
amer_df = pd.DataFrame(zip(obj_id_list, amer_artist_list, amer_title_list, amer_url_list), columns=('objectid', 'artist', 'title', 'url'))


#Pull records for European paintings on view, page 1
euro_url1 = "https://collections.mfa.org/collections/314107/european-paintings/objects/images?filter=onview%3Atrue&page=1"

headers = {"User-Agent" : "Chrome"}

euro_req1 = requests.get(euro_url1, headers=headers)
euro_req1.raise_for_status()

euro_req1.text

euro1 = BeautifulSoup(euro_req1.text, "html.parser")

#Extract titles
euro1_title_list_dupe = []

for i in euro1.find_all('a', class_=""):
    try:
        title = i.get('title')
        if title is not None and title != 'Sign in':
            euro1_title_list_dupe.append(title)
    except:
        pass

#Remove title duplicates
euro1_title_list = []

for item in euro1_title_list_dupe:
    if item not in euro1_title_list:
        euro1_title_list.append(item)

#Extract artists
euro1_artist_list = []

for i in euro1.find_all('div', class_='primaryMaker text-wrap'):
    artist = i.text
    euro1_artist_list.append(artist)

#Extract URLs
euro1_url_list_dupe = []

for i in euro1.select('a'):
    euro1_url = 'https://collections.mfa.org' + i.get('href')
    if 'object' in euro1_url:
        euro1_url_list_dupe.append(euro1_url)

#Remove URL duplicates
euro1_url_list = []

for item in euro1_url_list_dupe:
    if item not in euro1_url_list and 'login' not in item:
        euro1_url_list.append(item)

#Remove irrelevant URLs
euro1_url_list = euro1_url_list[2:]

#Extract object ID
obj_id_list = []

for i in euro1.find_all('div', {'class': 'result item grid-item col-lg-2 col-md-3 col-sm-4 col-xs-12'}):
    obj_id = i['data-emuseum-id']
    obj_id_list.append(obj_id)
    
#Create dataframe for European paintings on view, page 1
euro1_df = pd.DataFrame(zip(obj_id_list, euro1_artist_list, euro1_title_list, euro1_url_list), columns=('objectid', 'artist', 'title', 'url'))


#Pull European paitings on view, page 2
euro_url2 = "https://collections.mfa.org/collections/314107/european-paintings/objects/images?filter=onview%3Atrue&page=2"

headers = {"User-Agent" : "Chrome"}

euro_req2 = requests.get(euro_url2, headers=headers)
euro_req2.raise_for_status()

euro_req2.text

euro2 = BeautifulSoup(euro_req2.text, "html.parser")

#Extract titles
euro2_title_list_dupe = []

for i in euro2.find_all('a', class_=""):
    try:
        title = i.get('title')
        if title is not None and title != 'Sign in':
            euro2_title_list_dupe.append(title)
    except:
        pass

#Remove title duplicates
euro2_title_list = []

for item in euro2_title_list_dupe:
    if item not in euro2_title_list:
        euro2_title_list.append(item)

#Extract artists
euro2_artist_list = []

for i in euro2.find_all('div', class_='primaryMaker text-wrap'):
    artist = i.text
    euro2_artist_list.append(artist)

#Extract URLs
euro2_url_list_dupe = []

for i in euro2.select('a'):
    euro2_url = 'https://collections.mfa.org' + i.get('href')
    if 'object' in euro2_url:
        euro2_url_list_dupe.append(euro2_url)

#Remove URL duplicates
euro2_url_list = []

for item in euro2_url_list_dupe:
    if item not in euro2_url_list and 'login' not in item:
        euro2_url_list.append(item)

#Remove irrelevant URLs
euro2_url_list = euro2_url_list[2:]

#Extract object ID
obj_id_list = []

for i in euro2.find_all('div', {'class': 'result item grid-item col-lg-2 col-md-3 col-sm-4 col-xs-12'}):
    obj_id = i['data-emuseum-id']
    obj_id_list.append(obj_id)
    
#Create dataframe for European paitings on view, page 2
euro2_df = pd.DataFrame(zip(obj_id_list, euro2_artist_list, euro2_title_list, euro2_url_list), columns=('objectid', 'artist', 'title', 'url'))

#Concat dataframes
mfa_df = pd.concat([amer_df, euro1_df])
mfa_df = pd.concat([mfa_df, euro2_df])

#Save file
mfa_df.to_csv('mfa_df.csv')
