#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <pthread.h>
#include <sys/inotify.h>
#include <limits.h>

#define EVENT_SIZE  (sizeof(struct inotify_event))
#define BUF_LEN     (1024 * (EVENT_SIZE + NAME_MAX + 1))

// 互斥锁，保护共享资源
pthread_mutex_t file_mutex = PTHREAD_MUTEX_INITIALIZER;

// 监控目录结构
typedef struct {
    char path[PATH_MAX];
    int watch_descriptor;
} watch_dir;

// 文件事件处理函数
void process_file_event(struct inotify_event *event, char *watch_path) {
    // 加锁保护共享资源
    pthread_mutex_lock(&file_mutex);
    
    if (event->len) {
        if (event->mask & IN_CREATE) {
            printf("文件被创建: %s/%s\n", watch_path, event->name);
            // 将事件添加到同步队列
            add_to_sync_queue(event->name, watch_path, "CREATE");
        } else if (event->mask & IN_DELETE) {
            printf("文件被删除: %s/%s\n", watch_path, event->name);
            add_to_sync_queue(event->name, watch_path, "DELETE");
        } else if (event->mask & IN_MODIFY) {
            printf("文件被修改: %s/%s\n", watch_path, event->name);
            add_to_sync_queue(event->name, watch_path, "MODIFY");
        }
    }
    
    // 解锁
    pthread_mutex_unlock(&file_mutex);
}

// 监控线程函数
void* monitor_directory(void *arg) {
    watch_dir *dir = (watch_dir*)arg;
    char buffer[BUF_LEN];
    int fd, wd;
    
    // 初始化inotify
    fd = inotify_init();
    if (fd < 0) {
        perror("inotify_init");
        return NULL;
    }
    
    // 添加监控目录
    wd = inotify_add_watch(fd, dir->path, 
                          IN_CREATE | IN_DELETE | IN_MODIFY);
    dir->watch_descriptor = wd;
    
    if (wd < 0) {
        perror("inotify_add_watch");
        return NULL;
    }
    
    printf("开始监控目录: %s\n", dir->path);
    
    // 持续监控文件事件
    while (1) {
        int i = 0, length;
        length = read(fd, buffer, BUF_LEN);
        
        if (length < 0) {
            perror("read");
            break;
        }
        
        while (i < length) {
            struct inotify_event *event = 
                (struct inotify_event*)&buffer[i];
            
            process_file_event(event, dir->path);
            
            i += EVENT_SIZE + event->len;
        }
    }
    
    // 清理资源
    inotify_rm_watch(fd, wd);
    close(fd);
    
    return NULL;
}

// 初始化监控系统
int init_monitor_system(char *directory) {
    pthread_t monitor_thread;
    watch_dir *dir = malloc(sizeof(watch_dir));
    
    if (!dir) {
        perror("malloc");
        return -1;
    }
    
    strncpy(dir->path, directory, PATH_MAX);
    
    // 创建监控线程
    if (pthread_create(&monitor_thread, NULL, 
                      monitor_directory, dir) != 0) {
        perror("pthread_create");
        free(dir);
        return -1;
    }
    
    // 分离线程，使其独立运行
    pthread_detach(monitor_thread);
    return 0;
}