## 今天学了什么

> [!info] 今天学了什么
> - 学习实参、形参、可变位置参数 `*args`、可变关键字参数 `**kwargs`、默认值形参。
> - 学习 `return` 返回值，并区分返回结果和打印结果。
> - 学习局部作用域、全局作用域、嵌套作用域和 `global`。
> - 理解可变类型和不可变类型传入函数后的修改差异。
> - 通过回文字符串、总秒数、列表去重等题目练习函数设计。

## 抓主线

> [!tip] 抓主线
> 1. 参数把外部数据送进函数。
> 2. `return` 把函数结果交回调用处。
> 3. 作用域决定变量在哪里有效。
> 4. 函数设计决定代码是否清楚、可复用。

## 课堂代码合集

### Day07/01_args.py

```python
"""
实参专题
"""


# 位置传参:实参和形参的位置依次对应
def f1(p1, p2, p3):
    print(p1)
    print(p2)
    print(p3)

f1(1, 2, 3)

print("-" * 20)

# 关键字传参:实参根据形参的名字对应 
def f2(p1, p2, p3):
    print(p1)
    print(p2)
    print(p3)

f2(p3=1, p1=2, p2=3)
f2(1, p3=2, p2=3)
# f2(p3=1, 2, p1=3) #报错

print("-" * 20)

# 序列传参: 实参使用*号序列拆解后与形参的位置对应
def f3(p1, p2, p3):
    print(p1)
    print(p2)
    print(p3)

list1 = [1, 2, 3]
f3(*list1)
```

> [!note] 这份文件实际讲了什么
> - 文件说明/题目写的是：实参专题。
> - 文件中定义了函数：`f1(p1, p2, p3)`、`f2(p1, p2, p3)`、`f3(p1, p2, p3)`。
> - 主要变量/数据名包括：`list1`。

> [!example] 本文件出现的新代码 / 函数 / 方法
> - 本文件主要是在复习或组合前面已经学过的写法，没有引入需要单独记忆的新函数/方法；重点看它如何把旧知识组合成当前题目。
> - 从原文件注释/说明看，本文件重点是：实参专题。

> [!abstract] 代码逻辑怎么走
> - 先定义函数，把某段功能封装起来；后面通过函数名加括号调用。
> - 通过赋值语句保存中间结果，主要变量包括：`list1`。

> [!warning] 需要注意的点
> - 列表是可变对象，增删改会直接影响原列表。

> [!success] 举一反三
> - 可以把单个变量升级为列表，批量保存多条数据后统一遍历处理。
> - 可以继续把重复逻辑拆成函数，让主流程只负责调用。

### Day07/02_parameter.py

```python
"""
形参专题
"""


# 可变数量的位置参数(*号元组形参)
# 把实参合并成一个元组
def f1(*args):
    print(args)


f1()
f1(1)
f1(1, 2, 3)

print("-" * 20)

# 可变数量的关键字参数(**字典形参)
# 把实参合并成一个字典
def f2(**kwargs):
    print(kwargs)


f2()
f2(name="xiaoyu")
f2(name="xiaoyu", sex="女")


print("-" * 20)


# 默认值形参:形参拥有默认值
def f3(p1, p2=0, p3=0):

    print(p1)
    print(p2)
    print(p3)


f3(1)
f3(1, 2)
f3(1, p3=3)
```

> [!note] 这份文件实际讲了什么
> - 文件说明/题目写的是：形参专题。
> - 文件中定义了函数：`f1(*args)`、`f2(**kwargs)`、`f3(p1, p2, p3)`。

> [!example] 本文件出现的新代码 / 函数 / 方法
> - `*args`：可变数量的位置参数，函数内部接收到元组。
> - `**kwargs`：可变数量的关键字参数，函数内部接收到字典。
> - 默认值形参：调用函数时不传该参数，就使用默认值。
> - 从原文件注释/说明看，本文件重点是：形参专题；可变数量的位置参数(*号元组形参)。

> [!abstract] 代码逻辑怎么走
> - 先定义函数，把某段功能封装起来；后面通过函数名加括号调用。

> [!warning] 需要注意的点
> - 读这份代码时，先看变量如何变化，再看最终输出。

> [!success] 举一反三
> - 可以继续把重复逻辑拆成函数，让主流程只负责调用。

### Day07/03_retrun.py

```python
"""
返回值
retrun 把函数的结果返回出去,供其他程序使用

"""


def my_len(lst):
    num_count = 0
    for item in lst:
        num_count += 1

    # 如果函数没有 return 或return后没值 相当于None
    # 终止函数
    # 只能返回一个值,类型不限制 list str 函数...
    return num_count


list1 = [1, 2, 3, 4]
print(my_len(list1))

# for i in range(len(list1)):
#     print(list1[i])
#
# for i in range(my_len(list1)):
#     print(list1[i])
```

> [!note] 这份文件实际讲了什么
> - 文件说明/题目写的是：返回值；retrun 把函数的结果返回出去,供其他程序使用。
> - 文件中定义了函数：`my_len(lst)`。
> - 主要变量/数据名包括：`num_count`、`list1`。

> [!example] 本文件出现的新代码 / 函数 / 方法
> - `return`：结束函数并把结果返回给调用处。
> - 从原文件注释/说明看，本文件重点是：retrun 把函数的结果返回出去,供其他程序使用；如果函数没有 return 或return后没值 相当于None。

> [!abstract] 代码逻辑怎么走
> - 先定义函数，把某段功能封装起来；后面通过函数名加括号调用。
> - 使用 `for` 遍历序列或容器，对每个元素执行同样的处理。
> - 通过赋值语句保存中间结果，主要变量包括：`num_count`、`list1`。

> [!warning] 需要注意的点
> - 列表是可变对象，增删改会直接影响原列表。

> [!success] 举一反三
> - 可以把单个变量升级为列表，批量保存多条数据后统一遍历处理。
> - 可以把循环和条件组合起来做筛选、统计、累加、菜单系统。
> - 可以继续把重复逻辑拆成函数，让主流程只负责调用。

### Day07/04_scope.py

```python
"""
作用域 变量和函数起作用的范围
L 局部 Local 函数内部
E 嵌套 Encolsing 闭包
G 全局 Global 模块(.py)内部
B 内置 Builtins Python环境范围(超全局)
"""
data2 = 2  # 全局
data3 = 3

def f1(n):
    # 形参相当于函数内声明的变量
    # 局部 函数内声明的变量 特点:只能在函数内使用,函数外使用报错
    data1 = 11
    print("函数内data1:", data1)
    print("函数内data2:", data2)

    # 在函数内部定义全局变量(在函数内修改全局变量的值)
    global data3
    data3 = 33333
    print("函数内data3:", data3)


f1(1)
# print("函数外data1:", data1) # 报错
print("函数外data2:", data2)
print("函数外data3:", data3)
```

> [!note] 这份文件实际讲了什么
> - 文件说明/题目写的是：作用域 变量和函数起作用的范围；L 局部 Local 函数内部；E 嵌套 Encolsing 闭包；G 全局 Global 模块(.py)内部；B 内置 Builtins Python环境范围(超全局)。
> - 文件中定义了函数：`f1(n)`。
> - 主要变量/数据名包括：`data2`、`data3`、`data1`。

> [!example] 本文件出现的新代码 / 函数 / 方法
> - `global`：在函数内声明使用全局变量。
> - 从原文件注释/说明看，本文件重点是：作用域 变量和函数起作用的范围；L 局部 Local 函数内部。

> [!abstract] 代码逻辑怎么走
> - 先定义函数，把某段功能封装起来；后面通过函数名加括号调用。
> - 通过赋值语句保存中间结果，主要变量包括：`data2`、`data3`、`data1`。

> [!warning] 需要注意的点
> - 读这份代码时，先看变量如何变化，再看最终输出。

> [!success] 举一反三
> - 可以继续把重复逻辑拆成函数，让主流程只负责调用。

### Day07/05_scope.py

```python
"""
嵌套作用域

查找规则
L --> E --> G --> B
"""

def f1():
    print("f1")
    data1 = 1  # 嵌套

    def f2():
        # 不是本地(只在嵌套中找)
        nonlocal data1
        data1 = 11
        print("f2", data1)

    f2()
    print("f1", data1)


f1()
```

> [!note] 这份文件实际讲了什么
> - 文件说明/题目写的是：嵌套作用域；查找规则；L --> E --> G --> B。
> - 文件中定义了函数：`f1()`、`f2()`。
> - 主要变量/数据名包括：`data1`。

> [!example] 本文件出现的新代码 / 函数 / 方法
> - 本文件主要是在复习或组合前面已经学过的写法，没有引入需要单独记忆的新函数/方法；重点看它如何把旧知识组合成当前题目。

> [!abstract] 代码逻辑怎么走
> - 先定义函数，把某段功能封装起来；后面通过函数名加括号调用。
> - 通过赋值语句保存中间结果，主要变量包括：`data1`。

> [!warning] 需要注意的点
> - 读这份代码时，先看变量如何变化，再看最终输出。

> [!success] 举一反三
> - 可以继续把重复逻辑拆成函数，让主流程只负责调用。

### Day07/06_imm.py

```python
"""
可变类型和不可变类型在函数内修改时的区别
"""
int1 = 1
list1 = [11, 22, 33]


def f1():
    int1 = 10
    list1[1] = 666


f1()
print(int1, list1)  # 1 [11,666,33]
```

> [!quote] 相关图示理解
> ![[附件/正式课/Day07/内存图.png]]
> 这张图对应 `Day07/06_imm.py` 的知识点。复盘时重点看变量、对象和值之间的指向关系，再对照上面的代码运行过程。

> [!note] 这份文件实际讲了什么
> - 文件说明/题目写的是：可变类型和不可变类型在函数内修改时的区别。
> - 文件中定义了函数：`f1()`。
> - 主要变量/数据名包括：`int1`、`list1`、`list1[...]`。

> [!example] 本文件出现的新代码 / 函数 / 方法
> - 本文件主要是在复习或组合前面已经学过的写法，没有引入需要单独记忆的新函数/方法；重点看它如何把旧知识组合成当前题目。
> - 从原文件注释/说明看，本文件重点是：可变类型和不可变类型在函数内修改时的区别。

> [!abstract] 代码逻辑怎么走
> - 先定义函数，把某段功能封装起来；后面通过函数名加括号调用。
> - 通过赋值语句保存中间结果，主要变量包括：`int1`、`list1`、`list1[...]`。

> [!warning] 需要注意的点
> - 列表是可变对象，增删改会直接影响原列表。

> [!success] 举一反三
> - 可以把单个变量升级为列表，批量保存多条数据后统一遍历处理。
> - 可以继续把重复逻辑拆成函数，让主流程只负责调用。

### Day07/07_design.py

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


scores = [85, 90, 78, 92, 88]
print(filter_scores(scores, include_highest=False, include_lowest=True))
```

> [!note] 这份文件实际讲了什么
> - 文件说明/题目写的是：函数的设计原则；1.SRP 单一职责 1个函数只干1件事；2.函数名和参数的名称要清晰(太长/太短都不行,参数数量不能过多)；3.避免副作用；4.合理注释。
> - 后续说明/题目还包括：def calc_scores(scores, include_highest=True, include_lowest=True,；round_digits=2):；if include_highest:  # 保留最高分 / :param scores: scores；:param include_highest:是否保留最高分 默认True 保留；:param include_lowest:是否保留最低分 默认True 保留。
> - 文件中定义了函数：`filter_scores(scores, include_highest, include_lowest)`。
> - 主要变量/数据名包括：`scores`。

> [!example] 本文件出现的新代码 / 函数 / 方法
> - 本文件主要是在复习或组合前面已经学过的写法，没有引入需要单独记忆的新函数/方法；重点看它如何把旧知识组合成当前题目。
> - 从原文件注释/说明看，本文件重点是：函数的设计原则；1.SRP 单一职责 1个函数只干1件事。

> [!abstract] 代码逻辑怎么走
> - 先定义函数，把某段功能封装起来；后面通过函数名加括号调用。
> - 使用条件判断把不同情况分开处理。
> - 通过赋值语句保存中间结果，主要变量包括：`scores`。

> [!warning] 需要注意的点
> - 列表是可变对象，增删改会直接影响原列表。

> [!success] 举一反三
> - 可以把单个变量升级为列表，批量保存多条数据后统一遍历处理。
> - 可以继续把重复逻辑拆成函数，让主流程只负责调用。

### Day07/HomeWork.txt

```text
1.完成今日代码
2.完成下列练习
  ①完善 07_design.py的代码 完成要求的功能

3.预习:面向对象基础
4.思考:如何把 EShopManagerV1.py 改成 EShopManagerV2.py 函数版
```

> [!info] 课堂文本/作业说明
> - 1.完成今日代码
> - 2.完成下列练习
> - ①完善 07_design.py的代码 完成要求的功能
> - 3.预习:面向对象基础
> - 4.思考:如何把 EShopManagerV1.py 改成 EShopManagerV2.py 函数版

### Day07/HomeWork01.py

```python
"""
①定义一个函数, 接受一个字符串作为参数,判断是不是回文字符串
忽略大小写,忽略非字母的字符,忽略数字
"""
def is_palindrome(s):
    str_new = ""
    for char in s:
        if char.isalpha():
            str_new += char.lower()

    str_new = "".join([char.lower() for char in s if char.isalpha()])

    print("是回文") if str_new == str_new[::-1] else print("不回回文")


str1 = "上海自来水来自海上"
str2 = "A man, a plan, a canal, Panama"
str3 = "HEHE"
is_palindrome(str1)
is_palindrome(str2)
is_palindrome(str3)
```

> [!note] 这份文件实际讲了什么
> - 文件说明/题目写的是：①定义一个函数, 接受一个字符串作为参数,判断是不是回文字符串；忽略大小写,忽略非字母的字符,忽略数字。
> - 文件中定义了函数：`is_palindrome(s)`。
> - 主要变量/数据名包括：`str_new`、`str1`、`str2`、`str3`。

> [!example] 本文件出现的新代码 / 函数 / 方法
> - 本文件主要是在复习或组合前面已经学过的写法，没有引入需要单独记忆的新函数/方法；重点看它如何把旧知识组合成当前题目。
> - 从原文件注释/说明看，本文件重点是：①定义一个函数, 接受一个字符串作为参数,判断是不是回文字符串。

> [!abstract] 代码逻辑怎么走
> - 先定义函数，把某段功能封装起来；后面通过函数名加括号调用。
> - 使用 `for` 遍历序列或容器，对每个元素执行同样的处理。
> - 使用条件判断把不同情况分开处理。
> - 通过赋值语句保存中间结果，主要变量包括：`str_new`、`str1`、`str2`、`str3`。

> [!warning] 需要注意的点
> - 字符串方法通常返回新字符串，不会原地修改原字符串。

> [!success] 举一反三
> - 可以把循环和条件组合起来做筛选、统计、累加、菜单系统。
> - 可以继续把重复逻辑拆成函数，让主流程只负责调用。

### Day07/Review.py

```python
"""
函数
组织代码的方式
组织好的 完成一定功能的 可复用

def 函数名(形参):
    函数体

函数名(实参)
"""
```

> [!note] 这份文件实际讲了什么
> - 文件说明/题目写的是：函数；组织代码的方式；组织好的 完成一定功能的 可复用；def 函数名(形参):；函数体。

> [!example] 本文件出现的新代码 / 函数 / 方法
> - 本文件主要是在复习或组合前面已经学过的写法，没有引入需要单独记忆的新函数/方法；重点看它如何把旧知识组合成当前题目。
> - 从原文件注释/说明看，本文件重点是：函数；def 函数名(形参):。

> [!abstract] 代码逻辑怎么走
> - 这份代码主要是顺序执行：先准备数据，再调用函数或输出结果。

> [!warning] 需要注意的点
> - 读这份代码时，先看变量如何变化，再看最终输出。

> [!success] 举一反三
> - 可以修改示例数据重新运行，观察输出如何变化。

### Day07/exercise01.py

```python
"""
定义一个函数 根据传入的小时 分钟 秒数 计算总秒数
小时 分钟 秒数 都可以单独存在,也可以组合形式存在
"""


def calc_sec(h=0, m=0, s=0):
    total_seconds = 0
    total_seconds += h * 3600
    total_seconds += m * 60
    total_seconds += s

    print(total_seconds)


calc_sec(1, 2, 3)
calc_sec(h=1)
calc_sec(h=1, s=100)
```

> [!note] 这份文件实际讲了什么
> - 文件说明/题目写的是：定义一个函数 根据传入的小时 分钟 秒数 计算总秒数；小时 分钟 秒数 都可以单独存在,也可以组合形式存在。
> - 文件中定义了函数：`calc_sec(h, m, s)`。
> - 主要变量/数据名包括：`total_seconds`。

> [!example] 本文件出现的新代码 / 函数 / 方法
> - 本文件主要是在复习或组合前面已经学过的写法，没有引入需要单独记忆的新函数/方法；重点看它如何把旧知识组合成当前题目。
> - 从原文件注释/说明看，本文件重点是：定义一个函数 根据传入的小时 分钟 秒数 计算总秒数。

> [!abstract] 代码逻辑怎么走
> - 先定义函数，把某段功能封装起来；后面通过函数名加括号调用。
> - 通过赋值语句保存中间结果，主要变量包括：`total_seconds`。

> [!warning] 需要注意的点
> - 读这份代码时，先看变量如何变化，再看最终输出。

> [!success] 举一反三
> - 可以继续把重复逻辑拆成函数，让主流程只负责调用。

### Day07/exercise02.py

```python
"""
声明一个函数,接受多个订单字典作为参数,合并订单
"""


def merge_orders(*args):
    # merged_items = {}
    # for item in args:
    #     for oid, quantity in item.items():
    #         merged_items[oid] = merged_items.get(oid, 0) + quantity

    # 推导式
    merged_items = {
        sub_key: sum(item.get(sub_key, 0) for item in args)
        for item in args for sub_key in item
    }

    print(merged_items)


order1 = {"A001": 2, "B002": 1, "D004": 4}
order2 = {"A001": 3, "C003": 5}

# {'A001': 5, 'B002': 1, 'D004': 4, 'C003': 5}
merge_orders(order1, order2)
```

> [!note] 这份文件实际讲了什么
> - 文件说明/题目写的是：声明一个函数,接受多个订单字典作为参数,合并订单。
> - 文件中定义了函数：`merge_orders(*args)`。
> - 主要变量/数据名包括：`merged_items`、`order1`、`order2`。

> [!example] 本文件出现的新代码 / 函数 / 方法
> - 本文件主要是在复习或组合前面已经学过的写法，没有引入需要单独记忆的新函数/方法；重点看它如何把旧知识组合成当前题目。
> - 从原文件注释/说明看，本文件重点是：声明一个函数,接受多个订单字典作为参数,合并订单；推导式。

> [!abstract] 代码逻辑怎么走
> - 先定义函数，把某段功能封装起来；后面通过函数名加括号调用。
> - 通过赋值语句保存中间结果，主要变量包括：`merged_items`、`order1`、`order2`。

> [!warning] 需要注意的点
> - 字典按 key 取值，key 要唯一；遍历键值对时优先想到 `.items()`。

> [!success] 举一反三
> - 可以把同样结构用于学生信息、商品信息、地区数据等 key-value 场景。
> - 可以继续把重复逻辑拆成函数，让主流程只负责调用。

### Day07/exercise03.py

```python
"""
定义一个函数,
计算所有位置参数的和
计算所有关键字参数的乘积 并返回(参数个数数量不确定)
"""


def calc(*args, **kwargs):
    # 位置参数和:
    sum_args = sum(args)
    # 函数改进:
    # 如果只有1种参数,那么返回对应参数的结果即可
    # 如果有2种参数,返回元组形式
    # 如果没有参数,返回None
    # 关键字参数积:
    product_kwargs = 0
    if kwargs:
        product_num = 1
        for value in kwargs.values():
            product_num *= value
        product_kwargs = product_num

    return sum_args, product_kwargs


# 函数改进:
# 如果只有1种参数,那么返回对应参数的结果即可
# 如果有2种参数,返回元组形式
# 如果没有参数,返回None
# 关键字参数积:
def calc(*args, **kwargs):
    if not args and not kwargs:
        return

    # 位置参数的和
    sum_args = sum(args)

    # 关键字参数的积
    product_kwargs = 0
    if kwargs:
        product_num = 1
        for value in kwargs.values():
            product_num *= value
        product_kwargs = product_num

    # if args and not kwargs:  # 仅仅位置参数
    #     return sum_args
    # elif not args and kwargs:  # 仅仅关键字参数
    #     return product_kwargs
    # else:  # 2个都有
    #     return sum_args, product_kwargs

    # 真 if 条件 else 假
    return (
        sum_args if args and not kwargs else
        product_kwargs if not args and kwargs else
        (sum_args, product_kwargs)
    )



print(calc(1, 2, a=4, b=5))
print(calc(a=4, b=5))
print(calc(1, 2))
print(calc())
```

> [!note] 这份文件实际讲了什么
> - 文件说明/题目写的是：定义一个函数,；计算所有位置参数的和；计算所有关键字参数的乘积 并返回(参数个数数量不确定)。
> - 文件中定义了函数：`calc(*args, **kwargs)`、`calc(*args, **kwargs)`。
> - 主要变量/数据名包括：`sum_args`、`product_kwargs`、`product_num`。

> [!example] 本文件出现的新代码 / 函数 / 方法
> - `**kwargs`：可变数量的关键字参数，函数内部接收到字典。
> - 从原文件注释/说明看，本文件重点是：定义一个函数,；函数改进:。

> [!abstract] 代码逻辑怎么走
> - 先定义函数，把某段功能封装起来；后面通过函数名加括号调用。
> - 使用 `for` 遍历序列或容器，对每个元素执行同样的处理。
> - 使用条件判断把不同情况分开处理。
> - 通过赋值语句保存中间结果，主要变量包括：`sum_args`、`product_kwargs`、`product_num`。

> [!warning] 需要注意的点
> - 读这份代码时，先看变量如何变化，再看最终输出。

> [!success] 举一反三
> - 可以把循环和条件组合起来做筛选、统计、累加、菜单系统。
> - 可以继续把重复逻辑拆成函数，让主流程只负责调用。

### Day07/exercise04.py

```python
"""
下列代码的输出是什么
"""


def f1(n):
    def sum(n):
        print(n)  # [1,2]
        return n

    print(sum(n))  # [1,2]


list1 = [1, 2]
print(f1(list1))  # None
print(sum(list1))  # 3
```

> [!note] 这份文件实际讲了什么
> - 文件说明/题目写的是：下列代码的输出是什么。
> - 文件中定义了函数：`f1(n)`、`sum(n)`。
> - 主要变量/数据名包括：`list1`。

> [!example] 本文件出现的新代码 / 函数 / 方法
> - 本文件主要是在复习或组合前面已经学过的写法，没有引入需要单独记忆的新函数/方法；重点看它如何把旧知识组合成当前题目。

> [!abstract] 代码逻辑怎么走
> - 先定义函数，把某段功能封装起来；后面通过函数名加括号调用。
> - 通过赋值语句保存中间结果，主要变量包括：`list1`。

> [!warning] 需要注意的点
> - 列表是可变对象，增删改会直接影响原列表。

> [!success] 举一反三
> - 可以把单个变量升级为列表，批量保存多条数据后统一遍历处理。
> - 可以继续把重复逻辑拆成函数，让主流程只负责调用。

## 总结

> [!summary] 总结
> - **今天的核心任务**：学习实参、形参、可变位置参数 `*args`、可变关键字参数 `**kwargs`、默认值形参。；学习 `return` 返回值，并区分返回结果和打印结果。；学习局部作用域、全局作用域、嵌套作用域和 `global`。
> - **真实文件里的练习/主题**：实参专题；形参专题；返回值；作用域 变量和函数起作用的范围；嵌套作用域；可变类型和不可变类型在函数内修改时的区别；函数的设计原则；①定义一个函数, 接受一个字符串作为参数,判断是不是回文字符串。
>
> **新学代码怎么理解**
> - ***args**：`*args` 接收任意数量的位置实参，在函数内部表现为元组。
> - ****kwargs**：`**kwargs` 接收任意数量的关键字实参，在函数内部表现为字典。
> - **default**：默认值形参让调用者可以少传参数，函数会使用预设值。
> - **return**：把函数结果交回调用处，和只负责显示的 `print()` 不一样。
> - **global**：在函数内部声明使用全局变量，使用时要谨慎。
>
> **复盘建议**
> - 先看每份文件的三引号说明或注释，判断题目要解决什么问题。
> - 再看本文件真正新增的函数/方法，弄清楚它接收什么、返回什么、是否会修改原对象。
> - 最后把代码逻辑按“输入/准备数据 -> 分支或循环处理 -> 输出/返回结果”复述一遍。
