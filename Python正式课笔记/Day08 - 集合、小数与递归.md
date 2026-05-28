## 今天学了什么

> [!info] 今天学了什么
> - 复习引用计数和对象回收。
> - 学习集合 `set` 的去重、添加、更新、删除、遍历、交集、并集、差集。
> - 学习浮点数误差，并使用 `decimal.Decimal` 做精确小数计算。
> - 复习列表、元组、集合、字典之间的数据类型转换。
> - 学习递归的终止条件和递归调用，用阶乘例子理解展开过程。

## 抓主线

> [!tip] 抓主线
> 1. 引用计数帮助理解对象生命周期。
> 2. 集合用于唯一值和集合关系运算。
> 3. Decimal 用于避免常见浮点误差。
> 4. 递归把大问题拆成同结构的小问题。

## 课堂代码合集

### Day08/01_rc.py

```python
"""
引用计数
"""
a = [1, 2, 3]  # 列表对象的引用计数为1
b = a  # 引用计数+1
print(id(a))
print(id(b))

a = None # 列表对象的引用计数-1
b = 2 # 引用计数为0,被回收
```

> [!quote] 相关图示理解
> ![[附件/正式课/Day08/列表内存图.png]]
> 这张图对应 `Day08/01_rc.py` 的知识点。复盘时重点看变量、对象和值之间的指向关系，再对照上面的代码运行过程。

> [!note] 这份文件实际讲了什么
> - 文件说明/题目写的是：引用计数。
> - 主要变量/数据名包括：`a`、`b`。

> [!example] 本文件出现的新代码 / 函数 / 方法
> - `id()`：查看对象身份标识，常用于理解变量引用。
> - 从原文件注释/说明看，本文件重点是：列表对象的引用计数为1；列表对象的引用计数-1。

> [!abstract] 代码逻辑怎么走
> - 通过赋值语句保存中间结果，主要变量包括：`a`、`b`。

> [!warning] 需要注意的点
> - 列表是可变对象，增删改会直接影响原列表。

> [!success] 举一反三
> - 可以把单个变量升级为列表，批量保存多条数据后统一遍历处理。

### Day08/02_set.py

```python
"""
集合
由一系列不重复且不可变的值组成的可变散列容器
"""
set1 = {1, 1, 2, 3, "PHP", "js", "C++", 1, 5, (11, 22, 33)}

# 添加
set1.add("go")
set1.update(["语文", "数学"])

# 删除
set1.remove("语文")
set1.discard("数学")
set1.pop()  # 随机删
# set1.clear()

print(set1)
# 遍历
for item in set1:
    print(item)

# 交集
set1 = {1, 2, 3}
set2 = {3, 4, 5}
print(set1 & set2)
# 并集
print(set1 | set2)
# 差集
print(set1 - set2)
print(set2 - set1)
```

> [!quote] 相关图示理解
> ![[附件/正式课/Day08/内存图.png]]
> 这张图对应 `Day08/02_set.py` 的知识点。复盘时重点看变量、对象和值之间的指向关系，再对照上面的代码运行过程。

> [!note] 这份文件实际讲了什么
> - 文件说明/题目写的是：集合；由一系列不重复且不可变的值组成的可变散列容器。
> - 主要变量/数据名包括：`set1`、`set2`。

> [!example] 本文件出现的新代码 / 函数 / 方法
> - 集合 `{...}`：保存不重复元素，适合去重和集合运算。
> - `.add()`：向集合添加一个元素。
> - `.discard()`：从集合删除元素，元素不存在也不报错。
> - 从原文件注释/说明看，本文件重点是：集合。

> [!abstract] 代码逻辑怎么走
> - 使用 `for` 遍历序列或容器，对每个元素执行同样的处理。
> - 通过赋值语句保存中间结果，主要变量包括：`set1`、`set2`。

> [!warning] 需要注意的点
> - 列表是可变对象，增删改会直接影响原列表。
> - 集合无序且自动去重，不能依赖固定下标访问。

> [!success] 举一反三
> - 可以把单个变量升级为列表，批量保存多条数据后统一遍历处理。
> - 可以把循环和条件组合起来做筛选、统计、累加、菜单系统。
> - 可以用集合做名单去重、共同元素、差异元素统计。

### Day08/03_float.py

```python
"""
浮点数误差解决方案
"""
print((0.1 + 0.7) * 10 == 8)  # F
print((0.2 + 0.6) * 10 == 8)  # T

import decimal

dec_n1 = decimal.Decimal("0.1")
dec_n2 = decimal.Decimal("0.7")

print((dec_n1 + dec_n2) * 10 == 8)
print(type(dec_n1 + dec_n2))
```

> [!note] 这份文件实际讲了什么
> - 文件说明/题目写的是：浮点数误差解决方案。
> - 主要变量/数据名包括：`dec_n1`、`dec_n2`。

> [!example] 本文件出现的新代码 / 函数 / 方法
> - `import decimal`：导入 decimal 模块，为精确小数计算做准备。
> - `decimal.Decimal()`：创建精确十进制小数，用来处理浮点误差。

> [!abstract] 代码逻辑怎么走
> - 通过赋值语句保存中间结果，主要变量包括：`dec_n1`、`dec_n2`。

> [!warning] 需要注意的点
> - 浮点数可能有精度误差，精确小数计算可以使用 `decimal.Decimal`。

> [!success] 举一反三
> - 可以修改示例数据重新运行，观察输出如何变化。

### Day08/04_date_change.py

```python
"""
数据类型转换
"""
list1 = [1, 2, 3]
print(tuple(list1))
print(set(list1))

dict1 = {1: "a", 2: "b"}
print(list(dict1))

print(dict([[1, 2], [3, 4]]))
print(dict(((1, 2), [3, 4])))
print(dict(({1, 2}, {3, 4})))
```

> [!note] 这份文件实际讲了什么
> - 文件说明/题目写的是：数据类型转换。
> - 主要变量/数据名包括：`list1`、`dict1`。

> [!example] 本文件出现的新代码 / 函数 / 方法
> - `tuple()`：转换或创建元组。
> - `set()`：转换或创建集合，也常用于去重。
> - `list()`：转换或创建列表。
> - `dict()`：转换或创建字典。

> [!abstract] 代码逻辑怎么走
> - 通过赋值语句保存中间结果，主要变量包括：`list1`、`dict1`。

> [!warning] 需要注意的点
> - 字典按 key 取值，key 要唯一；遍历键值对时优先想到 `.items()`。
> - 列表是可变对象，增删改会直接影响原列表。
> - 集合无序且自动去重，不能依赖固定下标访问。

> [!success] 举一反三
> - 可以把同样结构用于学生信息、商品信息、地区数据等 key-value 场景。
> - 可以把单个变量升级为列表，批量保存多条数据后统一遍历处理。
> - 可以用集合做名单去重、共同元素、差异元素统计。

### Day08/05_func.py

```python
"""

"""


def connect(host, port, user, pwd, dbname):
    print(host, port, user, pwd, dbname)


connect(host="localhost", dbname="shukan", user="root", pwd="12346", port=3306)

# **字典实参 字典拆解后字典的键与函数的形参名称对应
connect_dict = {
    "host": "127.0.0.1",
    "dbname": "shops",
    "user": "root",
    "pwd": "66666",
    "port": 3307
}
connect(**connect_dict)


def fn(pos_p1, def_p2="default", *args, **kwargs):
    print(pos_p1, def_p2, args, kwargs)


fn(1, "2", 3, 4, 5, 6, key1=7, key2=8)
```

> [!note] 这份文件实际讲了什么
> - 文件说明/题目写的是：**字典实参 字典拆解后字典的键与函数的形参名称对应。
> - 文件中定义了函数：`connect(host, port, user, pwd, dbname)`、`fn(pos_p1, def_p2, *args, **kwargs)`。
> - 主要变量/数据名包括：`connect_dict`。

> [!example] 本文件出现的新代码 / 函数 / 方法
> - 本文件主要是在复习或组合前面已经学过的写法，没有引入需要单独记忆的新函数/方法；重点看它如何把旧知识组合成当前题目。
> - 从原文件注释/说明看，本文件重点是：**字典实参 字典拆解后字典的键与函数的形参名称对应。

> [!abstract] 代码逻辑怎么走
> - 先定义函数，把某段功能封装起来；后面通过函数名加括号调用。
> - 通过赋值语句保存中间结果，主要变量包括：`connect_dict`。

> [!warning] 需要注意的点
> - 字典按 key 取值，key 要唯一；遍历键值对时优先想到 `.items()`。

> [!success] 举一反三
> - 可以把同样结构用于学生信息、商品信息、地区数据等 key-value 场景。
> - 可以继续把重复逻辑拆成函数，让主流程只负责调用。

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

def factorial(n):
    if n == 0:  # 终止条件 0! = 1
        return 1
    else:
        return n * factorial(n - 1)

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

> [!note] 这份文件实际讲了什么
> - 文件说明/题目写的是：函数递归 函数内调用其自身；基本结构:；1.终止(基准/基线)条件 必须有一个终止条件；2.递归调用:把大问题分解成规模更小的相同的子问题,逐步逼近终止条件；应用场景:。
> - 后续说明/题目还包括：count = 0；def say():；print("Hi") / 递归展开；5 * factorial(4)；5 * 4 * factorial(3)。
> - 文件中定义了函数：`factorial(n)`。

> [!example] 本文件出现的新代码 / 函数 / 方法
> - 递归：函数在内部调用自身，必须配合终止条件。
> - 从原文件注释/说明看，本文件重点是：函数递归 函数内调用其自身；2.递归调用:把大问题分解成规模更小的相同的子问题,逐步逼近终止条件。

> [!abstract] 代码逻辑怎么走
> - 先定义函数，把某段功能封装起来；后面通过函数名加括号调用。
> - 使用条件判断把不同情况分开处理。

> [!warning] 需要注意的点
> - 递归必须有终止条件，并且每次递归调用都要向终止条件靠近。

> [!success] 举一反三
> - 可以继续把重复逻辑拆成函数，让主流程只负责调用。

### Day08/HomeWork.txt

```text
1.完成今日代码
2.完成下列练习
  ①EShopManagerV1.py 改成 EShopManagerV2.py 函数版
3.预习:面向对象基础
```

> [!info] 课堂文本/作业说明
> - 1.完成今日代码
> - 2.完成下列练习
> - ①EShopManagerV1.py 改成 EShopManagerV2.py 函数版
> - 3.预习:面向对象基础

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
def filter_scores(scores: list,
                  include_highest: bool = True,
                  include_lowest: bool = True
                  ) -> list:
    """
    :param scores: scores
    :param include_highest:是否保留最高分 默认True 保留
    :param include_lowest:是否保留最低分 默认True 保留
    :return: 过滤后的成绩
    """
    if not scores:
        return []
    if not include_highest:
        scores.remove(max(scores))
    if not include_lowest:
        scores.remove(min(scores))

    return scores


def calc_avg(scores: list, round_digits: int = 2) -> float:
    """
    计算平均分,并保留指定的小数位数,默认为2
    :param scores: 成绩
    :param round_digits: 保留小数位数
    :return: 平均分
    """
    if not scores:
        return 0
    avg_score = sum(scores) / len(scores)
    return round(avg_score, round_digits)


scores = [85, 90, 78, 92, 88]
filted_scores = filter_scores(scores, include_highest=False, include_lowest=True)
avg_score = calc_avg(filted_scores, round_digits=1)
print(avg_score)
```

> [!note] 这份文件实际讲了什么
> - 文件说明/题目写的是：函数的设计原则；1.SRP 单一职责 1个函数只干1件事；2.函数名和参数的名称要清晰(太长/太短都不行,参数数量不能过多)；3.避免副作用；4.合理注释。
> - 后续说明/题目还包括：def calc_scores(scores, include_highest=True, include_lowest=True,；round_digits=2):；if include_highest:  # 保留最高分 / :param scores: scores；:param include_highest:是否保留最高分 默认True 保留；:param include_lowest:是否保留最低分 默认True 保留 / 计算平均分,并保留指定的小数位数,默认为2；:param scores: 成绩；:param round_digits: 保留小数位数。
> - 文件中定义了函数：`filter_scores(scores, include_highest, include_lowest)`、`calc_avg(scores, round_digits)`。
> - 主要变量/数据名包括：`avg_score`、`scores`、`filted_scores`。

> [!example] 本文件出现的新代码 / 函数 / 方法
> - 本文件主要是在复习或组合前面已经学过的写法，没有引入需要单独记忆的新函数/方法；重点看它如何把旧知识组合成当前题目。
> - 从原文件注释/说明看，本文件重点是：函数的设计原则；1.SRP 单一职责 1个函数只干1件事。

> [!abstract] 代码逻辑怎么走
> - 先定义函数，把某段功能封装起来；后面通过函数名加括号调用。
> - 使用条件判断把不同情况分开处理。
> - 通过赋值语句保存中间结果，主要变量包括：`avg_score`、`scores`、`filted_scores`。

> [!warning] 需要注意的点
> - 列表是可变对象，增删改会直接影响原列表。

> [!success] 举一反三
> - 可以把单个变量升级为列表，批量保存多条数据后统一遍历处理。
> - 可以继续把重复逻辑拆成函数，让主流程只负责调用。

## 总结

> [!summary] 总结
> - **今天的核心任务**：复习引用计数和对象回收。；学习集合 `set` 的去重、添加、更新、删除、遍历、交集、并集、差集。；学习浮点数误差，并使用 `decimal.Decimal` 做精确小数计算。
> - **真实文件里的练习/主题**：引用计数；集合；浮点数误差解决方案；数据类型转换；函数递归 函数内调用其自身；函数的设计原则。
>
> **新学代码怎么理解**
> - `id()`：查看对象身份标识，常用于理解变量引用。
> - 集合 `{...}`：保存不重复元素，适合去重和集合运算。
> - `.add()`：向集合添加一个元素。
> - `.discard()`：从集合删除元素，元素不存在也不报错。
> - `import decimal`：导入 decimal 模块，为精确小数计算做准备。
> - **decimal.Decimal()**：`decimal.Decimal` 用十进制方式表示小数，能减少普通浮点数的精度误差。
> - **tuple()**：元组用于保存不可变序列，适合不希望被修改的数据组合。
> - **set()**：集合会自动去重，适合处理唯一值、交集、并集、差集。
> - **list()**：列表用于保存一组有顺序、可修改的数据，是批量处理的基础容器。
> - **dict()**：字典用 key-value 描述结构化数据，适合商品、学生、地区信息这类对象。
>
> **复盘建议**
> - 先看每份文件的三引号说明或注释，判断题目要解决什么问题。
> - 再看本文件真正新增的函数/方法，弄清楚它接收什么、返回什么、是否会修改原对象。
> - 最后把代码逻辑按“输入/准备数据 -> 分支或循环处理 -> 输出/返回结果”复述一遍。
