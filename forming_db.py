#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 28 14:32:33 2018

@author: shengwang
"""

import fetch_data
import sqlite3
import json
DBNAME = 'computer.db'

def recreate_db():
    conn = sqlite3.connect(DBNAME)
    cur = conn.cursor()
    #drop table to test
    statement = 'drop table if exists information'
    cur.execute(statement)
    statement = 'drop table if exists review'
    cur.execute(statement)
    conn.commit()
    
    statement = '''
        CREATE TABLE `information` (
    	`Id`	INTEGER PRIMARY KEY AUTOINCREMENT,
        'product_name' TEXT,
        'Company' TEXT,
        `price`	TEXT,
    	`model`	TEXT,
    	`processor_model`	TEXT,
    	`processor_speed`	TEXT,
    	`RAM`	TEXT,
    	`Screen`	TEXT,
    	`Storage`	TEXT,
        'basic_info' TEXT
    );
    '''
    cur.execute(statement)
    conn.commit()
    
    statement = '''
        CREATE TABLE `review` (
    	`CustomerId`	INTEGER PRIMARY KEY AUTOINCREMENT,
    	`ProductId`	INTEGER,
        `Title`	TEXT,
        `Time`	TEXT,
        `Rating`	TEXT,
    	`Content`	TEXT
    );
    '''
    cur.execute(statement)
    conn.commit()
    conn.close()

def add_new_data(company, product_name, company_name):
    conn = sqlite3.connect(DBNAME)
    cur = conn.cursor()
    for i in range(len(company)):
        info = company[i]['information']
        price = info['price']
        Id = info['id']
        try:
            model = info['model']
            processor_model = info['processor_model']
            processor_speed = info['processor_speed']
            ram = info['ram']
            screen = info['screen']
            storage = info['storage']
            cur.execute("INSERT INTO information (Id, product_name, model,price,processor_model,processor_speed,RAM,Screen,Storage, Company,basic_info) VALUES (?,?,?,?,?,?,?,?,?,?,?)",
                         (Id, product_name, model,price,processor_model,processor_speed,ram,screen,storage,company_name,info['basic']))
            conn.commit()
        except:  
#            if(company_name=='bestbuy'):
#                cur.execute("INSERT INTO information (Id,product_name,price,Company) VALUES (?,?,?,?)",
#                                 (Id, product_name, price, company_name))
#            else:
            cur.execute("INSERT INTO information (Id,product_name,price,Company,basic_info) VALUES (?,?,?,?,?)",
                                 (Id, product_name, price, company_name, info['basic']))
            conn.commit()
        
        review = company[i]['review']
        for j in range(len(review)):
            Id = review[j]['ProductId']
            title = review[j]['title']
            time = review[j]['time']
            rating = review[j]['rating']
            content = review[j]['content']
            cur.execute("INSERT INTO review (ProductId,Title,Time,Rating,Content) VALUES (?,?,?,?,?)",
                         (Id, title, time, rating, content))
            conn.commit()

    
def create_all_data():
    recreate_db()
    product_name = 'macbook pro'
    #getting data from bestbuy
    bestbuy = fetch_data.fetch_bestbuy(product_name,{})
    #getting data from amazon
    add_new_data(bestbuy, product_name, 'bestbuy')
    amazon = fetch_data.fetch_amazon(product_name,{})
    add_new_data(amazon, product_name, 'amazon')
    
    product_name = 'macbook air'
    bestbuy = fetch_data.fetch_bestbuy(product_name,{})
    #getting data from amazon
    add_new_data(bestbuy, product_name, 'bestbuy')
    amazon = fetch_data.fetch_amazon(product_name,{})
    add_new_data(amazon, product_name, 'amazon')
    
    bestbuy = fetch_data.fetch_bestbuy('surface',{})
    add_new_data(bestbuy, 'surface', 'bestbuy')
    amazon = fetch_data.fetch_amazon('surface',{})
    add_new_data(amazon,'surface','amazon')
    
    bestbuy = fetch_data.fetch_bestbuy('thinkpad',{})
    add_new_data(bestbuy, 'thinkpad', 'bestbuy')
    amazon = fetch_data.fetch_amazon('thinkpad',{})
    add_new_data(amazon,'thinkpad','amazon')
    
    
    
    