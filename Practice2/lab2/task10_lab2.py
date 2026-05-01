n = int(input())
s = list(map(int, input().split()))
s.sort(reverse=True)
for i in s:
    print (i,end=' ')
