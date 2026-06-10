import pytest
from fastapi.testclient import TestClient

import app.database as database
import main

# These are INTEGRATION tests: they drive the real app over HTTP (via TestClient)
# and therefore DO go through the database. To make sure they never touch your
# real bugs.db, the `client` fixture points the app at a fresh throwaway file.


@pytest.fixture
def client(tmp_path, monkeypatch):
    # tmp_path is a unique temp folder per test -> each test gets its own empty DB.
    test_db = tmp_path / 'test.db'
    # get_connection() reads database.DB_PATH at call time, so swapping it here
    # redirects BOTH init_db() and the get_db dependency to the temp database.
    monkeypatch.setattr(database, 'DB_PATH', str(test_db))
    # Using TestClient as a context manager runs the app's lifespan startup,
    # which calls init_db() and creates the defects table in the temp DB.
    with TestClient(main.app) as c:
        yield c


def make_payload(title='Login crash on mobile',
                 description='App crashes on the login page when tapping submit',
                 severity='high', reporter='yaron'):
    return {'title': title, 'description': description,
            'severity': severity, 'reporter': reporter}


def test_list_defects_starts_empty(client):
    res = client.get('/defects')
    assert res.status_code == 200
    assert res.json() == []   # fresh temp DB -> nothing stored yet


def test_triage_persists_and_can_be_fetched(client):
    # POST /triage should triage the bug AND save it.
    res = client.post('/triage', json=make_payload())
    assert res.status_code == 200
    defect_id = res.json()['bug_id']

    # The saved row should now be retrievable through GET /defects/{id}.
    got = client.get(f'/defects/{defect_id}')
    assert got.status_code == 200
    defect = got.json()
    assert defect['title'] == 'Login crash on mobile'
    assert defect['reporter'] == 'yaron'
    assert defect['status'] == 'open'   # default status on creation


def test_filter_by_status(client):
    client.post('/triage', json=make_payload())
    assert len(client.get('/defects?status=open').json()) == 1   # new defects are 'open'
    assert client.get('/defects?status=closed').json() == []     # nothing closed yet


def test_filter_by_severity(client):
    client.post('/triage', json=make_payload(severity='high'))
    client.post('/triage', json=make_payload(title='Tiny typo',
        description='Small cosmetic typo in the footer text', severity='low'))
    assert len(client.get('/defects?severity=high').json()) == 1
    assert len(client.get('/defects?severity=low').json()) == 1
    assert len(client.get('/defects').json()) == 2


def test_update_defect_changes_values(client):
    defect_id = client.post('/triage', json=make_payload()).json()['bug_id']

    res = client.put(f'/defects/{defect_id}',
                     json={'status': 'in_progress', 'suggested_assignee': 'backend-team'})
    assert res.status_code == 200
    updated = res.json()
    assert updated['status'] == 'in_progress'
    assert updated['suggested_assignee'] == 'backend-team'

    # The change persisted: the defect now shows up under status=in_progress.
    assert len(client.get('/defects?status=in_progress').json()) == 1


def test_get_missing_defect_returns_404(client):
    assert client.get('/defects/does-not-exist').status_code == 404


def test_update_missing_defect_returns_404(client):
    assert client.put('/defects/nope', json={'status': 'closed'}).status_code == 404


def test_does_not_touch_real_bugs_db(client):
    # Sanity check that the fixture isolation works: the app is pointed at the
    # temp file, NOT the project's real bugs.db.
    assert database.DB_PATH.endswith('test.db')
    client.post('/triage', json=make_payload())
    assert len(client.get('/defects').json()) == 1   # only this test's data
