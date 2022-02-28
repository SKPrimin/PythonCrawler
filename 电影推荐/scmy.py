from openpyxl import load_workbook

# 打开文件及表
wb = load_workbook('电影用户评价信息.xlsx')
ws = wb["Sheet"]

# 使用演员作为键，使用包含该演员参演电影名称的集合作为“值”
fimeDict = dict()
i = 0
# 遍历Excel文件中的所有行
for index, row in enumerate(ws.rows):
    # 跳过表头，对于每一行有效数据，获取每一行的电影名称和演员清单，
    if index == 0:
        continue
    # 获取电影名称和演员列表
    user = row[0].value
    fimescore = [row[i].value for i in range(1, 11)]
    # 得到评分字典，评价用户作为键，评分列表作为值
    fimeDict[user] = fimescore

print("评分字典：{}".format(fimeDict))

# 假设来了个新用户
username = "用户A"
user = [4, 0, 4, 4, 0, 0, 2, 0, 0, 5]
print(f"新来的用户为{username}:{user}")

filmSamenum = 0  # 共同打分的数目
filmSameNumDict = {}
for key, value in fimeDict.items():
    # 共同打分的电影分析
    filmiswatch = []
    for i in range(len(user)):
        # 如果双方都看了 ，便为True
        filmiswatch.append(bool(value[i]) & bool(user[i]))
    # 统计True的个数，即双方都看的个数
    filmSamenum = filmiswatch.count(True)
    # 将此用户名用户名与共同观看个数放入字典
    filmSameNumDict[key] = filmSamenum
print(filmSameNumDict)
# 调用max函数找出最大值对应的键 但此方法只会找到返回一个值
keyName = max(filmSameNumDict, key=filmSameNumDict.get)
print("第一个最高匹配人为：{}".format(keyName))

# 再次遍历查看有没有其他的用户观看次数一样
userSame = []
maxScore = filmSameNumDict[keyName]
for key, value in filmSameNumDict.items():
    # 如果观看次与最大值相同添加进列表
    if value == maxScore:
        userSame.append(key)
print("共同打分过的电影多的用户为：{}".format(userSame))

# 开始对相同次数的用户进行第二轮推荐
userScoreDifferentDict = {}
for username in userSame:
    score = 0
    for index, userscore in enumerate(fimeDict[username]):
        # 计算两个用户的打分差距
        if userscore != 0 and user[index] != 0:
            score += abs(userscore - user[index])
    # 将计算出的
    userScoreDifferentDict[username] = score
print("相似用户的得分字典为：{}".format(userScoreDifferentDict))

# 统计出其观看电影的清单
fimeName = ['电影1', '电影2', '电影3', '电影4', '电影5', '电影6', '电影7', '电影8', '电影9', '电影10']
selectefimeName = []
selecteName = min(userScoreDifferentDict, key=userScoreDifferentDict.get)
for index, fime in enumerate(fimeDict[selecteName]):
    if fime != 0:
        selectefimeName.append(fimeName[index])
print("最高匹配人为：{0}，他所观看的电影为{1}".format(selecteName, selectefimeName))
# 求出用户观看的电影列表
userfimeName = []
for index, fime in enumerate(user):
    if fime != 0:
        userfimeName.append(fimeName[index])

# 转成集合求差集
selectefimeName = set(selectefimeName)
userfimeName = set(userfimeName)
finallFimeName = selectefimeName.difference(userfimeName)
print("推荐的电影如下：{}".format(finallFimeName))

# 求出这些电影中评分最高的一个
finallScore = 0
finallFime = ""
for fime in finallFimeName:
    # 找到这个电影的索引
    index = fimeName.index(fime)
    # 根据索引找到分数
    score = fimeDict[selecteName][index]
    # 比较哪那个高
    if finallScore < score:
        finallScore = score
        finallFime = fime
    # 如果是最高评分则无需继续查找了
    if score == 5:
        break
print("最终推荐的电影为：{}".format(finallFime))
