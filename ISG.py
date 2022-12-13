# -*- coding: utf-8 -*-
"""
Created on Wed Nov 16 18:25:33 2022

@author: LKOSINSKI
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd

url = "https://www.gardnermuseum.org/experience/collection"

headers = {"User-Agent": "Chrome"}

#Create Object ID range
def IDList(minimum, maximum):

    if (minimum == maximum):
        return minimum

    else:

        IDs = []

        while(minimum < maximum + 1):

            IDs.append(minimum)
            minimum += 1
        return IDs


minimum = 10000
maximum = 16000

id_list = IDList(minimum, maximum)


#Extract object IDs
obj_id_list = []

for i in id_list:
    
    new_url = url + '/' + str(i)
    
    try:
      isg_req = requests.get(new_url)
      isg = BeautifulSoup(isg_req.text, 'html.parser')
      find_form = isg.find('form', class_='views-exposed-form')
      obj_id = find_form.get('action').split('/')[-1]
      obj_id_list.append(obj_id)
    except:
        pass

#Remove invalid IDs
obj_id_list = [x for x in obj_id_list if x != '404']


#Create list of all URLs
isg_url_list = []

for i in obj_id_list:
    new_url = url + '/' + str(i) + '#object-details'
    try:
        requests.get(new_url)
        isg_url_list.append(new_url)
    except:
        pass


#Initiate dataframe
isg1 = pd.DataFrame(columns=['objectid', 'artist', 'title', 'url', 'stolen', 'painting'])
isg1['objectid'] = obj_id_list
isg1['url'] = isg_url_list


#Create lists
artist_list = []
title_list = []
stolen_list = []
painting_list = []

for url in isg_url_list:  
    isg_req = requests.get(url)
    isg = BeautifulSoup(isg_req.text, 'html.parser')
    artist = isg.find('h3', class_='title-card__pre-title').text.split('(')[0].replace('\n','').strip()
    title = isg.find('h1', {'class': 'title-card__title'}).text.split(',')[0]
    stolen = "stolen" in isg.text.lower()
    painting = "paint" in isg.text.lower()
    artist_list.append(artist)
    title_list.append(title)
    stolen_list.append(stolen)
    painting_list.append(painting)

isg1['artist'] = artist_list
isg1['title'] = title_list
isg1['stolen'] = stolen_list
isg1['painting'] = painting_list

#Isolate paintings
isg_df = isg1[isg1['painting']]

#Filter out stolen items
isg_df = isg_df[isg_df['stolen'] == False]

isg_df['artist'] = isg_df['artist'].str.replace("\'", "")
isg_df['artist'] = isg_df['artist'].str.replace('After\s+', '')
isg_df['artist'] = isg_df['artist'].str.replace('after\s+', '')
isg_df['artist'] = isg_df['artist'].str.replace('Attributed to\s+', '')
isg_df['artist'] = isg_df['artist'].str.replace('Designed by\s+', '')
isg_df['artist'] = isg_df['artist'].str.replace('Studio of\s+', '')
isg_df['artist'] = isg_df['artist'].str.replace('Workshop of\s+', '')
isg_df['artist'] = isg_df['artist'].str.replace('Follower of\s+', '')
isg_df['artist'] = isg_df['artist'].str.replace('Style of\s+', '')
isg_df['artist'] = isg_df['artist'].str.replace('Traditionally attributed to\s+', '')
isg_df['artist'] = isg_df['artist'].str.replace('Influenced by\s+', '')
isg_df['artist'] = isg_df['artist'].str.replace('Imitator of\s+', '')
isg_df['artist'] = isg_df['artist'].str.replace('Circle of\s+', '')
#Note: Despite prefixes like "Follower of" or "Style of," the object details will say "Primary Creator" or "Creator(s)" = [artist]


#Drop extra columns
isg_df = isg_df.drop(isg_df.columns[[4,5]],axis = 1)

#Save file
isg_df.to_csv('isg_df.csv')















