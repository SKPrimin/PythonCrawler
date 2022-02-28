import json
import requests


def getdata():
    # 指定url 请求网址: http://scxk.nmpa.gov.cn:81/xk/itownet/portalAction.do?method=getXkzsList
    post_url = 'http://scxk.nmpa.gov.cn:81/xk/itownet/portalAction.do?method=getXkzsList'
    # UA伪装
    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36 Edg/96.0.1054.29"
    }
    listid = []
    msges = []
    # 设置翻页
    for page in range(1,6):
        # 处理url请求附带的表单数据
        data = {
            'on': 'true',
            'page': page,
            'pageSize': '15',
            'productName': '',
            'conditionType': '1',
            'applyname': '',
            'applysn': ''
        }
        # 发起请求，带3参数
        r = requests.post(url=post_url, headers=header,data=data)
        # 获取相应json格式数据
        dictdata = r.json()
        lidata = dictdata['list']

        for item in lidata:
            listid.append(item['ID'])
        print(listid)

    for id in listid:
        # 指定url 请求网址: 请求网址: http://scxk.nmpa.gov.cn:81/xk/itownet/portalAction.do?method=getXkzsById
        post_url = 'http://scxk.nmpa.gov.cn:81/xk/itownet/portalAction.do?method=getXkzsById'
        # 表单数据
        data = {
            'id': id
        }
        # 发起请求，带3参数
        msg = requests.post(url=post_url, headers=header, data=data).json()
        print(msg)
        msges.append(msg)

    with open("企业.json",'w',encoding='utf-8') as f:
        json.dump(msges,fp = f,ensure_ascii=False)


if __name__ == '__main__':
    getdata()
