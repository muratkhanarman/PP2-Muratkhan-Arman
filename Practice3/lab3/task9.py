class Circle:
    def __init__(self, radius):
        self.radius = radius

    def area(self):
        pi = 3.14159
        return pi * self.radius ** 2


r = int(input())
circle = Circle(r)
area = circle.area()

print(f"{area:.2f}")
