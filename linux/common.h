#ifndef COMMON_H
#define COMMON_H

// 平台检测
#if defined(_WIN32) || defined(_WIN64) || defined(__CYGWIN__)
    #define PLATFORM_WINDOWS
#else
    #define PLATFORM_LINUX
#endif

// 通用头文件
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <fcntl.h>
#include <limits.h>
#include <signal.h>
#include <time.h>

// 平台特定头文件
#ifdef PLATFORM_LINUX
    #include <unistd.h>
    #include <pthread.h>
    #include <semaphore.h>
    #include <sys/types.h>
    #include <sys/ipc.h>
    #include <sys/shm.h>
    #include <sys/msg.h>
    #include <sys/stat.h>
    #include <sys/wait.h>
    #include <sys/inotify.h>
    #include <arpa/inet.h>
    #include <sys/socket.h>
    #include <netinet/in.h>
#else
    #include <windows.h>
    #include <process.h>
    #include <io.h>
    #include <winsock2.h>
    #include <ws2tcpip.h>
    #include <direct.h>
    // Windows下模拟POSIX线程API
    typedef HANDLE pthread_t;
    typedef CRITICAL_SECTION pthread_mutex_t;
    typedef HANDLE sem_t;
    typedef HANDLE pid_t;
    
    // 定义Windows下的文件操作常量
    #define FILE_ACTION_ADDED 1
    #define FILE_ACTION_REMOVED 2
    #define FILE_ACTION_MODIFIED 3
    
    // 定义未定义的常量
    #ifndef PATH_MAX
        #define PATH_MAX 260
    #endif
#endif

#define MAX_QUEUE_SIZE 100
#define SHM_SIZE 1024
#define MSG_SIZE 256
#define PROJECT_ID 123
#define BUFFER_SIZE 4096
#define MIN(a, b) ((a) < (b) ? (a) : (b))

// Windows下的函数替代
#ifdef PLATFORM_WINDOWS
    #define sleep(x) Sleep((x) * 1000)
    #define close closesocket
    
    // 线程函数替代
    int pthread_create(pthread_t *thread, void *attr, void *(*start_routine)(void*), void *arg);
    int pthread_detach(pthread_t thread);
    int pthread_mutex_init(pthread_mutex_t *mutex, void *attr);
    int pthread_mutex_lock(pthread_mutex_t *mutex);
    int pthread_mutex_unlock(pthread_mutex_t *mutex);
    int pthread_mutex_destroy(pthread_mutex_t *mutex);
    
    // 信号量函数替代
    int sem_init(sem_t *sem, int pshared, unsigned int value);
    int sem_wait(sem_t *sem);
    int sem_post(sem_t *sem);
    int sem_destroy(sem_t *sem);
    
    // 文件监控替代结构
    typedef struct {
        DWORD action;
        char filename[MAX_PATH];
    } win_file_event;
    
    // 文件监控替代函数
    HANDLE win_init_monitor(const char *path);
    int win_read_changes(HANDLE handle, win_file_event *event);
#endif

// 同步队列项结构
typedef struct {
    char filename[256];
    char path[256];
    char operation[10];
} sync_item;

// 队列结构
typedef struct {
    sync_item items[MAX_QUEUE_SIZE];
    int front;
    int rear;
    int count;
    pthread_mutex_t mutex;
    sem_t empty;
    sem_t full;
} sync_queue;

// 共享内存结构
typedef struct {
    int status;  // 系统状态
    int file_count;  // 已同步文件数
    char last_file[256];  // 最后同步的文件
} shared_data;

// 消息结构
typedef struct {
    long mtype;  // 消息类型
    char mtext[MSG_SIZE];  // 消息内容
} message_buf;

// 监控目录结构
#ifdef PLATFORM_LINUX
typedef struct {
    char path[PATH_MAX];
    int watch_descriptor;
} watch_dir;
#else
typedef struct {
    char path[PATH_MAX];
    HANDLE handle;
    OVERLAPPED overlapped;
    char buffer[BUFFER_SIZE];
    DWORD bytes_returned;
} watch_dir;
#endif

// sync.c 函数声明
sync_queue* init_sync_queue();
int add_to_sync_queue(sync_queue *queue, const char *filename, const char *path, const char *operation);
int get_from_sync_queue(sync_queue *queue, sync_item *item);
void destroy_sync_queue(sync_queue *queue);

// ipc.c 函数声明
#ifdef PLATFORM_LINUX
int init_shared_memory();
int init_message_queue();
int send_message(int msgid, long type, const char *text);
int receive_message(int msgid, long type, char *buf, size_t buf_size);
#else
int init_shared_memory();
int init_message_queue();
int send_message(int msgid, long type, const char *text);
int receive_message(int msgid, long type, char *buf, size_t buf_size);
#endif

// monitor.c 函数声明
#ifdef PLATFORM_LINUX
void process_file_event(struct inotify_event *event, char *watch_path);
void* monitor_directory(void *arg);
int init_monitor_system(char *directory);
#else
void process_file_event(win_file_event *event, char *watch_path);
void* monitor_directory(void *arg);
int init_monitor_system(char *directory);
#endif

// network.c 函数声明
int init_server();
int send_file(int socket, const char *filename);
int receive_file(int socket, const char *filename, size_t filesize);

// 全局变量声明
extern int running;
extern sync_queue *queue;
#ifdef PLATFORM_LINUX
extern int shmid;
extern int msgid;
#else
extern HANDLE shmid;
extern HANDLE msgid;
#endif

#endif /* COMMON_H */
