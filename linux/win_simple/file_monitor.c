#include "common.h"

// 初始化文件监控器
file_monitor* init_file_monitor(const char* path) {
    file_monitor* monitor = (file_monitor*)malloc(sizeof(file_monitor));
    if (!monitor) {
        printf("Memory allocation failed\n");
        return NULL;
    }

    // 初始化结构
    memset(monitor, 0, sizeof(file_monitor));
    strncpy(monitor->path, path, MAX_PATH_LEN - 1);
    monitor->running = 1;

    // 转换路径格式，确保兼容性
    for (int i = 0; monitor->path[i] != '\0'; i++) {
        if (monitor->path[i] == '/') {
            monitor->path[i] = '\\';
        }
    }

    // 初始化监控
    monitor->dir_handle = FindFirstChangeNotification(
        monitor->path,
        TRUE,  // 监控子目录
        FILE_NOTIFY_CHANGE_FILE_NAME |  // 文件创建/删除
        FILE_NOTIFY_CHANGE_DIR_NAME |   // 目录创建/删除
        FILE_NOTIFY_CHANGE_LAST_WRITE   // 文件修改
    );

    if (monitor->dir_handle == INVALID_HANDLE_VALUE) {
        printf("Monitor initialization failed: %lu\n", GetLastError());
        free(monitor);
        return NULL;
    }

    printf("File monitor initialized, watching directory: %s\n", monitor->path);
    return monitor;
}

// 处理文件事件的线程函数
static unsigned __stdcall monitor_thread(void* arg) {
    file_monitor* monitor = (file_monitor*)arg;
    DWORD wait_status;

    printf("Starting to monitor file changes...\n");

    while (monitor->running) {
        // 等待文件变化通知
        wait_status = WaitForSingleObject(monitor->dir_handle, 1000);  // 1秒超时

        if (wait_status == WAIT_OBJECT_0) {
            // 检测到文件变化
            printf("File change detected\n");

            // 在实际应用中，这里应该获取具体的文件名和变化类型
            // 由于Windows API的限制，这需要额外的代码来实现
            // 这里简化处理，只报告有变化发生

            // 继续监控
            if (!FindNextChangeNotification(monitor->dir_handle)) {
                printf("Continue monitoring failed: %lu\n", GetLastError());
                break;
            }
        } else if (wait_status == WAIT_TIMEOUT) {
            // 超时，继续等待
            continue;
        } else {
            // 出错
            printf("Monitoring error: %lu\n", GetLastError());
            break;
        }
    }

    printf("File monitoring thread exited\n");
    return 0;
}

// 开始监控
int start_monitoring(file_monitor* monitor) {
    if (!monitor || monitor->dir_handle == INVALID_HANDLE_VALUE) {
        return -1;
    }

    // 创建监控线程
    HANDLE thread = (HANDLE)_beginthreadex(
        NULL,       // 默认安全属性
        0,          // 默认栈大小
        monitor_thread,
        monitor,
        0,          // 立即运行
        NULL        // 不需要线程ID
    );

    if (thread == NULL) {
        printf("Failed to create monitoring thread\n");
        return -1;
    }

    // 不需要线程句柄，关闭它
    CloseHandle(thread);
    return 0;
}

// 停止监控
void stop_monitoring(file_monitor* monitor) {
    if (monitor) {
        monitor->running = 0;
        // 给线程一些时间退出
        Sleep(1500);
    }
}

// 清理资源
void cleanup_monitor(file_monitor* monitor) {
    if (monitor) {
        if (monitor->dir_handle != INVALID_HANDLE_VALUE) {
            FindCloseChangeNotification(monitor->dir_handle);
        }
        free(monitor);
    }
}
