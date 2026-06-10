from app.models import BugReport, TriageResult

SEVERITY_KEYWORDS = {
    'critical': ['crash', 'down', 'data loss', 'security', 'breach', 'cannot login'],
    'high':     ['login', 'payment', 'timeout', 'error 500', 'fail'],
    'medium':   ['slow', 'ui issue', 'display', 'wrong', 'incorrect'],
    'low':      ['typo', 'cosmetic', 'minor', 'style'],
}

CATEGORY_KEYWORDS = {
    'auth':        ['login', 'logout', 'password', 'token', 'session'],
    'payment':     ['payment', 'charge', 'invoice', 'billing'],
    'performance': ['slow', 'timeout', 'hang', 'freeze', 'latency'],
    'ui':          ['display', 'layout', 'ui', 'css', 'style', 'typo'],
    'data':        ['data loss', 'corrupt', 'missing', 'wrong value'],
}

async def triage_bug(bug: BugReport) -> TriageResult:
    text = f'{bug.title} {bug.description}'.lower()   # combine and lowercase for matching

    severity = 'low'  # default   ← start with lowest severity
    for level in ['critical', 'high', 'medium', 'low']:   # check from most severe
        if any(kw in text for kw in SEVERITY_KEYWORDS[level]):
            severity = level
            break   # stop at first match

    category = 'general'  # default   ← 
    for cat, keywords in CATEGORY_KEYWORDS.items():
        if any(kw in text for kw in keywords):
            category = cat
            break

    return TriageResult(
        bug_id=bug.id,
        suggested_severity=severity,
        category=category,
        explanation=f'Keywords matched {severity} level in {category} category',
        confidence=0.72
    )

