## 今天学了什么

> [!info] 今天学了什么
> - 继续学习列表删除、弹出、遍历修改和随机排序。
> - 学习字典的创建、按键取值、添加/修改、成员判断和删除。
> - 通过抢红包、斗地主发牌、九九乘法表、共同元素等练习组合列表、字典和嵌套循环。

## 抓主线

> [!tip] 抓主线
> 1. 列表适合按顺序保存多条数据。
> 2. 字典适合用 key 描述结构化信息。
> 3. 嵌套循环适合处理二维关系或组合问题。
> 4. 项目练习把随机数、容器、循环和切片组织成完整流程。

## 课堂代码合集

### day05/01_demo.py

```python
"""
    列表的操作
"""
# 删除数据元素  del 列表名[索引值]      del 列表名[开始索引:结束索引:间隔]
list_names = ["悟空", "八戒", "唐僧", "悟空", "沙僧", "小白龙"]
# del list_names[-1]
# print(list_names)
# del list_names[1:]
# print(list_names)

# 列表名.remove(元素)    移除列表中第一个符合要求的数据元素
# list_names.remove("悟空")
# print(list_names)
# for item in list_names:
#     if item == "悟空":
#         list_names.remove("悟空")
# print(list_names)

# 列表名.pop(索引值)   不写索引值默认删除最后一个数据元素，并且将删除的结果返回
# print(list_names.pop())
print(list_names.pop(2))
```

> [!note] 这份文件实际讲了什么
> - 文件说明/题目写的是：列表的操作；删除数据元素  del 列表名[索引值]      del 列表名[开始索引:结束索引:间隔]；del list_names[-1]；print(list_names)。
> - 主要变量/数据名包括：`list_names`。

> [!example] 本文件出现的新代码 / 函数 / 方法
> - 列表 `[]`：保存一组有顺序、可修改的数据。
> - `.pop()`：弹出元素。

> [!abstract] 代码逻辑怎么走
> - 用列表保存多条数据，再通过添加、删除或遍历完成批量处理。
> - 通过赋值语句保存中间结果，主要变量包括：`list_names`。

> [!warning] 需要注意的点
> - 列表是可变对象，增删改会直接影响原列表。
> - `is` 比较对象身份，`==` 比较值是否相等，不要混用。

> [!success] 举一反三
> - 可以把单个变量升级为列表，批量保存多条数据后统一遍历处理。

### day05/02_demo.py

```python
"""
    字典dict
"""
# 1 创建列表
dict01 = {}   # 创建空字典
dict_stu = {"name": "Alan", "age": "23", "gender": "male"}   # 创建非空字典
# dict02 = dict(可迭代对象)
# dict02 = dict(["悟空","八戒"])    # {'悟': '空', '八': '戒'}

# 2 定位数据   通过键来找值   字典名[键] ---> 值
# print(dict_stu["age"])
#
# # 3 添加/修改   字典名[键] = 值   键存在于字典中，修改值;键不存在于字典中，是添加键值对
dict_stu["skill"] = 72   # 添加键值对
dict_stu["hobby"] = "killer"   # 添加键值对
# dict_stu["age"] = 32   # 修改值
print(dict_stu)

# 4 成员运算 in not in 判断键是否存在于字典中
# print("skill" in dict_stu) # False
# print("hobby" not in dict_stu) # True
# print("age" in dict_stu) # True
# print("Alan" not in dict_stu) # True

# # 5 删除 del   del 字典[键]
# del dict_stu["hobby"]
# print(dict_stu)
#
# # 6 循环遍历
# for k in dict_stu:   # 依次获取字典的键
#     print(k, dict_stu[k])
#
# for v in dict_stu.values():   # 依次获取字典的值
#     print(v)
#
# for item in dict_stu.items():   # 获取键值对
#     print(item)
#
for k,v in dict_stu.items():
    print(k,v)
```

> [!note] 这份文件实际讲了什么
> - 文件说明/题目写的是：字典dict；1 创建列表；创建空字典；创建非空字典。
> - 主要变量/数据名包括：`dict01`、`dict_stu`。

> [!example] 本文件出现的新代码 / 函数 / 方法
> - 字典 `{key: value}`：用键值对描述结构化数据。
> - `.items()`：调用对象自身的方法，重点看它修改了哪个对象或返回了什么结果。

> [!abstract] 代码逻辑怎么走
> - 使用 `for` 遍历序列或容器，对每个元素执行同样的处理。
> - 用字典组织 key-value 数据，再通过 key 读取、更新或遍历。
> - 通过赋值语句保存中间结果，主要变量包括：`dict01`、`dict_stu`。

> [!warning] 需要注意的点
> - 字典按 key 取值，key 要唯一；遍历键值对时优先想到 `.items()`。

> [!success] 举一反三
> - 可以把同样结构用于学生信息、商品信息、地区数据等 key-value 场景。
> - 可以把循环和条件组合起来做筛选、统计、累加、菜单系统。

### day05/exercise01.py

```python
"""
    1 索引定位单一数据元素
    2 切片定位多个数据元素
    3 for循环遍历直接获取每一个数据元素;通过索引获取数据元素
"""
list_names =["悟空","八戒","唐僧"]
# for item in list_names:
#     print(item)

# for i in range (len(list_names)):
#     print(list_names[i])

list_scores = [56,78,93,48,80,74,43,65]
# 需求:将列表中成绩小于60分的修改为60分

# # 错误做法
# for item in list_scores:
#     if item < 60:
#         item = 60    # 修改的是变量item,并未修改列表中的数据
# print(list_scores)

# # 勉强的做法
# list1 = []
# for item in list_scores:
#     if item < 60:
#         item = 60
#         list1.append(item)
#     else:
#         list1.append(item)
# print(list1)    # 本质是使用一个空列表重新装入数据，并未修改原列表

# 与上面的同理
# for item in list_scores:
#     if item < 60:
#        item = 60
#     print(item,end=" ")

# 合理做法
# for i in range(len(list_scores)):
#     if list_scores[i] < 60:
#         list_scores[i] = 60
# print(list_scores)
```

> [!note] 这份文件实际讲了什么
> - 文件说明/题目写的是：1 索引定位单一数据元素；2 切片定位多个数据元素；3 for循环遍历直接获取每一个数据元素;通过索引获取数据元素；for item in list_names:。
> - 主要变量/数据名包括：`list_names`、`list_scores`。

> [!example] 本文件出现的新代码 / 函数 / 方法
> - 列表 `[]`：保存一组有顺序、可修改的数据。

> [!abstract] 代码逻辑怎么走
> - 用列表保存多条数据，再通过添加、删除或遍历完成批量处理。
> - 通过赋值语句保存中间结果，主要变量包括：`list_names`、`list_scores`。

> [!warning] 需要注意的点
> - 列表是可变对象，增删改会直接影响原列表。
> - `is` 比较对象身份，`==` 比较值是否相等，不要混用。

> [!success] 举一反三
> - 可以把单个变量升级为列表，批量保存多条数据后统一遍历处理。

### day05/exercise02.py

```python
"""
    抢红包小案例
"""
import random   # 导入随机模块

# 第一步:获取用户发放红包的金额与个数
money = float(input("请输入发放红包金额:")) # money:10
count = int(input("请输入发放红包个数:"))

#第二步:系统产生count个随机金额的红包
list1 = []
for i in range(1,count):
    red_packet = random.uniform(0.01, money/count)  # 产生一定范围内的随机小数
    red_packet = round(red_packet,2)   # 将系统产生的随机金额四会五入，保留2位小数
    list1.append(red_packet)
    money -= red_packet   # 将生成的红包金额在总金额内扣减
    count -= 1   # 将生成的红包个数在总个数扣减

last_red_packet = money   # 将余额作为最后一个红包的金额
last_red_packet = round(last_red_packet,2)
list1.append(last_red_packet)
print("系统随机生成的红包金额是:", list1, sum(list1))

random.shuffle(list1)   # 将序列中的元素随机排序
print("系统随机排序后的红包金额是:", list1)

#第三步:发红包每个用户查看红包金额
for i in range(len(list1)):   # i:0 1 2
    print(f"第{i+1}个红包金是:", list1[i])
```

> [!note] 这份文件实际讲了什么
> - 文件说明/题目写的是：抢红包小案例；导入随机模块；第一步:获取用户发放红包的金额与个数；money:10。
> - 主要变量/数据名包括：`money`、`count`、`list1`、`red_packet`、`last_red_packet`。

> [!example] 本文件出现的新代码 / 函数 / 方法
> - `random.uniform()`：调用 `random` 中的 `uniform` 功能，结合本文件注释理解它在当前练习中的作用。
> - `random.shuffle()`：调用 `random` 中的 `shuffle` 功能，结合本文件注释理解它在当前练习中的作用。

> [!abstract] 代码逻辑怎么走
> - 先通过 `input()` 获取用户输入，再根据题目需要做类型转换或合法性判断。
> - 使用 `for` 遍历序列或容器，对每个元素执行同样的处理。
> - 用列表保存多条数据，再通过添加、删除或遍历完成批量处理。
> - 通过赋值语句保存中间结果，主要变量包括：`money`、`count`、`list1`、`red_packet`、`last_red_packet`。

> [!warning] 需要注意的点
> - `input()` 得到的是字符串；参与数学计算前要先转成 `int` 或 `float`。
> - `range()` 的结束值取不到，写循环边界时要特别小心。
> - 列表是可变对象，增删改会直接影响原列表。

> [!success] 举一反三
> - 可以给输入加合法性检查，例如不能为空、必须是数字、范围必须正确。
> - 可以把单个变量升级为列表，批量保存多条数据后统一遍历处理。
> - 可以把循环和条件组合起来做筛选、统计、累加、菜单系统。

### day05/exercise03.py

```python
"""
    使用python程序生成一副斗地主牌面
        1、生成一副扑克牌
        2、洗牌
        3、根据游戏规则，3个玩家，17张牌/玩家  底牌:3张
"""


# import random
#
# # 第一步：准备扑克牌
# list_numbers = ["2","3","4","5","6","7","8","9","10","J","Q","K","A"]
# list_colors = ['♠', '♣', '♥', '♦']  # ['\u2660','\u2663','\u2665','\u2666']
# list_kings = ["大王","小王"]
#
# list_pokers = []   # 创建一个空列表用于存储扑克牌
# for c in list_colors:   # 外层每循环1次
#     for n in list_numbers:   # 内层循环13次
#         list_pokers.append(c+n)
#
# list_pokers += list_kings
#
# # 第二步：洗牌
# random.shuffle(list_pokers)
# print(list_pokers)
#
# # 第三步：抓牌  3个玩家，每人17张，底牌3张
# xm = list_pokers[0:51:3]
# hh = list_pokers[1:51:3]
# dz = list_pokers[2:51:3]
# remains = list_pokers[51:]



# # 直观感受双重for循环
# list_number = [1,2]
# list_skill =["打拳","踢腿","肘击"]
# for n in list_number:
#     for s in list_skill:
#         print(f"第{n}次循环执行{s}动作")


# 使用 双重for循环 解决 降序排列问题
list9 = [12000, 24000, 13000, 45000, 13000]
# for i in range(len(list9)):
#     for j in range(i+1, len(list9)):
#         max_salary = list9[i]
#         if list9[j] > max_salary:
#             list9[i], list9[j] = list9[j], list9[i]
#         else:
#             continue
# print(list9)

# n = len(list9)
# for i in range(n):
#     # 找到未排序部分的最大值索引
#     max_idx = i
#     for j in range(i + 1, n):
#         if list9[j] > list9[max_idx]:
#             max_idx = j
#     # 将最大值交换到当前位置
#     list9[i], list9[max_idx] = list9[max_idx], list9[i]
# print(list9)  # 输出: [45000, 24000, 13000, 13000, 12000]

# 使用双重for循环实现降序排列
n = len(list9)
for i in range(n - 1):
    for j in range(0, n - i - 1):
        # 比较相邻元素，如果前一个比后一个小，则交换位置
        if list9[j] < list9[j + 1]:
            list9[j], list9[j + 1] = list9[j + 1], list9[j]
# 输出结果
print("降序排列后的列表:", list9)
```

> [!note] 这份文件实际讲了什么
> - 文件说明/题目写的是：使用python程序生成一副斗地主牌面；1、生成一副扑克牌；2、洗牌；3、根据游戏规则，3个玩家，17张牌/玩家  底牌:3张。
> - 主要变量/数据名包括：`list9`、`n`。

> [!example] 本文件出现的新代码 / 函数 / 方法
> - 列表 `[]`：保存一组有顺序、可修改的数据。

> [!abstract] 代码逻辑怎么走
> - 使用 `for` 遍历序列或容器，对每个元素执行同样的处理。
> - 使用条件判断把不同情况分开处理，让程序根据数据走不同分支。
> - 用列表保存多条数据，再通过添加、删除或遍历完成批量处理。
> - 通过赋值语句保存中间结果，主要变量包括：`list9`、`n`。

> [!warning] 需要注意的点
> - `range()` 的结束值取不到，写循环边界时要特别小心。
> - 列表是可变对象，增删改会直接影响原列表。
> - `is` 比较对象身份，`==` 比较值是否相等，不要混用。

> [!success] 举一反三
> - 可以把单个变量升级为列表，批量保存多条数据后统一遍历处理。
> - 可以把循环和条件组合起来做筛选、统计、累加、菜单系统。

### day05/exercisefor-for.py

```python
"""
打印9×9乘法表，格式如下：
1*1=1
1*2=2  2*2=4
...
9*9=81
"""
for i in range(1, 10):
    for j in range(1, i+1):
        print(f"{j}*{i}={i*j}", end="\t")
    print()

"""
找出两个列表中的共同元素：
list_a = [1, 3, 5, 7, 9]
list_b = [2, 3, 5, 8, 9]
输出: [3, 5, 9]
"""
list_a = [1, 3, 5, 7, 9]
list_b = [2, 3, 3, 5, 8, 9]
list_c = []
for a in list_a:
    for b in list_b:
        if a == b:
            list_c.append(a)
            break  # 避免重复添加
print(list_c)


"""
用星号(*)打印5层金字塔：
    *
   ***
  *****
 *******
*********
"""
n = 5
for i in range(n):
    # 打印空格
    for j in range(n-i-1):
        print(" ", end="")
    # 打印星号
    for k in range(2*i+1):
        print("*", end="")
    print()

"""
题目6：寻找素数
找出1-100之间的所有素数（只能被1和自身整除）
"""
for num in range(2, 101):
    is_prime = True
    for i in range(2, int(num**0.5)+1):
        if num % i == 0:
            is_prime = False
            break
    if is_prime:
        print(num, end=" ")
print()


"""
题目8：冒泡排序优化
实现带优化的冒泡排序（当某一轮没有交换时提前结束）：
nums = [5, 3, 8, 6, 7, 2]
# 排序后: [2, 3, 5, 6, 7, 8]
"""
nums = [5, 3, 2, 6, 7, 8]
# for i in range(len(nums)-1):
#     for j in range(0,len(nums)-i-1):
#         if nums[j] > nums[j+1]:
#             nums[j], nums[j+1] = nums[j+1], nums[j]
# print(nums)

n = len(nums)
for i in range(n-1):
    swapped = False
    for j in range(0, n-i-1):
        if nums[j] > nums[j+1]:
            nums[j], nums[j+1] = nums[j+1], nums[j]
            swapped = True
    if not swapped:
        break
print(nums)
```

> [!note] 这份文件实际讲了什么
> - 文件说明/题目写的是：打印9×9乘法表，格式如下：；1*1=1；1*2=2  2*2=4；...。
> - 主要变量/数据名包括：`list_a`、`list_b`、`list_c`、`n`、`is_prime`、`nums`、`swapped`。

> [!example] 本文件出现的新代码 / 函数 / 方法
> - 列表 `[]`：保存一组有顺序、可修改的数据。

> [!abstract] 代码逻辑怎么走
> - 使用 `for` 遍历序列或容器，对每个元素执行同样的处理。
> - 使用条件判断把不同情况分开处理，让程序根据数据走不同分支。
> - 用列表保存多条数据，再通过添加、删除或遍历完成批量处理。
> - 通过赋值语句保存中间结果，主要变量包括：`list_a`、`list_b`、`list_c`、`n`、`is_prime`、`nums`、`swapped`。

> [!warning] 需要注意的点
> - `range()` 的结束值取不到，写循环边界时要特别小心。
> - `break` 只跳出当前这一层循环。
> - 列表是可变对象，增删改会直接影响原列表。
> - `is` 比较对象身份，`==` 比较值是否相等，不要混用。

> [!success] 举一反三
> - 可以把单个变量升级为列表，批量保存多条数据后统一遍历处理。
> - 可以把循环和条件组合起来做筛选、统计、累加、菜单系统。

### day05/review.txt

```text
"""
有序容器：列表(可变)[]  字符串(不可变) ""  元组(不可变)()
for循环用于遍历可迭代对象中的数据元素
for与range结合做固定次数循环
range()函数：用于生成一系列整数的可迭代对象（整数生成器）
    range(开始值,结束值,间隔/步长)  间隔：任意两个相邻数字之间差值
    range(开始值,结束值,间隔/步长)
    range(开始值,结束值)  间隔/步长：默认是1可以省略不写;间隔值不是1必须指定。间隔值的方向要与生成数据方向保持一致
    range(结束值)   开始值默认是0,可以省略     range(0,结束值,1)
while循环和for循环的区别：相同都可以用与循环计数；不同点：while循环可以基于条件进行循环；for循环可以用于遍历获取容器中的元素
break语句与continue语句的区别： break用于结束整个循环；continue结束本次循环，进入到下一次循环
二 列表 list  用于存储任意数据类型的可变有序容器。
1 创建列表  列表名 = [元素,元素,...]   列表名 = list(可迭代对象)
2 添加数据
    末尾追加数据  列表名.append(元素)
    末尾同时添加多个数据元素  列表名.extend(可迭代对象)
    指定位置插入数据    列表名.insert(索引值,元素)
3 索引：定位容器中单一数据元素
        正向索引：左 ---> 右   默认从0   最大索引值len()-1
        反向索引：右---> 左    -1开始，以此类推，表达倒数
        索引越界是报错
4 切片：定位多个数据元素   容器名[开始索引值:结束索引值:间隔/步长]  切片越界不报错
        开始索引值默认是0,可以省略
        结束索引值，不包含该位置上的元素   左闭右开
        间隔/步长默认是1，可以省略
        容器名[开始索引值:结束索引值:间隔/步长]
        容器名[开始索引值:结束索引值]
        容器名[:结束索引值]
        容器名[::] 从左到右的数据元素全都要   间隔值方向要与切片范围保持一致    容器名[::-1] 从右到左的数据元素全都要
        容器名[1:1] -->[]
三 容器通用操作
1 运算符：算数运算符  +  拼接数据元素  +=拼接后的结果重新赋值给自己  list01 += list02-->  list01 = list01 + list02
         比较运算符  >  >=   <  <=  ==  !=   按照对应位置上的元素注意比较，一旦不同立刻返回结果
2 内建函数：len()容器的长度(统计容器中元素的个数)  max()  min()  sum()
3 有序容器：  索引    切片
4 成员运算  in   not  in
"""
```

> [!info] 课堂文本/作业说明
> - """
> - 有序容器：列表(可变)[]  字符串(不可变) ""  元组(不可变)()
> - for循环用于遍历可迭代对象中的数据元素
> - for与range结合做固定次数循环
> - range()函数：用于生成一系列整数的可迭代对象（整数生成器）
> -     range(开始值,结束值,间隔/步长)  间隔：任意两个相邻数字之间差值
> -     range(开始值,结束值,间隔/步长)
> -     range(开始值,结束值)  间隔/步长：默认是1可以省略不写;间隔值不是1必须指定。间隔值的方向要与生成数据方向保持一致

## 总结

> [!summary] 总结
> - **今天的核心任务**：继续学习列表删除、弹出、遍历修改和随机排序。；学习字典的创建、按键取值、添加/修改、成员判断和删除。；通过抢红包、斗地主发牌、九九乘法表、共同元素等练习组合列表、字典和嵌套循环。
> - **真实文件里的练习/主题**：列表的操作；字典dict；1 索引定位单一数据元素；抢红包小案例；使用python程序生成一副斗地主牌面；打印9×9乘法表，格式如下：。
>
> **新学代码怎么理解**
> - 列表 `[]`：保存一组有顺序、可修改的数据。
> - `.pop()`：弹出元素。
> - 字典 `{key: value}`：用键值对描述结构化数据。
> - `.items()`：调用对象自身的方法，重点看它修改了哪个对象或返回了什么结果。
> - `random.uniform()`：调用 `random` 中的 `uniform` 功能，结合本文件注释理解它在当前练习中的作用。
> - `random.shuffle()`：调用 `random` 中的 `shuffle` 功能，结合本文件注释理解它在当前练习中的作用。
>
> **复盘建议**
> - 先看文件说明，再看原代码，最后解释新函数/方法的输入、输出和用途。
