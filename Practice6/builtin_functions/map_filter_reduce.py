from functools import reduce
numbers = [1, 2, 3, 4, 5]
squared = list(map(lambda x: x ** 2, numbers))
print("Map:", squared)
evens = list(filter(lambda x: x % 2 == 0, numbers))
print("Filter:", evens)
total = reduce(lambda a, b: a + b, numbers)
print("Reduce:", total)