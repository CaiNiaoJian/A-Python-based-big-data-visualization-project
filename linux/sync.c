#include "common.h"

// 初始化同步队列
sync_queue* init_sync_queue() {
    sync_queue *queue = malloc(sizeof(sync_queue));
    if (!queue) {
        perror("malloc");
        return NULL;
    }
    
    queue->front = 0;
    queue->rear = -1;
    queue->count = 0;
    
    // 初始化互斥锁和信号量
    pthread_mutex_init(&queue->mutex, NULL);
    sem_init(&queue->empty, 0, MAX_QUEUE_SIZE);
    sem_init(&queue->full, 0, 0);
    
    return queue;
}

// 添加项目到同步队列
int add_to_sync_queue(sync_queue *queue, const char *filename, 
const char *path, const char *operation) {
    // 等待空槽
    sem_wait(&queue->empty);
    
    // 加锁保护共享资源
    pthread_mutex_lock(&queue->mutex);
    
    // 添加项目到队列
    queue->rear = (queue->rear + 1) % MAX_QUEUE_SIZE;
    strncpy(queue->items[queue->rear].filename, filename, 255);
    strncpy(queue->items[queue->rear].path, path, 255);
    strncpy(queue->items[queue->rear].operation, operation, 9);
    queue->count++;
    
    // 解锁
    pthread_mutex_unlock(&queue->mutex);
    
    // 通知消费者
    sem_post(&queue->full);
    
    return 0;
}

// 从同步队列获取项目
int get_from_sync_queue(sync_queue *queue, sync_item *item) {
    // 等待有数据
    sem_wait(&queue->full);
    
    // 加锁保护共享资源
    pthread_mutex_lock(&queue->mutex);
    
    // 从队列获取项目
    *item = queue->items[queue->front];
    queue->front = (queue->front + 1) % MAX_QUEUE_SIZE;
    queue->count--;
    
    // 解锁
    pthread_mutex_unlock(&queue->mutex);
    
    // 通知生产者
    sem_post(&queue->empty);
    
    return 0;
}

// 销毁同步队列
void destroy_sync_queue(sync_queue *queue) {
    pthread_mutex_destroy(&queue->mutex);
    sem_destroy(&queue->empty);
    sem_destroy(&queue->full);
    free(queue);
}