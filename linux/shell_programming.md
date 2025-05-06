# Shell编程学习指南

## 要求
1. 知道如何执行shell程序
2. 在shell脚本中要体现条件控制(如if结构和条件分支)
3. 在shell脚本中要体现循环(for, while和until循环)
4. 掌握shell程序的调试

## 评分标准
所写程序代码，不符合下列要求的扣1-20分：
1. 有效语句不少于20行(符合编程规范)
2. if语句不少于4个
3. 循环嵌套不少于1层

## 1. Shell程序执行方法

### 创建Shell脚本
首先创建一个文本文件，扩展名为`.sh`，例如`myscript.sh`。文件的第一行应该是shebang行，指定使用的shell：

```bash
#!/bin/bash
```

### 赋予执行权限
使用chmod命令赋予脚本执行权限：

```bash
chmod +x myscript.sh
```

### 执行Shell脚本的方法
有多种方式可以执行Shell脚本：

1. 使用绝对或相对路径执行：
```bash
./myscript.sh
/path/to/myscript.sh
```

2. 使用bash命令执行：
```bash
bash myscript.sh
```

3. 使用source命令在当前shell环境中执行：
```bash
source myscript.sh
. myscript.sh  # 简写形式
```

## 2. Shell脚本示例

下面是一个综合示例，包含条件控制、循环和调试技术的Shell脚本。此脚本满足评分标准的所有要求：
- 有效语句超过20行
- 包含4个以上if语句
- 包含至少1层循环嵌套

```bash
#!/bin/bash

# 启用调试模式
# set -x

# 函数定义：检查文件是否存在
check_file() {
    local filename="$1"
    if [ -f "$filename" ]; then
        echo "文件 $filename 存在"
        return 0
    else
        echo "文件 $filename 不存在"
        return 1
    fi
}

# 函数定义：计算两个数字的和
add_numbers() {
    local num1="$1"
    local num2="$2"
    echo $((num1 + num2))
}

# 变量定义
username="user1"
password="pass123"
max_attempts=3
current_attempts=0
files_to_check=("file1.txt" "file2.txt" "file3.txt" "file4.txt")
numbers=(1 2 3 4 5 6 7 8 9 10)

# 第一个if语句：检查用户认证
echo "用户认证检查："
if [ "$username" = "user1" ] && [ "$password" = "pass123" ]; then
    echo "认证成功！欢迎 $username"
else
    echo "认证失败！用户名或密码错误"
    exit 1
fi

# 第二个if语句：检查目录是否存在，不存在则创建
echo -e "\n目录检查："
directory="testdir"
if [ ! -d "$directory" ]; then
    echo "目录 $directory 不存在，正在创建..."
    mkdir -p "$directory"
    if [ $? -eq 0 ]; then
        echo "目录创建成功"
    else
        echo "目录创建失败"
        exit 2
    fi
else
    echo "目录 $directory 已存在"
fi

# 第三个if语句：使用case进行多条件分支
echo -e "\n系统信息检查："
os_type=$(uname)
case "$os_type" in
    "Linux")
        echo "当前系统是 Linux"
        ;;
    "Darwin")
        echo "当前系统是 macOS"
        ;;
    "MINGW"*|"CYGWIN"*)
        echo "当前系统是 Windows"
        ;;
    *)
        echo "未知系统类型: $os_type"
        ;;
esac

# for循环：检查文件列表
echo -e "\n文件检查："
for file in "${files_to_check[@]}"; do
    # 第四个if语句：在循环中使用if
    check_file "$directory/$file"
    if [ $? -eq 0 ]; then
        echo "处理文件 $file..."
    else
        echo "创建空文件 $file..."
        touch "$directory/$file"
    fi
done

# while循环：模拟登录尝试
echo -e "\n登录尝试模拟："
while [ $current_attempts -lt $max_attempts ]; do
    current_attempts=$((current_attempts + 1))
    echo "尝试 $current_attempts/$max_attempts"
    
    # 第五个if语句：在while循环中使用if
    if [ $current_attempts -eq $max_attempts ]; then
        echo "达到最大尝试次数"
        break
    else
        echo "还有 $((max_attempts - current_attempts)) 次尝试机会"
    fi
done

# 循环嵌套：外层for循环，内层while循环
echo -e "\n嵌套循环示例 - 九九乘法表："
for i in {1..9}; do
    j=1
    while [ $j -le $i ]; do
        printf "%d×%d=%-4d" $j $i $((j * i))
        j=$((j + 1))
    done
    echo ""
done

# until循环：直到条件为真才停止
echo -e "\nuntil循环示例："
counter=10
until [ $counter -le 0 ]; do
    echo "倒计时: $counter"
    counter=$((counter - 2))
done

# 数组操作和循环
echo -e "\n数组操作："
sum=0
for num in "${numbers[@]}"; do
    # 第六个if语句：检查是否为偶数
    if [ $((num % 2)) -eq 0 ]; then
        echo "$num 是偶数"
        sum=$((sum + num))
    else
        echo "$num 是奇数"
    fi
done
echo "所有偶数的和为: $sum"

# 使用函数
echo -e "\n函数调用示例："
result=$(add_numbers 15 27)
echo "15 + 27 = $result"

# 第七个if语句：检查结果
if [ $result -gt 40 ]; then
    echo "结果大于40"
else
    echo "结果小于或等于40"
fi

echo -e "\n脚本执行完成！"
exit 0
```

## 3. Shell程序调试技术

Shell脚本提供了多种调试选项，可以帮助找出脚本中的错误：

### 使用选项启用调试

1. 在脚本中使用 `set -x` 启用调试模式，显示每条命令及其参数：
```bash
#!/bin/bash
set -x  # 启用调试
# 脚本内容
set +x  # 禁用调试
```

2. 使用 `set -e` 使脚本在遇到错误时立即退出：
```bash
#!/bin/bash
set -e  # 遇到错误立即退出
# 脚本内容
```

3. 使用 `set -v` 显示读取的每一行：
```bash
#!/bin/bash
set -v  # 显示读取的每一行
# 脚本内容
```

### 在执行时启用调试

在执行脚本时可以启用调试：

```bash
bash -x myscript.sh  # 启用调试模式
bash -e myscript.sh  # 遇到错误立即退出
bash -v myscript.sh  # 显示读取的每一行
```

### 部分调试

可以只调试脚本的特定部分：

```bash
#!/bin/bash
# 正常执行部分
set -x  # 开始调试
# 需要调试的部分
set +x  # 结束调试
# 继续正常执行
```

### 使用echo进行简单调试

在关键位置添加echo语句，输出变量值和执行流程：

```bash
echo "DEBUG: 变量值为 $variable"
```

### 使用trap捕获信号

使用trap命令可以捕获信号并执行相应的操作：

```bash
trap 'echo "脚本在第 $LINENO 行被中断"' ERR
```

## 4. 实际应用示例

以下是一些Shell脚本的实际应用场景：

1. 系统维护脚本
2. 自动备份脚本
3. 日志分析脚本
4. 批量文件处理
5. 服务监控脚本

## 5. 练习

1. 修改上面的示例脚本，添加更多的条件判断
2. 实现一个文件备份脚本，包含错误处理
3. 编写一个系统监控脚本，定期检查系统资源使用情况
4. 创建一个批量文件重命名脚本，使用循环和条件判断

## 6. 注意事项

1. Shell脚本对空格敏感，特别是在条件测试中
2. 变量使用前最好用双引号括起来，避免空值和空格问题
3. 使用 `$?` 检查上一个命令的执行状态
4. 养成良好的注释习惯，提高脚本可读性
5. 对于复杂任务，考虑使用Python等更强大的语言

## 7. 参考资料

- [Bash Reference Manual](https://www.gnu.org/software/bash/manual/bash.html)
- [Advanced Bash-Scripting Guide](https://tldp.org/LDP/abs/html/)
- [Shell Style Guide](https://google.github.io/styleguide/shellguide.html)
