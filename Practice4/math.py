import math
import random
print("Square root:", math.sqrt(16))
print("Power:", math.pow(2, 3))
print("Factorial:", math.factorial(5))
print("Ceil:", math.ceil(4.3))
print("Floor:", math.floor(4.7))
print("Pi:", math.pi)
print("Random int:", random.randint(1, 10))
print("Random float:", random.random())
numbers = [1, 2, 3, 4, 5]
print("Random choice:", random.choice(numbers))
random.shuffle(numbers)
print("Shuffled list:", numbers)