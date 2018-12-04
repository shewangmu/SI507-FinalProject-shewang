from flask import Flask,render_template
import requests
from secrets import nyt_key
import sqlite3
conn = sqlite3.connect('computer.db')
cur = conn.cursor()

app = Flask(__name__)

@app.route('/')
def index():
    html = '''
    <h1> About this site</h1>
    <p> I fetch some data about the information of some computers from bestbuy and amazon.</p>
    <p>The information includes the basic information about the computer and the reviews 
    of customers.</p>
    <p>The computer type you can select is listed below</p>
    <a href='/macbook_pro'> Macbook Pro </a>
    <a href='/macbook_air'> Macbook Air </a>
    <a href='/surface'> Surface </a>
    <a href='/think_pad'> Think Pad </a>
    '''
    return html

@app.route('/user/product')
def product_info(product):
    statement = '''
        select basic_info from information
        where product_name='macbook pro'
    '''
    cur.execute(statement)
    res = cur.fetchall()
    basic_info = ''
    for bas in res:
        basic_info = basic_info + '<p>' + bas[0]
        basic_info += '</p>'
    html = render_template('product.html', product=product, basic=basic_info)
    return html





if __name__ == '__main__':
    app.run(debug=True)