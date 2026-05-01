import sys

k = int(sys.stdin.readline())

g = 0
n = 0

for _ in range(k):
    scope, val = sys.stdin.readline().split()
    val = int(val)
    if scope == "global":
        g += val
    elif scope == "nonlocal":
        n += val

print(g, n)