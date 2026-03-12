import re
import json

with open("raw.txt", "r", encoding="utf-8") as file:
    text = file.read()


def to_float(s):
    return float(s.replace(" ", "").replace(",", "."))


def extract_prices(text):
    prices = re.findall(r'\d[\d ]*,\d{2}', text)
    return [to_float(p) for p in prices]


def extract_products(text):
    products = []
    lines = text.splitlines()

    i = 0
    while i < len(lines):
        line = lines[i].strip()

        if re.fullmatch(r'\d+\.', line):
            if i + 1 < len(lines):
                product = lines[i + 1].strip()
                j = i + 2

                while j < len(lines):
                    next_line = lines[j].strip()
                    if re.fullmatch(r'\d[\d ]*,\d{2}\s*x\s*\d[\d ]*,\d{2}', next_line):
                        break
                    if re.fullmatch(r'\d+\.', next_line):
                        break
                    if next_line:
                        product += " " + next_line
                    j += 1

                products.append(product)
        i += 1

    return products


def extract_total(text):
    match = re.search(r'ИТОГО:\s*\n\s*(\d[\d ]*,\d{2})', text)
    if match:
        return to_float(match.group(1))
    return None


def extract_datetime(text):
    match = re.search(r'Время:\s*(\d{2}\.\d{2}\.\d{4})\s+(\d{2}:\d{2}:\d{2})', text)
    if match:
        return match.group(1), match.group(2)
    return None, None


def extract_payment_method(text):
    if "Банковская карта" in text:
        return "Банковская карта"
    if "Наличные" in text:
        return "Наличные"
    return None


prices = extract_prices(text)
products = extract_products(text)
total = extract_total(text)
date, time = extract_datetime(text)
payment_method = extract_payment_method(text)

result = {
    "prices": prices,
    "products": products,
    "total": total,
    "date": date,
    "time": time,
    "payment_method": payment_method
}

print(json.dumps(result, ensure_ascii=False, indent=4))