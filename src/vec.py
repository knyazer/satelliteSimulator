import math

class Vec2():
    def __init__(self, *args):
        if len(args) == 1:
            self.x = args[0].x
            self.y = args[0].y
        elif len(args) == 2:
            self.x = args[0]
            self.y = args[1]
        else:
            self.x = 0
            self.y = 0

    def sqsize(self):
        return self.x * self.x + self.y * self.y

    def size(self):
        return math.sqrt(self.sqsize())

    def norm(self):
        return Vec2(self / self.size())

    def direction(self):
        return math.atan2(self.x, self.y)

    def __add__(self, other):
        return Vec2(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vec2(self.x - other.x, self.y - other.y)

    def __mul__(self, other):
        return Vec2(self.x * other, self.y * other)

    def __truediv__(self, other):
        return Vec2(self.x / other, self.y / other)

    def __neg__(self):
        return Vec2(-self.x, -self.y)
