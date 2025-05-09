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

## 精选实用命令集合

以下是20-25条最实用的Linux命令，重点关注管道组合和高效操作，并说明其作用和一般输出结果：

### 1. `find . -name "*.log" -mtime -7 | xargs grep "ERROR"`
**作用**：查找最近7天内修改的所有日志文件中包含ERROR的行  
**输出**：文件名:行号:包含ERROR的内容

### 2. `ps aux | grep java | grep -v grep | awk '{print $2}' | xargs kill -9`
**作用**：查找并强制终止所有Java进程  
**输出**：无输出，但会终止所有匹配的进程

### 3. `du -sh * | sort -rh | head -5`
**作用**：显示当前目录下占用空间最大的5个文件/目录  
**输出**：文件大小和文件名，按大小降序排列

### 4. `find / -type f -size +100M -exec ls -lh {} \;`
**作用**：查找系统中所有大于100MB的文件  
**输出**：文件的详细信息，包括权限、大小、修改时间等

### 5. `netstat -tuln | grep LISTEN`
**作用**：显示所有正在监听的TCP和UDP端口  
**输出**：协议、本地地址、外部地址和连接状态

### 6. `history | awk '{print $2}' | sort | uniq -c | sort -rn | head -10`
**作用**：显示最常用的10个命令  
**输出**：使用次数和命令名称，按使用频率降序排列

### 7. `find . -type f -name "*.txt" -exec sed -i 's/old/new/g' {} \;`
**作用**：在所有txt文件中将"old"替换为"new"  
**输出**：无输出，但会修改所有匹配的文件

### 8. `ls -la | grep ^d | sort -k5 -nr`
**作用**：列出当前目录下所有子目录并按大小排序  
**输出**：目录的详细信息，按大小降序排列

### 9. `cat /var/log/syslog | grep $(date +"%b %d") | grep ERROR`
**作用**：查看今天的系统日志中的错误信息  
**输出**：今天的系统日志中包含ERROR的行

### 10. `ps aux | sort -nk 3 | tail -5`
**作用**：显示CPU占用最高的5个进程  
**输出**：进程详细信息，包括CPU和内存使用率

### 11. `find . -name "*.bak" -o -name "*.tmp" | xargs rm -f`
**作用**：删除所有备份和临时文件  
**输出**：无输出，但会删除所有匹配的文件

### 12. `tar -czvf backup-$(date +%Y%m%d).tar.gz /important/directory`
**作用**：创建带日期的目录备份  
**输出**：压缩过程中处理的文件列表

### 13. `df -h | grep -v tmpfs | sort -k5 -r`
**作用**：显示磁盘使用情况，排除临时文件系统，按使用率排序  
**输出**：文件系统、大小、已用空间、可用空间和使用率

### 14. `grep -r --include="*.php" "function" /var/www | wc -l`
**作用**：统计Web目录下所有PHP文件中函数的数量  
**输出**：一个数字，表示匹配的行数

### 15. `find . -type f -exec chmod 644 {} \; && find . -type d -exec chmod 755 {} \;`
**作用**：递归设置文件和目录的标准权限  
**输出**：无输出，但会修改所有文件和目录的权限

### 16. `ps aux | grep -i memory | awk '{sum+=$6} END {print sum/1024 "MB"}'`
**作用**：计算特定进程组使用的总内存  
**输出**：一个数字，表示总内存使用量（MB）

### 17. `curl -s https://api.example.com/data | jq '.items[] | select(.status=="active")'`
**作用**：获取API数据并过滤出活跃项目  
**输出**：格式化的JSON数据，只包含活跃项目

### 18. `find . -type f -mtime +30 -name "*.log" | xargs tar -czvf old-logs.tar.gz`
**作用**：将30天前的日志文件打包  
**输出**：压缩过程中处理的文件列表

### 19. `cat /etc/passwd | cut -d: -f1,3 | sort -t: -k2 -n`
**作用**：列出所有用户及其UID，按UID排序  
**输出**：用户名和UID，按UID升序排列

### 20. `dmesg | grep -i error | tee system-errors.log`
**作用**：查找内核错误并同时保存到文件  
**输出**：内核日志中包含error的行，同时写入文件

### 21. `watch -n 1 'ps aux | sort -nk 3 | tail -5'`
**作用**：每秒更新显示CPU占用最高的5个进程  
**输出**：实时更新的进程列表

### 22. `find . -name "*.jpg" | xargs -I{} convert {} -resize 50% {}.resized`
**作用**：批量将所有JPG图片调整为原来的50%大小  
**输出**：无输出，但会生成调整大小后的图片

### 23. `ls -la | awk '{total += $5} END {print "Total size: " total/1024/1024 " MB"}'`
**作用**：计算当前目录下所有文件的总大小  
**输出**：一行文本，显示总大小（MB）

### 24. `journalctl -u nginx --since today | grep error | tee -a nginx-errors.log`
**作用**：查看今天的Nginx服务错误并追加到日志文件  
**输出**：今天的Nginx错误日志，同时追加到文件

### 25. `find /var/log -type f -name "*.log" -size +100M -exec ls -lh {} \; | sort -k5hr`
**作用**：查找大于100MB的日志文件并按大小排序  
**输出**：大型日志文件的详细信息，按大小降序排列
