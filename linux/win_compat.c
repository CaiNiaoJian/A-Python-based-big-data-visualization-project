#include "common.h"

#ifdef PLATFORM_WINDOWS

// 线程启动结构
typedef struct {
    void *(*start_routine)(void*);
    void *arg;
} thread_start_params;

// 线程启动函数
static unsigned __stdcall thread_start(void *param) {
    thread_start_params *params = (thread_start_params*)param;
    void *(*start_routine)(void*) = params->start_routine;
    void *arg = params->arg;
    
    free(params); // 释放参数结构
    
    // 调用实际的线程函数
    return (unsigned)start_routine(arg);
}

// 创建线程
int pthread_create(pthread_t *thread, void *attr, void *(*start_routine)(void*), void *arg) {
    thread_start_params *params = malloc(sizeof(thread_start_params));
    if (!params) {
        return -1;
    }
    
    params->start_routine = start_routine;
    params->arg = arg;
    
    // 创建线程
    *thread = (HANDLE)_beginthreadex(NULL, 0, thread_start, params, 0, NULL);
    
    if (*thread == NULL) {
        free(params);
        return -1;
    }
    
    return 0;
}

// 分离线程
int pthread_detach(pthread_t thread) {
    CloseHandle(thread);
    return 0;
}

// 初始化互斥锁
int pthread_mutex_init(pthread_mutex_t *mutex, void *attr) {
    InitializeCriticalSection(mutex);
    return 0;
}

// 锁定互斥锁
int pthread_mutex_lock(pthread_mutex_t *mutex) {
    EnterCriticalSection(mutex);
    return 0;
}

// 解锁互斥锁
int pthread_mutex_unlock(pthread_mutex_t *mutex) {
    LeaveCriticalSection(mutex);
    return 0;
}

// 销毁互斥锁
int pthread_mutex_destroy(pthread_mutex_t *mutex) {
    DeleteCriticalSection(mutex);
    return 0;
}

// 初始化信号量
int sem_init(sem_t *sem, int pshared, unsigned int value) {
    *sem = CreateSemaphore(NULL, value, MAX_QUEUE_SIZE, NULL);
    return (*sem == NULL) ? -1 : 0;
}

// 等待信号量
int sem_wait(sem_t *sem) {
    DWORD result = WaitForSingleObject(*sem, INFINITE);
    return (result == WAIT_OBJECT_0) ? 0 : -1;
}

// 发送信号量
int sem_post(sem_t *sem) {
    return ReleaseSemaphore(*sem, 1, NULL) ? 0 : -1;
}

// 销毁信号量
int sem_destroy(sem_t *sem) {
    return CloseHandle(*sem) ? 0 : -1;
}

// Windows下的文件监控初始化
HANDLE win_init_monitor(const char *path) {
    HANDLE handle = FindFirstChangeNotification(
        path,                   // 监控的目录
        TRUE,                   // 监控子目录
        FILE_NOTIFY_CHANGE_FILE_NAME |  // 文件创建/删除
        FILE_NOTIFY_CHANGE_DIR_NAME |   // 目录创建/删除
        FILE_NOTIFY_CHANGE_LAST_WRITE   // 文件修改
    );
    
    return handle;
}

// Windows下读取文件变化
int win_read_changes(HANDLE handle, win_file_event *event) {
    // 等待文件变化通知
    DWORD wait_status = WaitForSingleObject(handle, INFINITE);
    
    if (wait_status == WAIT_OBJECT_0) {
        // 找到变化，但Windows API不提供具体文件信息
        // 这里需要应用程序自己记录目录内容并比较
        // 简化实现，假设有文件变化
        event->action = 1; // 1表示有变化
        strcpy(event->filename, "unknown"); // Windows API不直接提供文件名
        
        // 继续监控
        if (!FindNextChangeNotification(handle)) {
            return -1;
        }
        
        return 0;
    }
    
    return -1;
}

// Windows下的共享内存实现
int init_shared_memory() {
    // 创建一个命名共享内存
    HANDLE hMapFile = CreateFileMapping(
        INVALID_HANDLE_VALUE,   // 使用分页文件
        NULL,                   // 默认安全属性
        PAGE_READWRITE,         // 读写权限
        0,                      // 高位大小
        SHM_SIZE,               // 低位大小
        "FileSyncSharedMemory"  // 命名
    );
    
    if (hMapFile == NULL) {
        printf("共享内存创建失败: %d\n", GetLastError());
        return -1;
    }
    
    // 映射视图
    shared_data *data = (shared_data*)MapViewOfFile(
        hMapFile,               // 共享内存句柄
        FILE_MAP_ALL_ACCESS,    // 读写权限
        0,                      // 高位偏移
        0,                      // 低位偏移
        SHM_SIZE                // 映射大小
    );
    
    if (data == NULL) {
        printf("共享内存映射失败: %d\n", GetLastError());
        CloseHandle(hMapFile);
        return -1;
    }
    
    // 初始化共享数据
    data->status = 1;  // 1表示系统正常运行
    data->file_count = 0;
    strcpy(data->last_file, "");
    
    // 解除映射
    UnmapViewOfFile(data);
    
    printf("共享内存初始化成功\n");
    return (int)hMapFile;
}

// Windows下的消息队列实现（使用命名管道模拟）
int init_message_queue() {
    // 创建命名管道
    HANDLE hPipe = CreateNamedPipe(
        "\\\\.\\pipe\\FileSyncMessageQueue", // 管道名称
        PIPE_ACCESS_DUPLEX,      // 双向访问
        PIPE_TYPE_MESSAGE |      // 消息类型管道
        PIPE_READMODE_MESSAGE |  // 消息读取模式
        PIPE_WAIT,               // 阻塞模式
        PIPE_UNLIMITED_INSTANCES,// 无限实例
        MSG_SIZE,                // 输出缓冲区大小
        MSG_SIZE,                // 输入缓冲区大小
        0,                       // 默认超时
        NULL                     // 默认安全属性
    );
    
    if (hPipe == INVALID_HANDLE_VALUE) {
        printf("消息队列创建失败: %d\n", GetLastError());
        return -1;
    }
    
    printf("消息队列初始化成功\n");
    return (int)hPipe;
}

// Windows下的消息发送
int send_message(int msgid, long type, const char *text) {
    HANDLE hPipe = (HANDLE)msgid;
    DWORD bytes_written;
    message_buf msg;
    
    msg.mtype = type;
    strncpy(msg.mtext, text, MSG_SIZE);
    
    // 连接到管道
    if (!ConnectNamedPipe(hPipe, NULL) && GetLastError() != ERROR_PIPE_CONNECTED) {
        printf("连接到管道失败: %d\n", GetLastError());
        return -1;
    }
    
    // 写入消息
    if (!WriteFile(
        hPipe,                  // 管道句柄
        &msg,                   // 消息缓冲区
        sizeof(message_buf),    // 消息大小
        &bytes_written,         // 写入的字节数
        NULL                    // 不使用重叠IO
    )) {
        printf("发送消息失败: %d\n", GetLastError());
        return -1;
    }
    
    // 断开连接
    DisconnectNamedPipe(hPipe);
    
    return 0;
}

// Windows下的消息接收
int receive_message(int msgid, long type, char *buf, size_t buf_size) {
    HANDLE hPipe = (HANDLE)msgid;
    DWORD bytes_read;
    message_buf msg;
    
    // 连接到管道
    if (!ConnectNamedPipe(hPipe, NULL) && GetLastError() != ERROR_PIPE_CONNECTED) {
        printf("连接到管道失败: %d\n", GetLastError());
        return -1;
    }
    
    // 读取消息
    if (!ReadFile(
        hPipe,                  // 管道句柄
        &msg,                   // 消息缓冲区
        sizeof(message_buf),    // 消息大小
        &bytes_read,            // 读取的字节数
        NULL                    // 不使用重叠IO
    )) {
        printf("接收消息失败: %d\n", GetLastError());
        return -1;
    }
    
    // 断开连接
    DisconnectNamedPipe(hPipe);
    
    // 检查消息类型
    if (type != 0 && msg.mtype != type) {
        return -1;
    }
    
    strncpy(buf, msg.mtext, buf_size);
    return bytes_read;
}

#endif // PLATFORM_WINDOWS
