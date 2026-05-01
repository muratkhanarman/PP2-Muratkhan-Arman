class Countdown:
    def __init__(self, start):
        self.current = start

    def __iter__(self):
        return self

    def __next__(self):
        if self.current > 0:
            value = self.current
            self.current -= 1
            return value
        else:
            raise StopIteration


print("Iterator:")
for num in Countdown(5):
    print(num)

def even_numbers(n):
    for i in range(n):
        if i % 2 == 0:
            yield i


print("\nGenerator function:")
for num in even_numbers(10):
    print(num)
squares = (x*x for x in range(5))

print("\nGenerator expression:")
for s in squares:
    print(s)