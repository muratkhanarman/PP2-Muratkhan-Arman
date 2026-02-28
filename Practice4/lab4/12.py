import json

def deep_diff(obj1, obj2, path=""):
    differences = []

    keys = set(obj1.keys()) | set(obj2.keys())

    for key in keys:
        new_path = f"{path}.{key}" if path else key

        if key not in obj1:
            differences.append((new_path, "<missing>", obj2[key]))
        elif key not in obj2:
            differences.append((new_path, obj1[key], "<missing>"))
        else:
            val1 = obj1[key]
            val2 = obj2[key]

            if isinstance(val1, dict) and isinstance(val2, dict):
                differences.extend(deep_diff(val1, val2, new_path))
            elif val1 != val2:
                differences.append((new_path, val1, val2))

    return differences
obj1 = json.loads(input())
obj2 = json.loads(input())

diffs = deep_diff(obj1, obj2)

if not diffs:
    print("No differences")
else:
    for path, old, new in sorted(diffs, key=lambda x: x[0]):
        old_str = old if old == "<missing>" else json.dumps(old, separators=(',', ':'))
        new_str = new if new == "<missing>" else json.dumps(new, separators=(',', ':'))
        print(f"{path} : {old_str} -> {new_str}")