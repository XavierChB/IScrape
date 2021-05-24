import requests
import time
import os

from datetime import datetime
from color_print import cprint
from constant import cf_clearance_json_path

local_json_path = cf_clearance_json_path
full_path = os.sep.join((os.getcwd(), local_json_path))

debug = False

# Fix: use absolute path in windows to access files
if os.name == 'nt':
    full_path = local_json_path

def print_dict(dict):
    print("{:<10} {:<10}".format("NAME", "VALUE"))
    for key, value in dict.items():
        print("{:<10} {:<10}".format(key, value))

def get_log():
    import json
    if not os.path.isfile(local_json_path):
        return None
    try:
        with open(local_json_path) as ifstream:
            res_dict = json.load(ifstream)
    except json.decoder.JSONDecodeError as e:
        cprint('fail')(e.msg + ': 文件内容无法解码为JSON')
        return None

    return res_dict

def read_log(key):
    log = get_log()
    if log == None:
        return log
    return log.get(key)

def write_log(write_dict):
    import json
    with open(local_json_path, "wb+") as ofstream:
        ofstream.write(json.dumps(write_dict).encode("utf-8"))

def test_clearance(cf_clearance):
    import requests
    cprint('header')("测试Cloudflare密钥连通性...", end='', flush=True)
    head = {
        "Host" : "cn.investing.com",
        "User-Agent" : "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36",
        "Accept" : "text/plain, */*; q=0.01",
        "Accept-Language" : "en-US,en;q=0.5",
        "Accept-Encoding" : "gzip, deflate",
        "Content-Type" : "application/x-www-form-urlencoded",
        "X-Requested-With" : "XMLHttpRequest",
        "Origin" : "https://cn.investing.com",
        "DNT" : "1",
        "Connection" : "keep-alive",
        "Cookie" : 'cf_clearance=' + cf_clearance,
        "TE" : "Trailers",
    }

    url = "https://cn.investing.com"
    response = requests.get(url, headers=head)
    request_successful = (response.status_code == 200)
    if request_successful:
        cprint('ok')("OK")
        log_dict = get_log()
        log_dict['last_verified'] = int(datetime.now().timestamp())
        write_log(log_dict)
    else:
        cprint('fail')("COOKIE INVALID")
    return request_successful

def get_cf_clearance(force_reload=False):
    """
    This function retrievs the cf_clearance from cn.investing.com.
    Subsequent queries can set "cf_clearance=" + get_cf_clearance()
    to obtain 
    """
    import json
    # Obtain cf_clearance history
    res_dict = get_log()
    # If last cf_clearance was obtained 50 minuts ago // test 36000
    if res_dict != None and not force_reload:
        if ((res_dict.get('last_verified') != None
                and datetime.now().timestamp() - res_dict.get('last_verified') < 30)
                or test_clearance(res_dict.get('value'))):

            res = res_dict.get('value')
            # if debug:
                # print("Cloudflare密钥在有效时间内，直接输出:")
                # print(res)
            return res

    # If not, use undetected_chromedriver to obtain
    cprint('warning')(f"Cloudflare密钥已失效或本地存储({full_path})不存在/损坏")
    import undetected_chromedriver.v2 as uc
    from selenium.webdriver.chrome.options import Options
    options = Options()
    options.page_load_strategy = 'eager'

    print("正在创建Chrome进程...", end='', flush=True)
    driver = uc.Chrome(options=options)
    cprint('ok')("OK")

    url = 'https://cn.investing.com'
    print("正在打开" + url + "...", end='', flush=True)
    with driver:
        driver.get(url)
    cprint('ok')("OK")

    while driver.current_url == url:
        time.sleep(1)

    print("正在获取Cookie: cf_clearance...", end = '', flush=True)
    clearance_dict = driver.get_cookie("cf_clearance")
    cprint('ok')("OK")
    print(driver.current_url)
    driver.quit()
    clearance_dict['timestamp'] = int(datetime.now().timestamp())
    print_dict(clearance_dict)

    # Store result into json
    write_log(clearance_dict)
    res = clearance_dict['value']
    print("已获取Cloudflare密钥: " + res)
    print(f"结果保存至{full_path}")
    return res

def main():
    cprint('header')("Test: Remove local storage and test obtaining the key")
    if os.path.isfile(local_json_path):
        os.remove(local_json_path)
    print(get_cf_clearance())
    cprint('header')("Test: Get keys stored locally")
    print(get_cf_clearance())
    cprint('header')("Test: Repeat keys")
    start_time = datetime.now().timestamp()
    times = 10000
    for _ in range(times):
        print(get_cf_clearance())
    end_time = datetime.now().timestamp()
    result_str = " ".join(("Repeating", str(times), 'times took', str(end_time - start_time), 'seconds.'))
    print(result_str)
    cprint('header')("Test: Tampered JSON")
    with open(local_json_path, 'a') as ifstream:
        ifstream.write("hahahaha imma tamper this json like you know wut")
    print(get_cf_clearance())

if __name__ == "__main__":
    debug = True
    main()
