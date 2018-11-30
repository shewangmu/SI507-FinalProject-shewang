#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 28 11:27:40 2018

@author: shengwang
"""

import requests
from bs4 import BeautifulSoup
import json

try:
    cache_file = open('cache.json', 'r')
    cache_content = cache_file.read()
    cache_dic = json.loads(cache_content)
    cache_file.close()
except:
    cache_dic = {}
    cache_dic['num']=1


def get_information(i, res, name):
    info = {}
    information = res[i].find(class_='sku-header')
    info_url = information.find('a')['href']
    info_html = requests.get(info_url, headers={'User-Agent':'SI_CLASS'}).text
    info_soup = BeautifulSoup(info_html, 'html.parser')
    
    price = info_soup.find(id='price')
    price = price.find_all('span')
    price = price[4].text
    info['price'] = price
    
    if(name == 'macbook'):
        info_soup = info_soup.find(id='accordion-view')
        info_content = info_soup.find(class_='shop-specifications')
                
        #this contains all the information of the computer
        info_content = info_content.find_all(class_='category-wrapper row')
        #model number
        model = info_content[-2].find_all('li')
        model = model[-1].find_all('div')[-1].text
        #screen size
        key_spec = info_content[0].find_all('li')
        screen = key_spec[2].find_all('div')[-1].text
        #storage
        storage = key_spec[5].find_all('div')[-1].text
        #processor speed
        processor_speed = key_spec[8].find_all('div')[-1].text
        #proccessor model
        processor_model = key_spec[9].find_all('div')[-1].text
        #ram size
        ram = info_content[5].find('li')
        ram = ram.find_all('div')[-1].text
        
        info['ram'] = ram
        info['processor_model'] = processor_model
        info['processor_speed'] = processor_speed
        info['screen'] = screen
        info['model'] = model
        info['storage'] = storage
    return info

def fetch_review(i, res):
    rev_all = []
    review = res[i].find(class_='ratings-reviews')
    rev_url = review['href']
    rev_html = requests.get(rev_url, headers={'User-Agent':'SI-CLASS'}).text
    rev_soup = BeautifulSoup(rev_html, 'html.parser')
    rev_url = rev_soup.find(class_='see-all-reviews-button-container')
    rev_url = 'http://www.bestbuy.com' + rev_url.find('a')['href']
    rev_html = requests.get(rev_url, headers={'User-Agent':'SI-CLASS'}).text
    rev_soup = BeautifulSoup(rev_html, 'html.parser')
    rev_soup = rev_soup.find(class_='message-text').text
    #finding the total review number
    try:
        review_num = int(rev_soup.split()[-2])
    except:
        review_num = 1000
    page = 1
    while page<3 and page<(1+review_num/20):
        cur_url = rev_url+'?page={}'.format(page)
        rev_html = requests.get(cur_url, headers={'User-Agent':'SI-CLASS'}).text
        rev_soup = BeautifulSoup(rev_html, 'html.parser')
        rev_soup = rev_soup.find(class_='reviews-list')
        review_list = rev_soup.find_all(class_='review-item')
        for j in range(len(review_list)):
            rev = {}
            #time
            time = review_list[j].find(class_='disclaimer').find('time').text
            #rating
            rating = review_list[j].find(class_='c-ratings-reviews v-medium')
            rating = int(rating.find_all('span')[-1].text)
            #title
            title = review_list[j].find('h3').text
            #content
            rev_content = review_list[j].find(class_='ugc-review-body body-copy-lg').text
            
            rev['ProductId'] = cache_dic['num']
            rev['time'] = time
            rev['rating'] = rating
            rev['title'] = title
            rev['content'] = rev_content
            rev_all.append(rev)
        page += 1
    return rev_all

def fetch_bestbuy(name, dic):
    if(name in cache_dic):
        return cache_dic[name]['best_buy']
    else:
        name = name.split()
        name = '+'.join(name)
        url = 'https://www.bestbuy.com/site/searchpage.jsp?st={}&_dyncharset=UTF-8&id=pcat17071&type=page&sc=Global&cp=1&nrp=&sp=&qp=&list=n&af=true&iht=y&usc=All&ks=960&keys=keys'.format(name)
        html = requests.get(url, headers={'User-Agent': 'SI_CLASS'}).text
        soup = BeautifulSoup(html, 'html.parser')
        soup = soup.find('main')
        content = soup.find(class_='sku-item-list')
        content = content.find_all(class_='sku-item')
        res = content
        
        new_content = []
        #flag is used to print the information once
        i = 0 #make sure I fetch 5 product
        j = 0 #the number of res
        while i<5 and j<len(res):
            temp = {}
            try:
                #begin going into the information website
                info = get_information(j, res, name.split('+')[0])
                info['id'] = cache_dic['num']
                #begin going into customer review website
                rev_all = fetch_review(j, res)
                #maintaining the product number
                cache_dic['num'] += 1
                i +=1
                j+=1
                temp['information'] = info
                temp['review'] = rev_all
                new_content.append(temp)
            except:
                j+=1
        
        #update cache_file
        dic['best_buy'] = new_content
        return new_content
 
def fetch_amazon(name, dic):
    if(name in cache_dic):
        return cache_dic[name]['amazon']
    else:
        pass
    
def fetch_all(name):
    dic = {}
    fetch_bestbuy(name, dic)
    fetch_amazon(name, dic)
    cache_dic[name] = dic
    dumped_json_cache = json.dumps(cache_dic)
    fw = open('cache.json', 'w')
    fw.write(dumped_json_cache)
    fw.close()

if __name__=='__main__':
    fetch_all('surface')