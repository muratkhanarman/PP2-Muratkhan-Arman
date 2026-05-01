import json
data = {
    "name": "Aman",
    "age": 19,
    "skills": ["Python", "Math"]
}
json_string = json.dumps(data)
print("JSON string:", json_string)
parsed_data = json.loads(json_string)
print("Parsed name:", parsed_data["name"])
with open("data.json", "w") as f:
    json.dump(data, f)
with open("data.json", "r") as f:
    file_data = json.load(f)
print("Read from file:", file_data)