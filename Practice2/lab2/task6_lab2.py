a=int(input())
s=list(map(int,input().split()))
max=s[0]
for i in s:
    if i > max:
        max= i
print(s.index(max)+1)