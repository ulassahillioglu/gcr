from flask import Flask, render_template, request
from bs4 import BeautifulSoup
from finderClass import FacebookPostLinkExtractor
import requests
import re
import os


app = Flask(__name__)
link_extractor = FacebookPostLinkExtractor()

@app.route('/', methods=['GET', 'POST'])
def extract_facebook_post_link():
    if request.method == 'POST':
        link = request.form.get('url')
        post_link = link_extractor.get_facebook_post_link(link)
        return render_template('result.html', result=post_link)
    return render_template('index.html')

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == "__main__":
    server_port = os.environ.get('PORT', '8080')
    app.run(debug=False, port=server_port, host='0.0.0.0')


