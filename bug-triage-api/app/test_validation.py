import sys, os
# Put the project folder (parent of app/) on the path so 'app' is importable
# no matter which directory you run this file from.
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.models import BugReport
from pydantic import ValidationError

# Test 1: Valid bug
try:
    bug = BugReport(
        title='Login crash',
        description='App crashes on mobile login page',
        severity='critical',
        reporter='yaron'
    )
    print('Valid bug created:', bug.id)
except ValidationError as e:
    print('Error:', e)

# Test 2: Invalid severity
try:
    bad_bug = BugReport(
        title='Some bug',
        description='Description here ok',
        severity='urgent',   # THIS IS WRONG — not in Literal
        reporter='test'
    )
except ValidationError as e:
    print('Caught error (expected):', e.error_count(), 'error(s)')

# Test 3: Title too short
try:
    short_bug = BugReport(
        title='Hi',   # only 2 chars — minimum is 3
        description='Description ok here',
        severity='low',
        reporter='test'
    )
except ValidationError as e:
    print('Short title error:', e.error_count(), 'error(s)')
