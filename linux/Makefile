# 跨平台Makefile

# 检测操作系统类型
ifeq ($(OS),Windows_NT)
    PLATFORM = WINDOWS
    CC = g++
    CFLAGS = -Wall -std=c++11 -DPLATFORM_WINDOWS -D_WIN32_WINNT=0x0600
    LDFLAGS = -lws2_32 -lpsapi -lwinmm
    RM = del /Q
    TARGET = filesync.exe
else
    PLATFORM = LINUX
    CC = gcc
    CFLAGS = -Wall -DPLATFORM_LINUX
    LDFLAGS = -lpthread
    RM = rm -f
    TARGET = filesync
endif

# 源文件
SRCS = main.c sync.c ipc.c network.c monitor.c
ifeq ($(PLATFORM),WINDOWS)
    SRCS += win_compat.c
endif

# 目标文件
OBJS = $(SRCS:.c=.o)

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
ifeq ($(PLATFORM),WINDOWS)
	$(RM) $(OBJS) $(TARGET)
else
	$(RM) $(OBJS) $(TARGET)
endif

# 运行
run: $(TARGET)
	./$(TARGET) ./test_dir

# 创建测试目录
test_dir:
	mkdir -p test_dir

.PHONY: all clean run test_dir
