# -*- coding: utf-8 -*-
"""
Created on Sat Dec 10 20:47:28 2022

@author: LKOSINSKI
"""

import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State
import plotly.express as px
import pandas as pd
from dash import dash_table
import plotly.graph_objects as go


stylesheet = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

#Custom colors
colors = {
    'background': '#f6fcff',
    'text': '#2b306c'
}

app = dash.Dash(__name__, external_stylesheets=stylesheet)
server = app.server

df = pd.read_csv('artwork.csv')
dt_df = pd.read_csv('dt_df.csv')

#Counts by museum
paint_count = df.groupby('data_source', as_index=False).size()

#Top artists by museum
top_harvard = pd.DataFrame(df[df['data_source'] == 'Harvard']['artist'].value_counts().head(1)).reset_index()
top_harvard.rename(columns={"index": "Artist", "artist": "Paintings"})
harvard_no_ross = df[(df['data_source'] == 'Harvard') & (df['artist'] != 'Denman Waldo Ross')]
top_10_harvard_no_ross = pd.DataFrame(harvard_no_ross[harvard_no_ross['data_source'] == 'Harvard']['artist'].value_counts().head(10)).reset_index()
top_10_harvard_no_ross.rename(columns={"index": "Artist", "artist": "Paintings"})
isg_artists = df.loc[(df['data_source'] == 'ISG') & (df['isartist'] == 'Y')]
top_10_isg = pd.DataFrame(isg_artists['artist'].value_counts().head(10)).reset_index()
top_10_isg.rename(columns={"index": "Artist", "artist": "Paintings"})
mfa_artist = df[(df['data_source'] == 'MFA') & (df['artist'] != 'Unidentified artist, Spanish (Catalan), 12th century')][['artist']]
all_mfa = pd.DataFrame(mfa_artist['artist'].value_counts().reset_index()).sort_values('artist')
total_artists = df.loc[df['isartist'] == 'Y']
total = pd.DataFrame(total_artists['artist'].value_counts().head(10)).reset_index()

#Isolate artists with gender
df['has_gender'] = df['gender'].str.contains('male') | df['gender'].str.contains('female')
has_gender = df[df['has_gender']]

#Harvard works by gender
has_gender['sex'] = ['F' if 'female' in sex else 'M' for sex in has_gender.gender]
has_gender = pd.DataFrame(has_gender.groupby('sex').size()).reset_index()

#Harvard works by division
division = pd.DataFrame(df.division.value_counts()).reset_index()


#Create df for data table
#dt_df = df[['artist', 'title', 'data_source', 'url']].drop_duplicates()
#dt_df.to_csv('dt_df.csv')
dt_df = dt_df.iloc[4:]
dt_df = dt_df.sort_values('artist')


#Format URL to be clickable (source: https://github.com/plotly/dash-table/issues/222)
def f(row):
    l = "[{0}]({0})".format(row["url"])
    return l

dt_df["link"] = dt_df.apply(f, axis=1)

#Create figs
fig_sum = px.bar(paint_count, x="data_source", y="size",
                 labels={
                     "data_source": "Museum",
                     "size": "Paintings on View"
                 },
            title="<b>Number of Paintings Currently on Display by Museum</b>")

fig_sum.update_layout(
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    font_color=colors['text']
)

fig_sum.update_traces(width=.5)
fig_sum.update_traces(marker_line_width=1,marker_line_color="black")
#fig_sum.update_layout(xaxis_tickangle=45)
fig_sum.update_traces(marker_color='#9b5d8b')

fig_10_tot = px.bar(total, x="index", y="artist",
             labels={
                     "index": "Artist",
                     "artist": "No. of Paintings"
                 },
             title="<b>Top 10 Artists Displayed in Boston Area Museums</b>")

fig_10_tot.update_layout(
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    font_color=colors['text']
)

fig_10_tot.update_traces(marker_line_width=1,marker_line_color="black")
fig_10_tot.update_traces(marker_color='#5d8b9b')

fig_10_har = px.bar(top_10_harvard_no_ross, x="index", y="artist", 
             labels={
                     "index": "Artist",
                     "artist": "No. of Paintings"
                 },
             title="<b>Top 10 Artists (minus Denman Waldo Ross): Harvard Art Museum</b><br><sup>Denman Waldo Ross (former Harvard Art Professor) has 458 paintings displayed at the Harvard Art Museum</sup>",
)

fig_10_har.update_layout(
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    font_color=colors['text']
)

#fig_10_har.update(layout_showlegend=False)
fig_10_har.update_traces(marker_line_width=1,marker_line_color="black")
fig_10_har.update_traces(marker_color='#5d6c9b')

fig_10_isg = px.bar(top_10_isg, x="index", y="artist", 
             labels={
                     "index": "Artist",
                     "artist": "No. of Paintings"
                 },
             title="<b>Top 10 Artists: Isabella Stewart Gardener</b>")

fig_10_isg.update_layout(
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    font_color=colors['text']
)

#fig_10_isg.update(layout_showlegend=False)
fig_10_isg.update_traces(marker_line_width=1,marker_line_color="black")
fig_10_isg.update_traces(marker_color='#8b9b5d')

mfa_sort = mfa_artist.sort_values('artist')

fig_all_mfa = go.Figure(data=[go.Table(
    cells=dict(values=[mfa_sort.artist[:7], 
                       mfa_sort.artist[7:14], 
                       mfa_sort.artist[14:21], 
                       mfa_sort.artist[21:28]],
               line_color=colors['text'],
               fill_color=colors['background'],
               align='left'))
])

fig_all_mfa.update_layout(title_text='<b>There are currently 28 artists each with one painting displayed at the MFA Boston:</b>')
fig_all_mfa.update_layout(title_font_color = colors['text'])
fig_all_mfa.update_layout(
    paper_bgcolor=colors['background']
)


fig_sex = px.pie(has_gender, values=0, names='sex', 
                 labels={
                         "sex": "Gender",
                         "0": "#"
                     }, 
                 title='Artists Displayed at Harvard Art Museum by Known Gender')

fig_sex.update_layout(
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    font_color=colors['text']
)

fig_div = px.bar(division, x="index", y="division", color = "index", 
             labels={
                     "index": "Division",
                     "division": "No. of Paintings"
                 },
             title="Harvard Art Museum Paintings by Division")

fig_div.update_layout(
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    font_color=colors['text']
)


#Dash layout
app.layout = html.Div(style={'backgroundColor': colors['background']}, children=[
    html.H1('Boston Area Art Museums: Paintings Currently on View', 
            style={'textAlign': 'center', 'color': colors['text'], 'font-weight': 'bold', 'font-family': 'Perpetua'}),
    html.Div(children='''
        MA705 Individual Project | Fall 2022 | Lindsey Kosinski | Published December 13th, 2022''',
        style={'textAlign' : 'center', 'color': 'black'}),
    html.H6(' About This Dashboard:',
            style={'textAlign' : 'left', 'color': colors['text'], 'font-weight': 'bold', 'font-family': 'Perpetua'}),
    html.Div(children='''
        This dashboard displays the paintings currently on view at several Boston-area museums. Users can enter names of artists, titles, or keywords in the chart at the bottom of the page to discover whether they can be viewed at the Harvard Art Museum, Isabella Stewart Gardner Museum, or Museum of Fine Arts Boston. Not sure where to start? Explore some of the top artists represented below.''',
        style={'textAlign' : 'left', 'color': 'black', 'font-style' : 'italic'}),
    html.Div([
        html.H6(' Museums Included',
                style={'textAlign' : 'left', 'color': colors['text'], 'font-weight': 'bold', 'font-family': 'Perpetua'}),
        html.A(' Harvard Art Museum',
               href='https://harvardartmuseums.org/collections?',
               target='_blank'),
        html.Br(),
        html.A(' Isabella Stewart Gardner Museum (ISG)',
               href='https://www.gardnermuseum.org/experience/collection',
               target='_blank'),
        html.Br(),
        html.A(' Museum of Fine Arts Boston (MFA)',
               href='https://collections.mfa.org/collections;jsessionid=D0075348BABE0F011775F4F8001B199A',
               target='_blank')]),   
    html.Div([
        html.Div([
            dcc.Graph(figure=fig_sum, 
                      id='summary',
                      style={'height': 600,})
        ], className="six columns"),

        html.Div([
            dcc.Graph(figure=fig_10_tot, 
                      id='tot',
                      style={'height': 600,})
        ], className="six columns"),
        ], className="row"),    
    html.Div([
        html.Div([
            dcc.Graph(figure=fig_10_har, 
                      id='harvard_10',
                      style={'height': 600,})
        ], className="six columns"),

        html.Div([
            dcc.Graph(figure=fig_10_isg, 
                      id='isg_10',
                      style={'height': 600,})
        ], className="six columns"),
        ], className="row"),
    html.Br(),
    dcc.Graph(figure=fig_all_mfa,
              id='mfa_all',
              style={'float' : 'center'}),
    html.H6("Search Artist or Title to view location and details",
            style={'textAlign': 'left', 'color': colors['text'], 'font-weight': 'bold'}),
    html.Div(children='''
        Search terms are sensitive to special characters, so searching 'cezanne' will not yield any results, but 'cézanne' will. If your keyboard lacks the appropriate character, try searching a portion of the desired result (e.g., 'zanne'). Keywords can also be searched in the Title column to find paintings of certain topics (e.g., 'dog' will show all paintings with the word dog in the title). Use the button below to clear your filters.''',
        style={'font-style' : 'italic', 'color': colors['text']}),
    dash_table.DataTable(
        id='table',
        columns=[
            dict(name='Artist', id='artist', type='text'),
            dict(name='Title', id='title', type='text'),
            dict(name='Museum on Display', id='data_source', type='text'),
            dict(name='Click URL to View Details', id='link', type='text', presentation='markdown'),
        ],
        page_size=12,
        data=dt_df.to_dict("records"),
        style_cell={'textAlign': 'left'},
        sort_action="native",
        filter_action='native',
        filter_options={'case' : 'insensitive'},
        style_table={
            'height': 400,},
        style_data={
            'width': '150px', 'minWidth': '150px', 'maxWidth': '150px',
            'overflow': 'hidden',
            'textOverflow': 'ellipsis'}),
    html.Button(id='clear', 
                children='Clear filters',
                style={'background-color':  'white'}),
    ])

#source: https://github.com/plotly/dash-table/issues/370
@app.callback(
    Output('table', 'filter_query'),
    [Input('clear', 'n_clicks')],
    [State('table', 'filter_query')],
)
def clearFilter(n_clicks, state):
    if n_clicks is None:
        return '' if state is None else state

    return ''

#app.run(debug=True, use_reloader=False)

if __name__ == '__main__':
    app.run_server(debug=True)
