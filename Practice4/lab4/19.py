import sys
import math

R = float(sys.stdin.readline())
ax, ay = map(float, sys.stdin.readline().split())
bx, by = map(float, sys.stdin.readline().split())

da = math.hypot(ax, ay)
db = math.hypot(bx, by)

vx = bx - ax
vy = by - ay
vv = vx * vx + vy * vy

intersects = False
if vv != 0:
    t = -(ax * vx + ay * vy) / vv
    if t < 0:
        dmin = da
    elif t > 1:
        dmin = db
    else:
        px = ax + t * vx
        py = ay + t * vy
        dmin = math.hypot(px, py)
    intersects = dmin < R

if not intersects:
    print(f"{math.hypot(bx - ax, by - ay):.10f}")
    sys.exit(0)

alpha = math.acos(R / da)
beta = math.acos(R / db)

theta_a = math.atan2(ay, ax)
theta_b = math.atan2(by, bx)

def norm(x):
    return (x + math.pi) % (2 * math.pi) - math.pi

delta = abs(norm(theta_b - theta_a))
arc = R * abs(delta - (alpha + beta))

tangent = math.sqrt(da * da - R * R) + math.sqrt(db * db - R * R)

print(f"{tangent + arc:.10f}")