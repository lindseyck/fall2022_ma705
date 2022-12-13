# -*- coding: utf-8 -*-
"""
Created on Fri Dec  9 10:52:13 2022

@author: LKOSINSKI
"""

import requests
import pandas as pd
import numpy as np

#Pull all records for Paintings
records = []

def pagination(url):

    harvard_req = requests.get(url)

    harvard = harvard_req.json()

    info = harvard['info']
    
    records.extend(harvard['records'])

    try:
        if (info['next']):
            pagination(info['next'])
            
    except:
        pass

url = "https://api.harvardartmuseums.org/Object?classification=Paintings&apikey=a2aab107-f4f2-47ee-b77b-af4b15fe10c2&size=100"

pagination(url)

#Extract columns
objectid = [record['objectid'] for record in records]
artist = [[person['name'] for person in record['people']] if 'people' in record else 'NA' for record in records]
gender = [[person['gender'] for person in record['people']] if 'people' in record else 'NA' for record in records]
division = [record['division'] for record in records]
medium = [record['medium'] for record in records]
title = [record['title'] for record in records]
colors = [[color['hue'] for color in record['colors']] if 'colors' in record else 'NA' for record in records]
dated = [record['dated'] for record in records]
urls = [record['url'] for record in records]
century = [record['century'] for record in records]
culture = [record['culture'] for record in records]
description = [record['description'] for record in records]

#Create dataFrame
harvard_df = pd.DataFrame(zip(objectid, artist, title, urls, gender, division, medium, colors, dated, century, culture, description), columns = ('objectid','artist','title','url','gender','division','medium','colors','dated','century','culture','description'))

#Save file
harvard_df.to_csv('harvard_df.csv')

#Reload csv
harvard_df = pd.read_csv('harvard_df.csv')

#Clean the artist, gender, and colors objects
harvard_df['artist'] = harvard_df['artist'].str.replace("\'", "")
harvard_df['artist'] = harvard_df['artist'].str.replace("\[", "")
harvard_df['artist'] = harvard_df['artist'].str.replace("\]", "")
harvard_df['artist'] = harvard_df['artist'].str.replace('\"', '')
harvard_df['gender'] = harvard_df['gender'].str.replace("\'", "")
harvard_df['gender'] = harvard_df['gender'].str.replace("\[", "")
harvard_df['gender'] = harvard_df['gender'].str.replace("\]", "")
harvard_df['colors'] = harvard_df['colors'].str.replace("\'", "")
harvard_df['colors'] = harvard_df['colors'].str.replace("\[", "")
harvard_df['colors'] = harvard_df['colors'].str.replace("\]", "")

#Remove unknown artists
harvard_df = harvard_df[harvard_df['artist'].notna()]
harvard_df = harvard_df[(harvard_df['artist'] != 'NA') & (harvard_df['artist'] != 'Unknown Artist') & (harvard_df['artist'] != 'Unidentified Artist')]

#Drop first column
harvard_df = harvard_df.drop(harvard_df.columns[0],axis = 1)

#Resave csv
harvard_df.to_csv('harvard_df.csv')
