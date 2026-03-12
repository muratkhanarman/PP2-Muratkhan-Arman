import os

os.makedirs("test_folder", exist_ok=True)
print("Directory created")

items = os.listdir(".")
for item in items:
    print(item)