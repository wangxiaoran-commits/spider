import csv
import warnings
from datetime import datetime

import pytz
import requests
from bs4 import BeautifulSoup
from loguru import logger
import os

warnings.filterwarnings('ignore')

headers = {
    "authority": "search.prod.di.api.cnn.io",
    "method": "GET",
    "path": "/content?q=china&size=10&from=0&page=1&sort=newest&request_id=pdx-search-5ff743cf-fd07-4050-b6a7-4155fe2f8579",
    "scheme": "https",
    "accept": "*/*",
    "accept-encoding": "gzip, deflate, br",
    "accept-language": "zh-CN,zh;q=0.9",
    "cache-control": "no-cache",
    "origin": "https://www.cnn.com",
    "pragma": "no-cache",
    "referer": "https://www.cnn.com/search?q=china",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "cross-site",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36"
}


def datetime_convert_and_check(utc_time_str):
    # Handling both cases with or without microseconds
    formats = ['%Y-%m-%dT%H:%M:%S.%fZ', '%Y-%m-%dT%H:%M:%SZ']

    # Attempt to parse the time data using different formats
    for fmt in formats:
        try:
            utc_time = datetime.strptime(utc_time_str, fmt)
        except ValueError:
            pass
        else:
            break
    else:
        # If none of the formats match, raise an error
        raise ValueError(f"Invalid time data: {utc_time_str}")

    # 将UTC时间转换为北京时间
    beijing_timezone = pytz.timezone('Asia/Shanghai')
    beijing_time = utc_time.astimezone(beijing_timezone)

    # 定义目标时间字符串格式
    target_format = '%Y-%m-%d %H:%M:%S %Z%z'

    # 将北京时间转换为指定格式的字符串
    beijing_time_str = beijing_time.strftime(target_format)
    return beijing_time_str


def save_data(dic_data, file_name):
    file_name = f'{file_name}.csv'
    file_exists = os.path.exists(file_name)
    fieldnames = list(dic_data.keys())

    with open(file_name, mode='a' if file_exists else 'w', newline='', encoding='utf-8-sig') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        if not file_exists:
            writer.writeheader()  # 写入标题行，仅在文件不存在时执行
        writer.writerow(dic_data)
    return


def get_items(word, number):
    url = r'https://search.prod.di.api.cnn.io/content?'
    params = {
        'q': word,
        'from': int(50*int(number)),
        'size': 50,
        'page': number,
        'sort': 'newest',
        'request_id': 'pdx-search-5980dc21-25e3-4c74-8055-bb792539899c',
    }
    response = requests.get(url, params=params, headers=headers)
    result = response.json()['result']
    return result


def get_data(search_info):
    new_url = search_info['链接']
    res = requests.get(url=new_url, headers=headers, proxies=proxies)
    soup = BeautifulSoup(res.text)
    if soup.find('div', class_='article__content-container'):
        table = soup.find('div', class_='article__content-container')
        elements = table.find_all('p')
        txt = "\n".join([e.text for e in elements])
        try:
            authors = soup.find('div', class_="byline__names").text.strip()
        except:
            authors = ''
    elif soup.find('div', {'data-editable': 'description'}):
        table = soup.find('div', {'data-editable': 'description'})
        txt = table.text.strip()
        authors = ''
    else:
        txt = ''
        authors = ''
    search_info['文章'] = txt
    search_info['作者'] = authors
    save_data(dic_data=search_info, file_name='CNN NEWS')
    logger.info(f'已保存{search_info["标题"]}')
    return search_info


if __name__ == '__main__':
    proxies = {'http': 'http://127.0.0.1:10090', 'https': 'http://127.0.0.1:10090'}
    keyword = '2023 Ukraine civilian'
    for i in range(20):
        infos = get_items(keyword, i)
        for item in infos:
            if item['type'] == 'NewsArticle':
                info = {'来源': 'CNN', '标题': item['headline'],
                        '发布时间': datetime_convert_and_check(utc_time_str=item['lastModifiedDate']),
                        '链接': item.get('url', '')}
                if info['链接']:
                    get_data(info)
