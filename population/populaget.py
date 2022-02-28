from lxml import etree
from openpyxl import Workbook
import requests


def getdownload(url):
    # UA伪装
    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36 Edg/96.0.1054.29"
    }
    # 发起请求，带3参数
    r = requests.get(url=url, headers=header)
    # 将编码格式调成gb2312
    r.encoding = "gb2312"
    # 转成文本文件
    htm_text = r.text
    # 将文件本地保存下来，同时类型修改为html，编码格式改为utf-8 本文件仅做临时保存用，数据会储存在csv文件中
    with open("tmp.html", 'w', encoding='utf-8') as f:
        f.write(htm_text)


def getdata(id):
    # 转成标准的xml
    parser = etree.HTMLParser(encoding="utf-8")
    tree = etree.parse('tmp.html', parser=parser)
    # 解析出标题 大部分是 x166属性
    title = tree.xpath('/html/body/table/tr/td[@class="xl66"]/text()')
    # 小部分是x165属性
    if len(title) == 0:
        # 只有一个14号表格是x165属性
        classattribute = 'xl65' if id != 14 else 'xl67'
        title = tree.xpath(f'/html/body/table/tr/td[@class="{classattribute}"]/text()')
    # 返回的title是一个列表，转成一个str格式
    title = ''.join(title)
    print(title)
    # 获取表格中有效数据部分共有多少行
    elementnum = len(tree.xpath('/html/body/table/tr[@height="19"]'))
    ws = wb.create_sheet(title=f'{title}')  # 新建sheel插入到最后
    # 对所有行有效元素进行一一提取
    for i in range(1, elementnum + 1):
        tdele = tree.xpath(f'/html/body/table/tr[@height="19"][{i}]/td/text()')
        print(tdele)
        # 逐行添加数据
        ws.append(tdele)


if __name__ == '__main__':
    # 实例化表格
    wb = Workbook()
    for id in range(1, 27):
        url = f'http://tjj.ah.gov.cn/oldfiles/tjj/tjjweb/tjnj/2020/cn/3/cn3-{id}.files/sheet001.htm'
        getdownload(url)
        getdata(id)

    wb.save('anhuipopulation.xlsx')
