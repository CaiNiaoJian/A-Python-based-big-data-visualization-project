#include "common.h"

// 全局变量
int running = 1;
#ifdef PLATFORM_LINUX
int shmid = -1;
int msgid = -1;
int server_fd = -1;
sync_queue *queue = NULL;
pid_t monitor_pid = -1;
pid_t sync_pid = -1;
#else
HANDLE shmid = NULL;
HANDLE msgid = NULL;
HANDLE server_fd = INVALID_HANDLE_VALUE;
sync_queue *queue = NULL;
pid_t monitor_pid = NULL;
pid_t sync_pid = NULL;
#endif

// 信号处理函数
#ifdef PLATFORM_LINUX
void signal_handler(int sig) {
    printf("\n接收到信号 %d，正在清理资源...\n", sig);
    running = 0;
}
#else
BOOL WINAPI win_signal_handler(DWORD sig) {
    printf("\n接收到信号 %lu，正在清理资源...\n", sig);
    running = 0;
    return TRUE;
}
#endif

// 初始化系统
int init_system(const char *directory) {
    // 初始化共享内存
    shmid = init_shared_memory();
    if (shmid == -1) {
        fprintf(stderr, "初始化共享内存失败\n");
        return -1;
    }
    
    // 初始化消息队列
    msgid = init_message_queue();
    if (msgid == -1) {
        fprintf(stderr, "初始化消息队列失败\n");
        return -1;
    }
    
    // 初始化同步队列
    queue = init_sync_queue();
    if (!queue) {
        fprintf(stderr, "初始化同步队列失败\n");
        return -1;
    }
    
    // 初始化服务器
    server_fd = init_server();
    if (server_fd == -1) {
        fprintf(stderr, "初始化服务器失败\n");
        return -1;
    }
    
    // 初始化监控系统
    if (init_monitor_system(directory) == -1) {
        fprintf(stderr, "初始化监控系统失败\n");
        return -1;
    }
    
    printf("系统初始化成功\n");
    return 0;
}

// 创建监控进程
#ifdef PLATFORM_LINUX
pid_t create_monitor_process(const char *directory) {
    pid_t pid = fork();
    
    if (pid < 0) {
        perror("fork");
        return -1;
    } else if (pid == 0) {
        // 子进程
        printf("监控进程启动，监控目录: %s\n", directory);
        
        // 这里应该调用监控函数
        // 为简化示例，这里只是模拟
        while (running) {
            sleep(1);
        }
        
        printf("监控进程退出\n");
        exit(0);
    }
    
    return pid;
}
#else
pid_t create_monitor_process(const char *directory) {
    // Windows下使用线程代替进程
    pthread_t thread;
    watch_dir *dir = malloc(sizeof(watch_dir));
    
    if (!dir) {
        printf("malloc失败\n");
        return NULL;
    }
    
    strncpy(dir->path, directory, PATH_MAX);
    
    // 创建监控线程
    if (pthread_create(&thread, NULL, monitor_directory, dir) != 0) {
        printf("pthread_create失败\n");
        free(dir);
        return NULL;
    }
    
    printf("监控线程启动，监控目录: %s\n", directory);
    return (pid_t)thread;
}
#endif

// 创建同步进程
#ifdef PLATFORM_LINUX
pid_t create_sync_process() {
    pid_t pid = fork();
    
    if (pid < 0) {
        perror("fork");
        return -1;
    } else if (pid == 0) {
        // 子进程
        printf("同步进程启动\n");
        
        // 这里应该调用同步函数
        // 为简化示例，这里只是模拟
        while (running) {
            sleep(1);
        }
        
        printf("同步进程退出\n");
        exit(0);
    }
    
    return pid;
}
#else
// Windows下的同步线程函数
static unsigned __stdcall sync_thread_func(void *arg) {
    printf("同步线程启动\n");
    
    while (running) {
        Sleep(1000); // 1秒
    }
    
    printf("同步线程退出\n");
    return 0;
}

pid_t create_sync_process() {
    // Windows下使用线程代替进程
    HANDLE thread = (HANDLE)_beginthreadex(NULL, 0, sync_thread_func, NULL, 0, NULL);
    
    if (thread == NULL) {
        printf("_beginthreadex失败\n");
        return NULL;
    }
    
    return (pid_t)thread;
}
#endif

// 清理资源
void cleanup() {
#ifdef PLATFORM_LINUX
    // 停止子进程
    if (monitor_pid > 0) {
        kill(monitor_pid, SIGTERM);
        waitpid(monitor_pid, NULL, 0);
    }
    
    if (sync_pid > 0) {
        kill(sync_pid, SIGTERM);
        waitpid(sync_pid, NULL, 0);
    }
    
    // 清理资源
    if (queue) {
        destroy_sync_queue(queue);
    }
    
    if (server_fd != -1) {
        close(server_fd);
    }
    
    // 清理IPC资源
    if (shmid != -1) {
        // 删除共享内存段
    }
    
    if (msgid != -1) {
        // 删除消息队列
    }
#else
    // 停止线程
    if (monitor_pid != NULL) {
        TerminateThread(monitor_pid, 0);
        CloseHandle(monitor_pid);
    }
    
    if (sync_pid != NULL) {
        TerminateThread(sync_pid, 0);
        CloseHandle(sync_pid);
    }
    
    // 清理资源
    if (queue) {
        destroy_sync_queue(queue);
    }
    
    if (server_fd != INVALID_HANDLE_VALUE) {
        closesocket((SOCKET)server_fd);
    }
    
    // 清理IPC资源
    if (shmid != NULL) {
        CloseHandle(shmid);
    }
    
    if (msgid != NULL) {
        CloseHandle(msgid);
    }
    
    // 清理Winsock
    WSACleanup();
#endif
    
    printf("资源清理完成\n");
}

int main(int argc, char *argv[]) {
    if (argc < 2) {
        fprintf(stderr, "用法: %s <监控目录>\n", argv[0]);
        return 1;
    }
    
#ifdef PLATFORM_LINUX
    // 注册信号处理函数
    signal(SIGINT, signal_handler);
    signal(SIGTERM, signal_handler);
#else
    // Windows初始化
    WSADATA wsaData;
    if (WSAStartup(MAKEWORD(2, 2), &wsaData) != 0) {
        fprintf(stderr, "WSAStartup失败\n");
        return 1;
    }
    
    // 注册控制台处理函数
    SetConsoleCtrlHandler(win_signal_handler, TRUE);
#endif
    
    // 初始化系统
    if (init_system(argv[1]) != 0) {
        fprintf(stderr, "系统初始化失败\n");
        return 1;
    }
    
    // 创建监控进程/线程
    monitor_pid = create_monitor_process(argv[1]);
#ifdef PLATFORM_LINUX
    if (monitor_pid < 0) {
#else
    if (monitor_pid == NULL) {
#endif
        fprintf(stderr, "创建监控进程失败\n");
        cleanup();
        return 1;
    }
    
    // 创建同步进程/线程
    sync_pid = create_sync_process();
#ifdef PLATFORM_LINUX
    if (sync_pid < 0) {
#else
    if (sync_pid == NULL) {
#endif
        fprintf(stderr, "创建同步进程失败\n");
        cleanup();
        return 1;
    }
    
    printf("系统启动成功，按Ctrl+C退出\n");
    
    // 主循环
    while (running) {
        sleep(1);
    }
    
    // 清理资源
    cleanup();
    
    return 0;
}