import requests


def get_pm25():
    columns, values = None, None
    try:
        url = 'https://data.epa.gov.tw/api/v2/aqx_p_02?api_key=e8dd42e6-9b8b-43f8-991e-b3dee723a52d&limit=1000&sort=datacreationdate%20desc&format=JSON'
        resp = requests.get(url)
        datas = resp.json()['records']
        columns = list(datas[0].keys())
        values = []
        for data in datas:
            values.append(list(data.values()))

    except Exception as e:
        print(e)

    return columns, values


# 只有在本地端輸出,引用module時不會顯示
if __name__ == '__main__':
    print(get_pm25())