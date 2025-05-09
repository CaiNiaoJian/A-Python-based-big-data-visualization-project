#ifndef COMMON_H
#define COMMON_H

// 包含Windows所需头文件
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <windows.h>
#include <process.h>
#include <time.h>

// 定义常量
#define MAX_PATH_LEN 260
#define MAX_FILENAME 256
#define BUFFER_SIZE 4096

// 文件事件类型
#define FILE_EVENT_CREATED 1
#define FILE_EVENT_DELETED 2
#define FILE_EVENT_MODIFIED 3

// 文件事件结构
typedef struct {
    int event_type;
    char filename[MAX_FILENAME];
} file_event;

// 文件监控结构
typedef struct {
    char path[MAX_PATH_LEN];
    HANDLE dir_handle;
    OVERLAPPED overlapped;
    char buffer[BUFFER_SIZE];
    DWORD bytes_returned;
    int running;
} file_monitor;

// 函数声明
file_monitor* init_file_monitor(const char* path);
int start_monitoring(file_monitor* monitor);
void stop_monitoring(file_monitor* monitor);
void cleanup_monitor(file_monitor* monitor);

#endif /* COMMON_H */
