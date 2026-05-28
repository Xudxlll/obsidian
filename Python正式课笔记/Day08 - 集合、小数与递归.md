# Day08 - 集合、小数与递归

> [!summary] 今日一句话
> 今天补充集合、浮点数精度和递归：集合关注去重与关系，小数提醒我们计算有精度问题，递归让函数自己调用自己。

## 今天到底学了什么

- 集合 `set` 天然去重，适合集合关系运算
- 浮点数不是精确十进制，比较时要考虑误差
- 数据类型转换让不同类型之间可以协作
- 递归把大问题拆成结构相同的小问题

> [!important] 抓主线
> 这一天的代码不是零散练习，而是在训练一个能力链条：先理解数据，再控制流程，再把重复逻辑封装起来。读代码时先看“数据从哪里来”，再看“经过什么判断或循环”，最后看“结果输出到哪里”。

## 课堂图示

**Day08/内存图.png**

![[附件/正式课/Day08/内存图.png]]

**Day08/列表内存图.png**

![[附件/正式课/Day08/列表内存图.png]]


## 课堂代码合集

> 这里集中保留今天所有 `.py` 代码。代码块里补充的是理解代码用的中文说明，不是原项目必须运行的内容。

### Day08/01_rc.py

```python
"""
引用计数
"""
# 说明：把右侧结果保存到 `a`。
a = [1, 2, 3]  # 列表对象的引用计数为1
# 说明：把右侧结果保存到 `b`。
b = a  # 引用计数+1
# 说明：输出内容到控制台，常用于观察程序运行结果。
print(id(a))
# 说明：输出内容到控制台，常用于观察程序运行结果。
print(id(b))

# 说明：把右侧结果保存到 `a`。
a = None # 列表对象的引用计数-1
# 说明：把右侧结果保存到 `b`。
b = 2 # 引用计数为0,被回收
```

### Day08/02_set.py

```python
"""
集合
由一系列不重复且不可变的值组成的可变散列容器
"""
# 说明：把右侧结果保存到 `set1`。
set1 = {1, 1, 2, 3, "PHP", "js", "C++", 1, 5, (11, 22, 33)}

# 添加
set1.add("go")
set1.update(["语文", "数学"])

# 删除
# 说明：按值删除元素。
set1.remove("语文")
set1.discard("数学")
# 说明：弹出元素；不传索引时通常弹出最后一个。
set1.pop()  # 随机删
# set1.clear()

# 说明：输出内容到控制台，常用于观察程序运行结果。
print(set1)
# 遍历
# 说明：遍历可迭代对象，逐个取值执行循环体。
for item in set1:
    # 说明：输出内容到控制台，常用于观察程序运行结果。
    print(item)

# 交集
# 说明：把右侧结果保存到 `set1`。
set1 = {1, 2, 3}
# 说明：把右侧结果保存到 `set2`。
set2 = {3, 4, 5}
# 说明：输出内容到控制台，常用于观察程序运行结果。
print(set1 & set2)
# 并集
# 说明：输出内容到控制台，常用于观察程序运行结果。
print(set1 | set2)
# 差集
# 说明：输出内容到控制台，常用于观察程序运行结果。
print(set1 - set2)
# 说明：输出内容到控制台，常用于观察程序运行结果。
print(set2 - set1)
```

### Day08/03_float.py

```python
"""
浮点数误差解决方案
"""
# 说明：进行比较，结果是 True 或 False。
print((0.1 + 0.7) * 10 == 8)  # F
# 说明：进行比较，结果是 True 或 False。
print((0.2 + 0.6) * 10 == 8)  # T

# 说明：导入模块，后面可以使用模块里的工具。
import decimal

# 说明：把右侧结果保存到 `dec_n1`。
dec_n1 = decimal.Decimal("0.1")
# 说明：把右侧结果保存到 `dec_n2`。
dec_n2 = decimal.Decimal("0.7")

# 说明：进行比较，结果是 True 或 False。
print((dec_n1 + dec_n2) * 10 == 8)
# 说明：输出内容到控制台，常用于观察程序运行结果。
print(type(dec_n1 + dec_n2))
```

### Day08/04_date_change.py

```python
"""
数据类型转换
"""
# 说明：把右侧结果保存到 `list1`。
list1 = [1, 2, 3]
# 说明：输出内容到控制台，常用于观察程序运行结果。
print(tuple(list1))
# 说明：输出内容到控制台，常用于观察程序运行结果。
print(set(list1))

# 说明：把右侧结果保存到 `dict1`。
dict1 = {1: "a", 2: "b"}
# 说明：输出内容到控制台，常用于观察程序运行结果。
print(list(dict1))

# 说明：输出内容到控制台，常用于观察程序运行结果。
print(dict([[1, 2], [3, 4]]))
# 说明：输出内容到控制台，常用于观察程序运行结果。
print(dict(((1, 2), [3, 4])))
# 说明：输出内容到控制台，常用于观察程序运行结果。
print(dict(({1, 2}, {3, 4})))
```

### Day08/05_func.py

```python
"""

"""


# 说明：定义函数 `connect`，参数：host, port, user, pwd, dbname。
def connect(host, port, user, pwd, dbname):
    # 说明：输出内容到控制台，常用于观察程序运行结果。
    print(host, port, user, pwd, dbname)


# 说明：把右侧结果保存到 `connect(host`。
connect(host="localhost", dbname="shukan", user="root", pwd="12346", port=3306)

# **字典实参 字典拆解后字典的键与函数的形参名称对应
# 说明：把右侧结果保存到 `connect_dict`。
connect_dict = {
    "host": "127.0.0.1",
    "dbname": "shops",
    "user": "root",
    "pwd": "66666",
    "port": 3307
}
# 说明：执行算术运算，注意运算符含义和优先级。
connect(**connect_dict)


# 说明：定义函数 `fn`，参数：pos_p1, def_p2="default", *args, **kwargs。
def fn(pos_p1, def_p2="default", *args, **kwargs):
    # 说明：输出内容到控制台，常用于观察程序运行结果。
    print(pos_p1, def_p2, args, kwargs)


# 说明：把右侧结果保存到 `fn(1, "2", 3, 4, 5, 6, key1`。
fn(1, "2", 3, 4, 5, 6, key1=7, key2=8)
```

### Day08/06_recursion.py

```python
"""
函数递归 函数内调用其自身
基本结构:
1.终止(基准/基线)条件 必须有一个终止条件
2.递归调用:把大问题分解成规模更小的相同的子问题,逐步逼近终止条件

应用场景:
1.删除文件夹下的所有内容
2.网站多层级下拉菜单(树遍历)
3.计算数组的维度
4.多层分销佣金计算
...
"""

'''
count = 0

def say():
    print("Hi")

    global count
    count += 1

    if count > 3:
        return

    say()

say()
'''

# 利用递归求 n!(阶乘)
# 5! = 5 * 4 * 3 * 2 * 1 = 120
# 5! = 5 * (5-1) * (4-1) * (3-1) * (2-1) = 120

# 说明：定义函数 `factorial`，参数：n。
def factorial(n):
    # 说明：判断条件是否成立，成立才执行下面缩进代码。
    if n == 0:  # 终止条件 0! = 1
        # 说明：返回结果给函数调用处；return 后函数结束。
        return 1
    # 说明：前面条件都不成立时执行这里。
    else:
        # 说明：返回结果给函数调用处；return 后函数结束。
        return n * factorial(n - 1)

# 说明：输出内容到控制台，常用于观察程序运行结果。
print(factorial(5))
'''
递归展开
5 * factorial(4)
5 * 4 * factorial(3)
5 * 4 * 3 * factorial(2)
5 * 4 * 3 * 2 * factorial(1)
5 * 4 * 3 * 2 * 1 * factorial(0)
5 * 4 * 3 * 2 * 1 * 1
120
'''
```

### Day08/HomeWork01.py

```python
"""
函数的设计原则
1.SRP 单一职责 1个函数只干1件事
2.函数名和参数的名称要清晰(太长/太短都不行,参数数量不能过多)
3.避免副作用
4.合理注释
5.异常处理(后面学)
...
"""

# 不好的设计
'''
def calc_scores(scores, include_highest=True, include_lowest=True,
                round_digits=2):
    if include_highest:  # 保留最高分
        pass
    if include_lowest:  # 保留最低分
        pass
    # 过滤后的分数计算平均分
    average_score = sum(scores) / len(scores)
    # 四舍五入到指定小数位
    average_score = round(average_score, round_digits)
    return average_score


scores = [85, 90, 78, 92, 88]
print(calc_scores(scores, include_highest=False, include_lowest=True, round_digits=1))
'''


# 好的设计
# 说明：定义函数，把一段逻辑封装起来。
def filter_scores(scores: list,
                  # 说明：把右侧结果保存到 `include_highest: bool`。
                  include_highest: bool = True,
                  # 说明：把右侧结果保存到 `include_lowest: bool`。
                  include_lowest: bool = True
                  # 说明：进行比较，结果是 True 或 False。
                  ) -> list:
    """
    :param scores: scores
    :param include_highest:是否保留最高分 默认True 保留
    :param include_lowest:是否保留最低分 默认True 保留
    :return: 过滤后的成绩
    """
    # 说明：判断条件是否成立，成立才执行下面缩进代码。
    if not scores:
        # 说明：返回结果给函数调用处；return 后函数结束。
        return []
    # 说明：判断条件是否成立，成立才执行下面缩进代码。
    if not include_highest:
        # 说明：按值删除元素。
        scores.remove(max(scores))
    # 说明：判断条件是否成立，成立才执行下面缩进代码。
    if not include_lowest:
        # 说明：按值删除元素。
        scores.remove(min(scores))

    # 说明：返回结果给函数调用处；return 后函数结束。
    return scores


# 说明：定义函数，把一段逻辑封装起来。
def calc_avg(scores: list, round_digits: int = 2) -> float:
    """
    计算平均分,并保留指定的小数位数,默认为2
    :param scores: 成绩
    :param round_digits: 保留小数位数
    :return: 平均分
    """
    # 说明：判断条件是否成立，成立才执行下面缩进代码。
    if not scores:
        # 说明：返回结果给函数调用处；return 后函数结束。
        return 0
    # 说明：把右侧结果保存到 `avg_score`。
    avg_score = sum(scores) / len(scores)
    # 说明：返回结果给函数调用处；return 后函数结束。
    return round(avg_score, round_digits)


# 说明：把右侧结果保存到 `scores`。
scores = [85, 90, 78, 92, 88]
# 说明：把右侧结果保存到 `filted_scores`。
filted_scores = filter_scores(scores, include_highest=False, include_lowest=True)
# 说明：把右侧结果保存到 `avg_score`。
avg_score = calc_avg(filted_scores, round_digits=1)
# 说明：输出内容到控制台，常用于观察程序运行结果。
print(avg_score)
```

## 课堂要求与作业原文

### Day08/HomeWork.txt

```text
1.完成今日代码
2.完成下列练习
  ①EShopManagerV1.py 改成 EShopManagerV2.py 函数版
3.预习:面向对象基础
```

## 融会贯通笔记

### 集合适合处理“唯一性”和“关系”

- 集合不会保留重复元素。
- 交集、并集、差集可以表达两个数据组之间的关系。
- 集合无序，所以不能像列表一样靠索引取值。

### 浮点数精度是计算机表示方式导致的

- 有些十进制小数无法被二进制精确表示。
- 比较浮点数时不要直接迷信 `==`，可以比较差值是否足够小。
- 金额等高精度场景要考虑 `Decimal`。

### 递归的关键是出口和递推关系

- 递归函数会调用自己。
- 必须有结束条件，否则会无限调用直到栈溢出。
- 阶乘、累加、斐波那契都适合用来理解递归。

## 复盘自查

- [ ] 能用 set 去重
- [ ] 能解释为什么 0.1 + 0.2 可能不是精确 0.3
- [ ] 能写出有终止条件的递归函数
