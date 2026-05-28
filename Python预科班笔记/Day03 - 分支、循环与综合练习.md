## 今天学了什么

> [!info] 今天学了什么
> - 学习真值表达式和条件表达式，让判断写法更灵活。
> - 学习 `while` 和 `for` 两种循环方式，区分条件循环和遍历循环。
> - 使用 `break`、`while...else`、随机数和计数器完成猜数字等练习。
> - 通过闰年、平均成绩、小球反弹、出租车计价等题目综合流程控制。

## 抓主线

> [!tip] 抓主线
> 1. 分支负责判断当前情况。
> 2. 循环负责重复处理同类任务。
> 3. 计数器、累加器和状态变量记录循环过程。
> 4. 综合题把输入、判断、循环、计算和格式化输出连起来。

## 课堂代码合集

### day03/01_demo.py

```python
"""
    if 真值表达式
    在控制台获取一个内容，如果内容不为空，则打印输出内容
"""

# if 100:
#     print("真值”)
# # 等同于
# if bool(100):
#     print("真值”)

content = input("请输入一段数据:")
if content:   # bool(content)
    print("您的内容是:content")
else:
    print("输入内容为空")
```

> [!note] 这份文件实际讲了什么
> - 文件说明/题目写的是：if 真值表达式；在控制台获取一个内容，如果内容不为空，则打印输出内容；if 100:；print("真值”)。
> - 主要变量/数据名包括：`content`。

> [!example] 本文件出现的新代码 / 函数 / 方法
> - 本文件主要是在复习或组合前面已经学过的写法，没有引入需要单独记忆的新函数/方法；重点看它如何把旧知识组合成当前题目。

### day03/02_demo.py

```python
"""
    if 条件表达式
"""
# number = int(input("请输入一个大于0的整数:"))
# if number % 2 == 0:
#     print("偶数")
# else:
#     print("奇数")
#
# data = "偶数" if number % 2 == 0 else "奇数"
# print(data)

"""
    在终端输入一个正确的成绩，判断并打印是否及格(及格线:60)
"""
# grade = float(input("请输入成绩："))
# if grade >= 60:
#     print("成绩及格")
# else:
#     print("成绩不及格")

grade = "及格" if float(input("请输入成绩：")) >= 60 else "不及格"
print(grade)
```

> [!note] 这份文件实际讲了什么
> - 文件说明/题目写的是：if 条件表达式；在终端输入一个正确的成绩，判断并打印是否及格(及格线:60)；number = int(input("请输入一个大于0的整数:"))；if number % 2 == 0:。
> - 主要变量/数据名包括：`grade`。

> [!example] 本文件出现的新代码 / 函数 / 方法
> - 本文件主要是在复习或组合前面已经学过的写法，没有引入需要单独记忆的新函数/方法；重点看它如何把旧知识组合成当前题目。

### day03/03_demo.py

```python
""""
    循环结构
"""

# count = 0  # 循环前设定计数器初始值(记录自己的圈数值)
# while count < 3:  # 循环条件 设定计数器的结束值
#     # 重复执行的代码块(循环体)
#     print("跑圈")
#     count += 1  # 循环内让计数器值自增
#
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
# # 在终端中显示 1 3 5 7
# count = 1
# while count < 8:
#     print(count)
#     count += 2
# # 在终端中显示 8 7 6 5 4
# count = 8
# while count > 3:
#     print(count)
#     count -= 1
# # 在终端中显示 -1 -2 -3 -4 -5
# count = -1
# while count > -6:
#     print(count)
#     count -= 1

count = 0
while True:
    print("跑圈")
    count += 1
    if count == 3:
        print("到极限了")
        break  # 用break语句结束的循环，else不执行 (break执行的前提是while后面的条件满足)
else:  # 循环条件不满足
    print("循环条件不满足的情况下执行的语句")
```

> [!note] 这份文件实际讲了什么
> - 文件说明/题目写的是："；循环结构；count = 0  # 循环前设定计数器初始值(记录自己的圈数值)；while count < 3:  # 循环条件 设定计数器的结束值。
> - 主要变量/数据名包括：`count`。

> [!example] 本文件出现的新代码 / 函数 / 方法
> - `while`：条件循环，适合不知道具体循环次数的场景。
> - `break`：跳出当前循环。

> [!abstract] 代码逻辑怎么走
> - 使用 `while` 形成持续循环，通常用于菜单、重复输入或未知次数的处理。

> [!warning] 需要注意的点
> - `while` 循环要保证条件会变化，否则容易进入死循环。
> - `break` 只跳出当前这一层循环。

> [!success] 举一反三
> - 可以把循环和条件组合起来做筛选、统计、累加、菜单系统。

### day03/04_demo.py

```python
"""
    for循环：遍历可迭代对象的数据元素
    可迭代对象：指能依次获取数据元素的对象，例如:容器类型。
    遍历：按照一定的顺序逐个访问（拿）并处理（对数据的操作）数据集合中的元素的。
"""
# for 变量 in 可迭代对象:
#     对数据处理操作

message = "python"
for item in message:
    print(item)
```

> [!note] 这份文件实际讲了什么
> - 文件说明/题目写的是：for循环：遍历可迭代对象的数据元素；可迭代对象：指能依次获取数据元素的对象，例如:容器类型。；遍历：按照一定的顺序逐个访问（拿）并处理（对数据的操作）数据集合中的元素的。；for 变量 in 可迭代对象:。
> - 主要变量/数据名包括：`message`。

> [!example] 本文件出现的新代码 / 函数 / 方法
> - `for`：遍历循环，逐个处理序列或容器中的元素。

> [!abstract] 代码逻辑怎么走
> - 使用 `for` 遍历序列或容器，对每个元素执行同样的处理。

### day03/exercise02.py

```python
"""
商场推出了商品优惠活动，活动内容如下:
1、如果是VIP客户，消费小于500元，则享受85折，否则享受8折。
2、若不是VIP客户，消费大于800元，则享受9折，否则原价。
根据用户输入的账户类型及消费金额，打印折扣信息及折扣后的应付金额
"""
customer_type = input("请输入账户类型(VIP客户或者普通客户)：")
amount = float(input("请输入消费金额(元)："))
if customer_type == "VIP客户":
    if amount < 0:
        print("输入错误，金额不能为负")
    elif amount < 500:
        print(f"85折：{amount*0.85}元")
    else:
        print(f"8折：{amount*0.8}元")
elif customer_type == "普通客户":
    if amount < 0:
        print("输入错误，金额不能为负")
    elif amount > 800:
        print(f"9折：{amount*0.9}元")
    else:
        print(f"原价：{amount}元")
else:
    print("输入错误，请按要求输入账户类型")
```

> [!note] 这份文件实际讲了什么
> - 文件说明/题目写的是：商场推出了商品优惠活动，活动内容如下:；1、如果是VIP客户，消费小于500元，则享受85折，否则享受8折。；2、若不是VIP客户，消费大于800元，则享受9折，否则原价。；根据用户输入的账户类型及消费金额，打印折扣信息及折扣后的应付金额。
> - 主要变量/数据名包括：`customer_type`、`amount`。

> [!example] 本文件出现的新代码 / 函数 / 方法
> - 本文件主要是在复习或组合前面已经学过的写法，没有引入需要单独记忆的新函数/方法；重点看它如何把旧知识组合成当前题目。

### day03/exercise03.py

```python
"""
在终端中输入一个年份，如果是闰年为变量day赋值29，否则赋值28。
闰年条件:年份能被4整除但是不能被100整除 或者 年份能被400整除
效果:
请输入年份:2020
2月有29天
"""
# year = int(input("请输入年份："))
# if (year % 4 == 0 and year % 100 != 0) or year % 400 == 0:
#     day = 29
#     print(f"2月有{day}天")
# else:
#     day = 28
#     print(f"2月有{day}天")

year = int(input("请输入年份："))
day = 29 if (year % 4 == 0 and year % 100 != 0) or year % 400 == 0 else 28
print(f"2月有{day}天")
```

> [!note] 这份文件实际讲了什么
> - 文件说明/题目写的是：在终端中输入一个年份，如果是闰年为变量day赋值29，否则赋值28。；闰年条件:年份能被4整除但是不能被100整除 或者 年份能被400整除；效果:；请输入年份:2020。
> - 主要变量/数据名包括：`year`、`day`。

> [!example] 本文件出现的新代码 / 函数 / 方法
> - `%` 字符串格式化：用 `%s`、`%d` 等占位后再填入变量。

### day03/exercise04.py

```python
"""
    练习:在终端中循环录入5个成绩,最后打印平均成绩(总成绩除以人数)
"""

total = 0
count = 0
while count <= 4:
    grade = float(input("成绩："))
    total += grade
    count += 1
print(total/5)
```

> [!note] 这份文件实际讲了什么
> - 文件说明/题目写的是：练习:在终端中循环录入5个成绩,最后打印平均成绩(总成绩除以人数)。
> - 主要变量/数据名包括：`total`、`count`、`grade`。

> [!example] 本文件出现的新代码 / 函数 / 方法
> - 本文件主要是在复习或组合前面已经学过的写法，没有引入需要单独记忆的新函数/方法；重点看它如何把旧知识组合成当前题目。

### day03/exercise05.py

```python
"""
一个小球从100m的高度落下，每次弹回原高度一半。
请计算:
总共经过多少次，最终落地(最小弹起高度0.01
总共经过多少米
"""
# 最后一次落下的时候发现下一次弹起高度不足0.01，那这最后一次落下认为触地
height = 100
n = 0
total = 100
while height > 30:
    height /= 2
    total += 2 * height
    n += 1
print(f"总共经过{n}次，最终落地", f"总共经过{total}米")
```

> [!note] 这份文件实际讲了什么
> - 文件说明/题目写的是：一个小球从100m的高度落下，每次弹回原高度一半。；请计算:；总共经过多少次，最终落地(最小弹起高度0.01；总共经过多少米。
> - 主要变量/数据名包括：`height`、`n`、`total`。

> [!example] 本文件出现的新代码 / 函数 / 方法
> - 本文件主要是在复习或组合前面已经学过的写法，没有引入需要单独记忆的新函数/方法；重点看它如何把旧知识组合成当前题目。

### day03/exercise06.py

```python
"""
程序产生1个 1到100之间的随机数，让玩家重复猜测,直到猜对为止，每次提示:大了、小了、对了
打印总共猜了多少次。
"""
import random  # 导入随即模块   在当前文件中可以直接使用random模块的代码功能

## 方法一：理解break的用法
# # 第一步：系统随机产生1~100之间的整数
# true_number = random.randint(1,100)   # randint(a,b):在一定范围内产生一个随机整数
# print(true_number)
# # 第二步：猜数字
# count = 0
# while True:
#     count += 1
#     guess_number = int(input("请猜测一个1~100之间的整数："))
#     if guess_number > true_number:   # 如果玩家猜测的数字 大于 true_number --> 猜大了
#         print("猜大了")
#     elif guess_number < true_number:   # 如果玩家猜测的数字 小于 true_number --> 猜小了
#         print("猜小了")
#     else:   # 如果玩家猜测的数字 等于 true_number --> 猜对了
#         print("猜对了")
#         break
# # 第三步：输出结果
# print(f"玩家猜测了{count}次猜对了")

## 方法二：理解while...else的用法
# 第一步：系统随机产生1~100之间的整数
true_number = random.randint(1,100)   # randint(a,b):在一定范围内产生一个随机整数
print(true_number)
# 第二步：猜数字
count = 0
guess_number = int(input("请猜测一个1~100之间的整数："))
while guess_number != true_number:
    if guess_number > true_number:   # 如果玩家猜测的数字 大于 true_number --> 猜大了
        print("猜大了")
        guess_number = int(input("请猜测一个1~100之间的整数："))
    elif guess_number < true_number:   # 如果玩家猜测的数字 小于 true_number --> 猜小了
        print("猜小了")
        guess_number = int(input("请猜测一个1~100之间的整数："))
    count += 1
else:   # 如果玩家猜测的数字 等于 true_number --> 猜对了
    print("猜对了")
    count += 1
# 第三步：输出结果
print(f"玩家猜测了{count}次猜对了")
```

> [!note] 这份文件实际讲了什么
> - 文件说明/题目写的是：程序产生1个 1到100之间的随机数，让玩家重复猜测,直到猜对为止，每次提示:大了、小了、对了；打印总共猜了多少次。；导入随即模块   在当前文件中可以直接使用random模块的代码功能；方法一：理解break的用法。
> - 主要变量/数据名包括：`true_number`、`count`、`guess_number`。

> [!example] 本文件出现的新代码 / 函数 / 方法
> - `import random`：导入 `random` 模块，为本文件后续调用它的功能做准备。
> - `random.randint()`：调用 `random` 中的 `randint` 功能，结合本文件注释理解它在当前练习中的作用。

### day03/exercise07.py

```python
"""
在终端中获取一个四位整数，计算每位相加和。
输入:1234
输出:10
"""
num1 = input("请输入一个四位整数：")   # 不能用int()，因为整数值不能拆分
total = 0
for item in num1:
    total += int(item)
print(total)
```

> [!note] 这份文件实际讲了什么
> - 文件说明/题目写的是：在终端中获取一个四位整数，计算每位相加和。；输入:1234；输出:10；不能用int()，因为整数值不能拆分。
> - 主要变量/数据名包括：`num1`、`total`。

> [!example] 本文件出现的新代码 / 函数 / 方法
> - 本文件主要是在复习或组合前面已经学过的写法，没有引入需要单独记忆的新函数/方法；重点看它如何把旧知识组合成当前题目。

### day03/homework.py

```python
"""
模拟北京出租车计价器
起步价:13元(包含3公里)，
超过3公里，但没超过15公里的部分，每公里2.3元
超过15公里的部分，每公里加收2.3元的50%
要求:计算并打印应付的车费，小数部分保留2位数。
"""
distance = float(input("请输入行驶里程（公里）："))
if distance < 0:
    print("输入有误")
elif distance <= 3:
    money = 13
    print(f"应付车费{round(money,2)}元")
elif distance <= 15:
    money = 13 + (distance - 3) * 2.3
    print(f"应付车费{round(money,2)}元")
else:
    money = 13 + 2.3 * 12 + (distance - 15) * 2.3 * 0.5
    print((f"应付车费{round(money,2)}元"))
```

> [!note] 这份文件实际讲了什么
> - 文件说明/题目写的是：模拟北京出租车计价器；起步价:13元(包含3公里)，；超过3公里，但没超过15公里的部分，每公里2.3元；超过15公里的部分，每公里加收2.3元的50%。
> - 主要变量/数据名包括：`distance`、`money`。

> [!example] 本文件出现的新代码 / 函数 / 方法
> - `round()`：按指定小数位四舍五入。

## 总结

> [!summary] 总结
> - **今天的核心任务**：学习真值表达式和条件表达式，让判断写法更灵活。；学习 `while` 和 `for` 两种循环方式，区分条件循环和遍历循环。；使用 `break`、`while...else`、随机数和计数器完成猜数字等练习。
> - **真实文件里的练习/主题**：if 真值表达式；if 条件表达式；"；for循环：遍历可迭代对象的数据元素；商场推出了商品优惠活动，活动内容如下:；在终端中输入一个年份，如果是闰年为变量day赋值29，否则赋值28。；练习:在终端中循环录入5个成绩,最后打印平均成绩(总成绩除以人数)；一个小球从100m的高度落下，每次弹回原高度一半。。
>
> **新学代码怎么理解**
> - `while`：条件循环，适合不知道具体循环次数的场景。
> - `break`：跳出当前循环。
> - `for`：遍历循环，逐个处理序列或容器中的元素。
> - `%` 字符串格式化：用 `%s`、`%d` 等占位后再填入变量。
> - `import random`：导入 `random` 模块，为本文件后续调用它的功能做准备。
> - `random.randint()`：调用 `random` 中的 `randint` 功能，结合本文件注释理解它在当前练习中的作用。
> - `round()`：按指定小数位四舍五入。
>
> **复盘建议**
> - 先看文件说明，再看原代码，最后解释新函数/方法的输入、输出和用途。
