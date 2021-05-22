import requests
import json

import cloud_clearer as cc
import pandas as pd

from datetime import date

def get_stock_indice(code, start = '19910101', end='20210101'):
    url = 'https://q.stock.sohu.com/hisHq'
    param = {
            'code' : 'cn_' + str(code),
            'start' : start,
            'end' : '20210504'
            }
    res = requests.get(url, params=param).json()
    
def main():
    get_stock_indice('000001')

if __name__ == "__main__":
    main()
