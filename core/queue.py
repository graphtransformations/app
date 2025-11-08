class Queue:
    def __init__(self, max_size):
        self.items = [None] * max_size
        self.front = 0
        self.rear = -1
        self.size = 0
        self.max_size = max_size

    def enqueue(self, value):
        if self.isFull():
            print("Queue Overflow")
            return
        self.rear = (self.rear + 1) % self.max_size
        self.items[self.rear] = value
        self.size += 1

    def dequeue(self):
        if self.isEmpty():
            return None
        item = self.items[self.front]
        self.items[self.front] = None 
        self.front = (self.front + 1) % self.max_size
        self.size -= 1
        return item

    def isEmpty(self):
        return self.size == 0

    def isFull(self):
        return self.size == self.max_size
    
    def clear(self):
        while not self.isEmpty():
            self.dequeue()
    
    