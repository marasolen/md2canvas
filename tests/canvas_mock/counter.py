class Counter():
    def __init__(self):
        self.next_num = 0

    def get_next_num(self):
        num = self.next_num
        self.next_num += 1
        return str(num)