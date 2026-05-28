## 今天学了什么

> [!info] 今天学了什么
> - 学习字符串查找、判断、成员运算和身份比较。
> - 学习字典的创建、读取、修改、遍历，以及字典推导式。
> - 学习容器嵌套，用列表和字典组织多条复杂数据。
> - 学习函数定义与调用，并把函数作为字典的值进行菜单分发。
> - 完成电商后台管理系统 V1，练习商品增删改查。

## 抓主线

> [!tip] 抓主线
> 1. 字典让数据从按位置访问升级为按 key 访问。
> 2. 嵌套结构让多条业务数据能组织起来。
> 3. 函数让代码按功能拆分。
> 4. 项目把菜单、输入、分支、循环、容器和函数串起来。

## 课堂代码合集

### Day06_new/01_func.py

```python
"""
函数(组织代码的一种方式)
一段组织好的,能够实现一定功能的代码段,可以重复使用

"""


# 定义
def add1():
    print(1 + 2)


# 调用(只有调用函数,才会执行代码)
add1()
add1()
add1()


# 写在函数定义时的小括号内的参数,称为形式参数,也叫形参
def add2(m, n):
    # m,n本质上就是变量
    print(m + n)


# 写在函数调用时的小括号内的参数,称为实际参数,也叫实参
add2(1, 2)
a = 11
b = 22
add2(a, b)
```

> [!note] 这份文件实际讲了什么
> - 文件说明/题目写的是：函数(组织代码的一种方式)；一段组织好的,能够实现一定功能的代码段,可以重复使用。
> - 文件中定义了函数：`add1()`、`add2(m, n)`。
> - 主要变量/数据名包括：`a`、`b`。

> [!example] 本文件出现的新代码 / 函数 / 方法
> - 本文件主要是在复习或组合前面已经学过的写法，没有引入需要单独记忆的新函数/方法；重点看它如何把旧知识组合成当前题目。
> - 从原文件注释/说明看，本文件重点是：函数(组织代码的一种方式)；调用(只有调用函数,才会执行代码)。

> [!abstract] 代码逻辑怎么走
> - 先定义函数，把某段功能封装起来；后面通过函数名加括号调用。
> - 通过赋值语句保存中间结果，主要变量包括：`a`、`b`。

> [!warning] 需要注意的点
> - 读这份代码时，先看变量如何变化，再看最终输出。

> [!success] 举一反三
> - 可以继续把重复逻辑拆成函数，让主流程只负责调用。

### Day06_new/02_func.py

```python
"""
函数结合字典
"""

def add1():
    print(1 + 2)

def sub1():
    print(1 - 2)

dict_op = {
    "+": add1,
    "-": sub1
}

dict_op["+"]()
```

> [!note] 这份文件实际讲了什么
> - 文件说明/题目写的是：函数结合字典。
> - 文件中定义了函数：`add1()`、`sub1()`。
> - 主要变量/数据名包括：`dict_op`。

> [!example] 本文件出现的新代码 / 函数 / 方法
> - 字典 `{key: value}`：用键值对描述结构化数据。
> - 从原文件注释/说明看，本文件重点是：函数结合字典。

> [!abstract] 代码逻辑怎么走
> - 先定义函数，把某段功能封装起来；后面通过函数名加括号调用。
> - 通过赋值语句保存中间结果，主要变量包括：`dict_op`。

> [!warning] 需要注意的点
> - 字典按 key 取值，key 要唯一；遍历键值对时优先想到 `.items()`。

> [!success] 举一反三
> - 可以把同样结构用于学生信息、商品信息、地区数据等 key-value 场景。
> - 可以继续把重复逻辑拆成函数，让主流程只负责调用。

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
list_goods = []
while True:
    # 显示菜单
    print("按1键添加商品")
    print("按2键显示所有商品")
    print("按3键修改商品")
    print("按4键删除商品")
    print("按5键退出管理系统")

    # 选择菜单
    choose_number = input("请输入服务数字:")
    if choose_number == "1":
        # 不允许为空 不允许有空格 价格必须是数字
        while True:
            id = input("请输入商品id:").replace(" ", "")
            title = input("请输入商品标题:").replace(" ", "")
            price = input("请输入商品价格:").replace(" ", "")

            if id == "" or title == "" or price == "":
                print("内容不能为空,请重新输入!")
                continue

            if price.isdigit() or price.replace(".", "", 1).isdigit():
                print("价格是数字")
                break
            else:
                print("价格不是数字")

        dict_goods = {
            "id": id,
            "title": title,
            "price": price
        }
        list_goods.append(dict_goods)
        print(list_goods)
    elif choose_number == "2":
        if list_goods:
            for item in list_goods:
                print(F"ID:{item['id']},{item['title']},价格{item['price']}")
        else:
            print("暂无商品信息")
    elif choose_number == "3":
        id = input("请输入要修改的商品ID:").replace(" ", "")
        for item in list_goods:
            if item["id"] == id:
                while True:
                    title = input("请输入新标题:").replace(" ", "")
                    price = input("请输入新价格:").replace(" ", "")

                    if id == "" or title == "" or price == "":
                        print("内容不能为空,请重新输入!")
                        continue

                    if price.isdigit() or price.replace(".", "", 1).isdigit():
                        print("价格是数字")
                        break
                    else:
                        print("价格不是数字")

                item.update({"title": title, "price": price})
                break
        else:
            print("商品不存在")
    elif choose_number == "4":
        id = input("请输入要删除的ID:")
        for item in list_goods:
            if item["id"] == id:
                list_goods.remove(item)
                break
        else:
            print("商品不存在")
    elif choose_number == "5":
        print("Bye~")
        break
    else:
        print("暂无此服务~")
```

> [!note] 这份文件实际讲了什么
> - 文件说明/题目写的是：电商后台管理系统V1；运行文件 显示数字服务菜单；1.添加商品；2.显示所有商品；3.修改商品。
> - 主要变量/数据名包括：`list_goods`、`choose_number`、`id`、`title`、`price`、`dict_goods`。

> [!example] 本文件出现的新代码 / 函数 / 方法
> - `.isdigit()`：判断字符串是否只由数字组成。
> - `.update()`：更新字典内容。

> [!abstract] 代码逻辑怎么走
> - 使用 `while` 形成循环，循环内部根据输入或条件决定是否继续。
> - 使用 `for` 遍历序列或容器，对每个元素执行同样的处理。
> - 使用条件判断把不同情况分开处理。
> - 通过赋值语句保存中间结果，主要变量包括：`list_goods`、`choose_number`、`id`、`title`、`price`、`dict_goods`。

> [!warning] 需要注意的点
> - `input()` 读到的是字符串，做数学计算前要先转换为 `int` 或 `float`。
> - `while` 循环要保证循环条件会发生变化，否则可能死循环。
> - `break` 只结束当前这一层循环。
> - `continue` 会跳过本轮后续代码，直接进入下一轮。
> - 字典按 key 取值，key 要唯一；遍历键值对时优先想到 `.items()`。

> [!success] 举一反三
> - 可以给输入加合法性检查，例如不能为空、必须是数字、范围必须正确。
> - 可以把同样结构用于学生信息、商品信息、地区数据等 key-value 场景。
> - 可以把单个变量升级为列表，批量保存多条数据后统一遍历处理。

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

> [!info] 课堂文本/作业说明
> - 1.完成今日代码
> - 2.完成下列练习
> - ①定义一个函数, 接受一个字符串作为参数,判断是不是回文字符串
> - 忽略大小写,忽略非字母的字符,忽略数字
> - str1 = "上海自来水来自海上"
> - str2 = "A man, a plan, a canal, Panama"
> - str3 = "HEHE"
> - 普通写法 和 结合推导式写法

### Day06_new/HomeWork01.py

```python
"""
②字符串:Just do it ==> tsuJ od ti
2种方法
"""
str1 = "Just do it"

list_new = []
for item in str1.split():
    print(item[::-1])
    list_new.append(item[::-1])

print(" ".join(list_new))

# 推导式
print(" ".join([item[::-1] for item in str1.split()]))
print(" ".join(item[::-1] for item in str1.split()))

print(" ".join(str1[::-1].split()[::-1]))
```

> [!note] 这份文件实际讲了什么
> - 文件说明/题目写的是：②字符串:Just do it ==> tsuJ od ti；2种方法。
> - 主要变量/数据名包括：`str1`、`list_new`。

> [!example] 本文件出现的新代码 / 函数 / 方法
> - `.split()`：按分隔符拆分字符串。
> - 从原文件注释/说明看，本文件重点是：②字符串:Just do it ==> tsuJ od ti；推导式。

> [!abstract] 代码逻辑怎么走
> - 使用 `for` 遍历序列或容器，对每个元素执行同样的处理。
> - 通过赋值语句保存中间结果，主要变量包括：`str1`、`list_new`。

> [!warning] 需要注意的点
> - 列表是可变对象，增删改会直接影响原列表。
> - 字符串方法通常返回新字符串，不会原地修改原字符串。

> [!success] 举一反三
> - 可以把单个变量升级为列表，批量保存多条数据后统一遍历处理。
> - 可以把循环和条件组合起来做筛选、统计、累加、菜单系统。

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
dict1 = {"a": 1, "b": 2, "c": 3}
dict2 = {"a": 5, "b": 2, "c": 6}

dict_new = {
    key: val
    for key, val in dict1.items()
    if dict1[key] != dict2[key]
}
print(dict_new)
```

> [!note] 这份文件实际讲了什么
> - 文件说明/题目写的是：①推导式:找出在第一个字典中存在，在第二个字典中不存在的键值对；dict1 = {"a": 1, "b": 2, "c": 3}；dict2 = {"a": 5, "b": 2, "c": 6}；期望结果：{"a": 1,"c": 3}；②字符串:Just do it ==> tsuJ od ti。
> - 主要变量/数据名包括：`dict1`、`dict2`、`dict_new`。

> [!example] 本文件出现的新代码 / 函数 / 方法
> - 字典推导式：通过遍历快速生成新字典。
> - `.items()`：获取字典键值对，常用于遍历。
> - 从原文件注释/说明看，本文件重点是：①推导式:找出在第一个字典中存在，在第二个字典中不存在的键值对；②字符串:Just do it ==> tsuJ od ti。

> [!abstract] 代码逻辑怎么走
> - 通过赋值语句保存中间结果，主要变量包括：`dict1`、`dict2`、`dict_new`。

> [!warning] 需要注意的点
> - 字典按 key 取值，key 要唯一；遍历键值对时优先想到 `.items()`。

> [!success] 举一反三
> - 可以把同样结构用于学生信息、商品信息、地区数据等 key-value 场景。

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

> [!note] 这份文件实际讲了什么
> - 文件说明/题目写的是：字典；键:值 唯一且不可变 值没有限制；创建: dict1 = {键:值}；访问: dict1[键]  dict1.get(键)；添加/修改: dict1[键] = 值 dict1.update({键:值})。
> - 后续说明/题目还包括：知识听得懂, 代码看明白,但是就是写不出来  --> 正常；多敲多练  ==>；每天上课先听后写  + 自己组织笔记。

> [!example] 本文件出现的新代码 / 函数 / 方法
> - 本文件主要是在复习或组合前面已经学过的写法，没有引入需要单独记忆的新函数/方法；重点看它如何把旧知识组合成当前题目。
> - 从原文件注释/说明看，本文件重点是：字典。

> [!abstract] 代码逻辑怎么走
> - 这份代码主要是顺序执行：先准备数据，再调用函数或输出结果。

> [!warning] 需要注意的点
> - 读这份代码时，先看变量如何变化，再看最终输出。

> [!success] 举一反三
> - 可以修改示例数据重新运行，观察输出如何变化。

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
nums = [2, 7, 11, 15]
target = 9
length = len(nums)

# 第一次
# 时间复杂度:执行时间随着输入规模增长的趋势,操作次数与数据规模n的关系
# 外层 n次 内层平均遍历 n/2次
# 总操作次数: n(n-1)/2  O(n^2)

# 空间复杂度:所需的内存索这输入规模增长的趋势,占用的额外存储空间与数据规模n的关系
for i in range(length):
    print(f"外层i:{i}")
    for j in range(i + 1, length):
        print(f"内层j:{j}")
        if nums[i] + nums[j] == target:
            print([i, j])

print("-" * 10)

# 第二次 自己下去想一想用字典咋写呀?
nums = [3, 3]
target = 6
dict_num = {}

for i in range(len(nums)):
    num = nums[i]  # 获取当前数字
    complement = target - num  # 计算差值

    # 检查差值是否在字典中
    if complement in dict_num:
        # 找到结果后直接输出并退出循环
        print([dict_num[complement], i])
        break

    # 将当前数字及其索引存入字典
    dict_num[nums[i]] = i
else:
    # 循环正常结束
    print([])
```

> [!note] 这份文件实际讲了什么
> - 文件说明/题目写的是：两数之和；给定一个整数列表 nums 和一个整数目标值 target；请你在该列表中找出和为目标值 target  的那两个整数，并返回它们的索引；你可以假设每种输入只会对应一个答案，并且你不能使用两次相同的元素。；示例 1：。
> - 主要变量/数据名包括：`nums`、`target`、`length`、`dict_num`、`num`、`complement`、`dict_num[...]`。

> [!example] 本文件出现的新代码 / 函数 / 方法
> - 本文件主要是在复习或组合前面已经学过的写法，没有引入需要单独记忆的新函数/方法；重点看它如何把旧知识组合成当前题目。
> - 从原文件注释/说明看，本文件重点是：给定一个整数列表 nums 和一个整数目标值 target；请你在该列表中找出和为目标值 target  的那两个整数，并返回它们的索引。

> [!abstract] 代码逻辑怎么走
> - 使用 `for` 遍历序列或容器，对每个元素执行同样的处理。
> - 使用条件判断把不同情况分开处理。
> - 通过赋值语句保存中间结果，主要变量包括：`nums`、`target`、`length`、`dict_num`、`num`、`complement`、`dict_num[...]`。

> [!warning] 需要注意的点
> - `range()` 的结束值取不到，写边界时要特别小心。
> - `break` 只结束当前这一层循环。
> - 字典按 key 取值，key 要唯一；遍历键值对时优先想到 `.items()`。
> - 列表是可变对象，增删改会直接影响原列表。

> [!success] 举一反三
> - 可以把同样结构用于学生信息、商品信息、地区数据等 key-value 场景。
> - 可以把单个变量升级为列表，批量保存多条数据后统一遍历处理。
> - 可以把循环和条件组合起来做筛选、统计、累加、菜单系统。

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
def add(num1, num2):
    print(num1 + num2)


def sub(num1, num2):
    print(num1 - num2)


def mult(num1, num2):
    print(num1 * num2)


def div(num1, num2):
    print("除数不能为0" if num2 == 0 else num1 / num2)


def calc3(num1, f, num2):
    dict_op = {
        "+": add,
        "-": sub,
        "*": mult,
        "/": div
    }

    if f in dict_op:
        dict_op[f](num1, num2)
    else:
        print("符号无效")

num1 = int(input("请输入整数数字1:"))
f = input("请输入 + - * / 运算符号 :")
num2 = int(input("请输入整数数字2:"))
calc3(num1, f, num2)
```

> [!note] 这份文件实际讲了什么
> - 文件说明/题目写的是：定义一个函数,接受2个整数和1个符号作为参数,实现四则运算 + - * /。
> - 后续说明/题目还包括：def calc1(num1, f, num2):；if f == "+":；print(num1 + num2) / def calc2(num1, f, num2):；dict_op = {；"+": num1 + num2,。
> - 文件中定义了函数：`add(num1, num2)`、`sub(num1, num2)`、`mult(num1, num2)`、`div(num1, num2)`、`calc3(num1, f, num2)`。
> - 主要变量/数据名包括：`dict_op`、`num1`、`f`、`num2`。

> [!example] 本文件出现的新代码 / 函数 / 方法
> - 本文件主要是在复习或组合前面已经学过的写法，没有引入需要单独记忆的新函数/方法；重点看它如何把旧知识组合成当前题目。
> - 从原文件注释/说明看，本文件重点是：定义一个函数,接受2个整数和1个符号作为参数,实现四则运算 + - * /。

> [!abstract] 代码逻辑怎么走
> - 先定义函数，把某段功能封装起来；后面通过函数名加括号调用。
> - 使用条件判断把不同情况分开处理。
> - 通过赋值语句保存中间结果，主要变量包括：`dict_op`、`num1`、`f`、`num2`。

> [!warning] 需要注意的点
> - `input()` 读到的是字符串，做数学计算前要先转换为 `int` 或 `float`。
> - 字典按 key 取值，key 要唯一；遍历键值对时优先想到 `.items()`。

> [!success] 举一反三
> - 可以给输入加合法性检查，例如不能为空、必须是数字、范围必须正确。
> - 可以把同样结构用于学生信息、商品信息、地区数据等 key-value 场景。
> - 可以继续把重复逻辑拆成函数，让主流程只负责调用。

### Day06_new/exercise03.py

```python
"""
定义一个函数,接受一个二维列表作为参数
把二维列表变成一维的新列表,并打印
"""


def my_flatten(lst):
    list_new = []
    for item in lst:
        for sub in item:
            list_new.append(sub)

    list_new = [sub for item in lst for sub in item]
    print(list_new)


list_num = [[1, 2, 3], [4, 5, 6]]
my_flatten(list_num)
```

> [!note] 这份文件实际讲了什么
> - 文件说明/题目写的是：定义一个函数,接受一个二维列表作为参数；把二维列表变成一维的新列表,并打印。
> - 文件中定义了函数：`my_flatten(lst)`。
> - 主要变量/数据名包括：`list_new`、`list_num`。

> [!example] 本文件出现的新代码 / 函数 / 方法
> - 本文件主要是在复习或组合前面已经学过的写法，没有引入需要单独记忆的新函数/方法；重点看它如何把旧知识组合成当前题目。
> - 从原文件注释/说明看，本文件重点是：定义一个函数,接受一个二维列表作为参数；把二维列表变成一维的新列表,并打印。

> [!abstract] 代码逻辑怎么走
> - 先定义函数，把某段功能封装起来；后面通过函数名加括号调用。
> - 使用 `for` 遍历序列或容器，对每个元素执行同样的处理。
> - 通过赋值语句保存中间结果，主要变量包括：`list_new`、`list_num`。

> [!warning] 需要注意的点
> - 列表是可变对象，增删改会直接影响原列表。

> [!success] 举一反三
> - 可以把单个变量升级为列表，批量保存多条数据后统一遍历处理。
> - 可以把循环和条件组合起来做筛选、统计、累加、菜单系统。
> - 可以继续把重复逻辑拆成函数，让主流程只负责调用。

### Day06_old/01_find.py

```python
"""
字符串函数-查找相关
"""
str1 = "Hello WOrld"

# 第一次出现的位置,找不到返回-1
print(str1.find("O"))

# 最后一次出现的位置,找不到返回-1
print(str1.rfind("l"))
```

> [!note] 这份文件实际讲了什么
> - 文件说明/题目写的是：字符串函数-查找相关。
> - 主要变量/数据名包括：`str1`。

> [!example] 本文件出现的新代码 / 函数 / 方法
> - `.find()`：查找子串位置，找不到返回 -1。
> - 从原文件注释/说明看，本文件重点是：字符串函数-查找相关。

> [!abstract] 代码逻辑怎么走
> - 通过赋值语句保存中间结果，主要变量包括：`str1`。

> [!warning] 需要注意的点
> - 读这份代码时，先看变量如何变化，再看最终输出。

> [!success] 举一反三
> - 可以修改示例数据重新运行，观察输出如何变化。

### Day06_old/02_is.py

```python
"""
字符串函数-判断相关
"""
str1 = "Hello"
str2 = "666"
str3 = "999Hello"

# 只包含数字
print(str2.isdigit())
print(str3.isdigit())

# 只包含字母
print(str2.isalpha())
print(str3.isalpha())

# 只包含字母+数字
print(str1.isalnum())
print(str3.isalnum())
print("12He_".isalnum())
```

> [!quote] 相关图示理解
> ![[附件/正式课/Day06_old/内存图.png]]
> 这张图对应 `Day06_old/02_is.py` 的知识点。复盘时重点看变量、对象和值之间的指向关系，再对照上面的代码运行过程。

> [!note] 这份文件实际讲了什么
> - 文件说明/题目写的是：字符串函数-判断相关。
> - 主要变量/数据名包括：`str1`、`str2`、`str3`。

> [!example] 本文件出现的新代码 / 函数 / 方法
> - `.isalpha()`：判断字符串是否只由字母组成。
> - 从原文件注释/说明看，本文件重点是：字符串函数-判断相关。

> [!abstract] 代码逻辑怎么走
> - 通过赋值语句保存中间结果，主要变量包括：`str1`、`str2`、`str3`。

> [!warning] 需要注意的点
> - 读这份代码时，先看变量如何变化，再看最终输出。

> [!success] 举一反三
> - 可以修改示例数据重新运行，观察输出如何变化。

### Day06_old/03_dict.py

```python
"""
字典:
由一系列键值对组成的可变散列容器
键值对: 键:值 键必须是唯一且不可变 值没有限制
散列: 对键的哈希运算 确定在内存中存储的位置
"""
# 1.创建
dict_movie = {
    "name": 749,
    "index": 10086,
    "type": ("动画", "剧情"),
    "year": 2015
}
print(dict_movie)

# 2.添加/修改
# 给字典不存在的键赋值就是添加 存在的键赋值修改
dict_movie["city"] = "中国"
dict_movie["year"] = 2024

dict_movie.update({"index": 555, "director": "导演"})

# 3.删除
del dict_movie["year"]
dict_movie.pop("city", None)
# 删除最后一个
dict_movie.popitem()

# 4.访问
print(dict_movie["name"])
print(dict_movie.get("type"))
print(dict_movie.get("age", "不存在"))

# 5.遍历
# 默认得到的是键
for key in dict_movie:
    print(key, dict_movie.get(key))

# 每个键值
for value in dict_movie.values():
    print(value)

# 键值对组成一个个元组 元组的第一个元素是键 第二个元素是值
for key, value in dict_movie.items():
    print(key, value)
```

> [!note] 这份文件实际讲了什么
> - 文件说明/题目写的是：字典:；由一系列键值对组成的可变散列容器；键值对: 键:值 键必须是唯一且不可变 值没有限制；散列: 对键的哈希运算 确定在内存中存储的位置。
> - 主要变量/数据名包括：`dict_movie`、`dict_movie[...]`。

> [!example] 本文件出现的新代码 / 函数 / 方法
> - `.pop()`：弹出元素；列表按位置，集合随机弹出。
> - `.get()`：按 key 安全取值，可设置默认值。
> - `.values()`：获取字典所有值。
> - 从原文件注释/说明看，本文件重点是：字典:；给字典不存在的键赋值就是添加 存在的键赋值修改。

> [!abstract] 代码逻辑怎么走
> - 使用 `for` 遍历序列或容器，对每个元素执行同样的处理。
> - 通过赋值语句保存中间结果，主要变量包括：`dict_movie`、`dict_movie[...]`。

> [!warning] 需要注意的点
> - 字典按 key 取值，key 要唯一；遍历键值对时优先想到 `.items()`。
> - 列表是可变对象，增删改会直接影响原列表。

> [!success] 举一反三
> - 可以把同样结构用于学生信息、商品信息、地区数据等 key-value 场景。
> - 可以把循环和条件组合起来做筛选、统计、累加、菜单系统。

### Day06_old/04_member.py

```python
"""
成员运算符(list tuple str dict使用)
in 查看一个元素在不在其中 在返回true 反之返回false
not in 查看一个元素不在其中 不在返回true 反之返回false
"""
list1 = [1, 2, 3, 4]
tuple1 = (1, 2, 3, 4)
str1 = "1234"
dict1 = {1: "PHP", "name": 2}

print(1 in list1)
print("4" not in str1)
# 看的键
print(2 in dict1)

"""
身份运算符
比较2个对象是不是同一个对象(内存地址)
is 
"""
a = 1
b = 1
print(a is b)

# 尽管列表一样,但不是同一个内存地址
a = [1, 2, 3]
b = [1, 2, 3]
print(a is b)  # F

a = (1, 2, 3)
b = (1, 2, 3)
print(a is b)  # T

a = [1, 2, 3]
b = [1, 2, 1, 3]
print(a[0] is b[2])  # T
print(b[0] is b[2])  # T
```

> [!note] 这份文件实际讲了什么
> - 文件说明/题目写的是：成员运算符(list tuple str dict使用)；in 查看一个元素在不在其中 在返回true 反之返回false；not in 查看一个元素不在其中 不在返回true 反之返回false。
> - 后续说明/题目还包括：身份运算符；比较2个对象是不是同一个对象(内存地址)；is。
> - 主要变量/数据名包括：`list1`、`tuple1`、`str1`、`dict1`、`a`、`b`。

> [!example] 本文件出现的新代码 / 函数 / 方法
> - 本文件主要是在复习或组合前面已经学过的写法，没有引入需要单独记忆的新函数/方法；重点看它如何把旧知识组合成当前题目。
> - 从原文件注释/说明看，本文件重点是：成员运算符(list tuple str dict使用)；身份运算符。

> [!abstract] 代码逻辑怎么走
> - 通过赋值语句保存中间结果，主要变量包括：`list1`、`tuple1`、`str1`、`dict1`、`a`、`b`。

> [!warning] 需要注意的点
> - `is` 比较对象身份，`==` 比较值是否相等，二者含义不同。
> - 字典按 key 取值，key 要唯一；遍历键值对时优先想到 `.items()`。
> - 列表是可变对象，增删改会直接影响原列表。

> [!success] 举一反三
> - 可以把同样结构用于学生信息、商品信息、地区数据等 key-value 场景。
> - 可以把单个变量升级为列表，批量保存多条数据后统一遍历处理。

### Day06_old/05_derivative.py

```python
"""
字典推导式

字典名= {键:值 for 变量 in 可迭代对象}
字典名= {键:值 for 变量 in 可迭代对象 if 条件}
"""
dict1 = {
    "1001": "Beijing",
    "1002": "Tianjin",
    "1003": "Hebei"
}

dict_new = {value: key for key, value in dict1.items()}
print(dict_new)

dict_new = {value: key for key, value in dict1.items() if key == "1003"}
print(dict_new)
```

> [!note] 这份文件实际讲了什么
> - 文件说明/题目写的是：字典推导式；字典名= {键:值 for 变量 in 可迭代对象}；字典名= {键:值 for 变量 in 可迭代对象 if 条件}。
> - 主要变量/数据名包括：`dict1`、`dict_new`。

> [!example] 本文件出现的新代码 / 函数 / 方法
> - 本文件主要是在复习或组合前面已经学过的写法，没有引入需要单独记忆的新函数/方法；重点看它如何把旧知识组合成当前题目。
> - 从原文件注释/说明看，本文件重点是：字典推导式；字典名= {键:值 for 变量 in 可迭代对象}。

> [!abstract] 代码逻辑怎么走
> - 通过赋值语句保存中间结果，主要变量包括：`dict1`、`dict_new`。

> [!warning] 需要注意的点
> - 字典按 key 取值，key 要唯一；遍历键值对时优先想到 `.items()`。

> [!success] 举一反三
> - 可以把同样结构用于学生信息、商品信息、地区数据等 key-value 场景。

### Day06_old/06_nesting.py

```python
"""
容器嵌套
"""
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
print(list_movie[0]["actor"][1])

# 2.打印出所有的电影的类型 type
for item in list_movie:
    for sub_item in item["type"]:
        print(sub_item)
```

> [!note] 这份文件实际讲了什么
> - 文件说明/题目写的是：容器嵌套。
> - 主要变量/数据名包括：`list_movie`。

> [!example] 本文件出现的新代码 / 函数 / 方法
> - 本文件主要是在复习或组合前面已经学过的写法，没有引入需要单独记忆的新函数/方法；重点看它如何把旧知识组合成当前题目。

> [!abstract] 代码逻辑怎么走
> - 使用 `for` 遍历序列或容器，对每个元素执行同样的处理。
> - 通过赋值语句保存中间结果，主要变量包括：`list_movie`。

> [!warning] 需要注意的点
> - 字典按 key 取值，key 要唯一；遍历键值对时优先想到 `.items()`。
> - 列表是可变对象，增删改会直接影响原列表。

> [!success] 举一反三
> - 可以把同样结构用于学生信息、商品信息、地区数据等 key-value 场景。
> - 可以把单个变量升级为列表，批量保存多条数据后统一遍历处理。
> - 可以把循环和条件组合起来做筛选、统计、累加、菜单系统。

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

> [!note] 这份文件实际讲了什么
> - 文件说明/题目写的是：运行文件 显示数字服务菜单；1.添加商品；2.显示所有商品；3.修改商品；4.删除商品。

> [!example] 本文件出现的新代码 / 函数 / 方法
> - 本文件主要是在复习或组合前面已经学过的写法，没有引入需要单独记忆的新函数/方法；重点看它如何把旧知识组合成当前题目。

> [!abstract] 代码逻辑怎么走
> - 这份代码主要是顺序执行：先准备数据，再调用函数或输出结果。

> [!warning] 需要注意的点
> - 读这份代码时，先看变量如何变化，再看最终输出。

> [!success] 举一反三
> - 可以修改示例数据重新运行，观察输出如何变化。

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
list_goods = []
while True:
    # 显示菜单
    print("按1键添加商品")
    print("按2键显示所有商品")
    print("按3键修改商品")
    print("按4键删除商品")
    print("按5键退出管理系统")

    # 选择菜单
    choose_number = input("请输入服务数字：")
    if choose_number == "1":
        id = input("请输入商品id:").replace(" ", "")
        title = input("请输入商品标题:").replace(" ", "")
        price = input("请输入商品价格:").replace(" ", "")


        dict_goods = {
            "id": id,
            "title": title,
            "price": price
        }
        list_goods.append(dict_goods)
        print(list_goods)
    elif choose_number == "2":
        if list_goods:
            for item in list_goods:
                print(f"ID:{item['id']},标题:{item['title']},价格{item['price']}")
        else:
            print("暂无商品~")
    elif choose_number == "3":
        print("修改")
    elif choose_number == "4":
        print("删除")
    elif choose_number == "5":
        print("Bye~")
        break
    else:
        print("暂无此服务!")
```

> [!note] 这份文件实际讲了什么
> - 文件说明/题目写的是：电商后台管理系统V1；运行文件 显示数字服务菜单；1.添加商品；2.显示所有商品；3.修改商品。
> - 主要变量/数据名包括：`list_goods`、`choose_number`、`id`、`title`、`price`、`dict_goods`。

> [!example] 本文件出现的新代码 / 函数 / 方法
> - 本文件主要是在复习或组合前面已经学过的写法，没有引入需要单独记忆的新函数/方法；重点看它如何把旧知识组合成当前题目。

> [!abstract] 代码逻辑怎么走
> - 使用 `while` 形成循环，循环内部根据输入或条件决定是否继续。
> - 使用 `for` 遍历序列或容器，对每个元素执行同样的处理。
> - 使用条件判断把不同情况分开处理。
> - 通过赋值语句保存中间结果，主要变量包括：`list_goods`、`choose_number`、`id`、`title`、`price`、`dict_goods`。

> [!warning] 需要注意的点
> - `input()` 读到的是字符串，做数学计算前要先转换为 `int` 或 `float`。
> - `while` 循环要保证循环条件会发生变化，否则可能死循环。
> - `break` 只结束当前这一层循环。
> - 字典按 key 取值，key 要唯一；遍历键值对时优先想到 `.items()`。
> - 列表是可变对象，增删改会直接影响原列表。

> [!success] 举一反三
> - 可以给输入加合法性检查，例如不能为空、必须是数字、范围必须正确。
> - 可以把同样结构用于学生信息、商品信息、地区数据等 key-value 场景。
> - 可以把单个变量升级为列表，批量保存多条数据后统一遍历处理。

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

> [!info] 课堂文本/作业说明
> - 作业:
> - 1.完成今日代码
> - 2.提前向下预习 --> 容器类型(函数)
> - 3.完成EShopManagerV1代码
> - ①完成修改功能
> - ②完成删除功能
> - ③加入数据验证
> - a.用户输入的内容不能为空

### Day06_old/HomeWork/HomeWork01.py

```python
"""
把字符串中的每个单词,反转输出
Just do it  ==> Tsuj Od Ti
"""
str1 = "Just do it"
print(str1.split())

list_new = []
# 遍历split()得到的列表
for item in str1.split():
    # 把每个元素翻转且首字母大写后存入新列表
    list_new.append(item[::-1].title())
# join拼接元素得到字符串
print(" ".join(list_new))

print(" ".join([item[::-1].title() for item in str1.split()]))
```

> [!note] 这份文件实际讲了什么
> - 文件说明/题目写的是：把字符串中的每个单词,反转输出；Just do it  ==> Tsuj Od Ti。
> - 主要变量/数据名包括：`str1`、`list_new`。

> [!example] 本文件出现的新代码 / 函数 / 方法
> - 本文件主要是在复习或组合前面已经学过的写法，没有引入需要单独记忆的新函数/方法；重点看它如何把旧知识组合成当前题目。
> - 从原文件注释/说明看，本文件重点是：把字符串中的每个单词,反转输出；遍历split()得到的列表。

> [!abstract] 代码逻辑怎么走
> - 使用 `for` 遍历序列或容器，对每个元素执行同样的处理。
> - 通过赋值语句保存中间结果，主要变量包括：`str1`、`list_new`。

> [!warning] 需要注意的点
> - 列表是可变对象，增删改会直接影响原列表。
> - 字符串方法通常返回新字符串，不会原地修改原字符串。

> [!success] 举一反三
> - 可以把单个变量升级为列表，批量保存多条数据后统一遍历处理。
> - 可以把循环和条件组合起来做筛选、统计、累加、菜单系统。

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

> [!note] 这份文件实际讲了什么
> - 文件说明/题目写的是：列表推导式；[ 变量操作 for 变量 in 可迭代对象]；[ 变量操作 for 变量 in 可迭代对象 if 条件；深浅拷贝:；浅拷贝:切片 复制浅层数据, 共享深层数据。

> [!example] 本文件出现的新代码 / 函数 / 方法
> - 本文件主要是在复习或组合前面已经学过的写法，没有引入需要单独记忆的新函数/方法；重点看它如何把旧知识组合成当前题目。
> - 从原文件注释/说明看，本文件重点是：列表推导式；深浅拷贝:。

> [!abstract] 代码逻辑怎么走
> - 这份代码主要是顺序执行：先准备数据，再调用函数或输出结果。

> [!warning] 需要注意的点
> - 读这份代码时，先看变量如何变化，再看最终输出。

> [!success] 举一反三
> - 可以修改示例数据重新运行，观察输出如何变化。

### Day06_old/exercise01.py

```python
"""
编写一段程序,得到以下结果
["apple", "orange", "banana", "pear", "grape"]
"""
str1 = "apple,orange;banana | pear grape"

# 思路：遍历字符串每个元素,判断,是字母就拼接到新的字符串中,不是字符就拼接空格,然后使用split分割,分割后变成列表
str_new = ""
for char in str1:
    if char.isalpha():
        str_new += char
    else:
        str_new += " "

print(str_new.split())

# if三元表达式写法
# true_val if 条件 else false_vale
# print(666) if 1 == 1 else print("我丢")

# 推导式
# 思路:遍历字符串每个元素,判断是字母存在列表中,不是字母就存成空格在列表中,然后join连接列表中的每个字符形成新的字符串,最后使用split分割,分割后变成列表
print([char for char in str1])
print([char if char.isalpha() else " " for char in str1])
print("".join([char if char.isalpha() else " " for char in str1]))
print(
    "".join(
        [
            char if char.isalpha() else " "
            for char in str1
        ]
    ).split()
)
```

> [!note] 这份文件实际讲了什么
> - 文件说明/题目写的是：编写一段程序,得到以下结果；["apple", "orange", "banana", "pear", "grape"]。
> - 主要变量/数据名包括：`str1`、`str_new`。

> [!example] 本文件出现的新代码 / 函数 / 方法
> - 本文件主要是在复习或组合前面已经学过的写法，没有引入需要单独记忆的新函数/方法；重点看它如何把旧知识组合成当前题目。
> - 从原文件注释/说明看，本文件重点是：思路：遍历字符串每个元素,判断,是字母就拼接到新的字符串中,不是字符就拼接空格,然后使用split分割,分割后变成列表；推导式。

> [!abstract] 代码逻辑怎么走
> - 使用 `for` 遍历序列或容器，对每个元素执行同样的处理。
> - 使用条件判断把不同情况分开处理。
> - 通过赋值语句保存中间结果，主要变量包括：`str1`、`str_new`。

> [!warning] 需要注意的点
> - 字符串方法通常返回新字符串，不会原地修改原字符串。

> [!success] 举一反三
> - 可以把循环和条件组合起来做筛选、统计、累加、菜单系统。

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
dict_area = {
    "region": "湾湾",
    "new": 150,
    "now": 652
}
dict_area["new"] += 100

dict_area.update({"cure": 0, "total": 2000})
dict_area.update({"cure": dict_area.get("cure") + 20})

del dict_area["new"]

for key, value in dict_area.items():
    print(key, value)
```

> [!note] 这份文件实际讲了什么
> - 文件说明/题目写的是：创建字典,存储受感染地区的名称,新增感染人数,现有感染人数；感染人数新增100人；增加治愈人数与累积感染人数 2000人；治愈人数新增20人；删除新增感人人数。
> - 主要变量/数据名包括：`dict_area`、`dict_area[...]`。

> [!example] 本文件出现的新代码 / 函数 / 方法
> - 本文件主要是在复习或组合前面已经学过的写法，没有引入需要单独记忆的新函数/方法；重点看它如何把旧知识组合成当前题目。
> - 从原文件注释/说明看，本文件重点是：创建字典,存储受感染地区的名称,新增感染人数,现有感染人数；输出字典所有的信息。

> [!abstract] 代码逻辑怎么走
> - 使用 `for` 遍历序列或容器，对每个元素执行同样的处理。
> - 通过赋值语句保存中间结果，主要变量包括：`dict_area`、`dict_area[...]`。

> [!warning] 需要注意的点
> - 字典按 key 取值，key 要唯一；遍历键值对时优先想到 `.items()`。

> [!success] 举一反三
> - 可以把同样结构用于学生信息、商品信息、地区数据等 key-value 场景。
> - 可以把循环和条件组合起来做筛选、统计、累加、菜单系统。

### Day06_old/exercise03.py

```python
"""
颠倒字典的键和值
{"1001": "Beijing"} ==> {"Beijing": "1001"}
"""

dict1 = {
    "1001": "Beijing",
    "1002": "Tianjin",
    "1003": "Hebei"
}

dict_new = {}

for key, value in dict1.items():
    dict_new[value] = key
    dict_new.update({value:key})
print(dict_new)
```

> [!note] 这份文件实际讲了什么
> - 文件说明/题目写的是：颠倒字典的键和值；{"1001": "Beijing"} ==> {"Beijing": "1001"}。
> - 主要变量/数据名包括：`dict1`、`dict_new`、`dict_new[...]`。

> [!example] 本文件出现的新代码 / 函数 / 方法
> - 本文件主要是在复习或组合前面已经学过的写法，没有引入需要单独记忆的新函数/方法；重点看它如何把旧知识组合成当前题目。
> - 从原文件注释/说明看，本文件重点是：颠倒字典的键和值。

> [!abstract] 代码逻辑怎么走
> - 使用 `for` 遍历序列或容器，对每个元素执行同样的处理。
> - 通过赋值语句保存中间结果，主要变量包括：`dict1`、`dict_new`、`dict_new[...]`。

> [!warning] 需要注意的点
> - 字典按 key 取值，key 要唯一；遍历键值对时优先想到 `.items()`。

> [!success] 举一反三
> - 可以把同样结构用于学生信息、商品信息、地区数据等 key-value 场景。
> - 可以把循环和条件组合起来做筛选、统计、累加、菜单系统。

### Day06_old/exercise04.py

```python
"""
给定一个字符串
abcacbbc  ==> a2b3c3
只允许使用items 或者 isalpha 函数 其他函数不允许
"""
str1 = "abcacbbc"

dict_char = {}
for char in str1:
    if char in dict_char:
        dict_char[char] += 1
    else:
        dict_char[char] = 1
    print(dict_char)

output = ""
for char, count in dict_char.items():
    # print(f"{char}{count}",end="")
    output += f"{char}{count}"

print(output)
```

> [!note] 这份文件实际讲了什么
> - 文件说明/题目写的是：给定一个字符串；abcacbbc  ==> a2b3c3；只允许使用items 或者 isalpha 函数 其他函数不允许。
> - 主要变量/数据名包括：`str1`、`dict_char`、`dict_char[...]`、`output`。

> [!example] 本文件出现的新代码 / 函数 / 方法
> - 本文件主要是在复习或组合前面已经学过的写法，没有引入需要单独记忆的新函数/方法；重点看它如何把旧知识组合成当前题目。
> - 从原文件注释/说明看，本文件重点是：给定一个字符串；只允许使用items 或者 isalpha 函数 其他函数不允许。

> [!abstract] 代码逻辑怎么走
> - 使用 `for` 遍历序列或容器，对每个元素执行同样的处理。
> - 使用条件判断把不同情况分开处理。
> - 通过赋值语句保存中间结果，主要变量包括：`str1`、`dict_char`、`dict_char[...]`、`output`。

> [!warning] 需要注意的点
> - 字典按 key 取值，key 要唯一；遍历键值对时优先想到 `.items()`。

> [!success] 举一反三
> - 可以把同样结构用于学生信息、商品信息、地区数据等 key-value 场景。
> - 可以把循环和条件组合起来做筛选、统计、累加、菜单系统。

## 总结

> [!summary] 总结
> - **今天的核心任务**：学习字符串查找、判断、成员运算和身份比较。；学习字典的创建、读取、修改、遍历，以及字典推导式。；学习容器嵌套，用列表和字典组织多条复杂数据。
> - **真实文件里的练习/主题**：函数(组织代码的一种方式)；函数结合字典；电商后台管理系统V1；②字符串:Just do it ==> tsuJ od ti；①推导式:找出在第一个字典中存在，在第二个字典中不存在的键值对；字典；两数之和；定义一个函数,接受2个整数和1个符号作为参数,实现四则运算 + - * /。
>
> **新学代码怎么理解**
> - 字典 `{key: value}`：用键值对描述结构化数据。
> - **.isdigit()**：判断字符串是否全是数字，常用于输入合法性校验。
> - **.update()**：更新字典内容，也能用于集合批量添加。
> - **.split()**：把字符串拆成列表，适合处理按空格或符号分隔的数据。
> - **字典推导式**：字典推导式把“遍历并生成字典”的过程写得更简洁。
> - **.items()**：把字典键和值一起取出，适合 `for key, value in dict.items()` 这种遍历。
> - **.find()**：查找子串位置，找不到返回 -1。
> - `.isalpha()`：判断字符串是否只由字母组成。
> - **.pop()**：弹出元素；列表可按位置弹出，集合弹出则无固定顺序。
> - **.get()**：安全按 key 取值，key 不存在时可以返回默认值。
>
> **复盘建议**
> - 先看每份文件的三引号说明或注释，判断题目要解决什么问题。
> - 再看本文件真正新增的函数/方法，弄清楚它接收什么、返回什么、是否会修改原对象。
> - 最后把代码逻辑按“输入/准备数据 -> 分支或循环处理 -> 输出/返回结果”复述一遍。
