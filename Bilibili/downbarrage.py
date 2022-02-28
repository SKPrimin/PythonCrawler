import re
import requests
import wordcloud

url = 'https://comment.bilibili.com/285783437.xml'
# 根据网址请求
response = requests.get(url=url)
# 使用 utf-8 编码
response.encoding = 'utf-8'
# 将得到的响应解析为文本
text = response.text

barrages = re.findall('<d p=".*?">(.*?)</d>', text)
print(barrages)

# 保存评论
with open("弹幕.txt", mode='a', encoding='utf-8') as f:
    for barrage in barrages:
        f.write(barrage + '\n')
        print(barrage)

# 遍历评论
sentence = ""
for barrage in barrages:
    # print(barrage)
    sentence = sentence + ' ' + barrage
font = r'C:\Windows\Fonts\simfang.ttf'
w = wordcloud.WordCloud(
    font_path=font,
    background_color='white',
    width=3840,
    height=2160,
)
w.generate(sentence)
w.to_file('错位时空句云图.png')

# 导入jieba分词包
import jieba

with open("弹幕.txt", 'r', encoding="utf-8")as file:
    # 依照行读取文本内容，并返回一个列表
    text_lines = file.readlines()

    #  存放解析出的关键词
    keywords = []
    # 过滤器，去除其中的词
    filter = ['一双', '祖母', '熠熠', '生辉', '无论', '何时', '祖母绿', '熠熠生辉', '眼睛', ]
    for barrage in text_lines:
        # jieba 切开句子
        word_list = jieba.lcut_for_search(barrage)
        # 列表推导式去除单个字符的干扰项
        word_list = [i for i in word_list if (len(i) > 1 and i not in filter)]
        # 过滤后的列表加在一起
        keywords += word_list

    font = r'C:\Windows\Fonts\simfang.ttf'
    w = wordcloud.WordCloud(
        font_path=font,
        background_color='white',
        width=3840,
        height=2160,
    )
    # 列表最终加载成字符串
    w.generate(" ".join(keywords))
    w.to_file('错位时空词云图.png')
