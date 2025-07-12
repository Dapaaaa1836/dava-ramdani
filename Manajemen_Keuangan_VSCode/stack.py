class Stack:
    def __init__(self):
        self.stack = []

    def push(self, data):
        self.stack.append(data)

    def pop(self):
        return self.stack.pop() if not self.is_empty() else None

    def is_empty(self):
        return len(self.stack) == 0
