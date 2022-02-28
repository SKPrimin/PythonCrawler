import csv
import requests


def requestData(q,page):
    url = 'https://apimobile.meituan.com/group/v4/poi/pcsearch/56?'
    # userid为自己的用户名
    # limit 为一页请求数据，一页32条
    # offset为偏移量，类似于页数
    # q 为搜索项
    param = {
        'uuid': 'b1d19fbc950e4175a832.1638085938.1.0.0',
        'userid': '2726751799',
        'limit': '32',
        'offset': (page-1)*32,
        'cateId': '-1',
        'q': q,
        'token': 'tqTeHG29SRck00XjcYT82vKTs5cAAAAAVg8AAC6VkLIXcxDxsY2-VHKrCpj1Al4GUi2xyRDJEmvhwA2VUbhGObb90a4c-zpWh3LDsA',
    }
    # User-Agent:表示浏览器基本信息
    # Cookie: 用户信息，检测是否有登陆账号
    # Referer: 防盗链，从哪里跳转过来的请求url，相当于定位地址
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36',
        'Cookie': '_lxsdk_cuid=17d6587cf7cc8-02e3e6cf56a023-978183a-144000-17d6587cf7dc8; mtcdn=K; _hc.v=5e95310f-3c0a-8221-4070-2b354eb7f667.1638086371; ci=56; rvct=56%2C70; uuid=f79f1498663140408d8d.1638116128.1.0.0; _lx_utm=utm_source%3Dbing%26utm_medium%3Dorganic; userTicket=TlqDASPHrgUhoKvFXxFYHFwmmsZHfePXKAusSzPV; lt=tqTeHG29SRck00XjcYT82vKTs5cAAAAAVg8AAC6VkLIXcxDxsY2-VHKrCpj1Al4GUi2xyRDJEmvhwA2VUbhGObb90a4c-zpWh3LDsA; u=2726751799; n=%E9%87%8A%E6%B6%A6202; token2=tqTeHG29SRck00XjcYT82vKTs5cAAAAAVg8AAC6VkLIXcxDxsY2-VHKrCpj1Al4GUi2xyRDJEmvhwA2VUbhGObb90a4c-zpWh3LDsA; unc=%E9%87%8A%E6%B6%A6202; _lxsdk=17d6587cf7cc8-02e3e6cf56a023-978183a-144000-17d6587cf7dc8; firstTime=1638159465212; _lxsdk_s=17d69e6c02c-e27-51b-83c%7C%7C52',
        'Referer': 'https://hf.meituan.com/',
    }
    try:
        # 将参数、表头加载后发送请求
        response = requests.get(url=url, params=param, headers=header)
        # 反馈的数据进行json格式解析
        data_json = response.json()
        # pprint.pprint(datajson) # 标准格式打印 使用时需要import pprint
        return data_json
    except Exception as e:
        print("requests请求失败" + str(e))


def parseData(data):
    """对得到的json数据进行解析"""
    # 根据此前对数据的分析结果，searchResult值 位于data字典中，是一个列表形式数据
    searchResult = data['data']['searchResult']
    try:
        # 对searchResult列表进行索引解析，其内容是以字典形式存放，我们提取时也以字典存储
        for item in searchResult:
            data_dict = {
                '店铺名': item['title'],
                '店铺所在位置': item['areaname'],
                '人均消费': item['avgprice'],
                '评分': item['avgscore'],
                '美食名称': item['backCateName'],
                '店铺图片链接': item['imageUrl'],
                '纬度': item['latitude'],
                '经度': item['longitude'],
                '最低价格': item['lowestprice'],
                '店铺ID': item['id'],
                '店铺详情页': f'https://www.meituan.com/meishi/{item["id"]}/'
            }
            # 逐行立刻写入数据，以防出错导致的前功尽弃，同样是依照字典进行
            csvpencil.writerow(data_dict)
    except Exception as e:
        print("数据解析失败" + str(e))


if __name__ == '__main__':
    q = "奶茶"
    with open("{}.csv".format(q), mode="a", encoding='utf-8', newline="") as f:
        csvpencil = csv.DictWriter(f, fieldnames=['店铺名', '店铺所在位置', '人均消费', '评分', '美食名称', '店铺图片链接',
                                                  '纬度', '经度', '最低价格', '店铺ID', '店铺详情页'])
        csvpencil.writeheader()  # 写入表头
        # 搜索的页数
        for i in range(9):
            parseData(requestData(q=q,page=i))
