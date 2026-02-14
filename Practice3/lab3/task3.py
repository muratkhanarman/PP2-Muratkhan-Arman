triplet_to_digit = {
    "ZER": "0", "ONE": "1", "TWO": "2", "THR": "3",
    "FOU": "4", "FIV": "5", "SIX": "6",
    "SEV": "7", "EIG": "8", "NIN": "9"
}

digit_to_triplet = {v: k for k, v in triplet_to_digit.items()}

s = input().strip()
for op in ['+', '-', '*']:
    if op in s:
        operator = op
        break

left, right = s.split(operator)

def convert_to_number(expr):
    number = ""
    for i in range(0, len(expr), 3):
        triplet = expr[i:i+3]
        number += triplet_to_digit[triplet]
    return int(number)

num1 = convert_to_number(left)
num2 = convert_to_number(right)

if operator == '+':
    result = num1 + num2
elif operator == '-':
    result = num1 - num2
else:
    result = num1 * num2

result_str = str(result)

output = ""
for digit in result_str:
    output += digit_to_triplet[digit]

print(output)
