import pandas as pd

# TODO: Change resources to absolute path
indices_df = pd.read_csv('resources/indices.csv')

def contains_lower_case(s):
    assert isinstance(s, str)
    for c in s:
        if c.islower():
            return True
    return False

def get_index_row(symbol):
    row = indices_df[indices_df['symbol'] == symbol]
    if row.empty:
        if contains_lower_case(symbol):
            row = indices_df[indices_df['symbol'] == "".join([c.upper() for c in symbol])]
        else:
            row = indices_df[indices_df['symbol'] == "".join([c.lower() for c in symbol])]
    return row

def get_indices_info(lst):
    res_dict = {}
    for symbol in lst:
        row = get_index_row(symbol)
        if row.empty:
            print("未能找到" + symbol + "请检查大小写")
            continue
        res_dict[symbol] = row
    return res_dict
