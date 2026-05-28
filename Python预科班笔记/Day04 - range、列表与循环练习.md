## 今天学了什么

> [!info] 今天学了什么
> - 学习 `range()` 的开始、结束和步长规则。
> - 学习列表的创建、索引、切片、遍历、添加、插入、删除和排序。
> - 通过登录验证、福彩号码、列表筛选、八大行星等题目练习循环和列表。

## 抓主线

> [!tip] 抓主线
> 1. `range()` 生成一串数字，常用于固定次数循环。
> 2. 列表保存一组有顺序的数据。
> 3. 索引和切片负责定位数据。
> 4. 列表方法和循环配合完成批量处理。

## 课堂代码合集

### day04/01_demo.py

```python
"""
    range()函数：生成一系列整数的可迭代对象（整数生成器）
    range(开始值，结束值，间隔/步长)
        左闭右开区间：开始值包含，结束值不包含
        间隔值默认是 1 可以省略不写
        开始值默认是0，可以省略不写
        注意:生成数据范围要与间隔值方向保持一致
        while 和 for的区别：while可以设置条件，到了就终止。for适合遍历每个数
"""
for i in range(0,4,1):
    print(i,end=" ")
print()

for i in range(0,4):
    print(i,end=" ")
print()

for i in range(4):
    print(i,end=" ")
print()

for i in range(8,3,-1):
    print(i,end=" ")
print()

for i in range(-5,-1,-1):
    print(i,end=" ")
print()

# count = 0  # 循环前设定计数器初始值(记录自己的圈数值)
# while count < 3:  # 循环条件 设定计数器的结束值
#     # 重复执行的代码块(循环体)
#     print("跑圈")
#     count += 1  # 循环内让计数器值自增

for i in range(0,3,1):  # 0,1,2
    # print(i)
    print("跑圈")   # 同样可以计数跑圈


# # 练习:在终端中显示 0 1 2 3
# count = 0
# while count < 4:
#     print(count)
#     count += 1
# # 在终端中显示 2 3 4 5 6
# count = 2
# while count < 7:
#     print(count)
#     count += 1
```

> [!note] 这份文件实际讲了什么
> - 文件说明/题目写的是：range()函数：生成一系列整数的可迭代对象（整数生成器）；range(开始值，结束值，间隔/步长)；左闭右开区间：开始值包含，结束值不包含；间隔值默认是 1 可以省略不写。

> [!example] 本文件出现的新代码 / 函数 / 方法
> - `range()`：生成整数序列，常配合 `for` 控制循环次数。

> [!warning] 需要注意的点
> - `range()` 的结束值取不到，写循环边界时要特别小心。

### day04/02_demo.py

```python
"""
    列表list：存储任意数据类型的有序容器
"""
# # 一 创建列表   列表名 = []   列表名 = list(可迭代对象)
# list01 = []  # 创建空列表
# list_numbers = [1, 2, 3, 4]   # 创建非空列表
# # 可以将一个可迭代对象转换成列表  数据类型转换  目标数据类型(待转换数据)  int(7.89)
# list_words = list("python")
# print(list_words)  # ['p', 'y', 't', 'h', 'o', 'n']

# # 二 列表添加数据元素
list_names = ["悟空", "八戒", "唐僧"]
# # ① 列表名.append(元素)    列表末尾追加单一数据元素 append(元素)
# list_names.append("沙僧")
# # list_names.append("沙僧", "小白龙") # TypeError: list.append() takes exactly one argument (2 given)
# list_names.append(["红孩儿", "小白龙"])
# print(list_names)
#
# # ② 列表末尾添加多个数据元素列表名.extend(可迭代对象)
# list_names.extend(["八部天龙", "红孩儿"])
# print(list_names)

# ③ 指定位置插入数据  列表名.insert(索引,数据)
# list_names.insert(1, "红孩儿")
# print(list_names)
# list_names.insert(1,("牛魔王", "小红帽"))
# print(list_names)

# 二 列表元素定位 ① index索引定位单一元素 容器名[索引值] 通过切片获取的数据仍然是列表
# print(list_names[-3])  # 悟空
# 切片定位多个数据元素容器名[开始索引值:结束索引值:间隔|步长]
# print(list_names[0:]) # ['悟空'，'八戒'，'唐僧‘]

# 三 修改
list_names[0] = "孙悟空"
print(list_names)
list_names[-1] = "唐三藏"
print(list_names)

list_names[1] = ["牛魔王", "杨戬"]
print(list_names)
list_names[0:2] = ["齐天大胜"]
print(list_names)
```

> [!note] 这份文件实际讲了什么
> - 文件说明/题目写的是：列表list：存储任意数据类型的有序容器；# 一 创建列表   列表名 = []   列表名 = list(可迭代对象)；list01 = []  # 创建空列表；list_numbers = [1, 2, 3, 4]   # 创建非空列表。
> - 主要变量/数据名包括：`list_names`。

> [!example] 本文件出现的新代码 / 函数 / 方法
> - 列表 `[]`：保存一组有顺序、可修改的数据。

> [!abstract] 代码逻辑怎么走
> - 用列表保存多条数据，再通过添加、删除或遍历完成批量处理。

> [!warning] 需要注意的点
> - 列表是可变对象，增删改会直接影响原列表。

> [!success] 举一反三
> - 可以把单个变量升级为列表，批量保存多条数据后统一遍历处理。

### day04/03_demo.py

```python
"""
    容器通用操作
"""
# 1 运算符使用   +   +=   *重复生成容器中的元素   *=
# list01 = [1,2,3,4]
# list02 = [1,2,3,4,5]
# print(list01 + list02)  # + 拼接容器中数据元素的
# print("您本次消费" + str(34.5) + "元")   # 字符串也是一种特殊的容器
# list03 = list01 + list02
# print(list03)   #[1，2，3，4，5，6，7，8]
# list01 = list01 + list02
# list01 += list02
# print(list01)

# print(list01 * 2)
# list01 *= 2  # list01 = list01 * 2
# print(list01)

# # 2 比较运算符  >  >=  <  <=  ==  !=  按照对应位置上的元素逐一比较，一旦不同立刻返回结果
# print(list01 < list02)
# print(list01 != list02)
# print(list01 == list02)
#
# # 3 成员运算 in  not in 判断数据元素是否存储于容器中
# print(10 not in list02)  # 判断 "10不在list02中" 是否正确
# print(9 in list02)  # 判断 "9在list02中" 是否正确
#
# # 内建函数  max()  min()  sum()  len()容器的长度（容器中元素的个数）
# print(max(list02))
# print(min(list02))
# print(sum(list02))
# print(len(list02))
#
# print([9,8,7,6]<[5,6,7,8,9]) # False

# 4 索引index  定位容器中单一数据元素的  容器名[索引值]
# 正向索引       0      1       2      3        4
list_names = ["悟空", "八戒", "唐僧", "沙僧", "小白龙"]
#  反向索引       -5     -4     -3      -2      -1
# print(list_names[2])
# print(list_names[-3])
# print(list_names[-len(list_names)])
# print(list_names[len(list_names) - 1])
# print(list_names[100])  # IndexError: list index out of range 索引越界会报错

# 5 切片   定位容器中多个元素   容器名[开始索引值:结束索引值:间隔/步长]
# ① 所有数据元素
# print(list_names[0:100:1])   # 结束索引值不包含该位置上的元素,切片越界不报错
# 开始索引值::间隔/步长
print(list_names[0::1])  # 从索引值0开始到后面所有元素都要
# 开始索引值
print(list_names[0:])  # 间隔值默认是1 可以省略
# ::
print(list_names[::])  # 开始值默认是0，可以省略
print(list_names[::-1])  # 反转

print(list_names[:4])  # ['悟空'，'八戒’，'唐僧’，'沙僧‘]
print(list_names[:-1])  # ['悟空'，'八戒’，'唐僧’，'沙僧’]
print(list_names[:-1:2])  # ['悟空'，'唐僧‘]
print(list_names[:-1:-2])  # 从悟空开始往左取数据，取不到  切片的范围要与间隔值方向保持一致
```

> [!note] 这份文件实际讲了什么
> - 文件说明/题目写的是：容器通用操作；1 运算符使用   +   +=   *重复生成容器中的元素   *=；list01 = [1,2,3,4]；list02 = [1,2,3,4,5]。
> - 主要变量/数据名包括：`list_names`。

> [!example] 本文件出现的新代码 / 函数 / 方法
> - 列表 `[]`：保存一组有顺序、可修改的数据。

### day04/exercise01.py

```python
# 需求:计算1~100(包含1和100)数字相加之和
# total = 0
# for i in range(1,101,1):
#     total += i
# print(total)

#需求:求1~100之间是能被3整除
# # 顺着思想来
# total = 0
# for i in range(1, 101, 1):
#     if i % 3 == 0:  # 满足n表示的数字能被3 整除
#         total += i
# print(total)
#
# # 逆着思想来
# sum_values = 0
# for n in range(1, 101):   # range(1,101,1)
#     if n % 3 != 0:   # 不能被3整除的数字跳过
#         continue   # 结束本轮循环，进入到下一次循环
#     sum_values += n
# print(f"1~100之间的数字之和是{sum_values}")


# 求和10~60之间个位不是3/5/8的数字之和
# 个位不是3/5/8的数字，直接求和
# total = 0
# for i in range(10, 61):
#     if i % 10 != 3 and i % 10 != 5 and i % 10 != 8:
#         total += i
# print(total)

# # 个位是3/5/8的数字就跳过
# total = 0
# for i in range(10, 61):
#     if i % 10 == 3 or i % 10 == 5 or i % 10 == 8:
#         continue
#     total += i
# print(total)
```

> [!note] 这份文件实际讲了什么
> - 文件说明/题目写的是：需求:计算1~100(包含1和100)数字相加之和；total = 0；for i in range(1,101,1):；total += i。

> [!example] 本文件出现的新代码 / 函数 / 方法
> - 本文件主要是在复习或组合前面已经学过的写法，没有引入需要单独记忆的新函数/方法；重点看它如何把旧知识组合成当前题目。

### day04/exercise02.py

```python
"""
    登录验证
        设定正确的用户名和密码
        登录验证:输入用户名和密码，如果与系统存一致，则登录成功
                反之:如果用户名或密码错误，可以有3次重新输入机会
                    3次机会内输入正确，登录成功
                    3次机会用尽，则账号锁定
"""

user = "xujiahao"
code = "xu1005902828"
i = 3

while True:
    user1 = input("请输入用户名：")
    code1 = input("请输入密码：")
    if user1 == user and code1 == code:
        print("登录成功")
        break
    else:
        i -= 1
        print(f"用户名或密码错误,还剩{i}次机会")
    if i == 0:
        print("账号锁定")
        break

# 第一步:设定正确的用户名密码
user = "xujiahao"
code = "xu1005902828"
# 第二步:登录验证
for i in range(2, -1, -1):
    # 获取用户输入的用户名和密码
    user1 = input("请输入用户名：")
    code1 = input("请输入密码：")
    if user1 == user and code1 == code:
        print("登录成功")
        break
# 如果用户名或密码错误，3次机会重新输入 3次机会内输入正确，登录成功
    else:
        print(f"用户名或密码错误,还剩{i}次机会")
# 否则账号锁定
else:
    print("账号锁定")
```

> [!note] 这份文件实际讲了什么
> - 文件说明/题目写的是：登录验证；设定正确的用户名和密码；登录验证:输入用户名和密码，如果与系统存一致，则登录成功；反之:如果用户名或密码错误，可以有3次重新输入机会。
> - 主要变量/数据名包括：`user`、`code`、`i`、`user1`、`code1`。

> [!example] 本文件出现的新代码 / 函数 / 方法
> - 本文件主要是在复习或组合前面已经学过的写法，没有引入需要单独记忆的新函数/方法；重点看它如何把旧知识组合成当前题目。

### day04/exercise03.py

```python
"""
    列表的练习
"""
# 1 创建一个员工薪资表，存储数据:28000,22000,32000,18000
list_salary = [28000,22000,32000,18000]
print(list_salary)

# 2 添加一个员工薪资数据为:15000
list_salary.append(15000)
print(list_salary)

# 3 添加新入职员工薪资数据:9200，7800,8800,12000
list_salary.extend([9200,7800,8800,12000])
print(list_salary)

# 4 在索引值为3的位置，插入薪资数据:45000
list_salary.insert(3, 45000)
print(list_salary)

# 5 打印输出第一个员工和最后一个员工的薪资
print(list_salary[0])
print(list_salary[-1])

# 6 打印前三个员工的薪资
print(list_salary[:3])
```

> [!note] 这份文件实际讲了什么
> - 文件说明/题目写的是：列表的练习；1 创建一个员工薪资表，存储数据:28000,22000,32000,18000；2 添加一个员工薪资数据为:15000；3 添加新入职员工薪资数据:9200，7800,8800,12000。
> - 主要变量/数据名包括：`list_salary`。

> [!example] 本文件出现的新代码 / 函数 / 方法
> - 列表 `[]`：保存一组有顺序、可修改的数据。
> - `.append()`：向列表末尾添加一个元素。
> - `.extend()`：调用对象自身的方法，重点看它修改了哪个对象或返回了什么结果。
> - `.insert()`：在指定位置插入元素。

### day04/exercise04.py

```python
"""
    使用python程序生成一组福彩中奖号码，并判断自己是否中奖
    7个号码:6个红色球号码 1~33  红色球号码之间不能重复  1个蓝色球号码1~16
        random模块:模块就是以.py为结尾的python文件。用于产生随机数
"""
import random  # 导入随机模块

###########     方法一     ###########
# # 第一步:系统随机生成一组福彩号码
# # 创建一个容器用于存储系统生成的号码
# list_lottery = []
# count = 0
# # 系统每生成一个号码添加到列表中
# while count < 6:  # 0,1,2,3,4,5
#     red_number = random.randint(1,33)  # 重复执行6次
#     if red_number not in list_lottery:
#         list_lottery.append(red_number)
#         count += 1
#     # else:   可以不写一样的效果
#     #     count += 0
# list_lottery.append(random.randint(1,16))
#
# # 第二步:自己选购一组号码，判断是否中奖
# list_gift = []
# i = 0
# while i < 6:
#     choose = int(input(f"请输入第{i+1}个红色球号码(1~33之间的整数)："))
#     if choose not in list_gift:
#         if 1 <= choose <= 33:
#             list_gift.append(choose)
#             i = i + 1
#         else:
#             print("超出范围，请重试")
#     else:
#         print("不能输入与之前相同的号码，请重试")
# while i == 6:
#     choose = int(input("请输入蓝色球号码(1~16之间的整数)："))
#     if 1 <= choose <= 16:
#         list_gift.append(choose)
#         break
#     else:
#         print("超出范围，请重试")
# print("您所选择的福彩序列是：", list_gift)
# if list_gift == list_lottery:
#     print("恭喜你！获得500万大奖！")
# else:
#     print("很遗憾，未能中奖。中奖号码是", list_lottery)


###########    方法二     ###########
# 第一步:系统随机生成一组福彩号码
red_balls = random.sample(range(1,34),6)
blue_balls = random.randint(1,16)
list_lottery = list(red_balls) + list(blue_balls)
print(list_lottery)
# 第二步:自己选购一组号码，判断是否中奖
list_gift = []
for i in range(6):
    while True:
        choose = int(input(f"请输入第{i + 1}个红色球号码(1~33之间的整数)："))
        if choose < 1 or choose > 33:
            print("超出范围，请重试")
        elif choose in list_gift:
            print("不能输入与之前相同的号码，请重试")
        else:
            list_gift.append(choose)
            break
while i == 5:
    choose = int(input("请输入蓝色球号码(1~16之间的整数)："))
    if 1 <= choose <= 16:
        list_gift.append(choose)
        break
    else:
        print("超出范围，请重试")
print("您所选择的福彩序列是：", list_gift)
if list_gift == list_lottery:
    print("恭喜你！获得500万大奖！")
else:
    print("很遗憾，未能中奖。中奖号码是", list_lottery)
```

> [!note] 这份文件实际讲了什么
> - 文件说明/题目写的是：使用python程序生成一组福彩中奖号码，并判断自己是否中奖；7个号码:6个红色球号码 1~33  红色球号码之间不能重复  1个蓝色球号码1~16；random模块:模块就是以.py为结尾的python文件。用于产生随机数；导入随机模块。
> - 主要变量/数据名包括：`red_balls`、`blue_balls`、`list_lottery`、`list_gift`、`choose`。

> [!example] 本文件出现的新代码 / 函数 / 方法
> - `random.sample()`：调用 `random` 中的 `sample` 功能，结合本文件注释理解它在当前练习中的作用。
> - 列表 `[]`：保存一组有顺序、可修改的数据。

### day04/homework.py

```python
"""
content = "我是京师监狱狱长金海。"
打印第一个字符、最后一个字符、中间字符
打印前三个字符、打印后三个字符
命题：金海在字符串content中
命题：京师监狱不在字符串content中
通过切片打印“京师监狱狱长”
通过切片打印“长狱狱监师京”
通过切片打印“我师狱海”
倒序打印每个字符
"""
#          0 1 2 34 5 67 8 910
content = "我是京师监狱狱长金海。"
# 打印第一个字符、最后一个字符、中间字符
print(content[0])
print(content[-1])
print(content[len(content) // 2])
# 打印前三个字符、打印后三个字符
print(content[0:3])
print(content[8:])
print(content[-3:]) # content[-3::1]
# 命题：金海在字符串content中
print("金海" in content) # True
# 命题：京师监狱不在字符串content中
print("京师监狱" not in content) # False
print("京狱" in content) # False 连续字符串进行的判断比较
# 通过切片打印“京师监狱狱长”
print(content[2:-3])    #content[2:8:1]
# 通过切片打印“长狱狱监师京”
print(content[7:1:-1])  #content[-4:1:-1]
# 通过切片打印“我师狱海”
print(content[0:-1:3])
# 倒序打印每个字符
print(content[::-1])
```

> [!note] 这份文件实际讲了什么
> - 文件说明/题目写的是：content = "我是京师监狱狱长金海。"；打印第一个字符、最后一个字符、中间字符；打印前三个字符、打印后三个字符；命题：金海在字符串content中。
> - 主要变量/数据名包括：`content`。

> [!example] 本文件出现的新代码 / 函数 / 方法
> - `len()`：获取字符串或容器长度。

### day04/review.txt

```text
一 选择语句
1 if 真值表达式
  if 值:--> bool(值)
     语句块
  bool(0) bool(0.0) bool("") bool(None)---返回False的四种情况

2 if 条件表达式
    if 条件:

    else:
        语句2

    变量 = 语句1 if 条件 else 语句2

二 while 循环:让一段代码在满足条件情况下，重复执行   条件表达式结果为True:条件成立/满足  条件表达式结果为False:条件不成立/不满足
    ① while循环计数
        count = 0 # 计数器初始值
        while 条件:  # 计数器的结束值
            循环体(重复执行的代码)
            count += 值   # 循环计数器自增
    ② while 条件:
        循环体(重复执行的代码)
    ③ while True:
        循环体(重复执行的代码)
        if 条件:
            break # 终止结束循环
    注意:
    while 条件:
        条件满足执行循环体
        [break]  # 如果用break结束的循环，else部分不再执行
    else:
        条件不满足执行的代码

三 for循环:遍历可迭代对象中的数据元素。
        遍历：按照一定的顺序逐个去访问或处理数据集合中的元素的。
        可迭代对象：能依次获取数据元素的对象。例如：容器类型
    for 变量 in 可迭代对象:
        对数据处理的操作(循环体)
```

> [!info] 课堂文本/作业说明
> - 一 选择语句
> - 1 if 真值表达式
> -   if 值:--> bool(值)
> -      语句块
> -   bool(0) bool(0.0) bool("") bool(None)---返回False的四种情况
> - 2 if 条件表达式
> -     if 条件:
> -     else:

## 总结

> [!summary] 总结
> - **今天的核心任务**：学习 `range()` 的开始、结束和步长规则。；学习列表的创建、索引、切片、遍历、添加、插入、删除和排序。；通过登录验证、福彩号码、列表筛选、八大行星等题目练习循环和列表。
> - **真实文件里的练习/主题**：range()函数：生成一系列整数的可迭代对象（整数生成器）；列表list：存储任意数据类型的有序容器；容器通用操作；需求:计算1~100(包含1和100)数字相加之和；登录验证；列表的练习；使用python程序生成一组福彩中奖号码，并判断自己是否中奖；content = "我是京师监狱狱长金海。"。
>
> **新学代码怎么理解**
> - `range()`：生成整数序列，常配合 `for` 控制循环次数。
> - 列表 `[]`：保存一组有顺序、可修改的数据。
> - `.append()`：向列表末尾添加一个元素。
> - `.extend()`：调用对象自身的方法，重点看它修改了哪个对象或返回了什么结果。
> - `.insert()`：在指定位置插入元素。
> - `random.sample()`：调用 `random` 中的 `sample` 功能，结合本文件注释理解它在当前练习中的作用。
> - `len()`：获取字符串或容器长度。
>
> **复盘建议**
> - 先看文件说明，再看原代码，最后解释新函数/方法的输入、输出和用途。
