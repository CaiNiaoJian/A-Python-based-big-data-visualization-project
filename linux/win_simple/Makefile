# Windows简化版Makefile

# 编译器和选项
CC = g++
CFLAGS = -Wall -std=c++11
LDFLAGS = 

# 源文件和目标文件
SRCS = main.c file_monitor.c
OBJS = $(SRCS:.c=.o)
TARGET = file_monitor.exe

# 默认目标
all: $(TARGET)

# 链接
$(TARGET): $(OBJS)
	$(CC) -o $@ $^ $(LDFLAGS)

# 编译
%.o: %.c
	$(CC) $(CFLAGS) -c $< -o $@

# 清理
clean:
	del /Q $(OBJS) $(TARGET)

# 运行
run: $(TARGET)
	.\$(TARGET) test_dir

# 创建测试目录
test_dir:
	if not exist test_dir mkdir test_dir

.PHONY: all clean run test_dir
