#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/types.h>
#include <sys/ipc.h>
#include <sys/shm.h>
#include <sys/msg.h>
#include <errno.h>

#define SHM_SIZE 1024
#define MSG_SIZE 256
#define PROJECT_ID 123

// 消息结构
typedef struct {
    long mtype;  // 消息类型
    char mtext[MSG_SIZE];  // 消息内容
} message_buf;

// 共享内存结构
typedef struct {
    int status;  // 系统状态
    int file_count;  // 已同步文件数
    char last_file[256];  // 最后同步的文件
} shared_data;

// 初始化共享内存
int init_shared_memory() {
    key_t key;
    int shmid;
    shared_data *data;
    
    // 创建键值
    key = ftok("/tmp", PROJECT_ID);
    if (key == -1) {
        perror("ftok");
        return -1;
    }
    
    // 创建共享内存段
    shmid = shmget(key, SHM_SIZE, IPC_CREAT | 0666);
    if (shmid == -1) {
        perror("shmget");
        return -1;
    }
    
    // 附加共享内存段
    data = (shared_data*)shmat(shmid, NULL, 0);
    if (data == (shared_data*)-1) {
        perror("shmat");
        return -1;
    }
    
    // 初始化共享数据
    data->status = 1;  // 1表示系统正常运行
    data->file_count = 0;
    strcpy(data->last_file, "");
    
    // 分离共享内存
    if (shmdt(data) == -1) {
        perror("shmdt");
        return -1;
    }
    
    printf("共享内存初始化成功\n");
    return shmid;
}

// 初始化消息队列
int init_message_queue() {
    key_t key;
    int msgid;
    
    // 创建键值
    key = ftok("/tmp", PROJECT_ID + 1);
    if (key == -1) {
        perror("ftok");
        return -1;
    }
    
    // 创建消息队列
    msgid = msgget(key, IPC_CREAT | 0666);
    if (msgid == -1) {
        perror("msgget");
        return -1;
    }
    
    printf("消息队列初始化成功\n");
    return msgid;
}

// 发送消息
int send_message(int msgid, long type, const char *text) {
    message_buf msg;
    
    msg.mtype = type;
    strncpy(msg.mtext, text, MSG_SIZE);
    
    // 发送消息
    if (msgsnd(msgid, &msg, strlen(msg.mtext) + 1, 0) == -1) {
        perror("msgsnd");
        return -1;
    }
    
    return 0;
}

// 接收消息
int receive_message(int msgid, long type, char *buf, size_t buf_size) {
    message_buf msg;
    ssize_t bytes;
    
    // 接收消息
    bytes = msgrcv(msgid, &msg, MSG_SIZE, type, 0);
    if (bytes == -1) {
        perror("msgrcv");
        return -1;
    }
    
    strncpy(buf, msg.mtext, buf_size);
    return bytes;
}