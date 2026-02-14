n = input().strip()
is_valid = True
for digit in n:
    if int(digit) % 2 != 0:
        is_valid = False
        break

if is_valid:
    print("Valid")
else:
    print("Not valid")
