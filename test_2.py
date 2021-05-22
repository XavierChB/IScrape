import requests

head = {
    'Host' : 'cn.investing.com',
    'User-Agent' : 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:88.0) Gecko/20100101 Firefox/88.0',
    'Accept' : 'text/plain, */*; q=0.01',
    'Accept-Language' : 'en-US,en;q=0.5',
    'Accept-Encoding' : 'gzip, deflate, br',
    'Content-Type' : 'application/x-www-form-urlencoded',
    'X-Requested-With' : 'XMLHttpRequest',
    'Content-Length' : '245',
    'Origin' : 'https://cn.investing.com',
    'DNT' : '1',
    'Alt-Used' : 'cn.investing.com',
    'Connection' : 'keep-alive',
    'Referer' : 'https://cn.investing.com/indices/ftse-china-a50-historical-data',
    'Cookie' : 'cf_clearance=5c4687ac08a51fa3356153950b9eb8d5c076ac19-1621592323-0-150'
}

params = {
    'curr_id' : '28930',
    'smlID' : '2042582',
    'header' : '富时中国A50指数历史数据',
    'st_date' : '2021/04/20',
    'end_date' : '2021/05/20',
    'interval_sec' : 'Daily',
    'sort_col' : 'date',
    'sort_ord' : 'DESC',
    'action' : 'historical_data'
}

url = 'https://cn.investing.com/instruments/HistoricalDataAjax'
response = requests.post(url=url, headers=head, data=params)
print(response)
