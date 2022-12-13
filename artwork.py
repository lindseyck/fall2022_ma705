# -*- coding: utf-8 -*-
"""
Created on Fri Dec  9 18:41:47 2022

@author: LKOSINSKI
"""

import pandas as pd

harvard = pd.read_csv('harvard_df.csv')
isg = pd.read_csv('isg_df.csv')
mfa = pd.read_csv('mfa_df.csv')

#Concatenate the dataframes
artwork = pd.concat([harvard, isg, mfa], keys=['Harvard', 'ISG', 'MFA'])

#add data source column
artwork['data_source'] = artwork.index.get_level_values(0)
artwork.reset_index(level=0, inplace=True)
artwork.drop(columns='level_0', inplace=True)

#Drop first column
artwork = artwork.drop(artwork.columns[0],axis = 1)

#Flag non-artists included in dataframe
not_artists = [
'American',
'American, Philadelphia',
'Arab',
'British',
'Byzantine',
'Catalan, Catalonia',
'Chinese',
'Chinese, Canton province',
'Chinese, Jingdezhen',
'Dutch',
'East Asian',
'Egyptian',
'Egyptian, Cairo',
'English',
'Etruscan',
'European',
'Flemish, Flanders',
'French',
'French, Arles',
'French, Cannes',
'French, Limoges',
'French, Soissons',
'French, Utrecht',
'German',
'German, Bavaria',
'German, Berlin',
'German, Dresden',
'German, Franconia',
'German, Nuremberg',
'German, Nuremburg',
'German, Ravensburg',
'German, Rhineland Palatinate',
'German, Saxony',
'German, Southern Germany',
'German, Swabia',
'German, Ulm',
'German, Upper Rhine',
'Greek',
'Greek, Athens',
'Greek, Corfu',
'Greek, Myrina',
'Indian',
'Indian, Northern India',
'Iranian, Kashan',
'Italian',
'Italian, Central Italy',
'Italian, Florence',
'Italian, LAquila',
'Italian, Liguria',
'Italian, Lombardy',
'Italian, Marches',
'Italian, Milan',
'Italian, Naples',
'Italian, Netherlands, Italy, and France',
'Italian, Northern Italy',
'Italian, Orvieto',
'Italian, Piedmont',
'Italian, Rome',
'Italian, Siena',
'Italian, Southern Italy',
'Italian, Trentino-Alto Adige',
'Italian, Umbria',
'Italian, Urbino',
'Italian, Veneto',
'Italian, Venice',
'Japanese',
'Japanese, Kyoto',
'Korean',
'Mexican, Atlixco',
'Netherlandish, Southern Netherlands',
'Norwegian',
'Persian',
'Persian, Herat',
'Persian, Shiraz',
'Roman',
'Russian',
'Russian, Novgorod',
'Scottish',
'Spanish',
'Spanish, Alpujarra',
'Spanish, Basque Provinces',
'Spanish, Burgos',
'Spanish, Castilla y León',
'Spanish, Catalonia',
'Spanish, Catalonian, Catalonia',
'Spanish, Salamanca',
'Spanish, Valencia',
'Swan Group',
'Swiss',
'Syrian',
'Unidentified artist, Spanish (Catalan), 12th century']
#I swear I didn't type all of this out; I leveraged Excel and Notepad++. But still, there has to be a better way...

#Create artist indicator
artwork['isartist'] = ['N' if artist in not_artists else 'Y' for artist in artwork.artist]

#Save file
artwork.to_csv('artwork.csv')





















