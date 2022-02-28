from selenium import webdriver
import csv
import time


def search_thing(url):
    """本函数根据输入的url进行内容搜索"""
    driver.get(url)
    # 设置浏览器等待时间，以使页面加载完成
    driver.implicitly_wait(3)
    # 最大化浏览器
    driver.maximize_window()


def drop_down():
    """本函数实现页面下拉到底的操作"""
    # 将滚动条移动到页面的底部
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    # 等待数据加载
    time.sleep(3)


def get_commit():
    """本函数使用css选择器进行页面解析，分离出各成分"""
    # 异常处理，即使有的数据出问题也不会影响程序继续运行
    try:
        # 通过li的 class="comment-item" css属性选择出所有div 评论
        divs = driver.find_elements_by_css_selector('.comment-item')
        for div in divs:
            commit = div.find_element_by_css_selector('div.comment-column.J-comment-column > p.comment-con').text
            commit = commit.replace('\n', '')
            # 由于星级存在于class中，以class="comment-star star5"的形式存在，使用get_attribute('class')将其提取出
            start = div.find_element_by_css_selector('div > div.comment-star').get_attribute('class')
            # 部分评论并没有时间、物品，异常处理，没有就填入FALSE
            try:
                order = div.find_element_by_css_selector('div > div.comment-message > '
                                                         'div.order-info > span').text

                time = div.find_element_by_css_selector('div > div.comment-message > '
                                                        'div.order-info > span:nth-child(4)').text
                print(commit, start, order, time)
            except Exception as e:
                time = ''
                order = ''
                print(e)
            csvpencil.writerow([time, order, start, commit])
    except Exception as e:
        print(e)


def turn_page():
    """本函数用于翻页"""
    element = driver.find_element_by_css_selector('#comment-0 > div.com-table-footer > div > div > a.ui-pager-next')
    driver.execute_script("arguments[0].click();", element)


def main_commits(url, name):
    search_thing(url)
    # 获取评论标签
    get_tags(name)
    # # 进行10个页面的下拉，数据获取，翻页
    for _ in range(10):
        drop_down()
        get_commit()
        turn_page()


def get_tags(name):
    with open("标签数据.csv", mode="a", encoding='utf-8', newline="") as f2:
        # 创建笔，用来在问价上写入数据
        csvpencil2 = csv.writer(f2)
        # 写入表头
        csvpencil2.writerow(["商店名", "标签信息"])
        # 下拉使浏览器加载评论数据
        drop_down()
        time.sleep(3)
        # 通过tag 的class=" tag-1"来找到所有标签
        tags = driver.find_elements_by_css_selector('div.comment-info.J-comment-info > div.percent-info > div > span')
        for tag in tags:
            tagtext = tag.text
            csvpencil2.writerow([name, tagtext])


if __name__ == '__main__':
    # 创建一个webdriver浏览器实例
    driver = webdriver.Chrome()
    # 三家面霜的链接与名称
    urls = ['https://item.jd.com/819172.html', 'https://item.jd.com/100022610088.html',
            'https://item.jd.com/1750036.html']
    names = ['玉兰油（OLAY）大红瓶面霜50g', "科颜氏（Kiehl's）高保湿面霜50ml", '珂润（Curel）润浸保湿滋养乳霜40g']

    try:
        for i in range(3):
            # 创建csv文件，末尾加数据，utf-8编码,空新建
            with open("{}.csv".format(names[i]), mode="a", encoding='utf-8', newline="") as f:
                # 创建笔，用来在问价上写入数据
                csvpencil = csv.writer(f)
                # 写入表头
                csvpencil.writerow(['time', 'order', 'start', 'commit'])
                main_commits(urls[i], names[i])
    # 确保无论如何都会关闭
    finally:
        # 关闭浏览器
        driver.quit()
