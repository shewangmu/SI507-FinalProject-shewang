#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec  3 18:40:45 2018

@author: shengwang
"""

import unittest
import requests
from bs4 import BeautifulSoup
import fetch_data
import forming_db
import sqlite3
import json

class FetchData(unittest.TestCase):  
    def test_information_review(self):
        name = 'macbook+air'
        url = 'https://www.bestbuy.com/site/searchpage.jsp?st={}&_dyncharset=UTF-8&id=pcat17071&type=page&sc=Global&cp=1&nrp=&sp=&qp=&list=n&af=true&iht=y&usc=All&ks=960&keys=keys'.format(name)
        html = requests.get(url, headers={'User-Agent': 'SI_CLASS'}).text
        soup = BeautifulSoup(html, 'html.parser')
        soup = soup.find('main')
        content = soup.find(class_='sku-item-list')
        content = content.find_all(class_='sku-item')
        info = fetch_data.get_information(0,content,'macbook')
        self.assertEqual(type(info), dict)
        review = fetch_data.fetch_review(0,content)
        self.assertEqual(type(review), list)
        self.assertNotEqual(len(review), 0)
    
    def test_bestbuy(self):
        content = fetch_data.fetch_bestbuy('macbook air',{})
        self.assertEqual(type(content), list)
        self.assertNotEqual(len(content), 0)
        self.assertEqual(type(content[0]), dict)
    
    def test_amazon(self):
        content = fetch_data.fetch_amazon('macbook ari', {})
        self.assertEqual(type(content), list)
        self.assertNotEqual(len(content), 0)
        self.assertEqual(type(content[0]), dict)
    
    def test_fetchall(self):
        fetch_data.fetch_all('macbook air')
        try:
            cache_file = open('cache.json', 'r')
            cache_content = cache_file.read()
            cache_dic = json.loads(cache_content)
            cache_file.close()
        except:
            cache_dic = {}
            cache_dic['num']=1
        self.assertNotEqual(cache_dic['num'], 1)
    
class FormingDb(unittest.TestCase):
    def test_setup(self):
        forming_db.recreate_db()
    
    def test_addnewData(self):
        product_name = 'macbook air'
        bestbuy = fetch_data.fetch_bestbuy(product_name,{})
        forming_db.add_new_data(bestbuy, 'macbook air', 'bestbuy')
        statement = '''
        select count(*) from information
        '''
        conn = sqlite3.connect('computer.db')
        cur = conn.cursor()
        cur.execute(statement)
        count = cur.fetchone()
        self.assertNotEqual(count, 0)
        statement = '''
        select count(*) from review
        '''
        cur.execute(statement)
        count = cur.fetchone()
        self.assertNotEqual(count, 0)
        conn.close()
        
        
unittest.main()       