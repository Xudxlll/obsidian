# 一、`PyMySQL`

## 1.1 概述

`PyMySQ`L是一个纯`Python`编写的`MySQL`数据库客户端库，它基于`Python`数据库`API`规范

`PyMySQL`允许在`Python`应用程序中连接到`MySQL`数据库，并执行各种数据库操作--如查询、插入、更新等

## 1.2 安装

`Python`解释器版本要求

| `Python`解释器 | 版本     |
| -------------- | -------- |
| `CPython`      | `>=3.7+` |
| `PyPy`         | `>=3.X`  |

`MySQL`服务器版本要求

| `MySQL`服务器 | 版本     |
| ------------- | -------- |
| `MySQL`       | `>=5.7`  |
| `MariaDB`     | `>=10.4` |

```shell

$ sudo pip3 install pymysql

```

## 1.3 `pip3`

`pip3`是`Python 3`的默认包管理器，用于安装、卸载和管理`Python`软件包

# 二、`Connection`对象

```python

pymysql.connections.Connection(
   *, 
   user=None, 
   password='', 
   host=None, 
   database=None, 
   port=0,
   charset=''
)

```

```python

Connect = connect = Connection = connections.Connection

```

● `open`属性

`open`属性返回连接是否打开，其语法结构为：

```python

bool Connection.open

```

● `select_db()`方法

`select_db()`方法用于打开指定数据库，其语法结构为：

```python

Connection.select_db(db)

```

● `set_character_set()`方法

`set_character_set()`方法用于设置数据库的字符集，其语法结构为：

```python

Connection.set_character_set(charset)

```

● `cursor()`方法

`cursor()`方法用于创建游标对象，其语法结构为：

```python

Connection.cursor([Cursor/SSCursor/DictCursor/SSDictCursor])

```

● `Cursor`

与数据库进行交互的基本游标对象。它返回的结果以元组的形式表示

● `SSCursor`

一个不带缓冲的游标对象，主要用于返回大量数据的查询，或者用于与远程服务器的连接，结果以元组的形式表示

● `DictCursor`

一个返回结果为字典形式的游标对象，它会将结果集中的每一行作为一个字典返回

● `SSDictCursor`

一个不带缓冲的游标对象，返回结果为字典形式。它会将结果集中的每一行作为一个字典返回

```python

你可以使用以下示例代码来在PyMySQL中查找记录：

```python
import pymysql

# 创建连接
connection = pymysql.connect(host='localhost',
                             user='username',
                             password='password',
                             database='dbname')

# 创建游标对象
with connection.cursor() as cursor:
    # 执行查询
    sql = "SELECT * FROM your_table WHERE your_condition"
    cursor.execute(sql)
    result = cursor.fetchall()
    for row in result:
        print(row)

# 关闭连接
connection.close()


```

```python


import pymysql

# 创建连接
connection = pymysql.connect(host='localhost',
                             user='username',
                             password='password',
                             database='dbname')

# 创建字典游标对象
with connection.cursor(pymysql.cursors.DictCursor) as cursor:
    # 执行查询
    sql = "SELECT * FROM your_table WHERE your_condition"
    cursor.execute(sql)
    result = cursor.fetchall()
    for row in result:
        print(row)

# 关闭连接
connection.close()

```



# 三、`Cursor`对象

`Cursor`对象称为游标对象，通过游标对象用于与数据库进行交互，执行查询和获取结果

● `execute()`方法

`execute()`方法用于执行`SQL`查询，其语法结构为：

```python

Cursor.execute(query,args=None)

```

如果`args`参数为列表或元素，可通过`%s`作为查询语句中的占位符；如果为字典的话，可通过`%name`作为占位符

● `rowcount`属性

`rowcount`属性用于获取最后一次操作影响的记录数，其语法结构为：

```python

Cursor.rowcount

```

> 如`DQL`中的`SELECT`、`DML`中的`UPDATE`、`INSERT`、`DELETE`等

● `lastrowid`属性

`lastrowid`属性用于获取最后一次插入记录的`ID`，其语法结构为：

```python

Cursor.lastrowid

```

● `fetchone()`方法

`fetchone()`方法用于从结果集中获取下一行数据，并将其作为一个元组返回，其语法结构为：

```python

Cursor.fetchone()

```

如果结果集为空或者已经到达结果集的末尾，`fetchone()`方法将返回`None`

● `fetchmany()`方法

`fetchmany()` 方法用于从结果集中获取指定数量的行数据，并将其作为一个元组列表返回，其语法结构为：

```python

Cursor.fetchmany(size=None)

```

如果结果集为空或者已经到达结果集的末尾，则返回一个空列表

● `fetchall()`方法

`fetchall()` 方法用于从结果集中获取所有行的数据，并将其作为一个元组列表返回，其语法结构为：

```python

Cursor.fetchall()

```

● `close()` 方法

`close()`方法用于关闭游标，其语法结构为：

```python

Cursor.close()

```

