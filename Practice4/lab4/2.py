n=int(input())
def even_numbers(n):
    for i in range(n):
        if i % 2 == 0:
            yield i
if n % 2 == 0:
    for num in even_numbers(n):
        print(num, end=",")
    print (n)
else:
    for num in even_numbers(n-1):
        print(num, end=",")
    print (n-1)