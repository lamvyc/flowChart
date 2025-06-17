#!/usr/bin/env python3
"""
高级 Python 语法演示脚本
========================
运行方式（确保已激活虚拟环境或安装好 Python 3）：

    python advanced_basics.py

脚本覆盖以下内容：
1. 列表和字典的高级操作
2. 生成器和迭代器
3. 装饰器
4. 上下文管理器
5. 多线程和多进程
6. 正则表达式
7. 网络请求

执行后会在终端打印示例输出。
"""

# 1. 列表和字典的高级操作 ---------------------------------------------------
print("\n# 1. 列表和字典的高级操作")

nums = [5, 2, 9, 1, 5, 6]
sorted_nums = sorted(nums)
print("排序后的 nums:", sorted_nums)

filtered_nums = list(filter(lambda x: x > 3, nums))
print("过滤大于 3 的 nums:", filtered_nums)

# 字典合并
person = {"name": "Alice", "age": 25}
extra_info = {"city": "New York", "job": "Engineer"}
merged_person = {**person, **extra_info}
print("合并后的字典:", merged_person)

# 2. 生成器和迭代器 ---------------------------------------------------------
print("\n# 2. 生成器和迭代器")

def count_up_to(max: int):
    count = 1
    while count <= max:
        yield count
        count += 1

for number in count_up_to(5):
    print("生成器产生:", number)

# 3. 装饰器 -----------------------------------------------------------------
print("\n# 3. 装饰器")

def my_decorator(func):
    def wrapper():
        print("装饰器: 函数调用前")
        func()
        print("装饰器: 函数调用后")
    return wrapper

@my_decorator
def say_hello():
    print("Hello!")

say_hello()

# 4. 上下文管理器 -----------------------------------------------------------
print("\n# 4. 上下文管理器")

class CustomContext:
    def __enter__(self):
        print("进入上下文")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print("退出上下文")

with CustomContext() as ctx:
    print("在上下文中")

# 5. 多线程和多进程 ---------------------------------------------------------
print("\n# 5. 多线程和多进程")

import threading
import time

def worker():
    print("线程开始")
    time.sleep(1)
    print("线程结束")

thread = threading.Thread(target=worker)
thread.start()
thread.join()

# 6. 正则表达式 -------------------------------------------------------------
print("\n# 6. 正则表达式")

import re

text = "The rain in Spain"
match = re.search(r"\bS\w+", text)
print("找到的单词:", match.group())

# 7. 网络请求 ---------------------------------------------------------------
print("\n# 7. 网络请求")

import requests

response = requests.get("https://api.github.com")
print("GitHub API 状态:", response.status_code)

print("\n高级脚本演示结束 ✅") 