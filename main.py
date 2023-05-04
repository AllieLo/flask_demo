from flask import Flask, render_template, request
from datetime import datetime
from pm25 import get_pm25, get_pm25_db, get_six_pm25, get_county_pm25
import json

# 透過Flask(類別)產生實體物件(主程式__name__)-->run server
app = Flask(__name__)

stocks = [
    {"分類": "日經指數", "指數": "22,920.30"},
    {"分類": "韓國綜合", "指數": "2,304.59"},
    {"分類": "香港恆生", "指數": "25,083.71"},
    {"分類": "上海綜合", "指數": "3,380.68"},
]

# 建立首頁：函式綁定網頁


@app.route("/update")
def update_db():
    import pm25_db

    return "資料庫更新成功"


@app.route("/pm25-charts")
def pm25_charts():
    return render_template("./pm25-charts-bulma.html")


@app.route("/pm25-data/<county>")
def get_county_pm25_data(county):
    result = get_county_pm25(county)
    datas = {
        "site": [data[0] for data in result],
        "pm25": [data[1] for data in result],
    }

    return json.dumps(datas, ensure_ascii=False)


@app.route("/pm25-six-data")
def get_six_pm25_data():
    result = get_six_pm25()
    datas = {
        "county": list(result.keys()),
        "pm25": list(result.values()),
    }

    return json.dumps(datas, ensure_ascii=False)


@app.route("/pm25-data", methods=["POST"])
def get_pm25_data():
    columns, values = get_pm25_db()

    datas = {"error": "連線錯誤!"}
    if values is not None:
        # 縣市
        county = [value[1] for value in values]
        # 站點名稱
        site = [value[0] for value in values]
        # pm2.5數值
        pm25 = [value[2] for value in values]

        # result = list(zip(site, pm25))
        # sorted_data = sorted(result, key=lambda x: x[-1])
        # print(sorted_data)

        result = list(zip(site, pm25))
        sorted_data = sorted(result, key=lambda x: x[-1])
        print(sorted_data)

        datas = {
            "county": county,
            "site": site,
            "pm25": pm25,
            "highest": sorted_data[-1],
            "lowest": sorted_data[0],
            "date": get_date(),
        }

    return json.dumps(datas, ensure_ascii=False)


@app.route("/pm25", methods=["GET", "POST"])
def pm25():
    if request.method == "GET":
        columns, values = get_pm25_db()
    # 單純使用GET才能這樣寫=>request.args.get(name)
    # if request.args.get('sort'):
    #     columns, values = get_pm25(True)
    if request.method == "POST":
        if request.form.get("sort"):
            columns, values = get_pm25_db(True)
        else:
            columns, values = get_pm25()

    print(columns, values)

    return render_template("./pm25.html", **locals())


@app.route("/stock")
def stock():
    return render_template("./stock.html", stocks=stocks, datetime=get_date())


@app.route("/index")
@app.route("/")  # @route-->首頁
def index():
    name = "guest"
    date = get_date()
    content = {"name": name, "date": date}
    return render_template("./index.html", content=content)


@app.route("/date")
def get_date():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


@app.route("/book")
@app.route("/book/<int:id>")
def get_book(id=None):
    try:
        books = {1: "HTML-Book", 2: "CSS-Book", 3: "JavaScript-Book"}
        if id is not None:
            return books[id]
        else:
            return books
    except Exception as e:
        print(e)
        return "<h2>查詢錯誤，請重新輸入</h2>"


if __name__ == "__main__":
    app.run(debug=True)
