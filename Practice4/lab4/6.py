n=int(input())
a=1
b=0
c=0
if n==1:
    b=0
    print(b)
    quit()
if n==2:
    print("0,1")
    quit()
if n>1:
    while c<=n-1:
        c=c+1
        a,b=b,a+b
        if c==n:
            print(a, end="")
        else:
            print(a, end=",")


