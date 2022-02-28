import random

from openpyxl import Workbook

user = ['用户1', '用户2', '用户3', '用户4', '用户5', '用户6', '用户7', '用户8',
        '用户9', '用户10', '用户11', '用户12', '用户13', '用户14', '用户15']
# 实例化
wb = Workbook()
# 激活 worksheet
ws = wb.active
# 设置表头

ws.append(['用户', '电影1', '电影2', '电影3', '电影4', '电影5', '电影6', '电影7', '电影8', '电影9', '电影10'])

# i 为用户数 j为电影数
for i in range(15):
    numscore = []
    numscore.append(user[i])
    for j in range(10):
        # 生成电影j的分数
        numscore.append(random.randint(0, 5))
    # 生成第i行数据
    ws.append(numscore)

wb.save('电影用户评价信息.xlsx')
