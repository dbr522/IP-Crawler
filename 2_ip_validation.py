#coding=utf-8
#v0911 read csv and validate
import pandas as pd
import time
import math
import requests
import random
import os
from multiprocessing import Pool


headers = {'user-agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'}
num_workers = 8
path = 'G:\\unicom\\cell\\code\\v0911\\proxy\\'

def check_proxy(_param):
    print ('proxy validating...')
    proxy_list = _param[0]

    for proxy in proxy_list:
        time.sleep(random.randint(3,9))
        url = "http://www.baidu.com"
        proxy_handler = {'http': proxy, 'https': proxy}

        try:
            r = requests.get(url, headers=headers, proxies=proxy_handler, timeout=3)
            if r.status_code == 200:
                with open(path+'proxy_valid_temp.csv', 'a') as f:
                    f.write(proxy + '\n')
                print (proxy, 'good')

            else:
                print (proxy, 'bad')
        except Exception:
           print (proxy, 'error')
           pass


if __name__ == '__main__':
    while 1:
        
        df = pd.read_csv(path+'proxy_raw.csv', names=['proxy_info'])
        proxy_raw_list = df['proxy_info'].tolist()
        try:
            df1 = pd.read_csv(path+'proxy_valid.csv', names=['proxy_info'])
            proxy_valid_list = df1['proxy_info'].tolist()
        except:
            proxy_valid_list = []

        pool = Pool(processes=num_workers)

        test_proxy_list = list(set(proxy_valid_list+proxy_raw_list))

        eve = int(math.ceil(len(test_proxy_list) / float(num_workers)))
        paramList = []

        for i in range(num_workers):
            tempList = []
            tempList.append(test_proxy_list[i * eve:(i + 1) * eve])
            paramList.append(tempList)


        pool.map(check_proxy, paramList)
        
        valid_df = pd.read_csv(path+'proxy_valid_temp.csv', names=['proxy_info'])
        valid_df.to_csv(path+'proxy_valid.csv', index=False)
        print (time.asctime(), len(valid_df), 'valid ip checked')

        pool.terminate()
        os.remove(path+'proxy_valid_temp.csv')

        print (time.asctime(), 'sleeping...')
        time.sleep(300)


    
