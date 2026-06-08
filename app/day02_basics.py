# The # sign is a comment — Python ignores it
# Use it to explain your code

def add_numbers(a: int, b: int) -> int: #-> int: is a return type annotation in Python
    return a + b   # the return place will be indented= 4 spaces (tab) inside the method. Python requires this!

def greet_user(name: str, language: str = 'en') -> str:
    if language == 'he':   # if = condition
        return f'Shalom, {name}!'
    return f'Hello, {name}!'   # f-string: put variable inside {}

result = add_numbers(5, 3)
print(result)   # print = show in terminal

message = greet_user('Yaron', 'he')
print(message)

message2 = greet_user('Claude')
print(message2)

bugs = [
    {'id': 'BUG-001', 'severity': 'critical', 'status': 'open'},
    {'id': 'BUG-002', 'severity': 'low',      'status': 'open'},
    {'id': 'BUG-003', 'severity': 'high',     'status': 'closed'},
    {'id': 'BUG-004', 'severity': 'critical', 'status': 'open'},
]

open_bugs = [b for b in bugs if b['status'] == 'open']   # List comprehension: take b from bugs where status is open
print(f'Open bugs: {len(open_bugs)}')

"""
List comprehension — break it into 3 parts:

    for b in bugs            -> loop over bugs; each item is temporarily called b (a single bug dict)
    if b['status'] == 'open' -> keep only the ones where status is 'open' (optional filter)
    b (the part before for)  -> what to put in the new list — here, the whole bug b

b is just a variable name you chose for "the current item."
You could call it anything: [bug for bug in bugs] works identically.

The equivalent written as a normal loop:

    open_bugs = []
    for b in bugs:
        if b['status'] == 'open':
            open_bugs.append(b)
"""

ids = [b['id'] for b in open_bugs]   # Get just the IDs
print(f'IDs: {ids}')

critical = [b for b in bugs if b['severity'] == 'critical']   # Filter only critical
print(f'Critical count: {len(critical)}')

