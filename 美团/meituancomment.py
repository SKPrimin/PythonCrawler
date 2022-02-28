import pprint
import time
import requests
import csv


def requestCommentTags(id, page):
    url = 'https://www.meituan.com/meishi/api/poi/getMerchantComment?'
    # userid为自己的用户名
    # limit 为一次请求数据，一次10条
    # offset为偏移量，类似于页数
    # id 为店铺id
    param = {
        'uuid': 'f79f1498663140408d8d.1638116128.1.0.0',
        'platform': '1',
        'partner': '126',
        'originUrl': f'https://www.meituan.com/meishi/{id}/',
        'riskLevel': '1',
        'optimusCode': '10',
        'id': id,
        'userId': '2726751799',
        'offset': page * 10,
        'pageSize': '10',
        'sortType': '1',
    }
    # User-Agent:表示浏览器基本信息
    # Cookie: 用户信息，检测是否有登陆账号
    # Referer: 防盗链，从哪里跳转过来的请求url，相当于定位地址
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36',
        'Cookie': '_lxsdk_cuid=17d6587cf7cc8-02e3e6cf56a023-978183a-144000-17d6587cf7dc8; mtcdn=K; _hc.v=5e95310f-3c0a-8221-4070-2b354eb7f667.1638086371; ci=56; rvct=56%2C70; uuid=f79f1498663140408d8d.1638116128.1.0.0; _lx_utm=utm_source%3Dbing%26utm_medium%3Dorganic; userTicket=TlqDASPHrgUhoKvFXxFYHFwmmsZHfePXKAusSzPV; _lxsdk=17d6587cf7cc8-02e3e6cf56a023-978183a-144000-17d6587cf7dc8; lt=c7ANwxLVVDdZxyRxgZDevu2YkWkAAAAAVg8AALaEhZLD95Psq57O81X-GTAgsugFSS12myMeqbXkg4S93GWSRESb6V1uQXBRO2SyKg; u=2726751799; n=%E9%87%8A%E6%B6%A6202; token2=c7ANwxLVVDdZxyRxgZDevu2YkWkAAAAAVg8AALaEhZLD95Psq57O81X-GTAgsugFSS12myMeqbXkg4S93GWSRESb6V1uQXBRO2SyKg; unc=%E9%87%8A%E6%B6%A6202; client-id=12d63750-0f72-4eda-8419-f9f872f97eaf; lat=31.775631; lng=117.206641; firstTime=1638189439496; _lxsdk_s=17d6b9650d9-7ce-dce-c0f%7C%7C52',
        'Referer': f'https://www.meituan.com/meishi/{id}/',
    }
    try:
        # 将参数、表头加载后发送请求
        response = requests.get(url=url, params=param, headers=header)
        # 反馈的数据进行json格式解析
        data_json = response.json()
        pprint.pprint(data_json)  # 标准格式打印 使用时需要import pprint
        return data_json
    except Exception as e:
        print("requests请求失败" + str(e))


def parseComment(data):
    """对得到的json数据进行解析，选出评论"""
    try:
        # 根据此前对数据的分析结果，searchResult值 位于data字典中，是一个列表形式数据
        comments = data['data']['comments']
        # 对searchResult列表进行索引解析，其内容是以字典形式存放，我们提取时也以字典存储
        for item in comments:
            comments_dict = {
                '评论内容': item['comment'],
                '购买商品': item['menu'],
                '星级': item['star'],
            }
            # 逐行立刻写入数据，以防出错导致的前功尽弃，同样是依照字典进行
            commentpencil.writerow(comments_dict)
        total = data['data']['total']
        return total
    except Exception as e:
        print("评论数据解析失败" + str(e))


def parseTags(data, shopName):
    """对得到的json数据进行解析，选出评论"""
    try:
        tags = data['data']['tags']
        for tag in tags:
            tags_dict = {
                '店铺': shopName,
                '标签': tag['tag'],
                '数量': tag['count']
            }
            tagpencil.writerow(tags_dict)

    except Exception as e:
        print("标签数据解析失败" + str(e))


if __name__ == '__main__':
    shops = {1088411800: '古茗（蜀山安大店）', 1479103527: '书亦烧仙草（簋街大学城店）', 1616840469: '茶百道（大学城店）'}
    for shopId in shops.keys():
        shopName = shops[shopId]
        with open("{}.csv".format(shopName), mode="a", encoding='utf-8', newline="") as f, open("商店标签信息.csv", mode="a",
                                                                                                encoding='utf-8',
                                                                                                newline="") as tf:
            commentpencil = csv.DictWriter(f, fieldnames=['评论内容', '购买商品', '星级'])
            commentpencil.writeheader()  # 写入表头
            tagpencil = csv.DictWriter(tf, fieldnames=['店铺', '标签', '数量'])
            tagpencil.writeheader()  # 写入表头

            # 进行第一页获取
            jsdata = requestCommentTags(id=shopId, page=0)
            # 得到总评论数
            total = parseComment(jsdata)
            # 解析其tags，一家店铺仅需一次
            parseTags(jsdata, shopName)

            pages = int(total / 10)
            # 进行其他页数获取
            for i in range(1, pages):
                # 暂停三秒，模拟人浏览页面正常翻页
                time.sleep(3)
                parseComment(requestCommentTags(id=shopId, page=i))
