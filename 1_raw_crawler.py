#coding=utf8
from bs4 import BeautifulSoup
import pandas as pd
import time
import requests
import sys

header = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.99 Safari/537.36"}


def get_html(url):
    
    html = requests.get(url, headers=header)
    return html.text


def get_soup(url):
    soup = BeautifulSoup(get_html(url))
    return soup


def fetch_kxdaili(page):
    """
    从www.kxdaili.com抓取免费代理
    """
    proxyes = []
    try:
        url = "http://www.kxdaili.com/dailiip/1/%d.html" % page
        soup = get_soup(url)
        table_tag = soup.find("table", attrs={"class": "ui table segment"})
        trs = table_tag.tbody.find_all("tr")
        for tr in trs:
            tds = tr.find_all("td")
            ip = tds[0].text
            port = tds[1].text
            latency = tds[4].text.split(" ")[0]
            if float(latency) < 3: # 输出延迟小于3秒的代理
                proxy = "%s:%s" % (ip, port)
                proxyes.append(proxy)
        print (len(proxyes), 'from kxdaili')
    except:
        print ("fail to fetch from kxdaili")
    return proxyes


def fetch_xici(page):
    """
    http://www.xicidaili.com/nn/
    """
    proxyes = []
    try:
        url = "http://www.xicidaili.com/nn/"+str(page)
        soup = get_soup(url)
        table = soup.find("table", attrs={"id": "ip_list"})
        trs = table.find_all("tr")
        for i in range(1, len(trs)):
            tr = trs[i]
            tds = tr.find_all("td")
            ip = tds[1].text
            port = tds[2].text
            speed = tds[6].div["title"][:-1]
            latency = tds[7].div["title"][:-1]
            if float(speed) < 3 and float(latency) < 3:
                proxyes.append("%s:%s" % (ip, port))
        print (len(proxyes), 'from xici')
    except:
        print ("fail to fetch from xici")
    return proxyes

def fetch_ip181():
    """
    http://www.ip181.com/
    """
    proxyes = []
    try:
        url = "http://www.ip181.com/"
        soup = get_soup(url)
        table = soup.find("table")
        trs = table.find_all("tr")
        for i in range(1, len(trs)):
            tds = trs[i].find_all("td")
            ip = tds[0].text
            port = tds[1].text
            latency = tds[4].text[:-2]
            if float(latency) < 3:
                proxyes.append("%s:%s" % (ip, port))
    except Exception as e:
        print ("fail to fetch from ip181: %s" % e)
    return proxyes

def fetch_httpdaili():
    """
    http://www.httpdaili.com/mfdl/
    更新比较频繁
    """
    proxyes = []
    try:
        url = "http://www.httpdaili.com/mfdl/"
        soup = get_soup(url)
        table = soup.find("div", attrs={"kb-item-wrap11"}).table
        trs = table.find_all("tr")
        for i in range(1, len(trs)):
            try:
                tds = trs[i].find_all("td")
                ip = tds[0].text
                port = tds[1].text
                #type = tds[2].text
                #if type == u"匿名":
                proxyes.append("%s:%s" % (ip, port))
            except:
                pass
        print (len(proxyes), 'httpdaili')
    except Exception as e:
        print ("fail to fetch from httpdaili: %s" % e)
    return proxyes

def fetch_66ip():
    """
    http://www.66ip.cn/
    每次打开此链接都能得到一批代理, 速度不保证
    """
    proxyes = []
    try:
        # 修改getnum大小可以一次获取不同数量的代理
        url = "http://www.66ip.cn/nmtq.php?getnum=50&isp=0&anonymoustype=3&start=&ports=&export=&ipaddress=&area=1&proxytype=0&api=66ip"
        content = get_html(url)
        urls = content.split("</script>")[-4].split("<br />")
        for u in urls:
            if u.strip():
                proxyes.append(u.strip())
        print (len(proxyes), 'from 66ip')
    except Exception as e:
        print ("fail to fetch from httpdaili: %s" % e)
    return proxyes[:99]

def fetch_all(endpage=3):
    proxyes = []
    proxyes += fetch_66ip()
    for i in range(1, endpage):
        proxyes += fetch_kxdaili(i)
        proxyes += fetch_xici(i)
    # proxyes += fetch_ip181()
    proxyes += fetch_httpdaili()
    
    ss = pd.Series(proxyes).drop_duplicates()
    ss.to_csv('G:\\unicom\\cell\\code\\v0911\\proxy\\proxy_raw.csv', index=False)

    print (time.asctime(), str(len(proxyes)), 'ip addresses crawled')


def main():
    while 1:
        fetch_all()
        time.sleep(600)


if __name__ == '__main__':
    main()
