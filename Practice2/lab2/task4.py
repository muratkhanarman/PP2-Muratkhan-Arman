n = int(input())
c=0
numbers = list(map(int, input().split()))
for i in numbers:
    if i>=0:
        c=c+1
print(c)

