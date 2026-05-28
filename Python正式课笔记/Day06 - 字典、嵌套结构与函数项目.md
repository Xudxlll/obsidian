# Day06 - 字典、嵌套结构与函数项目

> [!summary] 今日一句话
> 今天把容器能力推进到字典和嵌套结构，并开始用函数组织一个电商后台小项目。

## 今天到底学了什么

- 字典用键值对保存数据，适合按名字查信息
- `in` 可以判断成员，`is` 判断对象身份
- 字典和列表可以互相嵌套，表达复杂数据结构
- 函数把一段逻辑封装起来，项目开始从脚本走向模块化

> [!important] 抓主线
> 这一天的代码不是零散练习，而是在训练一个能力链条：先理解数据，再控制流程，再把重复逻辑封装起来。读代码时先看“数据从哪里来”，再看“经过什么判断或循环”，最后看“结果输出到哪里”。

## 课堂图示

**Day06_old/内存图.png**

![[附件/正式课/Day06_old/内存图.png]]


## 课堂代码合集

> 这里集中保留今天所有 `.py` 代码。代码块里补充的是理解代码用的中文说明，不是原项目必须运行的内容。

### Day06_new/01_func.py

```python
"""
函数(组织代码的一种方式)
一段组织好的,能够实现一定功能的代码段,可以重复使用

"""


# 定义
# 说明：定义函数 `add1`，参数：无参数。
def add1():
    # 说明：输出内容到控制台，常用于观察程序运行结果。
    print(1 + 2)


# 调用(只有调用函数,才会执行代码)
# 说明：调用函数，让已经定义好的逻辑真正执行。
add1()
# 说明：调用函数，让已经定义好的逻辑真正执行。
add1()
# 说明：调用函数，让已经定义好的逻辑真正执行。
add1()


# 写在函数定义时的小括号内的参数,称为形式参数,也叫形参
# 说明：定义函数 `add2`，参数：m, n。
def add2(m, n):
    # m,n本质上就是变量
    # 说明：输出内容到控制台，常用于观察程序运行结果。
    print(m + n)


# 写在函数调用时的小括号内的参数,称为实际参数,也叫实参
# 说明：调用函数，让已经定义好的逻辑真正执行。
add2(1, 2)
# 说明：把右侧结果保存到 `a`。
a = 11
# 说明：把右侧结果保存到 `b`。
b = 22
# 说明：调用函数，让已经定义好的逻辑真正执行。
add2(a, b)
```

### Day06_new/02_func.py

```python
"""
函数结合字典
"""

# 说明：定义函数 `add1`，参数：无参数。
def add1():
    # 说明：输出内容到控制台，常用于观察程序运行结果。
    print(1 + 2)

# 说明：定义函数 `sub1`，参数：无参数。
def sub1():
    # 说明：输出内容到控制台，常用于观察程序运行结果。
    print(1 - 2)

# 说明：把右侧结果保存到 `dict_op`。
dict_op = {
    # 说明：执行算术运算，注意运算符含义和优先级。
    "+": add1,
    # 说明：执行算术运算，注意运算符含义和优先级。
    "-": sub1
}

# 说明：执行算术运算，注意运算符含义和优先级。
dict_op["+"]()
```

### Day06_new/EShopManagerV1.py

```python
"""
电商后台管理系统V1

运行文件 显示数字服务菜单
    1.添加商品
    2.显示所有商品
    3.修改商品
    4.删除商品
    5.退出管理系统

用户在终端中输入(1~5)数字触发对应的操作
    按1键添加商品
        商品的id 标题 价格
    按2键显示所有商品
        ID1,苹果16手机,价格100
    按3键修改商品
        用户输入要修改的商品id
        修改标题和价格
    按4键删除商品
        用户输入要删除的商品id
    按5键
        退出管理系统
    按其他键
        提示暂无此服务
"""
# 说明：把右侧结果保存到 `list_goods`。
list_goods = []
# 说明：只要条件为 True，就持续循环。
while True:
    # 显示菜单
    # 说明：输出内容到控制台，常用于观察程序运行结果。
    print("按1键添加商品")
    # 说明：输出内容到控制台，常用于观察程序运行结果。
    print("按2键显示所有商品")
    # 说明：输出内容到控制台，常用于观察程序运行结果。
    print("按3键修改商品")
    # 说明：输出内容到控制台，常用于观察程序运行结果。
    print("按4键删除商品")
    # 说明：输出内容到控制台，常用于观察程序运行结果。
    print("按5键退出管理系统")

    # 选择菜单
    # 说明：把右侧结果保存到 `choose_number`。
    choose_number = input("请输入服务数字:")
    # 说明：判断条件是否成立，成立才执行下面缩进代码。
    if choose_number == "1":
        # 不允许为空 不允许有空格 价格必须是数字
        # 说明：只要条件为 True，就持续循环。
        while True:
            # 说明：把右侧结果保存到 `id`。
            id = input("请输入商品id:").replace(" ", "")
            # 说明：把右侧结果保存到 `title`。
            title = input("请输入商品标题:").replace(" ", "")
            # 说明：把右侧结果保存到 `price`。
            price = input("请输入商品价格:").replace(" ", "")

            # 说明：判断条件是否成立，成立才执行下面缩进代码。
            if id == "" or title == "" or price == "":
                # 说明：输出内容到控制台，常用于观察程序运行结果。
                print("内容不能为空,请重新输入!")
                # 说明：跳过本轮剩余代码，进入下一轮循环。
                continue

            # 说明：判断条件是否成立，成立才执行下面缩进代码。
            if price.isdigit() or price.replace(".", "", 1).isdigit():
                # 说明：输出内容到控制台，常用于观察程序运行结果。
                print("价格是数字")
                # 说明：立刻结束当前循环。
                break
            # 说明：前面条件都不成立时执行这里。
            else:
                # 说明：输出内容到控制台，常用于观察程序运行结果。
                print("价格不是数字")

        # 说明：把右侧结果保存到 `dict_goods`。
        dict_goods = {
            "id": id,
            "title": title,
            "price": price
        }
        # 说明：向列表末尾追加元素。
        list_goods.append(dict_goods)
        # 说明：输出内容到控制台，常用于观察程序运行结果。
        print(list_goods)
    # 说明：前面条件不成立时，继续判断这个分支。
    elif choose_number == "2":
        # 说明：判断条件是否成立，成立才执行下面缩进代码。
        if list_goods:
            # 说明：遍历可迭代对象，逐个取值执行循环体。
            for item in list_goods:
                # 说明：输出内容到控制台，常用于观察程序运行结果。
                print(F"ID:{item['id']},{item['title']},价格{item['price']}")
        # 说明：前面条件都不成立时执行这里。
        else:
            # 说明：输出内容到控制台，常用于观察程序运行结果。
            print("暂无商品信息")
    # 说明：前面条件不成立时，继续判断这个分支。
    elif choose_number == "3":
        # 说明：把右侧结果保存到 `id`。
        id = input("请输入要修改的商品ID:").replace(" ", "")
        # 说明：遍历可迭代对象，逐个取值执行循环体。
        for item in list_goods:
            # 说明：判断条件是否成立，成立才执行下面缩进代码。
            if item["id"] == id:
                # 说明：只要条件为 True，就持续循环。
                while True:
                    # 说明：把右侧结果保存到 `title`。
                    title = input("请输入新标题:").replace(" ", "")
                    # 说明：把右侧结果保存到 `price`。
                    price = input("请输入新价格:").replace(" ", "")

                    # 说明：判断条件是否成立，成立才执行下面缩进代码。
                    if id == "" or title == "" or price == "":
                        # 说明：输出内容到控制台，常用于观察程序运行结果。
                        print("内容不能为空,请重新输入!")
                        # 说明：跳过本轮剩余代码，进入下一轮循环。
                        continue

                    # 说明：判断条件是否成立，成立才执行下面缩进代码。
                    if price.isdigit() or price.replace(".", "", 1).isdigit():
                        # 说明：输出内容到控制台，常用于观察程序运行结果。
                        print("价格是数字")
                        # 说明：立刻结束当前循环。
                        break
                    # 说明：前面条件都不成立时执行这里。
                    else:
                        # 说明：输出内容到控制台，常用于观察程序运行结果。
                        print("价格不是数字")

                item.update({"title": title, "price": price})
                # 说明：立刻结束当前循环。
                break
        # 说明：前面条件都不成立时执行这里。
        else:
            # 说明：输出内容到控制台，常用于观察程序运行结果。
            print("商品不存在")
    # 说明：前面条件不成立时，继续判断这个分支。
    elif choose_number == "4":
        # 说明：把右侧结果保存到 `id`。
        id = input("请输入要删除的ID:")
        # 说明：遍历可迭代对象，逐个取值执行循环体。
        for item in list_goods:
            # 说明：判断条件是否成立，成立才执行下面缩进代码。
            if item["id"] == id:
                # 说明：按值删除元素。
                list_goods.remove(item)
                # 说明：立刻结束当前循环。
                break
        # 说明：前面条件都不成立时执行这里。
        else:
            # 说明：输出内容到控制台，常用于观察程序运行结果。
            print("商品不存在")
    # 说明：前面条件不成立时，继续判断这个分支。
    elif choose_number == "5":
        # 说明：输出内容到控制台，常用于观察程序运行结果。
        print("Bye~")
        # 说明：立刻结束当前循环。
        break
    # 说明：前面条件都不成立时执行这里。
    else:
        # 说明：输出内容到控制台，常用于观察程序运行结果。
        print("暂无此服务~")
```

### Day06_new/HomeWork01.py

```python
"""
②字符串:Just do it ==> tsuJ od ti
2种方法
"""
# 说明：把右侧结果保存到 `str1`。
str1 = "Just do it"

# 说明：把右侧结果保存到 `list_new`。
list_new = []
# 说明：遍历可迭代对象，逐个取值执行循环体。
for item in str1.split():
    # 说明：输出内容到控制台，常用于观察程序运行结果。
    print(item[::-1])
    # 说明：向列表末尾追加元素。
    list_new.append(item[::-1])

# 说明：输出内容到控制台，常用于观察程序运行结果。
print(" ".join(list_new))

# 推导式
# 说明：输出内容到控制台，常用于观察程序运行结果。
print(" ".join([item[::-1] for item in str1.split()]))
# 说明：输出内容到控制台，常用于观察程序运行结果。
print(" ".join(item[::-1] for item in str1.split()))

# 说明：输出内容到控制台，常用于观察程序运行结果。
print(" ".join(str1[::-1].split()[::-1]))
```

### Day06_new/HomeWork02.py

```python
"""
①推导式:找出在第一个字典中存在，在第二个字典中不存在的键值对
dict1 = {"a": 1, "b": 2, "c": 3}
dict2 = {"a": 5, "b": 2, "c": 6}
期望结果：{"a": 1,"c": 3}

②字符串:Just do it ==> tsuJ od ti
2种方法
"""
# 说明：把右侧结果保存到 `dict1`。
dict1 = {"a": 1, "b": 2, "c": 3}
# 说明：把右侧结果保存到 `dict2`。
dict2 = {"a": 5, "b": 2, "c": 6}

# 说明：把右侧结果保存到 `dict_new`。
dict_new = {
    key: val
    # 说明：遍历可迭代对象，逐个取值执行循环体。
    for key, val in dict1.items()
    # 说明：判断条件是否成立，成立才执行下面缩进代码。
    if dict1[key] != dict2[key]
}
# 说明：输出内容到控制台，常用于观察程序运行结果。
print(dict_new)
```

### Day06_new/Review.py

```python
"""
字典
键:值 唯一且不可变 值没有限制
创建: dict1 = {键:值}
访问: dict1[键]  dict1.get(键)
添加/修改: dict1[键] = 值 dict1.update({键:值})
删除: del dict1[键]  pop(键) popitem() clear()
遍历: for key in dict1
     for val in dict1.values() [值,值]
     for key,val in dict1.items() [(键,值),(键,值)]
推导式: {键:值  for 变量 in 可迭代对象 if 条件}
"""

'''
知识听得懂, 代码看明白,但是就是写不出来  --> 正常

多敲多练  ==>
每天上课先听后写  + 自己组织笔记
每周把本周的内容重新组织一遍


'''
```

### Day06_new/exercise01.py

```python
"""
两数之和
给定一个整数列表 nums 和一个整数目标值 target
请你在该列表中找出和为目标值 target  的那两个整数，并返回它们的索引
你可以假设每种输入只会对应一个答案，并且你不能使用两次相同的元素。

示例 1：
输入：nums = [2,7,11,15], target = 9
输出：[0,1]
解释：因为 nums[0] + nums[1] == 9 ，返回 [0, 1]

示例 2：
输入：nums = [3,2,4], target = 6
输出：[1,2]

示例 3：
输入：nums = [3,3], target = 6
输出：[0,1]

只会存在一个有效答案
"""
# 说明：把右侧结果保存到 `nums`。
nums = [2, 7, 11, 15]
# 说明：把右侧结果保存到 `target`。
target = 9
# 说明：把右侧结果保存到 `length`。
length = len(nums)

# 第一次
# 时间复杂度:执行时间随着输入规模增长的趋势,操作次数与数据规模n的关系
# 外层 n次 内层平均遍历 n/2次
# 总操作次数: n(n-1)/2  O(n^2)

# 空间复杂度:所需的内存索这输入规模增长的趋势,占用的额外存储空间与数据规模n的关系
# 说明：遍历可迭代对象，逐个取值执行循环体。
for i in range(length):
    # 说明：输出内容到控制台，常用于观察程序运行结果。
    print(f"外层i:{i}")
    # 说明：遍历可迭代对象，逐个取值执行循环体。
    for j in range(i + 1, length):
        # 说明：输出内容到控制台，常用于观察程序运行结果。
        print(f"内层j:{j}")
        # 说明：判断条件是否成立，成立才执行下面缩进代码。
        if nums[i] + nums[j] == target:
            # 说明：输出内容到控制台，常用于观察程序运行结果。
            print([i, j])

# 说明：输出内容到控制台，常用于观察程序运行结果。
print("-" * 10)

# 第二次 自己下去想一想用字典咋写呀?
# 说明：把右侧结果保存到 `nums`。
nums = [3, 3]
# 说明：把右侧结果保存到 `target`。
target = 6
# 说明：把右侧结果保存到 `dict_num`。
dict_num = {}

# 说明：遍历可迭代对象，逐个取值执行循环体。
for i in range(len(nums)):
    # 说明：把右侧结果保存到 `num`。
    num = nums[i]  # 获取当前数字
    # 说明：把右侧结果保存到 `complement`。
    complement = target - num  # 计算差值

    # 检查差值是否在字典中
    # 说明：判断条件是否成立，成立才执行下面缩进代码。
    if complement in dict_num:
        # 找到结果后直接输出并退出循环
        # 说明：输出内容到控制台，常用于观察程序运行结果。
        print([dict_num[complement], i])
        # 说明：立刻结束当前循环。
        break

    # 将当前数字及其索引存入字典
    # 说明：把右侧结果保存到 `dict_num[nums[i]]`。
    dict_num[nums[i]] = i
# 说明：前面条件都不成立时执行这里。
else:
    # 循环正常结束
    # 说明：输出内容到控制台，常用于观察程序运行结果。
    print([])
```

### Day06_new/exercise02.py

```python
"""
定义一个函数,接受2个整数和1个符号作为参数,实现四则运算 + - * /
"""


# 第一种
'''
def calc1(num1, f, num2):
    if f == "+":
        print(num1 + num2)
    elif f == "-":
        print(num1 - num2)
    elif f == "*":
        print(num1 * num2)
    elif f == "/":
        if num2 == 0:
            print("除数不能为0")
        else:
            print(num1 / num2)

num1 = int(input("请输入整数数字1:"))
f = input("请输入 + - * / 运算符号 :")
num2 = int(input("请输入整数数字2:"))
calc1(num1, f, num2)
'''


# 第二种:利用字典优化代码
'''
def calc2(num1, f, num2):
    dict_op = {
        "+": num1 + num2,
        "-": num1 - num2,
        "*": num1 * num2,
        "/": "除数不能为0" if num2 == 0 else num1 / num2
    }
    if f in dict_op:
        res = dict_op[f]
        print(res)
    else:
        print("运算符无效")

num1 = int(input("请输入整数数字1:"))
f = input("请输入 + - * / 运算符号 :")
num2 = int(input("请输入整数数字2:"))
calc2(num1, f, num2)
'''


# 第三种
# 说明：定义函数 `add`，参数：num1, num2。
def add(num1, num2):
    # 说明：输出内容到控制台，常用于观察程序运行结果。
    print(num1 + num2)


# 说明：定义函数 `sub`，参数：num1, num2。
def sub(num1, num2):
    # 说明：输出内容到控制台，常用于观察程序运行结果。
    print(num1 - num2)


# 说明：定义函数 `mult`，参数：num1, num2。
def mult(num1, num2):
    # 说明：输出内容到控制台，常用于观察程序运行结果。
    print(num1 * num2)


# 说明：定义函数 `div`，参数：num1, num2。
def div(num1, num2):
    # 说明：进行比较，结果是 True 或 False。
    print("除数不能为0" if num2 == 0 else num1 / num2)


# 说明：定义函数 `calc3`，参数：num1, f, num2。
def calc3(num1, f, num2):
    # 说明：把右侧结果保存到 `dict_op`。
    dict_op = {
        # 说明：执行算术运算，注意运算符含义和优先级。
        "+": add,
        # 说明：执行算术运算，注意运算符含义和优先级。
        "-": sub,
        # 说明：执行算术运算，注意运算符含义和优先级。
        "*": mult,
        # 说明：执行算术运算，注意运算符含义和优先级。
        "/": div
    }

    # 说明：判断条件是否成立，成立才执行下面缩进代码。
    if f in dict_op:
        dict_op[f](num1, num2)
    # 说明：前面条件都不成立时执行这里。
    else:
        # 说明：输出内容到控制台，常用于观察程序运行结果。
        print("符号无效")

# 说明：把右侧结果保存到 `num1`。
num1 = int(input("请输入整数数字1:"))
# 说明：把右侧结果保存到 `f`。
f = input("请输入 + - * / 运算符号 :")
# 说明：把右侧结果保存到 `num2`。
num2 = int(input("请输入整数数字2:"))
# 说明：调用函数，让已经定义好的逻辑真正执行。
calc3(num1, f, num2)
```

### Day06_new/exercise03.py

```python
"""
定义一个函数,接受一个二维列表作为参数
把二维列表变成一维的新列表,并打印
"""


# 说明：定义函数 `my_flatten`，参数：lst。
def my_flatten(lst):
    # 说明：把右侧结果保存到 `list_new`。
    list_new = []
    # 说明：遍历可迭代对象，逐个取值执行循环体。
    for item in lst:
        # 说明：遍历可迭代对象，逐个取值执行循环体。
        for sub in item:
            # 说明：向列表末尾追加元素。
            list_new.append(sub)

    # 说明：把右侧结果保存到 `list_new`。
    list_new = [sub for item in lst for sub in item]
    # 说明：输出内容到控制台，常用于观察程序运行结果。
    print(list_new)


# 说明：把右侧结果保存到 `list_num`。
list_num = [[1, 2, 3], [4, 5, 6]]
# 说明：调用函数，让已经定义好的逻辑真正执行。
my_flatten(list_num)
```

### Day06_old/01_find.py

```python
"""
字符串函数-查找相关
"""
# 说明：把右侧结果保存到 `str1`。
str1 = "Hello WOrld"

# 第一次出现的位置,找不到返回-1
# 说明：输出内容到控制台，常用于观察程序运行结果。
print(str1.find("O"))

# 最后一次出现的位置,找不到返回-1
# 说明：输出内容到控制台，常用于观察程序运行结果。
print(str1.rfind("l"))
```

### Day06_old/02_is.py

```python
"""
字符串函数-判断相关
"""
# 说明：把右侧结果保存到 `str1`。
str1 = "Hello"
# 说明：把右侧结果保存到 `str2`。
str2 = "666"
# 说明：把右侧结果保存到 `str3`。
str3 = "999Hello"

# 只包含数字
# 说明：输出内容到控制台，常用于观察程序运行结果。
print(str2.isdigit())
# 说明：输出内容到控制台，常用于观察程序运行结果。
print(str3.isdigit())

# 只包含字母
# 说明：输出内容到控制台，常用于观察程序运行结果。
print(str2.isalpha())
# 说明：输出内容到控制台，常用于观察程序运行结果。
print(str3.isalpha())

# 只包含字母+数字
# 说明：输出内容到控制台，常用于观察程序运行结果。
print(str1.isalnum())
# 说明：输出内容到控制台，常用于观察程序运行结果。
print(str3.isalnum())
# 说明：输出内容到控制台，常用于观察程序运行结果。
print("12He_".isalnum())
```

### Day06_old/03_dict.py

```python
"""
字典:
由一系列键值对组成的可变散列容器
键值对: 键:值 键必须是唯一且不可变 值没有限制
散列: 对键的哈希运算 确定在内存中存储的位置
"""
# 1.创建
# 说明：把右侧结果保存到 `dict_movie`。
dict_movie = {
    "name": 749,
    "index": 10086,
    "type": ("动画", "剧情"),
    "year": 2015
}
# 说明：输出内容到控制台，常用于观察程序运行结果。
print(dict_movie)

# 2.添加/修改
# 给字典不存在的键赋值就是添加 存在的键赋值修改
# 说明：把右侧结果保存到 `dict_movie["city"]`。
dict_movie["city"] = "中国"
# 说明：把右侧结果保存到 `dict_movie["year"]`。
dict_movie["year"] = 2024

dict_movie.update({"index": 555, "director": "导演"})

# 3.删除
del dict_movie["year"]
# 说明：弹出元素；不传索引时通常弹出最后一个。
dict_movie.pop("city", None)
# 删除最后一个
dict_movie.popitem()

# 4.访问
# 说明：输出内容到控制台，常用于观察程序运行结果。
print(dict_movie["name"])
# 说明：输出内容到控制台，常用于观察程序运行结果。
print(dict_movie.get("type"))
# 说明：输出内容到控制台，常用于观察程序运行结果。
print(dict_movie.get("age", "不存在"))

# 5.遍历
# 默认得到的是键
# 说明：遍历可迭代对象，逐个取值执行循环体。
for key in dict_movie:
    # 说明：输出内容到控制台，常用于观察程序运行结果。
    print(key, dict_movie.get(key))

# 每个键值
# 说明：遍历可迭代对象，逐个取值执行循环体。
for value in dict_movie.values():
    # 说明：输出内容到控制台，常用于观察程序运行结果。
    print(value)

# 键值对组成一个个元组 元组的第一个元素是键 第二个元素是值
# 说明：遍历可迭代对象，逐个取值执行循环体。
for key, value in dict_movie.items():
    # 说明：输出内容到控制台，常用于观察程序运行结果。
    print(key, value)
```

### Day06_old/04_member.py

```python
"""
成员运算符(list tuple str dict使用)
in 查看一个元素在不在其中 在返回true 反之返回false
not in 查看一个元素不在其中 不在返回true 反之返回false
"""
# 说明：把右侧结果保存到 `list1`。
list1 = [1, 2, 3, 4]
# 说明：把右侧结果保存到 `tuple1`。
tuple1 = (1, 2, 3, 4)
# 说明：把右侧结果保存到 `str1`。
str1 = "1234"
# 说明：把右侧结果保存到 `dict1`。
dict1 = {1: "PHP", "name": 2}

# 说明：输出内容到控制台，常用于观察程序运行结果。
print(1 in list1)
# 说明：组合多个布尔条件。
print("4" not in str1)
# 看的键
# 说明：输出内容到控制台，常用于观察程序运行结果。
print(2 in dict1)

"""
身份运算符
比较2个对象是不是同一个对象(内存地址)
is
"""
# 说明：把右侧结果保存到 `a`。
a = 1
# 说明：把右侧结果保存到 `b`。
b = 1
# 说明：输出内容到控制台，常用于观察程序运行结果。
print(a is b)

# 尽管列表一样,但不是同一个内存地址
# 说明：把右侧结果保存到 `a`。
a = [1, 2, 3]
# 说明：把右侧结果保存到 `b`。
b = [1, 2, 3]
# 说明：输出内容到控制台，常用于观察程序运行结果。
print(a is b)  # F

# 说明：把右侧结果保存到 `a`。
a = (1, 2, 3)
# 说明：把右侧结果保存到 `b`。
b = (1, 2, 3)
# 说明：输出内容到控制台，常用于观察程序运行结果。
print(a is b)  # T

# 说明：把右侧结果保存到 `a`。
a = [1, 2, 3]
# 说明：把右侧结果保存到 `b`。
b = [1, 2, 1, 3]
# 说明：输出内容到控制台，常用于观察程序运行结果。
print(a[0] is b[2])  # T
# 说明：输出内容到控制台，常用于观察程序运行结果。
print(b[0] is b[2])  # T
```

### Day06_old/05_derivative.py

```python
"""
字典推导式

字典名= {键:值 for 变量 in 可迭代对象}
字典名= {键:值 for 变量 in 可迭代对象 if 条件}
"""
# 说明：把右侧结果保存到 `dict1`。
dict1 = {
    "1001": "Beijing",
    "1002": "Tianjin",
    "1003": "Hebei"
}

# 说明：把右侧结果保存到 `dict_new`。
dict_new = {value: key for key, value in dict1.items()}
# 说明：输出内容到控制台，常用于观察程序运行结果。
print(dict_new)

# 说明：把右侧结果保存到 `dict_new`。
dict_new = {value: key for key, value in dict1.items() if key == "1003"}
# 说明：输出内容到控制台，常用于观察程序运行结果。
print(dict_new)
```

### Day06_old/06_nesting.py

```python
"""
容器嵌套
"""
# 说明：把右侧结果保存到 `list_movie`。
list_movie = [
    {
        "name": "咒怨",
        "index": 10086,
        "type": ("动画", "科幻"),
        "actor": ["子牙", "申公豹"]
    },
    {
        "name": "娃娃",
        "index": 10010,
        "type": ("喜剧", "情节"),
        "actor": ["沈腾", "马丽"]
    }
]
# 1.打印申公豹
# 说明：输出内容到控制台，常用于观察程序运行结果。
print(list_movie[0]["actor"][1])

# 2.打印出所有的电影的类型 type
# 说明：遍历可迭代对象，逐个取值执行循环体。
for item in list_movie:
    # 说明：遍历可迭代对象，逐个取值执行循环体。
    for sub_item in item["type"]:
        # 说明：输出内容到控制台，常用于观察程序运行结果。
        print(sub_item)
```

### Day06_old/1111111111.py

```python
"""
运行文件 显示数字服务菜单
1.添加商品
2.显示所有商品
3.修改商品
4.删除商品
5.退出管理系统
用户在终端中输入(1~5)数字触发对应
按1键添加商品
商品的id 标题 价格
按2键显示所有商品
    ID1,苹果16手机，价格100
按3键修改商品
    用户输入要修改的商品id
    修改标题和价格
按4键删除商品
    用户输入要删除的商品id
按5键
退出管理系统
按其他键提示誓无此服务
"""
```

### Day06_old/EShopManagerV1.py

```python
"""
电商后台管理系统V1

运行文件 显示数字服务菜单
    1.添加商品
    2.显示所有商品
    3.修改商品
    4.删除商品
    5.退出管理系统

用户在终端中输入(1~5)数字触发对应的操作
    按1键添加商品
        商品的id 标题 价格
    按2键显示所有商品
        ID1,苹果16手机,价格100
    按3键修改商品  重复赋值
        用户输入要修改的商品id
        修改标题和价格
    按4键删除商品
        用户输入要删除的商品id
    按5键
        退出管理系统
    按其他键
        提示暂无此服务
"""
# 存储商品数据
# 说明：把右侧结果保存到 `list_goods`。
list_goods = []
# 说明：只要条件为 True，就持续循环。
while True:
    # 显示菜单
    # 说明：输出内容到控制台，常用于观察程序运行结果。
    print("按1键添加商品")
    # 说明：输出内容到控制台，常用于观察程序运行结果。
    print("按2键显示所有商品")
    # 说明：输出内容到控制台，常用于观察程序运行结果。
    print("按3键修改商品")
    # 说明：输出内容到控制台，常用于观察程序运行结果。
    print("按4键删除商品")
    # 说明：输出内容到控制台，常用于观察程序运行结果。
    print("按5键退出管理系统")

    # 选择菜单
    # 说明：把右侧结果保存到 `choose_number`。
    choose_number = input("请输入服务数字：")
    # 说明：判断条件是否成立，成立才执行下面缩进代码。
    if choose_number == "1":
        # 说明：把右侧结果保存到 `id`。
        id = input("请输入商品id:").replace(" ", "")
        # 说明：把右侧结果保存到 `title`。
        title = input("请输入商品标题:").replace(" ", "")
        # 说明：把右侧结果保存到 `price`。
        price = input("请输入商品价格:").replace(" ", "")


        # 说明：把右侧结果保存到 `dict_goods`。
        dict_goods = {
            "id": id,
            "title": title,
            "price": price
        }
        # 说明：向列表末尾追加元素。
        list_goods.append(dict_goods)
        # 说明：输出内容到控制台，常用于观察程序运行结果。
        print(list_goods)
    # 说明：前面条件不成立时，继续判断这个分支。
    elif choose_number == "2":
        # 说明：判断条件是否成立，成立才执行下面缩进代码。
        if list_goods:
            # 说明：遍历可迭代对象，逐个取值执行循环体。
            for item in list_goods:
                # 说明：输出内容到控制台，常用于观察程序运行结果。
                print(f"ID:{item['id']},标题:{item['title']},价格{item['price']}")
        # 说明：前面条件都不成立时执行这里。
        else:
            # 说明：输出内容到控制台，常用于观察程序运行结果。
            print("暂无商品~")
    # 说明：前面条件不成立时，继续判断这个分支。
    elif choose_number == "3":
        # 说明：输出内容到控制台，常用于观察程序运行结果。
        print("修改")
    # 说明：前面条件不成立时，继续判断这个分支。
    elif choose_number == "4":
        # 说明：输出内容到控制台，常用于观察程序运行结果。
        print("删除")
    # 说明：前面条件不成立时，继续判断这个分支。
    elif choose_number == "5":
        # 说明：输出内容到控制台，常用于观察程序运行结果。
        print("Bye~")
        # 说明：立刻结束当前循环。
        break
    # 说明：前面条件都不成立时执行这里。
    else:
        # 说明：输出内容到控制台，常用于观察程序运行结果。
        print("暂无此服务!")
```

### Day06_old/HomeWork/HomeWork01.py

```python
"""
把字符串中的每个单词,反转输出
Just do it  ==> Tsuj Od Ti
"""
# 说明：把右侧结果保存到 `str1`。
str1 = "Just do it"
# 说明：输出内容到控制台，常用于观察程序运行结果。
print(str1.split())

# 说明：把右侧结果保存到 `list_new`。
list_new = []
# 遍历split()得到的列表
# 说明：遍历可迭代对象，逐个取值执行循环体。
for item in str1.split():
    # 把每个元素翻转且首字母大写后存入新列表
    # 说明：向列表末尾追加元素。
    list_new.append(item[::-1].title())
# join拼接元素得到字符串
# 说明：输出内容到控制台，常用于观察程序运行结果。
print(" ".join(list_new))

# 说明：输出内容到控制台，常用于观察程序运行结果。
print(" ".join([item[::-1].title() for item in str1.split()]))
```

### Day06_old/Reviw.py

```python
"""
列表推导式
    [ 变量操作 for 变量 in 可迭代对象]
    [ 变量操作 for 变量 in 可迭代对象 if 条件

深浅拷贝:
    浅拷贝:切片 复制浅层数据, 共享深层数据
    深拷贝:deepcopy() 复制所有层数据

元组
    由一系列变量组成的不可变序列容器
    索引 切片 函数 ==> len max min sum 循环
    元组解包:
        依次获取元素 复制给变量
        基础解包:变量的数量和元组的数量一致
        *号解包:*号收集多余的元素,放在列表里

字符串:
    由一系列字符的编码值组成的不可变序列容器
    创建: "" '' 三引号
    索引和切片 遍历
    转义:改变原有字符的含义 \反斜杠
    格式化: f"{}"
    函数:
        大小写和字符:
            upper() lower() title() strip()
            split() join() replace()
"""
```

### Day06_old/exercise01.py

```python
"""
编写一段程序,得到以下结果
["apple", "orange", "banana", "pear", "grape"]
"""
# 说明：把右侧结果保存到 `str1`。
str1 = "apple,orange;banana | pear grape"

# 思路：遍历字符串每个元素,判断,是字母就拼接到新的字符串中,不是字符就拼接空格,然后使用split分割,分割后变成列表
# 说明：把右侧结果保存到 `str_new`。
str_new = ""
# 说明：遍历可迭代对象，逐个取值执行循环体。
for char in str1:
    # 说明：判断条件是否成立，成立才执行下面缩进代码。
    if char.isalpha():
        # 说明：更新 `str_new +` 的值，属于复合赋值。
        str_new += char
    # 说明：前面条件都不成立时执行这里。
    else:
        # 说明：更新 `str_new +` 的值，属于复合赋值。
        str_new += " "

# 说明：输出内容到控制台，常用于观察程序运行结果。
print(str_new.split())

# if三元表达式写法
# true_val if 条件 else false_vale
# print(666) if 1 == 1 else print("我丢")

# 推导式
# 思路:遍历字符串每个元素,判断是字母存在列表中,不是字母就存成空格在列表中,然后join连接列表中的每个字符形成新的字符串,最后使用split分割,分割后变成列表
# 说明：输出内容到控制台，常用于观察程序运行结果。
print([char for char in str1])
# 说明：输出内容到控制台，常用于观察程序运行结果。
print([char if char.isalpha() else " " for char in str1])
# 说明：输出内容到控制台，常用于观察程序运行结果。
print("".join([char if char.isalpha() else " " for char in str1]))
# 说明：输出内容到控制台，常用于观察程序运行结果。
print(
    # 说明：把多个字符串拼接成一个字符串。
    "".join(
        [
            char if char.isalpha() else " "
            # 说明：遍历可迭代对象，逐个取值执行循环体。
            for char in str1
        ]
    # 说明：把字符串按规则拆成列表。
    ).split()
)
```

### Day06_old/exercise02.py

```python
"""
创建字典,存储受感染地区的名称,新增感染人数,现有感染人数
感染人数新增100人
增加治愈人数与累积感染人数 2000人
治愈人数新增20人
删除新增感人人数
输出字典所有的信息
"""
# 说明：把右侧结果保存到 `dict_area`。
dict_area = {
    "region": "湾湾",
    "new": 150,
    "now": 652
}
# 说明：更新 `dict_area["new"] +` 的值，属于复合赋值。
dict_area["new"] += 100

dict_area.update({"cure": 0, "total": 2000})
# 说明：按键取值，取不到时可返回默认值。
dict_area.update({"cure": dict_area.get("cure") + 20})

del dict_area["new"]

# 说明：遍历可迭代对象，逐个取值执行循环体。
for key, value in dict_area.items():
    # 说明：输出内容到控制台，常用于观察程序运行结果。
    print(key, value)
```

### Day06_old/exercise03.py

```python
"""
颠倒字典的键和值
{"1001": "Beijing"} ==> {"Beijing": "1001"}
"""

# 说明：把右侧结果保存到 `dict1`。
dict1 = {
    "1001": "Beijing",
    "1002": "Tianjin",
    "1003": "Hebei"
}

# 说明：把右侧结果保存到 `dict_new`。
dict_new = {}

# 说明：遍历可迭代对象，逐个取值执行循环体。
for key, value in dict1.items():
    # 说明：把右侧结果保存到 `dict_new[value]`。
    dict_new[value] = key
    dict_new.update({value:key})
# 说明：输出内容到控制台，常用于观察程序运行结果。
print(dict_new)
```

### Day06_old/exercise04.py

```python
"""
给定一个字符串
abcacbbc  ==> a2b3c3
只允许使用items 或者 isalpha 函数 其他函数不允许
"""
# 说明：把右侧结果保存到 `str1`。
str1 = "abcacbbc"

# 说明：把右侧结果保存到 `dict_char`。
dict_char = {}
# 说明：遍历可迭代对象，逐个取值执行循环体。
for char in str1:
    # 说明：判断条件是否成立，成立才执行下面缩进代码。
    if char in dict_char:
        # 说明：更新 `dict_char[char] +` 的值，属于复合赋值。
        dict_char[char] += 1
    # 说明：前面条件都不成立时执行这里。
    else:
        # 说明：把右侧结果保存到 `dict_char[char]`。
        dict_char[char] = 1
    # 说明：输出内容到控制台，常用于观察程序运行结果。
    print(dict_char)

# 说明：把右侧结果保存到 `output`。
output = ""
# 说明：遍历可迭代对象，逐个取值执行循环体。
for char, count in dict_char.items():
    # print(f"{char}{count}",end="")
    # 说明：更新 `output +` 的值，属于复合赋值。
    output += f"{char}{count}"

# 说明：输出内容到控制台，常用于观察程序运行结果。
print(output)
```

## 课堂要求与作业原文

### Day06_new/HomeWork.txt

```text
1.完成今日代码
2.完成下列练习
  ①定义一个函数, 接受一个字符串作为参数,判断是不是回文字符串
    忽略大小写,忽略非字母的字符,忽略数字
    str1 = "上海自来水来自海上"
    str2 = "A man, a plan, a canal, Panama"
    str3 = "HEHE"

    普通写法 和 结合推导式写法

3.预习:函数
```

### Day06_old/HomeWork.txt

```text
作业:
1.完成今日代码
2.提前向下预习 --> 容器类型(函数)
3.完成EShopManagerV1代码
  ①完成修改功能
  ②完成删除功能  
  ③加入数据验证
    a.用户输入的内容不能为空
    b.用户输入的价格必须数字
    c.修改和删除商品时,验证商品存不存在
```

## 融会贯通笔记

### 字典解决“按键查值”的问题

- 列表适合按位置找，字典适合按名字找。
- `dict[key]` 取不到会报错，`dict.get(key)` 可以给默认值，更安全。
- `keys()`、`values()`、`items()` 分别遍历键、值、键值对。

### 成员运算和身份比较不要混

- `in` 问的是“这个元素在不在容器里”。
- `==` 问的是“值是否相等”。
- `is` 问的是“是不是同一个对象”，常用于理解内存和对象身份。

### 嵌套结构是项目数据的雏形

- 商品可以用字典表示：id、标题、价格。
- 多个商品可以放进列表里，形成“商品列表”。
- 当数据结构清楚后，增删改查其实就是围绕这个结构做操作。

### 函数让项目变得可维护

- 菜单显示、添加商品、显示商品、修改商品、删除商品都可以拆成函数。
- 函数名就是功能说明，好的函数名能让主流程像目录一样清楚。
- 用字典保存“操作编号 -> 函数”时，就能少写很多 if/elif。

## 复盘自查

- [ ] 能用字典表示一个商品
- [ ] 能遍历商品列表并打印每个商品信息
- [ ] 能把菜单的每个操作拆成独立函数
