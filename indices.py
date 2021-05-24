import requests
import symbol_resolve as sr
import pandas as pd
import cloud_clearer as cc

from random import randint
from color_print import cprint
from constant import chrome_user_agent
from datetime import date

def get_symbol_historical_data_response(code, data_type='indices', st_date='2020/01/01', end_date=date.today().strftime('%Y/%m/%d')):
    assert isinstance(code, str)

    if 'cid' in code:
        code_split_list = code.split('?', 1)
        item = code_split_list[0]
        cid_str = code_split_list[1]
        id_ = cid_str.split('=', 1)[1]
        referer = '/'.join(('https://cn.investing.com', data_type, item + '-historical-data' + cid_str))
    elif data_type != "stocks" and data_type != "indices":
        row_df = sr.get_tag_row(code, data_type=data_type)
        assert isinstance(row_df, pd.core.frame.DataFrame)
        if row_df.empty:
            return None
        id_ = row_df['id'].values[0]
        referer = '/'.join(('https://cn.investing.com', data_type, code + '-historical_data'))
    else:
        row_df = sr.get_symbol_row(code, data_type=data_type)
        assert isinstance(row_df, pd.core.frame.DataFrame)
        if row_df.empty:
            return None
        id_ = row_df['id'].values[0]
        referer = '/'.join(('https://cn.investing.com', data_type, row_df['tag'].values[0] + '-historical_data'))

    head = {
        'Host' : 'cn.investing.com',
        "User-Agent" : chrome_user_agent,
        'Accept' : 'text/plain, */*; q=0.01',
        'Accept-Language' : 'en-US,en;q=0.5',
        'Accept-Encoding' : 'gzip, deflate',
        'Content-Type' : 'application/x-www-form-urlencoded',
        'X-Requested-With' : 'XMLHttpRequest',
        'Origin' : 'https://cn.investing.com',
        'DNT' : '1',
        'Alt-Used' : 'cn.investing.com',
        'Connection' : 'keep-alive',
        # 'Referer' : '' + data_type + '/' + row_df['tag'].values[0] + '-historical_data',
        'Referer' : referer,
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
    # print(response)
    return response

def main():
    from symbol_resolve import stocks_df, indices_df
    index_list = [
            'SSEC', 'SZI', 'ftxin9', 'china-a50', 'HSI', 'DJI', 'SPX', 'FCHI', 'N225', 'KS50', 'STOXX50E'
            ]
    stocks_list = [
            '600000', '600519', 'TSLA', 'BABA', '300750', '002737', '601127'
            ]
    commodities_list = [
            'copper?cid=959211', 'copper', 'lead?cid=959207', 'london-cocoa', 'london-coffee', 'live-cattle', 'nickel?cid=959208', 'nickel?cid=996730', 'nickel', 'aluminum', 'aluminum?cid=996726'
            ]

    for symbol in index_list:
        response = get_symbol_historical_data_response(symbol)
        print(symbol + '...', end='')
        if response == None:
            cprint('fail')('No Such Symbol')
            continue
        elif (response.status_code == 200):
            cprint('ok')("OK")
        else:
            cprint('fail')(response.status_code)
        df = pd.read_html(response.text)
        print(df[0]['收盘'])
    
    for symbol in stocks_list:
        response = get_symbol_historical_data_response(symbol, data_type='stocks')
        print(symbol + '...', end='')
        if response == None:
            cprint('fail')('No Such Symbol')
            continue
        elif (response.status_code == 200):
            cprint('ok')("OK")
        else:
            cprint('fail')(response.status_code)
        df = pd.read_html(response.text)
        print(stocks_df[stocks_df['symbol'] == symbol]['full_name'].values[0])
        print(df[0]['收盘'])

    for symbol in commodities_list:
        response = get_symbol_historical_data_response(symbol, data_type='commodities')
        print(symbol + '...', end='')
        if response == None:
            cprint('fail')('No Such Symbol')
            continue
        elif (response.status_code == 200):
            cprint('ok')("OK")
        else:
            cprint('fail')(response.status_code)
        df = pd.read_html(response.text)
        print(df[0]['收盘'])

if __name__ == "__main__":
    main()
