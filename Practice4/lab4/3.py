n=int(input())
def div(n):
    for i in range(n+1):
        if i % 12 == 0:
            yield i
for i in div(n):
    print(i,end=" ")