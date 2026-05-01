def isUsual(num):
    if num <= 0:
        return False

    for divisor in [2, 3, 5]:
        while num % divisor == 0:
            num //= divisor

    return num == 1


n = int(input())

if isUsual(n):
    print("Yes")
else:
    print("No")
