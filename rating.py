#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec  3 19:19:55 2018

@author: shengwang
"""

import secret
import forming_db
import plotly
import plotly.plotly as py
import plotly.graph_objs as go

import sqlite3
forming_db.create_all_data()
conn = sqlite3.connect('computer.db')
cur = conn.cursor()

#rating histogram
def rating_histogram(product_name):
    rating_num = []
    for i in range(5):
        statement = '''
        select count(*) from review
        inner join information on information.Id=review.ProductId
        where Rating={}
        and information.product_name='{}'
        '''.format(i+1, product_name)
        cur.execute(statement)
        rating_num.append(cur.fetchone()[0])
    
    PLOTLY_USERNAME = secret.PLOTLY_USERNAME
    PLOTLY_API_KEY = secret.PLOTLY_API_KEY
    
    plotly.tools.set_credentials_file(username=PLOTLY_USERNAME, api_key=PLOTLY_API_KEY)
    data1 = [go.Bar(
                x=['rating_1', 'rating_2', 'rating_3', 'rating_4', 'rating_5'],
                y=rating_num
        )]
    layout1 = go.Layout(
            title = "{} histogram of rating".format(product_name)
            )
    fig = go.Figure(data=data1, layout=layout1)
    py.iplot(fig, filename='rating histgram {}'.format(product_name),auto_open=True)

#rating through time
def rating_time(product_name):
    statement='''
    select  Time,avg(Rating) from review
    inner join information on information.Id=review.ProductId
    where information.Company='bestbuy'
    and information.product_name='{}'
    group by review.Time
    '''.format(product_name)
    cur.execute(statement)
    res = cur.fetchall()
    year = []
    month = []
    week = []
    day = []
    hour = []
    for time in res:
        if(time[0].split()[1]=='year' or time[0].split()[1]=='years'):
            year.append([time[0],time[1]])
        elif(time[0].split()[1]=='months' or time[0].split()[1]=='month'):
            month.append([time[0],time[1]])
        elif(time[0].split()[1]=='weeks' or time[0].split()[1]=='week'):
            week.append([time[0], time[1]])
        elif(time[0].split()[1]=='days' or time[0].split()[1]=='day'):
            day.append([time[0], time[1]])
        else:
            hour.append([time[0], time[1]])
    hour = sorted(hour, key=lambda x:x[0], reverse = False)
    day = sorted(day, key=lambda x:x[0], reverse = False)
    week = sorted(week, key=lambda x:x[0], reverse = False)
    month = sorted(month, key=lambda x:x[0], reverse = False)
    year = sorted(year, key=lambda x:x[0], reverse = False)
    data_x = day+week+month+year
    
    time = [i[0] for i in data_x]
    rating = [i[1] for i in data_x]
    data2 = [go.Scatter(
        x = time,
        y = rating,
        name = 'rating',
        line = dict(
            color = ('rgb(205, 12, 24)'),
            width = 4,)
    )]
    layout2 = dict(title = 'rating through time {}'.format(product_name),
                  xaxis = dict(title = 'time'),
                  yaxis = dict(title = 'average rating'),
                  )
    fig = go.Figure(data=data2, layout=layout2)
    py.iplot(fig, filenam='rating time {}'.format(product_name), auto_open=True)

def rating_title(rating,product_name):
    statement = '''
    select title from review
    inner join information on information.Id=review.ProductId
    where information.product_name={}
    and 
    review.Rating={}
    '''.format(rating,product_name)
    cur.execute(statement)
    res = cur.fetchall()
    return res


        