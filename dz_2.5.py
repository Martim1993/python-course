# Посмотрите самый низ

class IndexError(Exception):
    pass


class StatefulIterator:
    def __init__(self,
                 iterable):
        self.iterable = iterable
        self.index = 0

    def __iter__(self):
        return self

    def __next__(self):
        while self.index < len(self.iterable):
            current_iterable = self.iterable[self.index]
            self.index += 1
            return current_iterable
        raise IndexError("Перемотка вперед невозможна так как достигнут конец списка")

    def rewind(self,
               n: int):
        while self.index < len(self.iterable):
            current_iterable = self.iterable[self.index]
            self.index -= n
            if self.index < 0:
                raise IndexError("Перемотка назад невозможна так как достигнуто начало списка")
            return current_iterable
        raise IndexError("Перемотка вперед невозможна так как достигнут конец списка")

    def forward(self,
               n: int):
        while self.index < len(self.iterable):
            self.index += n
            current_iterable = self.iterable[self.index]
            return current_iterable
        raise IndexError("Перемотка вперед невозможна так как достигнут конец списка")

    def reset(self):
        self.index = 0
        current_iterable = self.iterable[self.index]
        return current_iterable

    def current(self):
        if self.index == 0:
            current_iterable = self.iterable[self.index]
            return current_iterable
        else:
            self.index -= 1
            current_iterable = self.iterable[self.index]
            self.index += 1
            return current_iterable


iterable1 = [10, 20, 30, 40, 50]
iterator = StatefulIterator(iterable1)
print(next(iterator))
print(next(iterator))
iterator.rewind(1)
print(next(iterator))
iterator.forward(2)
print(next(iterator))
print(iterator.current())
iterator.reset()
print(iterator.current())
print(iterator.forward(4))