# Day07 - 函数参数、返回值与作用域

> [!summary] 今日一句话
> 今天继续深入函数：参数负责把外部数据送进函数，返回值负责把结果带出来，作用域决定变量在哪里可见。

## 今天到底学了什么

- 实参传给形参，函数才能处理不同数据
- 位置参数、关键字参数、默认参数、可变参数各有使用场景
- `return` 把计算结果交还给调用者
- 局部变量、全局变量和可变对象传参会影响数据修改方式

> [!important] 抓主线
> 这一天的代码不是零散练习，而是在训练一个能力链条：先理解数据，再控制流程，再把重复逻辑封装起来。读代码时先看“数据从哪里来”，再看“经过什么判断或循环”，最后看“结果输出到哪里”。

## 课堂图示

**Day07/内存图.png**

![[附件/正式课/Day07/内存图.png]]


## 课堂代码合集

> 这里集中保留今天所有 `.py` 代码。代码块里补充的是理解代码用的中文说明，不是原项目必须运行的内容。

### Day07/01_args.py

```python
"""
实参专题
"""


# 位置传参:实参和形参的位置依次对应
# 说明：定义函数 `f1`，参数：p1, p2, p3。
def f1(p1, p2, p3):
    # 说明：输出内容到控制台，常用于观察程序运行结果。
    print(p1)
    # 说明：输出内容到控制台，常用于观察程序运行结果。
    print(p2)
    # 说明：输出内容到控制台，常用于观察程序运行结果。
    print(p3)

# 说明：调用函数，让已经定义好的逻辑真正执行。
f1(1, 2, 3)

# 说明：输出内容到控制台，常用于观察程序运行结果。
print("-" * 20)

# 关键字传参:实参根据形参的名字对应
# 说明：定义函数 `f2`，参数：p1, p2, p3。
def f2(p1, p2, p3):
    # 说明：输出内容到控制台，常用于观察程序运行结果。
    print(p1)
    # 说明：输出内容到控制台，常用于观察程序运行结果。
    print(p2)
    # 说明：输出内容到控制台，常用于观察程序运行结果。
    print(p3)

# 说明：把右侧结果保存到 `f2(p3`。
f2(p3=1, p1=2, p2=3)
# 说明：把右侧结果保存到 `f2(1, p3`。
f2(1, p3=2, p2=3)
# f2(p3=1, 2, p1=3) #报错

# 说明：输出内容到控制台，常用于观察程序运行结果。
print("-" * 20)

# 序列传参: 实参使用*号序列拆解后与形参的位置对应
# 说明：定义函数 `f3`，参数：p1, p2, p3。
def f3(p1, p2, p3):
    # 说明：输出内容到控制台，常用于观察程序运行结果。
    print(p1)
    # 说明：输出内容到控制台，常用于观察程序运行结果。
    print(p2)
    # 说明：输出内容到控制台，常用于观察程序运行结果。
    print(p3)

# 说明：把右侧结果保存到 `list1`。
list1 = [1, 2, 3]
# 说明：执行算术运算，注意运算符含义和优先级。
f3(*list1)
```

### Day07/02_parameter.py

```python
"""
形参专题
"""


# 可变数量的位置参数(*号元组形参)
# 把实参合并成一个元组
# 说明：定义函数 `f1`，参数：*args。
def f1(*args):
    # 说明：输出内容到控制台，常用于观察程序运行结果。
    print(args)


# 说明：调用函数，让已经定义好的逻辑真正执行。
f1()
# 说明：调用函数，让已经定义好的逻辑真正执行。
f1(1)
# 说明：调用函数，让已经定义好的逻辑真正执行。
f1(1, 2, 3)

# 说明：输出内容到控制台，常用于观察程序运行结果。
print("-" * 20)

# 可变数量的关键字参数(**字典形参)
# 把实参合并成一个字典
# 说明：定义函数 `f2`，参数：**kwargs。
def f2(**kwargs):
    # 说明：输出内容到控制台，常用于观察程序运行结果。
    print(kwargs)


# 说明：调用函数，让已经定义好的逻辑真正执行。
f2()
# 说明：把右侧结果保存到 `f2(name`。
f2(name="xiaoyu")
# 说明：把右侧结果保存到 `f2(name`。
f2(name="xiaoyu", sex="女")


# 说明：输出内容到控制台，常用于观察程序运行结果。
print("-" * 20)


# 默认值形参:形参拥有默认值
# 说明：定义函数 `f3`，参数：p1, p2=0, p3=0。
def f3(p1, p2=0, p3=0):

    # 说明：输出内容到控制台，常用于观察程序运行结果。
    print(p1)
    # 说明：输出内容到控制台，常用于观察程序运行结果。
    print(p2)
    # 说明：输出内容到控制台，常用于观察程序运行结果。
    print(p3)


# 说明：调用函数，让已经定义好的逻辑真正执行。
f3(1)
# 说明：调用函数，让已经定义好的逻辑真正执行。
f3(1, 2)
# 说明：把右侧结果保存到 `f3(1, p3`。
f3(1, p3=3)
```

### Day07/03_retrun.py

```python
"""
返回值
retrun 把函数的结果返回出去,供其他程序使用

"""


# 说明：定义函数 `my_len`，参数：lst。
def my_len(lst):
    # 说明：把右侧结果保存到 `num_count`。
    num_count = 0
    # 说明：遍历可迭代对象，逐个取值执行循环体。
    for item in lst:
        # 说明：更新 `num_count +` 的值，属于复合赋值。
        num_count += 1

    # 如果函数没有 return 或return后没值 相当于None
    # 终止函数
    # 只能返回一个值,类型不限制 list str 函数...
    # 说明：返回结果给函数调用处；return 后函数结束。
    return num_count


# 说明：把右侧结果保存到 `list1`。
list1 = [1, 2, 3, 4]
# 说明：输出内容到控制台，常用于观察程序运行结果。
print(my_len(list1))

# for i in range(len(list1)):
#     print(list1[i])
#
# for i in range(my_len(list1)):
#     print(list1[i])
```

### Day07/04_scope.py

```python
"""
作用域 变量和函数起作用的范围
L 局部 Local 函数内部
E 嵌套 Encolsing 闭包
G 全局 Global 模块(.py)内部
B 内置 Builtins Python环境范围(超全局)
"""
# 说明：把右侧结果保存到 `data2`。
data2 = 2  # 全局
# 说明：把右侧结果保存到 `data3`。
data3 = 3

# 说明：定义函数 `f1`，参数：n。
def f1(n):
    # 形参相当于函数内声明的变量
    # 局部 函数内声明的变量 特点:只能在函数内使用,函数外使用报错
    # 说明：把右侧结果保存到 `data1`。
    data1 = 11
    # 说明：输出内容到控制台，常用于观察程序运行结果。
    print("函数内data1:", data1)
    # 说明：输出内容到控制台，常用于观察程序运行结果。
    print("函数内data2:", data2)

    # 在函数内部定义全局变量(在函数内修改全局变量的值)
    global data3
    # 说明：把右侧结果保存到 `data3`。
    data3 = 33333
    # 说明：输出内容到控制台，常用于观察程序运行结果。
    print("函数内data3:", data3)


# 说明：调用函数，让已经定义好的逻辑真正执行。
f1(1)
# print("函数外data1:", data1) # 报错
# 说明：输出内容到控制台，常用于观察程序运行结果。
print("函数外data2:", data2)
# 说明：输出内容到控制台，常用于观察程序运行结果。
print("函数外data3:", data3)
```

### Day07/05_scope.py

```python
"""
嵌套作用域

查找规则
L --> E --> G --> B
"""

# 说明：定义函数 `f1`，参数：无参数。
def f1():
    # 说明：输出内容到控制台，常用于观察程序运行结果。
    print("f1")
    # 说明：把右侧结果保存到 `data1`。
    data1 = 1  # 嵌套

    # 说明：定义函数 `f2`，参数：无参数。
    def f2():
        # 不是本地(只在嵌套中找)
        nonlocal data1
        # 说明：把右侧结果保存到 `data1`。
        data1 = 11
        # 说明：输出内容到控制台，常用于观察程序运行结果。
        print("f2", data1)

    # 说明：调用函数，让已经定义好的逻辑真正执行。
    f2()
    # 说明：输出内容到控制台，常用于观察程序运行结果。
    print("f1", data1)


# 说明：调用函数，让已经定义好的逻辑真正执行。
f1()
```

### Day07/06_imm.py

```python
"""
可变类型和不可变类型在函数内修改时的区别
"""
# 说明：把右侧结果保存到 `int1`。
int1 = 1
# 说明：把右侧结果保存到 `list1`。
list1 = [11, 22, 33]


# 说明：定义函数 `f1`，参数：无参数。
def f1():
    # 说明：把右侧结果保存到 `int1`。
    int1 = 10
    # 说明：把右侧结果保存到 `list1[1]`。
    list1[1] = 666


# 说明：调用函数，让已经定义好的逻辑真正执行。
f1()
# 说明：输出内容到控制台，常用于观察程序运行结果。
print(int1, list1)  # 1 [11,666,33]
```

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


# 说明：把右侧结果保存到 `scores`。
scores = [85, 90, 78, 92, 88]
# 说明：输出内容到控制台，常用于观察程序运行结果。
print(filter_scores(scores, include_highest=False, include_lowest=True))
```

### Day07/HomeWork01.py

```python
"""
①定义一个函数, 接受一个字符串作为参数,判断是不是回文字符串
忽略大小写,忽略非字母的字符,忽略数字
"""
# 说明：定义函数 `is_palindrome`，参数：s。
def is_palindrome(s):
    # 说明：把右侧结果保存到 `str_new`。
    str_new = ""
    # 说明：遍历可迭代对象，逐个取值执行循环体。
    for char in s:
        # 说明：判断条件是否成立，成立才执行下面缩进代码。
        if char.isalpha():
            # 说明：更新 `str_new +` 的值，属于复合赋值。
            str_new += char.lower()

    # 说明：把右侧结果保存到 `str_new`。
    str_new = "".join([char.lower() for char in s if char.isalpha()])

    # 说明：进行比较，结果是 True 或 False。
    print("是回文") if str_new == str_new[::-1] else print("不回回文")


# 说明：把右侧结果保存到 `str1`。
str1 = "上海自来水来自海上"
# 说明：把右侧结果保存到 `str2`。
str2 = "A man, a plan, a canal, Panama"
# 说明：把右侧结果保存到 `str3`。
str3 = "HEHE"
# 说明：调用函数，让已经定义好的逻辑真正执行。
is_palindrome(str1)
# 说明：调用函数，让已经定义好的逻辑真正执行。
is_palindrome(str2)
# 说明：调用函数，让已经定义好的逻辑真正执行。
is_palindrome(str3)
```

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

### Day07/exercise01.py

```python
"""
定义一个函数 根据传入的小时 分钟 秒数 计算总秒数
小时 分钟 秒数 都可以单独存在,也可以组合形式存在
"""


# 说明：定义函数 `calc_sec`，参数：h=0, m=0, s=0。
def calc_sec(h=0, m=0, s=0):
    # 说明：把右侧结果保存到 `total_seconds`。
    total_seconds = 0
    # 说明：更新 `total_seconds +` 的值，属于复合赋值。
    total_seconds += h * 3600
    # 说明：更新 `total_seconds +` 的值，属于复合赋值。
    total_seconds += m * 60
    # 说明：更新 `total_seconds +` 的值，属于复合赋值。
    total_seconds += s

    # 说明：输出内容到控制台，常用于观察程序运行结果。
    print(total_seconds)


# 说明：调用函数，让已经定义好的逻辑真正执行。
calc_sec(1, 2, 3)
# 说明：把右侧结果保存到 `calc_sec(h`。
calc_sec(h=1)
# 说明：把右侧结果保存到 `calc_sec(h`。
calc_sec(h=1, s=100)
```

### Day07/exercise02.py

```python
"""
声明一个函数,接受多个订单字典作为参数,合并订单
"""


# 说明：定义函数 `merge_orders`，参数：*args。
def merge_orders(*args):
    # merged_items = {}
    # for item in args:
    #     for oid, quantity in item.items():
    #         merged_items[oid] = merged_items.get(oid, 0) + quantity

    # 推导式
    # 说明：把右侧结果保存到 `merged_items`。
    merged_items = {
        # 说明：按键取值，取不到时可返回默认值。
        sub_key: sum(item.get(sub_key, 0) for item in args)
        # 说明：遍历可迭代对象，逐个取值执行循环体。
        for item in args for sub_key in item
    }

    # 说明：输出内容到控制台，常用于观察程序运行结果。
    print(merged_items)


# 说明：把右侧结果保存到 `order1`。
order1 = {"A001": 2, "B002": 1, "D004": 4}
# 说明：把右侧结果保存到 `order2`。
order2 = {"A001": 3, "C003": 5}

# {'A001': 5, 'B002': 1, 'D004': 4, 'C003': 5}
# 说明：调用函数，让已经定义好的逻辑真正执行。
merge_orders(order1, order2)
```

### Day07/exercise03.py

```python
"""
定义一个函数,
计算所有位置参数的和
计算所有关键字参数的乘积 并返回(参数个数数量不确定)
"""


# 说明：定义函数 `calc`，参数：*args, **kwargs。
def calc(*args, **kwargs):
    # 位置参数和:
    # 说明：把右侧结果保存到 `sum_args`。
    sum_args = sum(args)
    # 函数改进:
    # 如果只有1种参数,那么返回对应参数的结果即可
    # 如果有2种参数,返回元组形式
    # 如果没有参数,返回None
    # 关键字参数积:
    # 说明：把右侧结果保存到 `product_kwargs`。
    product_kwargs = 0
    # 说明：判断条件是否成立，成立才执行下面缩进代码。
    if kwargs:
        # 说明：把右侧结果保存到 `product_num`。
        product_num = 1
        # 说明：遍历可迭代对象，逐个取值执行循环体。
        for value in kwargs.values():
            # 说明：更新 `product_num *` 的值，属于复合赋值。
            product_num *= value
        # 说明：把右侧结果保存到 `product_kwargs`。
        product_kwargs = product_num

    # 说明：返回结果给函数调用处；return 后函数结束。
    return sum_args, product_kwargs


# 函数改进:
# 如果只有1种参数,那么返回对应参数的结果即可
# 如果有2种参数,返回元组形式
# 如果没有参数,返回None
# 关键字参数积:
# 说明：定义函数 `calc`，参数：*args, **kwargs。
def calc(*args, **kwargs):
    # 说明：判断条件是否成立，成立才执行下面缩进代码。
    if not args and not kwargs:
        # 说明：返回结果给函数调用处；return 后函数结束。
        return

    # 位置参数的和
    # 说明：把右侧结果保存到 `sum_args`。
    sum_args = sum(args)

    # 关键字参数的积
    # 说明：把右侧结果保存到 `product_kwargs`。
    product_kwargs = 0
    # 说明：判断条件是否成立，成立才执行下面缩进代码。
    if kwargs:
        # 说明：把右侧结果保存到 `product_num`。
        product_num = 1
        # 说明：遍历可迭代对象，逐个取值执行循环体。
        for value in kwargs.values():
            # 说明：更新 `product_num *` 的值，属于复合赋值。
            product_num *= value
        # 说明：把右侧结果保存到 `product_kwargs`。
        product_kwargs = product_num

    # if args and not kwargs:  # 仅仅位置参数
    #     return sum_args
    # elif not args and kwargs:  # 仅仅关键字参数
    #     return product_kwargs
    # else:  # 2个都有
    #     return sum_args, product_kwargs

    # 真 if 条件 else 假
    # 说明：返回结果给函数调用处；return 后函数结束。
    return (
        # 说明：组合多个布尔条件。
        sum_args if args and not kwargs else
        # 说明：组合多个布尔条件。
        product_kwargs if not args and kwargs else
        (sum_args, product_kwargs)
    )



# 说明：输出内容到控制台，常用于观察程序运行结果。
print(calc(1, 2, a=4, b=5))
# 说明：输出内容到控制台，常用于观察程序运行结果。
print(calc(a=4, b=5))
# 说明：输出内容到控制台，常用于观察程序运行结果。
print(calc(1, 2))
# 说明：输出内容到控制台，常用于观察程序运行结果。
print(calc())
```

### Day07/exercise04.py

```python
"""
下列代码的输出是什么
"""


# 说明：定义函数 `f1`，参数：n。
def f1(n):
    # 说明：定义函数 `sum`，参数：n。
    def sum(n):
        # 说明：输出内容到控制台，常用于观察程序运行结果。
        print(n)  # [1,2]
        # 说明：返回结果给函数调用处；return 后函数结束。
        return n

    # 说明：输出内容到控制台，常用于观察程序运行结果。
    print(sum(n))  # [1,2]


# 说明：把右侧结果保存到 `list1`。
list1 = [1, 2]
# 说明：输出内容到控制台，常用于观察程序运行结果。
print(f1(list1))  # None
# 说明：输出内容到控制台，常用于观察程序运行结果。
print(sum(list1))  # 3
```

## 课堂要求与作业原文

### Day07/HomeWork.txt

```text
1.完成今日代码
2.完成下列练习
  ①完善 07_design.py的代码 完成要求的功能

3.预习:面向对象基础
4.思考:如何把 EShopManagerV1.py 改成 EShopManagerV2.py 函数版
```

## 融会贯通笔记

### 参数让函数从“固定动作”变成“通用工具”

- 形参写在函数定义里，是占位变量。
- 实参写在函数调用里，是这一次真正传进去的数据。
- 位置参数靠顺序匹配，关键字参数靠名字匹配，后者可读性更好。

### 默认参数和可变参数提升灵活度

- 默认参数适合给常用值一个默认选择。
- `*args` 接收多个位置参数，`**kwargs` 接收多个关键字参数。
- 默认参数如果是列表、字典这类可变对象，要格外小心共享状态。

### return 才是函数真正的“结果出口”

- 只 `print()` 的函数适合展示，不方便继续计算。
- `return` 的结果可以赋值给变量，也可以作为另一个表达式的一部分。
- 函数执行到 return 就会结束。

### 作用域决定变量在哪里生效

- 函数内部定义的是局部变量，函数外默认访问不到。
- 全局变量能被函数读取，但在函数内修改通常需要 `global`。
- 传入可变对象时，函数内部如果原地修改，外部也会看到变化。

## 复盘自查

- [ ] 能区分形参和实参
- [ ] 能写一个有返回值的函数并继续使用结果
- [ ] 能解释局部变量和全局变量的区别
