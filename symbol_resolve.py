import pandas as pd

from constant import indices_csv_path, commodities_csv_path, stocks_csv_path

indices_df = pd.read_csv(indices_csv_path)
commodities_df = pd.read_csv(commodities_csv_path)
stocks_df = pd.read_csv(stocks_csv_path)

def contains_lower_case(s):
    assert isinstance(s, str)
    for c in s:
        if c.islower():
            return True
    return False

def get_symbol_row(symbol, data_type='indicies'):
    if data_type == 'indicies':
        cur_df = indices_df
    elif data_type == 'stocks':
        cur_df = stocks_df
    else:
        cur_df = indices_df

    search_key = 'symbol'

    row = cur_df[cur_df[search_key] == symbol]
    if row.empty:
        if contains_lower_case(symbol):
            row = cur_df[cur_df[search_key] == "".join([c.upper() for c in symbol])]
        else:
            row = cur_df[cur_df[search_key] == "".join([c.lower() for c in symbol])]
    return row

def get_tag_row(tag, data_type='commodities'):
    if data_type == 'commodities':
        cur_df = commodities_df
    else:
        cur_df = commodities_df

    search_key = 'tag'
    row = cur_df[cur_df[search_key] == tag]
    if row.empty:
        if contains_lower_case(tag):
            row = cur_df[cur_df[search_key] == "".join([c.upper() for c in tag])]
        else:
            row = cur_df[cur_df[search_key] == "".join([c.lower() for c in tag])]
    return row
