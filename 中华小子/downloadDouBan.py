import time

import requests
import re
from openpyxl import Workbook


def get_response(page):
    url = f'https://movie.douban.com/subject/{id}/comments?'
    print(url)
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/96.0.4664.45 Safari/537.36',
        'Cookie': 'bid=sqN-RF8Q0sA; douban-fav-remind=1; ll="118183"; '
                  '_vwo_uuid_v2=DB6F71C6FE6E2094D9C9E90F9A217C760|c690e19d27c9e2c8d1dc3112d64dafcc; '
                  '__utmz=30149280.1638367797.4.2.utmcsr=cn.bing.com|utmccn=(referral)|utmcmd=referral|utmcct=/; '
                  'dbcl2="241340612:KBnCLh0OA2Y"; push_noty_num=0; push_doumail_num=0; __utmv=30149280.24134; '
                  '__gads=ID=5cb32a7c62ecb399-22c2758650cf008e:T=1638367869:RT=1638367869:S'
                  '=ALNI_MbN2MI6nblZQBXmTiG6tfcUAta5Kg; __yadk_uid=cinJqYPBq2Slh4AkdIKChvqw8audIJFk; ck=ToPN; ap_v=0,'
                  '6.0; __utmc=30149280; __utmc=223695111; __utmz=223695111.1638442306.5.3.utmcsr=douban.com|utmccn=('
                  'referral)|utmcmd=referral|utmcct=/; __utma=30149280.588577938.1619332011.1638442163.1638446410.7; '
                  '__utmb=30149280.0.10.1638446410; __utma=223695111.384741408.1637857999.1638442306.1638446410.6; '
                  '__utmb=223695111.0.10.1638446410; '
                  '_pk_ref.100001.4cf6=%5B%22%22%2C%22%22%2C1638446410%2C%22https%3A%2F%2Fwww.douban.com%2F%22%5D; '
                  '_pk_ses.100001.4cf6=*; _pk_id.100001.4cf6=e04b8604af318c25.1637857998.6.1638446418.1638442357.'}
    param = {
        'start': page * 20,
        'limit': 20,
        'status': 'P',
        'sort': 'new_score'
    }
    response = requests.get(url, params=param, headers=header)
    print(f"正在进行第{page + 1}页评论获取{response.url}")
    return response.text


def get_comments(text):
    """使用正则表达式匹配并写入文件"""

    # 正则表达式匹配出评论 惰性匹配任意字符
    comments = re.findall('<span class="short">(.*?)</span>', text)
    # 评论时间 匹配 \s空格 \d数字 -日期间隔
    times = re.findall('<span class="comment-time " title=".*?">([\s\d-]*)</span>', text)
    # 评论打分
    stars = re.findall('<span class="allstar(\d+) rating" title=".*?"></span>', text)
    print("正则表达式匹配阶段")
    # print(times, stars, comments) # 测试时查看正则表达式匹配结果

    # 使用enumerate函数同时实现索引与内容处理
    for i, comment in enumerate(comments):
        # 使用异常处理在一条出错时不影响其他条
        try:
            # 评论内容原样输出 时间去除换行与空格，星级只取第一个数字50->5
            time = times[i].replace("\n", "").replace(" ", "")
            star = stars[i][:-1]
            # 添加第i行数据
            print(time, star, comment)
            ws.append([time, star, comment])
        except IndexError as ie:
            print(f"索引越界：{ie}")


if __name__ == '__main__':
    # 创建Workbook
    wb = Workbook()
    # 创建一个sheet表
    ws = wb.active
    # 设置表头
    ws.append(['时间', '星级', '评论'])
    col1 = ws.column_dimensions['A']  # 将时间列拓宽
    col1.width = 20
    col3 = ws.column_dimensions['C']  # 将评论列拓宽
    col3.width = 150

    # 中华小子的 id 号
    id = 2244765
    # 获取多少页的评论,一页20条
    pages = 20
    try:
        # 循环发送请求、匹配评论并保存到文件
        for i in range(pages):
            text = get_response(i)
            get_comments(text)
            print(f"写入第{i + 1}页评论")
            # 等待3秒，模拟人的翻页
            time.sleep(3)
    except Exception as e:
        print(f"出现异常:{e}")
    # finally:
        # 无论成功与否都会保存文件
        # wb.save('中华小子评论2.xlsx')
