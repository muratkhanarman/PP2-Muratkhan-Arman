a=int(input())
b=list(map(int,input().split()))
max=b[0]
min=b[0]
for i in b:
    if i>max:
        max=i
for i in b:
    if i<min:
        min=i
for i in b:
    if i==max:
        print(min,end=' ')
    else:
        print(i,end=' ')
