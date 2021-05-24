import os
import pkg_resources

path_prefix = '.'

if 'nt' in os.name:
    path_prefix = os.sep.join(('D:', 'Program Files (x86)', 'Investing-Python', 'Investing-Scrape'))

cf_clearance_json_path = os.sep.join((path_prefix, 'local', 'cf_clearance.json'))
indices_csv_path = os.sep.join((path_prefix, 'resources', 'indices.csv'))
stocks_csv_path = os.sep.join((path_prefix, 'resources', 'stocks.csv'))
commodities_csv_path = os.sep.join((path_prefix, 'resources', 'commodities.csv'))
