n = int(input())
schet=0
s= list(map(int, input().split()))
for i in s:
    freq=0
    for a in s:
        if i==a:
            freq+=1
    if freq>schet:
        schet=freq
    
