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
    	`model`	TEXT,
    	`price`	TEXT,
    	`processor_model`	TEXT,
    	`processor_speed`	TEXT,
    	`RAM`	TEXT,
    	`Screen`	TEXT,
    	`Storage`	TEXT,
        'Company' TEXT
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

def add_new_data(company, name):
    conn = sqlite3.connect(DBNAME)
    cur = conn.cursor()
    for i in range(len(company)):
        info = company[i]['information']
        Id = info['id']
        model = info['model']
        price = info['price']
        processor_model = info['processor_model']
        processor_speed = info['processor_speed']
        ram = info['ram']
        screen = info['screen']
        storage = info['storage']
        cur.execute("INSERT INTO information (Id, product_name, model,price,processor_model,processor_speed,RAM,Screen,Storage, Company) VALUES (?,?,?,?,?,?,?,?,?,?)",
                         (Id, name, model,price,processor_model,processor_speed,ram,screen,storage,'bestbuy'))
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
    
if __name__=='__main__':
    name = 'macbook air'
    #getting data from bestbuy
    bestbuy = fetch_data.fetch_bestbuy(name,{})
    #getting data from amazon
    recreate_db()
    add_new_data(bestbuy, name)
    bestbuy = fetch_data.fetch_bestbuy('macbook pro',{})
    add_new_data(bestbuy, 'macBook pro')
    
    