import sys
x1, y1 = map(float, sys.stdin.readline().split())
x2, y2 = map(float, sys.stdin.readline().split())
x2r, y2r = x2, -y2
t = -y1 / (y2r - y1)
xr = x1 + t * (x2r - x1)
yr = 0.0
print(f"{xr:.10f} {yr:.10f}")