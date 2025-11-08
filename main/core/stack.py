class Stack:
    def __init__(self, max_size):
        self.items = [None] * max_size
        self.top_index = 0
        self.max_size = max_size

    def push(self, value):
        if self.top_index == self.max_size:
            print("Stack Overflow")
            return
        self.items[self.top_index] = value
        self.top_index += 1

    def pop(self):
        if self.top_index == 0:
            print("Stack Underflow")
            return None
        self.top_index -= 1
        value = self.items[self.top_index]
        self.items[self.top_index] = None  
        return value

    def top(self):
        if self.top_index == 0:
            return None
        return self.items[self.top_index - 1]

    def empty(self):
        return self.top_index == 0

    def size(self):
        return self.top_index