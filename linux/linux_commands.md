# Linux平台基本命令学习

## 掌握LINUX平台下的基本命令

### 要求
1. 尽可能的多测试LINUX平台的各种命令
2. 学习使用管道符组合使用命令

### 评分标准
实验的命令必须有运行结果截图，命令不少于25个

## 基本命令列表及用法

### 1. `ls` - 列出目录内容
```bash
ls                  # 列出当前目录文件
ls -l               # 以长格式列出文件详细信息
ls -a               # 显示所有文件（包括隐藏文件）
ls -lh              # 以人类可读的方式显示文件大小
```

### 2. `cd` - 切换目录
```bash
cd /home            # 切换到/home目录
cd ~                # 切换到用户主目录
cd ..               # 切换到上一级目录
cd -                # 切换到上一个工作目录
```

### 3. `pwd` - 显示当前工作目录
```bash
pwd                 # 显示当前完整路径
```

### 4. `mkdir` - 创建目录
```bash
mkdir test          # 创建test目录
mkdir -p a/b/c      # 创建多级目录
```

### 5. `rm` - 删除文件或目录
```bash
rm file.txt         # 删除文件
rm -r directory     # 递归删除目录及其内容
rm -f file.txt      # 强制删除文件，不提示
```

### 6. `cp` - 复制文件或目录
```bash
cp file1 file2      # 将file1复制为file2
cp -r dir1 dir2     # 递归复制目录
```

### 7. `mv` - 移动或重命名文件
```bash
mv file1 file2      # 将file1重命名为file2
mv file dir/        # 将文件移动到目录中
```

### 8. `cat` - 查看文件内容
```bash
cat file.txt        # 显示文件内容
cat -n file.txt     # 显示行号
```

### 9. `grep` - 文本搜索
```bash
grep "text" file.txt        # 在文件中搜索文本
grep -r "text" directory    # 递归搜索目录中的文本
grep -i "text" file.txt     # 不区分大小写搜索
```

### 10. `find` - 查找文件
```bash
find . -name "*.txt"        # 在当前目录查找所有.txt文件
find /home -type d -name "test"  # 在/home中查找名为test的目录
find . -type f -mtime -7    # 查找7天内修改的文件
```

### 11. `chmod` - 修改文件权限
```bash
chmod 755 file.txt          # 设置文件权限为rwxr-xr-x
chmod +x script.sh          # 添加执行权限
```

### 12. `chown` - 修改文件所有者
```bash
chown user:group file.txt   # 修改文件的所有者和组
```

### 13. `ps` - 显示进程状态
```bash
ps                  # 显示当前终端的进程
ps aux              # 显示所有进程详细信息
```

### 14. `top` - 动态显示进程信息
```bash
top                 # 实时显示系统资源和进程信息
```

### 15. `kill` - 终止进程
```bash
kill PID            # 终止指定PID的进程
kill -9 PID         # 强制终止进程
```

### 16. `df` - 显示磁盘空间使用情况
```bash
df -h               # 以人类可读的方式显示磁盘使用情况
```

### 17. `du` - 显示目录空间使用情况
```bash
du -sh directory    # 显示目录的总大小
```

### 18. `tar` - 文件归档
```bash
tar -cvf archive.tar files/  # 创建归档
tar -xvf archive.tar         # 解压归档
tar -czvf archive.tar.gz files/  # 创建gzip压缩归档
```

### 19. `wget` - 下载文件
```bash
wget URL            # 从网络下载文件
```

### 20. `curl` - 传输数据
```bash
curl URL            # 获取网页内容
curl -O URL         # 下载文件并保存为原始文件名
```

### 21. `history` - 显示命令历史
```bash
history             # 显示命令历史记录
!n                  # 执行历史记录中的第n条命令
```

### 22. `echo` - 输出文本
```bash
echo "Hello World"  # 输出文本
echo $PATH          # 输出环境变量
```

### 23. `man` - 显示手册页
```bash
man ls              # 显示ls命令的手册
```

### 24. `head` - 显示文件开头
```bash
head file.txt       # 显示文件前10行
head -n 5 file.txt  # 显示文件前5行
```

### 25. `tail` - 显示文件结尾
```bash
tail file.txt       # 显示文件后10行
tail -f log.txt     # 实时查看文件更新
```

### 26. `wc` - 统计文件
```bash
wc file.txt         # 显示行数、单词数和字节数
wc -l file.txt      # 只显示行数
```

### 27. `sort` - 排序文件内容
```bash
sort file.txt       # 按字母顺序排序文件
sort -n file.txt    # 按数字顺序排序
```

### 28. `uniq` - 报告或忽略重复行
```bash
uniq file.txt       # 删除重复行（需要先排序）
```

### 29. `diff` - 比较文件差异
```bash
diff file1 file2    # 比较两个文件的差异
```

### 30. `ssh` - 安全登录远程主机
```bash
ssh user@hostname   # 登录远程主机
```

## 管道符组合命令示例

管道符（|）可以将一个命令的输出作为另一个命令的输入，实现命令的组合使用。

### 1. 查找包含特定文本的文件并计数
```bash
grep -r "text" directory | wc -l
```

### 2. 查看最常用的10个命令
```bash
history | awk '{print $2}' | sort | uniq -c | sort -rn | head -10
```

### 3. 查看当前目录下最大的5个文件
```bash
du -sh * | sort -rh | head -5
```

### 4. 查找并杀死特定进程
```bash
ps aux | grep "process_name" | grep -v grep | awk '{print $2}' | xargs kill -9
```

### 5. 统计文件中某个单词出现的次数
```bash
cat file.txt | grep -o "word" | wc -l
```

### 6. 查看系统中占用内存最多的5个进程
```bash
ps aux | sort -nk 4 | tail -5
```

### 7. 查看系统中占用CPU最多的5个进程
```bash
ps aux | sort -nk 3 | tail -5
```

### 8. 查找最近修改的文件并按时间排序
```bash
find . -type f -mtime -7 | xargs ls -lt | head
```

### 9. 统计当前目录下各类型文件的数量
```bash
find . -type f | grep -o "\.[^\.]*$" | sort | uniq -c | sort -nr
```

### 10. 查找并替换文件中的文本
```bash
grep -l "old_text" *.txt | xargs sed -i 's/old_text/new_text/g'
```

## 注意事项

1. 在执行删除、修改等危险操作前，请确认命令的正确性
2. 使用管道符组合命令时，注意每个命令的输入输出格式
3. 对于不熟悉的命令，建议先查看其手册（使用`man`命令）
4. 在生产环境中执行命令前，建议先在测试环境中验证

## 实验结果

请在此处添加各命令的运行结果截图。
