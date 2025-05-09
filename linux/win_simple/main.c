#include "common.h"

// 全局变量，用于控制程序运行
int running = 1;

// Console handler function
BOOL WINAPI console_handler(DWORD sig) {
    printf("\nReceived signal %lu, exiting...\n", sig);
    running = 0;
    return TRUE;
}

int main(int argc, char* argv[]) {
    char monitor_path[MAX_PATH_LEN];
    file_monitor* monitor;

    // 设置控制台处理函数，捕获Ctrl+C等信号
    SetConsoleCtrlHandler(console_handler, TRUE);

    // Check command line arguments
    if (argc < 2) {
        // If no path is provided, use current directory
        strcpy(monitor_path, ".");
        printf("No directory specified, using current directory\n");
    } else {
        strncpy(monitor_path, argv[1], MAX_PATH_LEN - 1);
    }

    // Initialize file monitor
    monitor = init_file_monitor(monitor_path);
    if (!monitor) {
        printf("Failed to initialize file monitor\n");
        return 1;
    }

    // Start monitoring
    if (start_monitoring(monitor) != 0) {
        printf("Failed to start monitoring\n");
        cleanup_monitor(monitor);
        return 1;
    }

    printf("File monitoring system started successfully, press Ctrl+C to exit\n");
    printf("Monitoring directory: %s\n", monitor_path);
    printf("Try creating, modifying, or deleting files in this directory to observe changes\n");

    // 主循环
    while (running) {
        Sleep(1000);  // 1秒
    }

    // Stop monitoring and clean up resources
    printf("Stopping monitoring...\n");
    stop_monitoring(monitor);
    cleanup_monitor(monitor);
    printf("Resources cleaned up\n");

    return 0;
}
