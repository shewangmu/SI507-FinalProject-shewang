from flask import Flask,render_template
import model

app = Flask(__name__)

@app.route('/')
def index():
    html = '''
    <link rel="stylesheet" href="/static/style.css">
    <h1 align="center"> About this site</h1>
    <p> I fetch some data about the information of some computers from bestbuy and amazon.</p>
    <p>The information includes the basic information about the computer and the reviews 
    of customers.</p>
    <p>The computer type you can select is listed below</p>
    <a href='/macbook_pro'> macbook Pro </a>
    <br> </br>
    <a href='/macbook_air'> macbook Air </a>
    <br> </br>
    <a href='/surface'> surface </a>
    <br> </br>
    <a href='/thinkpad'> ThinkPad </a>
    '''
    return html

@app.route('/<nm>')
def product_info(nm):
    reflect = {'macbook_air':'Macbook Air', 'macbook_pro':'Macbook Pro', 
               'surface':'Surface', 'thinkpad':'Thinkpad'}
    html = render_template('product.html', product=reflect[nm], information=model.get_info()[nm])
    html += '<h3>The histogram of rating</h3>'
    html += '<img src="/static/rating_histgram_{}.png" width="600" height="400">'.format(nm)
    html += '<h3> The change of average rating through time</h3>'
    html += '<img src="/static/rating_time_{}.png" width="600" height="400">'.format(nm)
    html += '<h3> The tile of reviews of different ratings</h3>'
    html += '<a href="/{}/review">Reviews</a>'.format(nm)
    html += '<br></br><a href="/"> Return Home</a>'
    return html

@app.route('/<nm>/review')
def review_title(nm):
    reflect = {'macbook_air':'Macbook Air', 'macbook_pro':'Macbook Pro', 
               'surface':'Surface', 'thinkpad':'Thinkpad'}
    html = render_template('title.html', nm=nm, product = reflect[nm], review=model.get_title()[nm])
    return html

@app.route('/<nm>/details')
def review_content(nm):
    reflect = {'macbook_air':'Macbook Air', 'macbook_pro':'Macbook Pro', 
               'surface':'Surface', 'thinkpad':'Thinkpad'}
    html = render_template('content.html', product = reflect[nm], review=model.get_content()[nm])
    return html



if __name__ == '__main__':
    model.init_info()
    model.init_title()
    model.init_review()
    app.run(debug=True)