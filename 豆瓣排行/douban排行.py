import csv
import json
import requests


def getdata(i):
    # 指定url 请求网址: https://movie.douban.com/j/chart/top_list?type=4&interval_id=100%3A90&action=&start=0&limit=1
    post_url = 'https://movie.douban.com/j/chart/top_list'
    # UA伪装
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36 Edg/96.0.1054.29"
    }
    # 处理url所带的参数，封装到字典 type类型 4为历史 start获得元素起始点 limit限制，相当于获取元素终点
    param = {
        'type': 4,
        'interval_id': '100:90',
        'action': '',
        'start': i*20,
        'limit': 20
    }
    # 发起请求，带3参数
    r = requests.get(url=post_url, params=param, headers=headers)
    print(r.url)
    # 获取相应json格式数据
    lidata = r.json()
    print(lidata)
    # 数据存储
    with open('douban.json', 'w', encoding='utf-8') as f:
        json.dump(lidata, fp=f, ensure_ascii=False)
    return lidata

def download(data):
    for item in data:
        film_dict = {
            '电影名': item['title'],
            '评分': item['score'],
            '发布日期':item['release_date'],
            '地区':item['regions'],
            '类型': item['types'],
            '投票数':item['vote_count'],
            '演员数':item['actor_count'],
            '演员':item['actors']
        }
        fp.writerow(film_dict)


if __name__ == '__main__':

    with open("电影排行榜.csv",mode='w',encoding='utf-8',newline="") as f:
        fp = csv.DictWriter(f,fieldnames=['电影名','评分','发布日期','地区','类型','投票数','演员数','演员'])
        fp.writeheader()  # 写入表头
        for i in range(2):
            data = getdata(i)
            download(data)
