import csv
import time
import requests

headers = {
    # 浏览器标识符
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/96.0.4664.45 Safari/537.36',
    # 防盗链
    'referer': 'https://www.bilibili.com/video/'
}


def get_response(url):
    """发送请求"""
    response = requests.get(url=url, headers=headers).json()
    return response


def parse_response(response):
    """对得到的json数据进行解析，选出评论"""

    for i in range(20):
        try:
            reply = response['data']['replies'][i]
            # 将评论时间的时间戳格式转为标准时间格式
            t = reply['ctime']
            timeArray = time.localtime(t)
            otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
            comment_dict = {
                "评论": reply['content']['message'].replace("\n", ""),
                '时间': otherStyleTime,
                '点赞数': reply['like']
            }
            fp.writerow(comment_dict)
        except Exception as e:
            print("本评论解析写入失败" + str(i) + str(e))


if __name__ == '__main__':

    oid = 586259038

    with open("评论.csv", mode="a", encoding='utf-8', newline="") as f:
        fp = csv.DictWriter(f, fieldnames=['评论', '时间', '点赞数'])
        fp.writeheader()  # 写入表头
        for next in range(10):
            url = f'https://api.bilibili.com/x/v2/reply/main?jsonp=jsonp&next={next}&type=1&oid={oid}&mode=3&plat=1'
            response = get_response(url)
            parse_response(response)