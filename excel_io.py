import pandas as pd
import datetime
import os

from indices import get_symbol_historical_data_response
from datetime import date, datetime
from color_print import cprint
from constant import result_state_json, result_xlsx_path

def get_log():
    import json
    if not os.path.isfile(result_state_json):
        return None
    try:
        with open(result_state_json) as ifstream:
            res_dict = json.load(ifstream)
    except json.decoder.JSONDecodeError as e:
        cprint('fail')(e.msg + ': 文件内容无法解码为JSON')
        return None

    return res_dict

def write_log(write_dict):
    import json
    with open(result_state_json, "wb+") as ofstream:
        ofstream.write(json.dumps(write_dict).encode("utf-8"))

def get_current_dataframe():
    df = pd.read_excel(result_xlsx_path, sheet_name=0)
    return df

date_format = "%Y/%m/%d"
today_req_str = date.today().strftime(date_format)
cur_state_dict = get_log()
global cur_df 
cur_df = get_current_dataframe()
if cur_df.index.name != '代码':
    cur_df = cur_df.set_index('代码')
global cur_dft 
cur_dft = cur_df.T
global complete_update 
complete_update = False

def chinese_date_to_datetime(c_date_str):
    year_str = c_date_str.split('年')[0]
    month_str = c_date_str.split('年')[1].split('月')[0]
    day_str = c_date_str.split('月')[1].split('日')[0]
    return date(int(year_str), int(month_str), int(day_str))

def get_result_series(symbol, data_type='indices', start='2020/01/01', end=today_req_str):
    response = get_symbol_historical_data_response(symbol, data_type=data_type, st_date=start, end_date=end)
    if __name__ == "__main__":
        print(symbol + '...', end='')
        if response == None:
            cprint('fail')('No Such Symbol')
        elif (response.status_code == 200):
            cprint('ok')('OK')
        else:
            cprint('fail')(response.status_code)
    df = pd.read_html(response.text)[0]
    df['日期'] = df['日期'].map(chinese_date_to_datetime)
    df = df.iloc[::-1]
    df = df.set_index('日期')
    res_sr = df['收盘']
    res_sr.index = res_sr.index.map(lambda x : x.date() if isinstance(x, datetime) else x)
    return res_sr


def chinese_data_type_to_english(dt):
    assert isinstance(dt, str)
    if dt == '指数':
        return 'indices'
    elif dt == '个股':
        return 'stocks'
    elif dt == '期货':
        return 'commodities'
    else:
        return 'indices'

def get_start_dates(symbols, sheet_earlist_date):
    global prev_dict
    prev_dict = get_log()
    if (prev_dict == None 
            or prev_dict.get('GLOBAL_LOCAL') == None
            or date.fromisoformat(prev_dict['GLOBAL_LOCAL']) != sheet_earlist_date):
        global complete_update
        complete_update = True
        query_dates = map(lambda symbol : sheet_earlist_date, symbols)
    else:
        query_dates = map(lambda symbol: date.fromisoformat(prev_dict.get(symbol)) if prev_dict.get(symbol) != None else sheet_earlist_date, symbols)
    new_stamp_dates = map(lambda symbol : date.today().isoformat(), symbols)
    stamp_dict = dict(zip(symbols, new_stamp_dates))
    stamp_dict['GLOBAL_LOCAL'] = sheet_earlist_date.isoformat()
    res_dict = dict(zip(symbols, query_dates))
    write_log(stamp_dict)
    return res_dict
        

def get_query_results():
    symbol_list = cur_dft.columns.to_list()
    if __name__ == "__main__":
        print(type(symbol_list))
    earlist_date = date.fromisoformat(cur_dft.index.to_list()[2])
    print(earlist_date)
    start_date_dict = get_start_dates(symbol_list, earlist_date)
    res_dict = {}
    print(symbol_list)
    for symbol in symbol_list:
        start_date = start_date_dict[symbol]
        if start_date == date.today():
            continue
        series = cur_dft[symbol]
        data_type = chinese_data_type_to_english(series['种类'])
        res_dict[symbol] = get_result_series(symbol=str(symbol), data_type=data_type, start=start_date.strftime(date_format))
    return res_dict

def update_result_df():
    symbol_list = cur_dft.columns.to_list()
    res_dict = {}
    new_series_dict = get_query_results()
    ret_df = pd.DataFrame()
    if complete_update:
        new_dft = cur_dft[0:2]
    else:
        new_dft = cur_dft
    for symbol in symbol_list:
        cur_sr = new_dft[symbol]
        cur_sr.index = cur_sr.index.map(lambda x : x.date() if isinstance(x, datetime) else x)
        print(cur_sr)
        if symbol not in new_series_dict.keys():
            res_dict[symbol] = cur_sr[3:]
        elif prev_dict == None or symbol not in prev_dict:
            res_dict[symbol] = new_series_dict[symbol]
        else:
            res_dict[symbol] = cur_sr[3:].append(new_series_dict[symbol])
        res_dict[symbol] = res_dict[symbol].rename(symbol)
        print(res_dict[symbol])
    ret_df = pd.DataFrame.from_dict(res_dict)
    final_df = cur_dft[0:3].append(ret_df)
    return final_df

def main():
    print(complete_update)
    res_df = update_result_df()
    print(res_df)
    writer = pd.ExcelWriter(result_xlsx_path)
    res_df = res_df.T
    res_df.index.rename('代码', inplace=True)
    res_df.to_excel(writer, 'Sheet1')
    writer.save()
    writer.close()

if __name__ == "__main__":
    main()
