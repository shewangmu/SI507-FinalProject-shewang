import sqlite3
information = {}
title = {}
review = {}
name = ['macbook air', 'macbook pro', 'surface', 'thinkpad']
reflect = {'macbook air':'macbook_air', 'macbook pro':'macbook_pro', 
               'surface':'surface', 'thinkpad':'thinkpad'}

def init_info():
    conn = sqlite3.connect('computer.db')
    cur = conn.cursor()  
    for nm in name:
        statement = '''
            select Company, price,avg(review.Rating), basic_info from information
            inner join review on review.ProductId=information.Id
            where product_name='{}'
            group by information.Id
            '''.format(nm)
        cur.execute(statement)
        global information
        info = []
        for i in cur.fetchall():
            info.append([i[0],i[1],round(i[2],2),i[3]])
        information[reflect[nm]] = info
        
def init_title():
    conn = sqlite3.connect('computer.db')
    cur = conn.cursor()
    global title
    for nm in name:
        rev = [[],[],[],[],[]]
        for i in range(5):
            statement = '''
            select review.Title from review
            inner join information on information.Id = review.ProductId
            where information.product_name='{}'
            and review.Rating={}
            '''.format(nm, i+1)
            cur.execute(statement)
            for res in cur.fetchall():
                rev[i].append(res[0])
        max_length = 0
        for i in range(5):
            if(len(rev[i])>max_length):
                max_length=len(rev[i])
        for i in range(max_length):
            for j in range(5):
                try:
                    rev[j][i]
                except:
                    rev[j].append('')
        rev_refine = []
        for i in range(max_length):
            rev_refine.append([rev[0][i],rev[1][i],rev[2][i],rev[3][i],rev[4][i]])
        title[reflect[nm]] = rev_refine

def init_review():
    conn = sqlite3.connect('computer.db')
    cur = conn.cursor()
    for nm in name:
        rev = [[],[],[],[],[]]
        for i in range(5):
            statement = '''
            select review.Content from review
            inner join information on information.Id = review.ProductId
            where information.product_name='{}'
            and review.Rating={}
            '''.format(nm, i+1)
            cur.execute(statement)
            for res in cur.fetchall():
                rev[i].append(res[0])
        max_length = 0
        for i in range(5):
            if(len(rev[i])>max_length):
                max_length=len(rev[i])
        for i in range(max_length):
            for j in range(5):
                try:
                    rev[j][i]
                except:
                    rev[j].append('')
        rev_refine = []
        for i in range(max_length):
            rev_refine.append([rev[0][i],rev[1][i],rev[2][i],rev[3][i],rev[4][i]])
        review[reflect[nm]] = rev_refine

def get_info():
    global information
    return information

def get_title():
    global title
    return title

def get_content():
    global review
    return review
