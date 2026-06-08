
import json

# Write a list of bugs to a JSON file
bugs = [
    {"id": "BUG-001", "title": "Login fails", "status": "open"},
    {"id": "BUG-002", "title": "Page crashes", "status": "closed"},
    {"id": "BUG-003", "title": "Feature not working", "status": "open"}

]

with open("bugs.json", "w") as file:
    json.dump(bugs, file, indent=2)
print("Saved!")

# Read it back
with open("bugs.json", "r") as file:
    loaded_bugs = json.load(file)

print("Loaded", len(loaded_bugs), "bugs")
for bug in loaded_bugs:
    print(bug["id"], "—", bug["title"])





"""" Block of remarkable code:
indent parameter in json.dump() is used to pretty-print the JSON data with the specified number of spaces for indentation. This makes the JSON file more human-readable by adding line breaks and indentation to the output. For example, indent=2 will format the JSON with 2 spaces of indentation for each level of nesting.
With indent=2 still, the file just gets a third block:
  {
    "id": "BUG-001",
    "title": "Login fails",
    "status": "open"
  },
  {
    "id": "BUG-002",
    "title": "Page crashes",
    "status": "closed"
  },
  {
    "id": "BUG-003",
    "title": "Button missing",
    "status": "open"
  }
]

Without indent (the default, indent=None) — everything is crammed onto one line:
[{"id": "BUG-001", "title": "Login fails", "status": "open"}, {"id": "BUG-002", "ti
"""
