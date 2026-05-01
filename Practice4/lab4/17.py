import math

r = float(input())
x1, y1 = map(float, input().split())
x2, y2 = map(float, input().split())

dx = x2 - x1
dy = y2 - y1
a = dx*dx + dy*dy
b = 2*(dx*x1 + dy*y1)
c = x1*x1 + y1*y1 - r*r

discriminant = b*b - 4*a*c

if discriminant <= 0:
    if x1*x1 + y1*y1 <= r*r and x2*x2 + y2*y2 <= r*r:
        length = math.hypot(dx, dy)
    else:
        length = 0.0
else:
    sqrt_disc = math.sqrt(discriminant)
    t1 = (-b - sqrt_disc)/(2*a)
    t2 = (-b + sqrt_disc)/(2*a)
    t_low = max(0, min(t1, t2))
    t_high = min(1, max(t1, t2))
    if t_low >= t_high:
        length = 0.0
    else:
        px1 = x1 + t_low*dx
        py1 = y1 + t_low*dy
        px2 = x1 + t_high*dx
        py2 = y1 + t_high*dy
        length = math.hypot(px2 - px1, py2 - py1)

print(f"{length:.10f}")