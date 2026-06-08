
# A bug report as a dictionary
bug = {
    "id": "BUG-001",
    "title": "Login fails on mobile",
    "severity": "high",
    "status": "open"
}

# Read values
print(bug["title"])
print(bug["severity"])

# Update a value
bug["status"] = "in-progress"
print("Status updated to:", bug["status"])

# List of bugs
bugs = [
    {"id": "BUG-001", "severity": "high"},
    {"id": "BUG-002", "severity": "low"},
    {"id": "BUG-003", "severity": "high"},
]

# Print only high severity
for bug in bugs:
    if bug["severity"] == "high":
        print("High severity bug:", bug["id"])
