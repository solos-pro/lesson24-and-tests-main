# Вам нужно сделать обратную процедуру по сравнению
# с предыдущим заданием. Вам нужно переписать
# датакласс Point на обычный класс.
from dataclasses import dataclass


# @dataclass
# class Point:
#     x: float
#     y: float


class Point:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

