import sys
import importlib
q = int(sys.stdin.readline())
for _ in range(q):
    module_path, attr = sys.stdin.readline().split()
    try:
        module = importlib.import_module(module_path)
    except Exception:
        print("MODULE_NOT_FOUND")
        continue

    if not hasattr(module, attr):
        print("ATTRIBUTE_NOT_FOUND")
        continue

    obj = getattr(module, attr)
    if callable(obj):
        print("CALLABLE")
    else:
        print("VALUE")