from dataclasses import dataclass, field
from typing import Optional, Literal
from datetime import datetime

@dataclass   # decorator — tells Python: make this a dataclass
class BugReport:
    id: str   # field: must be string
    title: str   # field: must be string
    description: str   # field: must be string
    severity: Literal['low', 'medium', 'high', 'critical']   # only these 4 values allowed
    reporter: str   # who reported it
    created_at: datetime = field(default_factory=datetime.now)   # auto-set to now if not given
    status: str = 'open'   # default value = 'open'

    def is_critical(self) -> bool:
        return self.severity == 'critical'   # method: returns True or False

    def __str__(self) -> str:
        return f'[{self.severity.upper()}] {self.title}'

"""
__str__(self) is a special method (also called a "dunder method" — short for double underscore). It defines what your object looks like when it's turned into a string — for example, when you print() it or call str() on it.

In your models.py:18-19:


def __str__(self) -> str:
    return f'[{self.severity.upper()}] {self.title}'
This says: "Whenever someone converts a BugReport to text, show it as [SEVERITY] title."

Without __str__, printing an object gives you the useless default:


bug = BugReport(id='BUG-001', title='Login fails', description='...', severity='critical', reporter='Yaron')
print(bug)
# <app.models.BugReport object at 0x000001F2A3B4C5D0>   ← ugly, unhelpful
With your __str__, the same print becomes:


print(bug)
# [CRITICAL] Login fails   ← clean and readable
Breaking down the pieces:

Piece	Meaning
__str__	The dunder name Python looks for when making a string. You don't call it directly — print() / str() call it for you.
self	The current object (this specific bug). Lets you read its fields like self.title.
-> str	Return-type hint — __str__ must return a string.
self.severity.upper()	Takes the severity (e.g. 'critical') and uppercases it → 'CRITICAL'.
It's the same idea as is_critical(self) right above it — both are methods (functions that belong to the class and take self). The difference is that __str__ is a special name Python already knows about, so it gets called automatically by print(), str(), and f-strings.

Related one you'll see often: __repr__ (the "developer-facing" string, shown in the debugger / REPL), and __init__ (the constructor — though @dataclass writes that one for you automatically).
"""

if __name__ == '__main__':
    bug = BugReport(   # create a BugReport object
        id='BUG-001',
        title='Login page crashes',
        description='App crashes on mobile login',
        severity='critical',
        reporter='yaron'
    )
    print(bug)
    print('Is critical:', bug.is_critical())
    print('Created at:', bug.created_at)


    """
    if __name__ == '__main__': is Python's way of asking: "Am I being run directly, or imported by another file?" The code inside only runs in the first case.

How it works: Every Python file has a built-in variable called __name__. Python sets it automatically:

When you run the file directly (python models.py) → __name__ is set to the string '__main__'.
When the file is imported by another file (import models) → __name__ is set to the module's name, 'models'.
So in your models.py:54:


if __name__ == '__main__':
    bug = BugReport(...)   # demo / test code
    print(bug)
This block runs only when you do python app/models.py directly. The BugReport demo prints out. But if another file does from app.models import BugReport, that demo code is skipped — you just get the BugReport class, no printing.
"""
