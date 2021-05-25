import os
import pkg_resources

path_prefix = '.'

chrome_user_agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36"

if 'nt' in os.name:
    path_prefix = os.sep.join(('D:', 'Program Files (x86)', 'Investing-Python', 'IScrape'))
    chrome_user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36"

cf_clearance_json_path = os.sep.join((path_prefix, 'local', 'cf_clearance.json'))
result_state_json = os.sep.join((path_prefix, 'local', 'result_state.json'))
indices_csv_path = os.sep.join((path_prefix, 'resources', 'indices.csv'))
stocks_csv_path = os.sep.join((path_prefix, 'resources', 'stocks.csv'))
commodities_csv_path = os.sep.join((path_prefix, 'resources', 'commodities.csv'))
result_xlsx_path = os.sep.join((path_prefix, 'result', 'Result.xlsx'))
