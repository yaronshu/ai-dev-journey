"""
Bug Tracker - Day 6
A simple command-line bug tracker.

Features:
  - add_bug(id, title, severity)  -> add a bug to the list
  - get_open_bugs()               -> return only the open bugs
  - save_to_file(filename)        -> save all bugs to a JSON file
  - load_from_file(filename)      -> load bugs from a JSON file
  - Main loop: let the user add bugs and view them
"""

import json
from dataclasses import dataclass, asdict
from typing import Optional


@dataclass
class BugReport:
    id: str
    title: str
    severity: str = "unknown"   # default so older saved bugs (without severity) still load
    status: str = "open"
    assignee: Optional[str] = None


# This list holds all the bugs while the program is running
bugs = []


def add_bug(id: str, title: str, severity: str):
    """Create a BugReport and add it to the bugs list."""
    bug = BugReport(id, title, severity)
    bugs.append(bug)
    print(f"Added {bug.id}: {bug.title} ({bug.severity})")


def get_open_bugs():
    """Return a list of only the bugs whose status is 'open'."""
    return [bug for bug in bugs if bug.status == "open"]


def save_to_file(filename: str):
    """Save all bugs to a JSON file."""
    # asdict() turns each BugReport into a plain dictionary so json can write it
    data = [asdict(bug) for bug in bugs]
    with open(filename, "w") as file:
        json.dump(data, file, indent=2)
    print(f"Saved {len(bugs)} bugs to {filename}")


def load_from_file(filename: str):
    """Load bugs from a JSON file into the bugs list."""
    global bugs
    try:
        with open(filename, "r") as file:
            data = json.load(file)
        # Rebuild a BugReport object from each dictionary.
        # We keep only fields the class actually knows about, so unexpected
        # or missing fields in older files don't crash the program.
        known_fields = {"id", "title", "severity", "status", "assignee"}
        bugs = [
            BugReport(**{k: v for k, v in item.items() if k in known_fields})
            for item in data
        ]
        print(f"Loaded {len(bugs)} bugs from {filename}")
    except FileNotFoundError:
        print(f"No file named {filename} yet - starting with an empty list")


def show_bugs(bug_list):
    """Print a list of bugs in a readable way."""
    if not bug_list:
        print("  (no bugs to show)")
        return
    for bug in bug_list:
        print(f"  {bug.id} | {bug.title} | {bug.severity} | {bug.status}")


def change_status(id: str, new_status: str):
    """Find a bug by its id and update its status."""
    for bug in bugs:
        if bug.id == id:
            bug.status = new_status
            print(f"Updated {bug.id} -> status is now '{bug.status}'")
            return
    # If the loop finishes without finding the id, there was no match
    print(f"No bug found with id {id}")


# ---------------------------------------------------------------------------
# Main loop
# ---------------------------------------------------------------------------
def main():
    filename = "bugs.json"
    load_from_file(filename)

    while True:
        print("\n=== Bug Tracker ===")
        print("1. Add a bug")
        print("2. Show all bugs")
        print("3. Show open bugs only")
        print("4. Change a bug's status")
        print("5. Save and quit")

        choice = input("Choose an option (1-5): ").strip()

        if choice == "1":
            id = input("  Bug id (e.g. BUG-001): ").strip()
            title = input("  Title: ").strip()
            severity = input("  Severity (low/medium/critical): ").strip()
            add_bug(id, title, severity)

        elif choice == "2":
            print("\nAll bugs:")
            show_bugs(bugs)

        elif choice == "3":
            print("\nOpen bugs:")
            show_bugs(get_open_bugs())

        elif choice == "4":
            id = input("  Bug id to update: ").strip()
            new_status = input("  New status (open/in-progress/closed): ").strip()
            change_status(id, new_status)

        elif choice == "5":
            save_to_file(filename)
            print("Goodbye!")
            break

        else:
            print("Invalid choice, please type a number from 1 to 5.")


# This runs main() only when you execute this file directly
if __name__ == "__main__":
    main()
