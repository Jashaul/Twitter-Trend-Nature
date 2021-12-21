
import os
import json
import random
import sqlite3
import warnings

warnings.filterwarnings("ignore")

import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate
import plotly.express as px

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from wordcloud import WordCloud

conn = sqlite3.connect("db.sqlite3")

trends_data = pd.read_sql_query("SELECT * FROM TTN_trends;", conn)
table_df = trends_data[['trend_name', 'trend_date', 'negative_count',  'positive_count', 'sentiment_ratio']]
table_df["sentiment_ratio"] = table_df["sentiment_ratio"].round(4)

external_stylesheets = [dbc.themes.BOOTSTRAP]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

pie_fig = px.pie(data_frame=trends_data, values='sentiment_ratio', names='trend_name')
bar_fig = px.bar(data_frame=trends_data, x = "trend_name", y = ["negative_count", "positive_count"])
app.layout = html.Div(
        children = [html.H4("Nature of Twitter trends", style = {"text-align" : "center", "font-size": "32px", "padding-bottom" : "20px"}),
                    html.Div(children = [html.Label("Ratio of sentiment in each trend"),
                                        dcc.Graph(id = "pie_chart", figure= pie_fig)], 
                             style={'display': 'inline-block', "width":"50%"}),
                    html.Div(children = [html.Label("Number of positive and negative tweets in a trend"),
                                        dcc.Graph(id = "bar_neg_pos_count", figure = bar_fig)], 
                             style={ 'display': 'inline-block',"width":"50%"}),
                    html.Div(children = [html.Label("Trend Information"),
                                        dash_table.DataTable(
                                                id='table',
                                                columns=[{"name": i, "id": i} for i in table_df.columns],
                                                data=table_df.to_dict('records'),
                                                style_data_conditional=[{'if': {'row_index': 'odd'},
                                                                'backgroundColor': 'rgb(248, 248, 248)'
                                                                }],
                                                style_header={'backgroundColor': 'rgb(230, 230, 230)',
                                                        'fontWeight': 'bold'},
                                                style_cell={'width': '20%','fontSize':15, 'font-family':'sans-serif', "text-align": "center"},
                                                fixed_rows={'headers': True})
                                                ], 
                                        style = {"padding-top": "20px"}),
                    html.Div(children = [html.Label("Word Cloud for each trend"),
                                        dcc.Dropdown(id = "trend_dropdown", options = [{"label" : i, "value" : i} for i in trends_data["trend_name"].values.tolist()]),
                                        html.Div(id = "word_clouds", 
                                                 children = [
                                                        html.Div(id="word_cloud_positive", style={"display": "inline-block", "width":"50%"}), 
                                                        html.Div(id="word_cloud_negative",   style={"display": "inline-block", "width":"50%"})],
                                                 style = {"width":"100%", "display" : "inline-block","width": "100%" ,"padding-top" : "20px"})],
                             style = {"width" : "100%", "display" : "inline-block"}
                                        )],
        style={"width":"100%", "padding": "20px"})

@app.callback(Output(component_id = "word_cloud_positive", component_property="children"),
              Output(component_id = "word_cloud_negative", component_property="children"),
              Input(component_id = "trend_dropdown", component_property="value"))
def update_word_cloud(trend_value):

        if trend_value == None:
                return None, None

        else:
                positive_words = trends_data[trends_data["trend_name"] == trend_value]["positive_words"].values.tolist()[0]
                negative_words = trends_data[trends_data["trend_name"] == trend_value]["negative_words"].values.tolist()[0]

                pos_wc = WordCloud(background_color = "white", width = 500, height = 300)
                pos_word_cloud = pos_wc.generate(positive_words)
                pos_wc.to_file("assets/positive_word_cloud.png")

                neg_wc = WordCloud(background_color = "white", width = 500, height = 300)
                neg_word_cloud = neg_wc.generate(negative_words)
                neg_wc.to_file("assets/negative_word_cloud.png")

                pos_label = html.Label("Positive word cloud")
                pos_img = html.Img(src = app.get_asset_url('positive_word_cloud.png'), style = {"width": "100%", "border-style": "solid"})

                neg_label = html.Label("Negative word cloud")
                neg_img = html.Img(src = app.get_asset_url("negative_word_cloud.png"), style = {"width": "100%", "border-style": "solid"})

                return [pos_label,pos_img] , [neg_label,neg_img]
        
app.run_server(debug=False)