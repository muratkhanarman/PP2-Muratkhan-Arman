import json
import re
def resolve_query(data, query):
    parts = re.findall(r'\w+|\[\d+\]', query)
    current = data
    try:
        for part in parts:
            if part.startswith('['):
                index = int(part[1:-1])
                current = current[index]
            else:
                current = current[part]
        return json.dumps(current, separators=(',', ':'))
    except (KeyError, IndexError, TypeError):
        return "NOT_FOUND"
json_value = input()
data = json.loads(json_value)
q = int(input())
queries = [input() for _ in range(q)]
for query in queries:
    print(resolve_query(data, query))