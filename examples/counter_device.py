"""通信方式に依存しない、純粋な制御クラスの例。"""
class Counter:
    def __init__(self): self.value = 0
    def increment(self, amount=1):
        self.value += amount
        return self.value
    def read(self): return self.value
