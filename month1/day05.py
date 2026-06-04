
#dataclass — a special tool ("decorator") that saves you a lot of typing when making a class that mainly holds data.
from dataclasses import dataclass

# Optional — a type hint that indicates a variable can be of a certain type or None.
from typing import Optional

# Define a BugReport class with dataclass
"""
Think of a class as a blueprint/template — here, a blueprint for "a bug report." Each line describes a piece of information (a "field") every bug will have:


Field	Type	Meaning
id	text (str)	required — e.g. "BUG-001"
title	text	required — e.g. "Login crash"
severity	text	required — e.g. "critical"
status	text	optional, defaults to "open"
assignee	text or nothing	optional, defaults to None (nobody assigned yet)


The : str part is a type hint — it documents that the value should be text.
= "open" means: if you don't provide a status, it automatically becomes "open".
The @dataclass line on top is the magic: it automatically writes the "setup" code for you, so you can create a bug just by passing values in. Without it you'd have to write a longer __init__ method by hand.
"""
@dataclass
class BugReport:
    id: str
    title: str
    severity: str
    status: str = "open"
    assignee: Optional[str] = None

    """
    A method is just a function that belongs to the class. The first parameter is always self, which means "this particular bug."

    is_critical checks: "Is this bug's severity equal to 'critical'?"
    It returns True or False (that's what -> bool means).
    self.severity = "the severity of this bug."
    """

    def is_critical(self) -> bool:
        return self.severity == "critical"

    def assign_to(self, name: str):
        self.assignee = name
        self.status = "in-progress"

# Create two bugs
bug1 = BugReport("BUG-001", "Login crash", "critical")
bug2 = BugReport("BUG-002", "Slow load", "low")

print(bug1.title, "is critical:", bug1.is_critical())

# Only assign the bug if it is critical
if bug1.is_critical():
    bug1.assign_to("Yaron")
    print("Assigned to:", bug1.assignee)
else:
    print(bug1.title, "is not critical, no assignment needed")


if bug2.is_critical():
    bug2.assign_to("Hanan")
    print("Assigned to:", bug2.assignee)
else:
    print(bug2.title, "is not critical, no assignment needed")