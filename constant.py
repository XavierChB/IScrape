import os
import pkg_resources

from color_print import cprint

path_prefix = '.'

chrome_prefix = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/"
chrome_suffix = " Safari/537.36"

global session_chrome_version
session_chrome_version = ""

if 'nt' in os.name:
    path_prefix = os.sep.join(('D:', 'Program Files (x86)', 'Investing-Python', 'IScrape'))
    chrome_prefix = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/"

cf_clearance_json_path = os.sep.join((path_prefix, 'local', 'cf_clearance.json'))
result_state_json = os.sep.join((path_prefix, 'local', 'result_state.json'))
browser_info_json = os.sep.join((path_prefix, 'local', 'brower_info.json'))
indices_csv_path = os.sep.join((path_prefix, 'resources', 'indices.csv'))
stocks_csv_path = os.sep.join((path_prefix, 'resources', 'stocks.csv'))
commodities_csv_path = os.sep.join((path_prefix, 'resources', 'commodities.csv'))
result_xlsx_path = os.sep.join((path_prefix, 'result', 'Result.xlsx'))

def update_browser_info(chromeVersion):
    import json
    write_dict = {'chromeVersion' : chromeVersion}
    with open(browser_info_json, "wb+") as ofstream:
        ofstream.write(json.dumps(write_dict).encode("utf-8"))

def get_chrome_user_agent():
    global session_chrome_version
    if session_chrome_version != "":
        chrome_version = session_chrome_version
    else:
        import json
        if not os.path.isfile(browser_info_json):
            return None
        try:
            with open(browser_info_json) as ifstream:
                res_dict = json.load(ifstream)
        except json.decoder.JSONDecodeError as e:
            cprint('fail')(e.msg + ': 文件内容无法解码为JSON')
            return None
        chrome_version = res_dict['chromeVersion']
        session_chrome_version = chrome_version
    res = chrome_prefix + chrome_version + chrome_suffix
    return res
