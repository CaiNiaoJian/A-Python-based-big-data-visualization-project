#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <arpa/inet.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <pthread.h>
#include <fcntl.h>
#include <sys/stat.h>
#include "common.h"

#define PORT 8080
#define BUFFER_SIZE 4096
#define MAX_CLIENTS 10

// 文件传输请求结构
typedef struct {
    char filename[256];
    char operation[10];  // CREATE, MODIFY, DELETE
    size_t filesize;
} file_request;

// 客户端连接结构
typedef struct {
    int socket;
    struct sockaddr_in address;
} client_info;

// 线程池中的线程数据
typedef struct {
    pthread_t thread_id;
    int is_alive;
} thread_data;

// 线程池
thread_data thread_pool[MAX_CLIENTS];
pthread_mutex_t client_mutex = PTHREAD_MUTEX_INITIALIZER;

// 发送文件
int send_file(int socket, const char *filename) {
    char buffer[BUFFER_SIZE];
    FILE *file;
    size_t bytes_read;
    
    // 打开文件
    file = fopen(filename, "rb");
    if (!file) {
        perror("fopen");
        return -1;
    }
    
    // 读取并发送文件内容
    while ((bytes_read = fread(buffer, 1, BUFFER_SIZE, file)) > 0) {
        if (send(socket, buffer, bytes_read, 0) < 0) {
            perror("send");
            fclose(file);
            return -1;
        }
    }
    
    fclose(file);
    return 0;
}

// 接收文件
int receive_file(int socket, const char *filename, size_t filesize) {
    char buffer[BUFFER_SIZE];
    FILE *file;
    size_t bytes_received = 0;
    ssize_t n;
    
    // 创建文件
    file = fopen(filename, "wb");
    if (!file) {
        perror("fopen");
        return -1;
    }
    
    // 接收并写入文件内容
    while (bytes_received < filesize) {
        n = recv(socket, buffer, 
                 MIN(BUFFER_SIZE, filesize - bytes_received), 0);
        if (n <= 0) {
            if (n < 0) perror("recv");
            break;
        }
        
        fwrite(buffer, 1, n, file);
        bytes_received += n;
    }
    
    fclose(file);
    return (bytes_received == filesize) ? 0 : -1;
}

// 处理客户端连接的线程函数
void* handle_client(void *arg) {
    client_info *client = (client_info*)arg;
    int socket = client->socket;
    char buffer[BUFFER_SIZE];
    file_request request;
    
    printf("客户端已连接: %s:%d\n", 
           inet_ntoa(client->address.sin_addr),
           ntohs(client->address.sin_port));
    
    while (1) {
        // 接收文件请求
        ssize_t bytes = recv(socket, &request, sizeof(request), 0);
        if (bytes <= 0) {
            if (bytes < 0) perror("recv");
            break;
        }
        
        printf("收到请求: %s, 操作: %s, 大小: %zu\n", 
               request.filename, request.operation, request.filesize);
        
        // 根据操作类型处理请求
        if (strcmp(request.operation, "CREATE") == 0 || 
            strcmp(request.operation, "MODIFY") == 0) {
            // 接收文件
            if (receive_file(socket, request.filename, 
                            request.filesize) == 0) {
                strcpy(buffer, "文件接收成功");
            } else {
                strcpy(buffer, "文件接收失败");
            }
        } else if (strcmp(request.operation, "DELETE") == 0) {
            // 删除文件
            if (unlink(request.filename) == 0) {
                strcpy(buffer, "文件删除成功");
            } else {
                perror("unlink");
                strcpy(buffer, "文件删除失败");
            }
        } else {
            strcpy(buffer, "未知操作");
        }
        
        // 发送响应
        send(socket, buffer, strlen(buffer) + 1, 0);
    }
    
    close(socket);
    free(client);
    
    printf("客户端断开连接\n");
    return NULL;
}

// 初始化服务器
int init_server() {
    int server_fd;
    struct sockaddr_in address;
    int opt = 1;
    
    // 创建套接字
    server_fd = socket(AF_INET, SOCK_STREAM, 0);
    if (server_fd < 0) {
        perror("socket");
        return -1;
    }
    
    // 设置套接字选项
    if (setsockopt(server_fd, SOL_SOCKET, SO_REUSEADDR, 
                  &opt, sizeof(opt)) < 0) {
        perror("setsockopt");
        close(server_fd);
        return -1;
    }
    
    // 设置地址
    address.sin_family = AF_INET;
    address.sin_addr.s_addr = INADDR_ANY;
    address.sin_port = htons(PORT);
    
    // 绑定套接字
    if (bind(server_fd, (struct sockaddr*)&address, 
            sizeof(address)) < 0) {
        perror("bind");
        close(server_fd);
        return -1;
    }
    
    // 监听连接
    if (listen(server_fd, MAX_CLIENTS) < 0) {
        perror("listen");
        close(server_fd);
        return -1;
    }
    
    printf("服务器初始化成功，监听端口: %d\n", PORT);
    return server_fd;
}