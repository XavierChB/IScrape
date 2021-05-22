import cloud_clearance as cc
from cloud_clearance import bcolors
import requests
import indice_info as ii
import pandas as pd
from random import randint

def get_index_historical_data_response(code, st_date='2020/01/01', end_date='2021/01/01'):
    assert isinstance(code, str)
    row_df = ii.get_index_row(code)
    assert isinstance(row_df, pd.core.frame.DataFrame)
    if row_df.empty:
        return None

    id_ = int(row_df["id"].values[0])

    head = {
        'Host' : 'cn.investing.com',
        "User-Agent" : "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36",
        'Accept' : 'text/plain, */*; q=0.01',
        'Accept-Language' : 'en-US,en;q=0.5',
        'Accept-Encoding' : 'gzip, deflate',
        'Content-Type' : 'application/x-www-form-urlencoded',
        'X-Requested-With' : 'XMLHttpRequest',
        'Origin' : 'https://cn.investing.com',
        'DNT' : '1',
        'Alt-Used' : 'cn.investing.com',
        'Connection' : 'keep-alive',
        'Referer' : 'https://cn.investing.com/indices/' + row_df['tag'].values[0] + '-historical_data',
        'Cookie' : 'cf_clearance=' + cc.get_cf_clearance(),
    }

    params = {
        'curr_id' : id_,
        'smlID' : str(randint(1000000, 9999999)),
        'st_date' : st_date,
        'end_date' : end_date,
        'interval_sec' : 'Daily',
        'sort_col' : 'date',
        'sort_ord' : 'DESC',
        'action' : 'historical_data'
    }

    url = 'https://cn.investing.com/instruments/HistoricalDataAjax'
    response = requests.post(url=url, headers=head, data=params)
    print(response)
    return response

def main():
    index_list = [
            'SSEC', 'SZI', 'ftxin9', 'china50', 'HSI', 'DE30'
            ]

    for symbol in index_list:
        response = get_index_historical_data_response(symbol)
        if response == None:
            continue
        print(symbol + ':', end='')
        print(response.status_code, end='')
        if (response.status_code == 200):
            print(f' {bcolors.OKGREEN}OK{bcolors.ENDC}')
        df = pd.read_html(response.text)
        print(df)

if __name__ == "__main__":
    main()
