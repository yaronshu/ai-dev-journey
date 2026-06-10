import pytest
from app.models import BugReport
from app.services import triage_bug

def make_bug(title, description, severity='low', reporter='tester'):   # helper to create bugs quickly
    return BugReport(title=title, description=description,
                     severity=severity, reporter=reporter)

@pytest.mark.asyncio   # mark: this test is async
async def test_crash_keywords_give_critical():
    # Arrange — prepare the data   ← 
    bug = make_bug(
        title='App crash on login',
        description='Complete crash every time user tries to login, data loss')
    # Act — run the code   ← 
    result = await triage_bug(bug)
    # Assert — check the result   ← 
    assert result.suggested_severity == 'critical'   # THIS must be true or test fails

@pytest.mark.asyncio
async def test_typo_gives_low():
    bug = make_bug('Minor typo', 'There is a small cosmetic typo in footer text')
    result = await triage_bug(bug)
    assert result.suggested_severity == 'low'

@pytest.mark.asyncio
async def test_payment_gives_high():
    bug = make_bug('Payment fail', 'Payment fails when checkout with credit card')
    result = await triage_bug(bug)
    assert result.suggested_severity == 'high'
    assert result.category == 'payment'

@pytest.mark.asyncio
async def test_confidence_is_valid():
    bug = make_bug('Any bug', 'Description of the bug goes here properly')
    result = await triage_bug(bug)
    assert 0.0 <= result.confidence <= 1.0   # confidence must be between 0 and 1

def test_bug_model_validation():
    from pydantic import ValidationError   # import inside test — OK
    with pytest.raises(ValidationError):
        make_bug('Ab', 'short', 'invalid_severity')
        # 'Ab' is too short (min 3), severity is invalid   
