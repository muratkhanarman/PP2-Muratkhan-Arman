n, a, b = map(int, input().split())
s = list(map(int, input().split()))
a -= 1
b -= 1
while a < b:
    s[a], s[b] = s[b], s[a]
    a += 1
    b -= 1
print(*s)
