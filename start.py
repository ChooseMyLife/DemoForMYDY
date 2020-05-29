import requests
import re
import random
import chardet
import json
import time


def get_one_page(url):
    # my_headers = [
    #     "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36",
    #     "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36",
    #     "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:30.0) Gecko/20100101 Firefox/30.0",
    #     "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/537.75.14",
    #     "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Win64; x64; Trident/6.0)",
    #     'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11',
    #     'Opera/9.25 (Windows NT 5.1; U; en)',
    #     'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)',
    #     'Mozilla/5.0 (compatible; Konqueror/3.5; Linux) KHTML/3.5.5 (like Gecko) (Kubuntu)',
    #     'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.0.12) Gecko/20070731 Ubuntu/dapper-security Firefox/1.5.0.12',
    #     'Lynx/2.8.5rel.1 libwww-FM/2.14 SSL-MM/1.4.1 GNUTLS/1.2.9',
    #     "Mozilla/5.0 (X11; Linux i686) AppleWebKit/535.7 (KHTML, like Gecko) Ubuntu/11.04 Chromium/16.0.912.77 Chrome/16.0.912.77 Safari/535.7",
    #     "Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:10.0) Gecko/20100101 Firefox/10.0 "
    # ]
    # response = requests.get(
    #     url, headers={"User-Agent": random.choice(my_headers)})
    my_headers = {"User-Agent":
                  'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36'}
    cookies = {"uuid": 'de57f64af8884b5ba7e2.1590719565.1.0.0',
               "H_PS_PSSID": '31728_1439_31670_21091_31069_31596_31270_31464_31321_30824_26350', 'PSINO': '7',
               'H_BDCLCKID_SF': 'tRk8oK-atDvDqTrP-trf5DCShUFsWU4JB2Q-XPoO3KO1bqoO5Jjdht_pjxbQLtriW4jNLfbgylRp8P3y0bb2DUA1y4vpWj5-tgTxoUJ2X-JTeM7sqtnWhfkebPRiJPb9Qg-qahQ7tt5W8ncFbT7l5hKpbt-q0x-jLTnhVn0MBCK0hD0wDT8hD6PVKgTa54cbb4o2WbCQKJRd8pcN2b5oQTtnet59-R5raR7Z_JOsQJ6vOj6-5lOUWfAkXpJvQnJjt2JxaqRCBDQqhh5jDh3MBn8dbbnre4ROamby0hvctn3cShPCyUjrDRLbXU6BK5vPbNcZ0l8K3l02V-bIe-t2XjQhDHt8J50ttJ3aQ5rtKRTffjrnhPF3360rXP6-hnjy3b77Vlovb4QdDtj_j4bS34uUyecN-q3RymJ42-39LPO2hpRjyxv4X6K8D-oxJpOJX5Rm0U71HR7WDqnvbURvD--g3-AqBM5dtjTO2bc_5KnlfMQ_bf--QfbQ0hOhqP-jBRIEoC0XtK-hhCvPKITD-tFO5eT22-us5j7d2hcHMPoosIOSef5c5JKThfnZttJQQDjia664bfbUoqRHXnJi0btQDPvxBf7pBJc-op5TtUJM_PJJbhndqt4bht7yKMnitIv9-pPKWhQrh459XP68bTkA5bjZKxtq3mkjbPbDfn028DKuDjtBDT30DGR22Pc22KAX3RbEK4OMet_k-PnVq4tHepCqqnJZ5m7mXp0bWnvUM45CbTJ5KTLLharhQx7MMe5d0-DytCOkbCD6ej-MjjjM-Uv05-n2HD6bWRjbbn5KKROvhDTjh6P8hgceBtQm05bxohno3IQhfR3ajM8-5JIvXJQrKbTAXKvDVIDbWDcjqR8Zjju2D5QP'}
    response = requests.get(
        url, headers=my_headers, cookies=cookies)
    if (response.status_code == 200):
        return response.text
    return None


def parse_one_page(html):
    # pattern = re.compile(
    #     r'<i.*?>(\d+)</i><a.*?title="(.*?)".*?src="(.*?)".*?</a>.*?class="start">(.*?)</p>.*?class="releasetime">(.*?)</p>.*?<i\sclass="integer">(.*?)</i.*?class="fraction">(.*?)</i>')
    pattern = re.compile(
        r'<dd>.*?<i.*?>(\d+)</i>.*?<a.*?title="(.*?)".*?src="(.*?)".*?class="star">\n\s+(.*?)\n\s+</p>.*?time">(.*?)</p>.*?integer">(.*?)</i>.*?fraction">(.*?)</i>.*?</dd>', re.S)
    res = re.findall(pattern, html)
    for result in res:
        yield {
            "index": result[0], 'title': result[1], 'image': 'https:' +
            result[2], "actor": result[3], "time": result[4], 'score': result[5]+result[6]}


def write_to_file(content):
    with open('demo.txt', 'a', encoding='utf-8') as f:
        # print(type(json.dumps(content)))
        f.write(json.dumps(content, ensure_ascii=False)+'\n')


def main(offset):
    url = 'http://maoyan.com/board/4?offset='+str(offset)
    html = get_one_page(url)
    results = parse_one_page(html)
    for item in results:
        write_to_file(item)


if __name__ == "__main__":
    for i in range(10):
        main(offset=i * 10)
        time.sleep(1)
