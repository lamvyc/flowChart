#!/usr/bin/env python3
"""
基础 Python 语法演示脚本
========================
运行方式（确保已激活虚拟环境或安装好 Python 3）：

    python learn_basics.py

脚本覆盖以下内容：
1. 变量与基本数据类型
2. 列表（数组）
3. 字典（对象 / Map）
4. 条件判断与循环
5. 函数定义与调用
6. 类与对象（面向对象）
7. 常用标准库导入
8. 异常处理
9. 文件读写

执行后会在终端打印示例输出，并生成 `sample.txt` 文件。
"""

# 1. 变量与基本类型 -----------------------------------------------------------
print("\n# 1. 变量与基本类型")

x = 42                      # 整数 int
name = "Alice"              # 字符串 str
pi = 3.14159                # 浮点数 float
is_active = True            # 布尔 bool

print("整数 x =", x)
print("字符串 name =", name)
print("浮点数 pi =", pi)
print("布尔 is_active =", is_active)

# 2. 列表（数组） --------------------------------------------------------------
print("\n# 2. 列表（数组）")

nums = [1, 2, 3, 4, 5]
print("nums 列表:", nums)
print("nums 第一个元素:", nums[0])
print("nums 所有元素 * 2:", [n * 2 for n in nums])  # 列表推导式（类似 JS map）

# 3. 字典（对象 / Map） --------------------------------------------------------
print("\n# 3. 字典（对象 / Map）")

person = {"name": "Bob", "age": 30}
print("person 字典:", person)
print("访问 person['name'] ->", person["name"])

# 4. 条件与循环 ---------------------------------------------------------------
print("\n# 4. 条件与循环")

for n in nums:
    if n % 2 == 0:
        print(n, "是偶数")
    else:
        print(n, "是奇数")

# 5. 函数 ---------------------------------------------------------------------
print("\n# 5. 函数")

def greet(who: str = "world") -> str:
    """返回一段问候语，类似 JS 的 arrow function。"""
    return f"Hello, {who}!"

print(greet())
print(greet("Python"))

# 6. 类与对象（面向对象） -----------------------------------------------------
print("\n# 6. 类与对象（面向对象）")

class Counter:
    """一个简单的计数器类。"""

    def __init__(self, start: int = 0):
        self.value = start  # 实例属性

    def inc(self) -> None:
        """给计数器 +1"""
        self.value += 1

    def __repr__(self) -> str:  # 调试打印
        return f"<Counter value={self.value}>"

c = Counter()
for _ in range(3):
    c.inc()
print("Counter 当前值:", c.value)

# 7. 常用标准库导入 -----------------------------------------------------------
print("\n# 7. 常用标准库导入")

import math
print("math.sqrt(16) =", math.sqrt(16))

# 8. 错误与异常 ---------------------------------------------------------------
print("\n# 8. 错误与异常")

try:
    1 / 0
except ZeroDivisionError as e:
    print("捕获到异常:", e)

# 9. 文件读写 -----------------------------------------------------------------
print("\n# 9. 文件读写")

file_path = "sample.txt"

with open(file_path, "w", encoding="utf-8") as f:
    f.write("Hello 文件!\n")

with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

print("读取 sample.txt 内容:", content.strip())

print("\n脚本演示结束 ✅") 