from selenium import webdriver
import csv
import time


def search_thing(keyword):
    """本函数根据输入的关键字进行内容搜索"""
    # 打开搜索好的网页页面 https://search.jd.com/Search?keyword= &enc=utf-8&wq=
    driver.get('https://search.jd.com/Search?keyword=' + keyword + '&enc=utf-8&wq=' + keyword)
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


def get_data():
    """本函数使用css选择器进行页面解析，分离出各成分"""
    # 异常处理，即使有的数据出问题也不会影响程序继续运行
    try:
        # 通过li的 class="gl-item" css属性选择出所有li
        lis = driver.find_elements_by_css_selector('.gl-item')
        for li in lis:
            price = li.find_element_by_css_selector('div.p-price strong i').text
            name = li.find_element_by_css_selector('div.p-name.p-name-type-2 a em').text
            name = name.replace('京东超市', '').replace('京东国际', '').replace('"', '').replace('\n', '')
            commit = li.find_element_by_css_selector('div.p-commit strong a').text
            shop = li.find_element_by_css_selector('div.p-shop span a').text
            print(name, price, shop, commit)
            csvpencil.writerow([name, price, shop, commit])
    except Exception as e:
        print(e)


def turn_page():
    """本函数用于翻页"""
    driver.find_element_by_css_selector('#J_bottomPage > span.p-num > a.pn-next').click()


if __name__ == '__main__':
    # keyword = input("请输入想要搜索的商品：")
    keyword = '面霜'
    # 创建一个webdriver浏览器实例
    driver = webdriver.Chrome()

    search_thing(keyword)
    # 打开文件 keyword.csv文件，追加数据格式，使用utf-8编码,新建一行不换行
    with open("{}.csv".format(keyword), mode="a", encoding='utf-8', newline="") as f:
        # 创建笔，用来在问价上写入数据
        csvpencil = csv.writer(f)
        # 写入表头
        csvpencil.writerow(["name", "price", "shop", "commit"])
        # 进行5个页面的下拉，数据获取，翻页
        for _ in range(5):
            drop_down()
            get_data()
            turn_page()
    # 关闭浏览器
    driver.quit()