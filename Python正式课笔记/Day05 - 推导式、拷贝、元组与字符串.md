# Day05 - 推导式、拷贝、元组与字符串

> [!summary] 今日一句话
> 今天开始理解 Python 容器背后的对象特性：怎样快速生成列表，怎样复制，哪些对象能改，哪些不能改。

## 今天到底学了什么

- 列表推导式让“循环生成列表”更简洁
- 浅拷贝只复制外层容器，深拷贝会递归复制内部对象
- 元组不可变，适合保存不希望被修改的数据
- 字符串也是不可变序列，支持索引、切片和大量方法

> [!important] 抓主线
> 这一天的代码不是零散练习，而是在训练一个能力链条：先理解数据，再控制流程，再把重复逻辑封装起来。读代码时先看“数据从哪里来”，再看“经过什么判断或循环”，最后看“结果输出到哪里”。

## 课堂图示

**Day05/内存图1.png**

![[附件/正式课/Day05/内存图1.png]]

**Day05/内存图2.png**

![[附件/正式课/Day05/内存图2.png]]

**Day05/内存图3.png**

![[附件/正式课/Day05/内存图3.png]]

**Day05/内存图4.png**

![[附件/正式课/Day05/内存图4.png]]

**Day05/内存图5.png**

![[附件/正式课/Day05/内存图5.png]]


## 课堂代码合集

> 这里集中保留今天所有 `.py` 代码。代码块里补充的是理解代码用的中文说明，不是原项目必须运行的内容。

### Day05/01_derivative.py

```python
"""
列表推导式

列表= [元素操作 for 变量 in 可迭代对象]
列表= [元素操作 for 变量 in 可迭代对象 if 条件]
"""
# 说明：把右侧结果保存到 `list_num`。
list_num = [1, 2, 4, 3, 5, 6, 10, 8]

# 说明：把右侧结果保存到 `list_new`。
list_new = []
# 说明：遍历可迭代对象，逐个取值执行循环体。
for item in list_num:
    # 说明：判断条件是否成立，成立才执行下面缩进代码。
    if item % 2 != 0:
        # 说明：向列表末尾追加元素。
        list_new.append(item)
# 说明：输出内容到控制台，常用于观察程序运行结果。
print(list_new)

# 说明：把右侧结果保存到 `list_new`。
list_new = [item for item in list_num if item % 2 != 0]
# 说明：输出内容到控制台，常用于观察程序运行结果。
print(list_new)

# Just do it  ==> Tsuj Od Ti
# 说明：把右侧结果保存到 `str1`。
str1 = "Just do it"
# 说明：把右侧结果保存到 `a, b, c`。
a, b, c = str1[3::-1], str1[6:4:-1], str1[9:7:-1]
# 说明：把右侧结果保存到 `str2`。
str2 = a + b + c
# 说明：把右侧结果保存到 `str3`。
str3 = str2.title()
# 说明：输出内容到控制台，常用于观察程序运行结果。
print(str3)
```

### Day05/02_copy.py

```python
"""
深浅拷贝
"""
# 说明：把右侧结果保存到 `list_movie`。
list_movie = ["昆池岩", ["门铃", "娃娃"]]
# print(list_movie[0])
# print(list_movie[1][0])

# 1.赋值 共享一份1数据 互相影响
# list_new = list_movie
# list_new[0] = "咒怨"
# list_new[1][0] = "深瞳"
# print(list_movie)
# print(list_new)

# 2.切片后赋值
# 复制了第一次数据,共享深层数据
# 浅拷贝: 浅层(第一次层)数据独立 2份 互不影响 深层数据1份, 互相影响
# 应用场景: 缓存优化 配置管理
# list_new = list_movie[:]
# list_new[0] = "咒怨"
# list_new[1][0] = "深瞳"
# print(list_movie)
# print(list_new)

# 3.深拷贝 所有层数据都是独立的 互不影响
# 应用场景: 数据隔离 状态快照
# 说明：导入模块，后面可以使用模块里的工具。
import copy

# 说明：把右侧结果保存到 `list_new`。
list_new = copy.deepcopy(list_movie)
# 说明：把右侧结果保存到 `list_new[0]`。
list_new[0] = "咒怨"
# 说明：把右侧结果保存到 `list_new[1][0]`。
list_new[1][0] = "深瞳"
# 说明：输出内容到控制台，常用于观察程序运行结果。
print(list_movie)
# 说明：输出内容到控制台，常用于观察程序运行结果。
print(list_new)
```

### Day05/03_tuple.py

```python
"""
元组
由一系列变量组成的不可变序列容器
不可变:一旦创建,不允许再添加,删除,修改
"""
# 1.创建
# 说明：把右侧结果保存到 `tuple1`。
tuple1 = ()  # 空元组
# 说明：把右侧结果保存到 `tuple2`。
tuple2 = ("剧情", "动作")

# 1个元素的元组必须有逗号
# 说明：把右侧结果保存到 `tuple3`。
tuple3 = ("剧情",)
# 说明：把右侧结果保存到 `tuple4`。
tuple4 = "剧情",
# 说明：进行比较，结果是 True 或 False。
print(type(tuple3))  # <class 'tuple'>

# 2.访问 索引 切片 同列表
# 说明：输出内容到控制台，常用于观察程序运行结果。
print(tuple2[0])
# 说明：输出内容到控制台，常用于观察程序运行结果。
print(tuple2[::-1])

# 3.遍历 同列表
# 说明：遍历可迭代对象，逐个取值执行循环体。
for item in tuple2:
    # 说明：输出内容到控制台，常用于观察程序运行结果。
    print(item)

# 4.函数
# len() max() min() sum()等
```

### Day05/04_unpacking.py

```python
"""
元组解包
"""
# 基础解包
# 依次获取元素,赋值给左边的变量,变量个数和元素个数一致
# 说明：把右侧结果保存到 `tuple1`。
tuple1 = (1, 2, 3)
# 说明：把右侧结果保存到 `a, b, c`。
a, b, c = tuple1
# 说明：输出内容到控制台，常用于观察程序运行结果。
print(a, b, c)

# *号解包
# 长度不确定的时候,把多余的元素收集起来
# 说明：把右侧结果保存到 `tuple2`。
tuple2 = (1, 2, 3, 4)
# 说明：把右侧结果保存到 `a, *b`。
a, *b = tuple2
# 说明：输出内容到控制台，常用于观察程序运行结果。
print(a, b)

# 说明：把右侧结果保存到 `a, *b, c`。
a, *b, c = tuple2
# 说明：输出内容到控制台，常用于观察程序运行结果。
print(a, b, c)

# 说明：把右侧结果保存到 `a, *b, c, d, e`。
a, *b, c, d, e = tuple2
# 说明：输出内容到控制台，常用于观察程序运行结果。
print(a, b, c)

# 不借助第三方变量交换2个变量的值
# 说明：把右侧结果保存到 `a`。
a = 1
# 说明：把右侧结果保存到 `b`。
b = 2
# 说明：把右侧结果保存到 `a, b`。
a, b = b, a
```

### Day05/05_immutable.py

```python
"""
元组不可变为啥变了?
"""
# 说明：把右侧结果保存到 `tuple1`。
tuple1 = (1, 2)
# 变量关联的地址已经发生变化
# 说明：把右侧结果保存到 `tuple1`。
tuple1 = (3, 4)
# 说明：输出内容到控制台，常用于观察程序运行结果。
print(tuple1)
```

### Day05/06_str.py

```python
"""
字符串
由一系列字符的编码值组成的不可变序列容器
"""
# 1.创建
# 说明：把右侧结果保存到 `str1`。
str1 = "Hi Roes"
# 说明：把右侧结果保存到 `str2`。
str2 = 'Hi'
# 多行字符串
str3 = """Hi
Roes"""
# 说明：输出内容到控制台，常用于观察程序运行结果。
print(str1, str3)

# 2.包裹关系
# 说明：输出内容到控制台，常用于观察程序运行结果。
print("我是'小艺'")
# 说明：输出内容到控制台，常用于观察程序运行结果。
print('我是"小艺"')

# 3.转义  \ 转义符
# 说明：输出内容到控制台，常用于观察程序运行结果。
print("我是\"小艺\"")
# \n 换行符 \t \v 水平/垂直制表符
# 说明：输出内容到控制台，常用于观察程序运行结果。
print("我是\n小艺")

# 4.访问 索引和切片
# 说明：输出内容到控制台，常用于观察程序运行结果。
print(str1[0])
# 说明：输出内容到控制台，常用于观察程序运行结果。
print(str1[::-1])

# 5.遍历
# 说明：遍历可迭代对象，逐个取值执行循环体。
for item in str1:
    # 说明：输出内容到控制台，常用于观察程序运行结果。
    print(item)

# 6.格式化
# 说明：把右侧结果保存到 `scene`。
scene = "上课"
# 说明：把右侧结果保存到 `count`。
count = 5
# %d整数 %s字符串 %f浮点
# 利用元组进行格式化 使用元组作为参数 替换占位符
# 说明：输出内容到控制台，常用于观察程序运行结果。
print("%s玩手机的人数:%d人" % (scene, count))

# F-string格式化字符串字面量(强烈推荐!!!!!!)
# 说明：输出内容到控制台，常用于观察程序运行结果。
print(F"{scene}玩手机的人数:{count}人")

# 说明：把右侧结果保存到 `format_str`。
format_str = "{}玩手机的人数:{}人".format(scene, count)
# 说明：输出内容到控制台，常用于观察程序运行结果。
print(format_str)
```

### Day05/07_str_func_case.py

```python
"""
大小写和字符相关
"""

# 说明：把右侧结果保存到 `str1`。
str1 = " HeLlO WorLd xiaoYiAA "

# 长度
# 说明：输出内容到控制台，常用于观察程序运行结果。
print(len(str1))
# 大/小写
# 说明：输出内容到控制台，常用于观察程序运行结果。
print(str1.upper())
# 说明：输出内容到控制台，常用于观察程序运行结果。
print(str1.lower())
# 首字母大写
# 说明：输出内容到控制台，常用于观察程序运行结果。
print(str1.title())

# 去除首尾指定字符 默认是空格 大写敏感
# 说明：输出内容到控制台，常用于观察程序运行结果。
print(str1.strip())
# 说明：输出内容到控制台，常用于观察程序运行结果。
print("AA BB aa".strip("A"))

# 替换 默认替换全部
# 说明：输出内容到控制台，常用于观察程序运行结果。
print(str1.replace(" ", ""))
# 说明：输出内容到控制台，常用于观察程序运行结果。
print("CNM太菜了CNM能不能用手玩CNM".replace("CNM", "**"))
# 可以指定替换次数
# 说明：输出内容到控制台，常用于观察程序运行结果。
print("CNM太菜了CNM能不能用手玩CNM".replace("CNM", "**", 1))

# 分割 列表 默认就是空格
# 说明：输出内容到控制台，常用于观察程序运行结果。
print("a,b,c,d,e".split(","))
# 说明：输出内容到控制台，常用于观察程序运行结果。
print("a b c d e".split())
# 说明：输出内容到控制台，常用于观察程序运行结果。
print("a b c d e".split(" "))

# 拼接
# 函数接受可迭代对象作为参数,用指定的字符串,连接可迭代对象中的每一个元素,形成新的字符串
# 说明：把右侧结果保存到 `list1`。
list1 = ["a", "b", "c", "d"]
# 说明：输出内容到控制台，常用于观察程序运行结果。
print("-".join(list1))  # a-b-c-d
```

### Day05/HomeWork/HomeWork01.py

```python
"""
交替合并2个列表
    list1 = [1,3,5]
    list2 = [2,4,6,8]
    结果:[1,2,3,4,5,6,8]
"""
# 说明：把右侧结果保存到 `list1`。
list1 = [1, 3, 5]
# 说明：把右侧结果保存到 `list2`。
list2 = [2, 4, 6, 8]
# 说明：把右侧结果保存到 `list_new`。
list_new = []
# 说明：把右侧结果保存到 `index`。
index = 0
# 说明：只要条件为 True，就持续循环。
while index < max(len(list1), len(list2)):
    # 说明：判断条件是否成立，成立才执行下面缩进代码。
    if len(list1) > index:
        # 说明：向列表末尾追加元素。
        list_new.append(list1[index])
    # 说明：判断条件是否成立，成立才执行下面缩进代码。
    if len(list2) > index:
        # 说明：向列表末尾追加元素。
        list_new.append(list2[index])
    # 说明：更新 `index +` 的值，属于复合赋值。
    index += 1
# 说明：输出内容到控制台，常用于观察程序运行结果。
print(list_new)
















# # 两个列表长度不相等,保证列表所有的元素都能遍历
# while index < len(list1) or index < len(list2):
#     if index < len(list1):
#         list_new.append(list1[index])
#     if index < len(list2):
#         list_new.append(list2[index])
#     index += 1
#
# print(list_new)
#
# # for循环方法
# list_new = []
# max_idx = max(len(list1),len(list2))
# for i in range(max_idx):
#     if i < len(list1):
#         list_new.append(list1[i])
#     if i < len(list2):
#         list_new.append(list2[i])
# print(list_new)
```

### Day05/HomeWork/HomeWork02.py

```python
"""
删除列表中的偶数
    list_num = [1,2,3,4,5,6]
    结果:[1,3,5]
"""
# 说明：把右侧结果保存到 `list_num`。
list_num = [1, 2, 4, 3, 5, 6, 10, 8]

# 下方代码的思想(邪修):把奇数插入到新列表中
# 说明：把右侧结果保存到 `list_new`。
list_new = []
# 说明：遍历可迭代对象，逐个取值执行循环体。
for item in list_num:
    # 说明：判断条件是否成立，成立才执行下面缩进代码。
    if item % 2 != 0:
        # 说明：向列表末尾追加元素。
        list_new.append(item)
# 说明：输出内容到控制台，常用于观察程序运行结果。
print(list_new)

# 切片思想
# 说明：遍历可迭代对象，逐个取值执行循环体。
for item in list_num[:]:
    # 说明：判断条件是否成立，成立才执行下面缩进代码。
    if not item % 2:
        # 说明：按值删除元素。
        list_num.remove(item)
# 说明：输出内容到控制台，常用于观察程序运行结果。
print(list_num)

# [::-1]反向切片
# del + range(len()-1,-1,-1)
# 手动管理索引 + while
```

### Day05/Review.py

```python
"""
for循环
 for 变量 in 可迭代对象

 循环嵌套
    先执行外层,再执行内层
    外层执行1次, 内层执行n次
    外层结束循环,整个循环终止

列表
    由一系列变量组成的可变序列容器
    数据结构 可迭代对象
    创建:列表名 = []
    访问:索引 单个元素 正:0 len() -1 反:-1
        切片 多个元素 产生新的列表
        [开始:结束:步长] [开始:结束] [:]  [::-1]
    修改: 列表名[索引] = 值
    删除: del 列表名[索引] 列表名.remove(值)
    添加: append(单个值) extend(多个值) insert(索引,单个值)
    遍历: for item in 列表
    函数: len() max() min() sum()
"""
```

### Day05/exercise01.py

```python
"""
使用列表推导式 计算每个元素的移动平均值(窗口大小为3)
[1,2,3,4,5] ==> [2.0,3.0,4.0]

(1+2+3) / 3 2
(2+3+4) / 3 3
...
窗口滑动
"""
# 说明：把右侧结果保存到 `list_num`。
list_num = [1, 2, 3, 4, 5]
# 说明：把右侧结果保存到 `w_size`。
w_size = 3
# 说明：把右侧结果保存到 `list_new`。
list_new = []

# 所有可能的窗口起始位置
# 说明：遍历可迭代对象，逐个取值执行循环体。
for i in range(len(list_num) - w_size + 1):
    # print(i) 0 1 2
    # 利用窗口在列表中提取子列表
    # 0:3 1:4 2:5
    # 说明：把右侧结果保存到 `sub_list`。
    sub_list = list_num[i:i + w_size]
    # 说明：输出内容到控制台，常用于观察程序运行结果。
    print(sub_list)
    # 计算平均值 元素之和 / 数量
    # 说明：向列表末尾追加元素。
    list_new.append(sum(sub_list) / w_size)
# 说明：输出内容到控制台，常用于观察程序运行结果。
print(list_new)

# 推导式:
# 说明：把右侧结果保存到 `list_new`。
list_new = [
    # 说明：执行算术运算，注意运算符含义和优先级。
    sum(list_num[i:i + w_size]) / w_size
    # 说明：遍历可迭代对象，逐个取值执行循环体。
    for i in range(len(list_num) - w_size + 1)
]
# 说明：输出内容到控制台，常用于观察程序运行结果。
print(list_new)
```

### Day05/exercise02.py

```python
"""
在终端中分别输入月和日
计算这是一年中的第几天 2月份默认29天
4月7日 98天

"""
# 每个月的天数放在元组中
# 说明：把右侧结果保存到 `tuple_day`。
tuple_day = (31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31)

# 说明：把右侧结果保存到 `month`。
month = int(input("请输入月份:"))
# 说明：把右侧结果保存到 `day`。
day = int(input("请输入日:"))

# 说明：把右侧结果保存到 `days`。
days = sum(tuple_day[:month - 1]) + day
# 说明：输出内容到控制台，常用于观察程序运行结果。
print(days)

"""
将列表中的质数提取出来，形成一个新的表格
"""

# 说明：把右侧结果保存到 `list1`。
list1 = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
# 说明：把右侧结果保存到 `list2`。
list2 = [num for num in list1 if not [item for item in range(2, int(num ** 0.5) + 1) if num % item == 0]]
# 说明：输出内容到控制台，常用于观察程序运行结果。
print(list2)
```

## 课堂要求与作业原文

### Day05/HomeWork.txt

```text
作业:
1.完成今日代码
2.提前向下预习 --> 容器类型(字典)
3.完成下列代码
  ①把字符串中的每个单词,反转输出
    Just do it  ==> Tsuj Od Ti
```

## 融会贯通笔记

### 推导式是循环的压缩写法

- `[表达式 for 变量 in 可迭代对象 if 条件]` 可以把筛选、加工、收集写在一行。
- 推导式适合简单逻辑，逻辑太复杂时还是普通 for 更清楚。

### 拷贝要看嵌套层级

- 直接赋值只是多了一个名字，两个名字指向同一个对象。
- 浅拷贝复制外层列表，但里面的嵌套列表仍然共享。
- 深拷贝复制所有层级，适合嵌套数据要完全独立的场景。

### 可变与不可变影响程序行为

- 列表、字典、集合通常可变；数字、字符串、元组通常不可变。
- 可变对象原地修改后，所有指向它的变量都会看到变化。
- 字符串看起来能“改”，本质上通常是生成了新字符串。

### 字符串方法是文本处理基本功

- 大小写转换、查找、替换、分割、拼接都属于高频操作。
- `split()` 把字符串拆成列表，`join()` 把字符串列表拼回字符串。

## 复盘自查

- [ ] 能写出带 if 条件的列表推导式
- [ ] 能解释浅拷贝为什么会影响嵌套列表
- [ ] 能用 split 和 join 完成字符串拆分与拼接
