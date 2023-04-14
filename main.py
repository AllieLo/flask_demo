from flask import Flask
from datetime import datetime

# 透過Flask(類別)產生實體物件(主程式__name__)-->run server
app = Flask(__name__)

# 建立首頁：函式綁定網頁


@app.route('/index')
@app.route('/')             # @route-->首頁
def index():
    return '<h1>Hello Flask!</h1>'


@app.route('/date')
def get_date():
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')


@app.route('/book/<id>')
def get_book(id):
    books = {1: "HTML-Book", 2: "CSS-Book", 3: "JavaScript-Book"}
    return books[id]


if __name__ == '__main__':
    app.run(debug=True)
