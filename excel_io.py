import pandas as pd
import datetime
import os

from indices import get_symbol_historical_data_response
from datetime import date
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

def get_current_dataframe():
    df = pd.read_excel(result_xlsx_path, sheet_name=0)
    return df

date_format = "%Y/%m/%d"
today_req_str = date.today().strftime(date_format)
cur_state_dict = get_log()
cur_df = get_current_dataframe()
if cur_df.index.name != '代码':
    cur_df = cur_df.set_index('代码')

def chinese_date_to_datetime(c_date_str):
    year_str = c_date_str.split('年')[0]
    month_str = c_date_str.split('年')[1].split('月')[0]
    day_str = c_date_str.split('月')[1].split('日')[0]
    return date(int(year_str), int(month_str), int(day_str))

def get_result_series(symbol, data_type='indices', start='2020/01/01', end=today_req_str):
    print(today_req_str)
    response = get_symbol_historical_data_response(symbol, data_type=data_type, st_date=start, end_date=end)
    print(response)
    df = pd.read_html(response.text)[0]
    df['日期'] = df['日期'].map(chinese_date_to_datetime)
    df = df.iloc[::-1]
    df = df.set_index('日期')
    return df['收盘']

def main():
    print(chinese_date_to_datetime('2100年9月30日'))

if __name__ == "__main__":
    main()
