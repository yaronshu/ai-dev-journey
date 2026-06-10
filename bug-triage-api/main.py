from contextlib import asynccontextmanager
from typing import Optional
import sqlite3

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware

from app.models import BugReport, TriageResult, Defect, DefectUpdate
from app.services import triage_bug
from app.database import init_db, get_db


@asynccontextmanager
async def lifespan(app: FastAPI):   # runs once on startup (and shutdown)
    init_db()   # make sure the defects table exists before serving requests
    yield

app = FastAPI(   # create the FastAPI application
    title='Bug Triage API',
    description='AI-powered bug severity classification',
    version='0.2.0',
    lifespan=lifespan
)

app.add_middleware(CORSMiddleware, allow_origins=['*'],   # allow browser to call this API
    allow_methods=['*'], allow_headers=['*'])

@app.get('/health')
async def health_check():
    return {'status': 'ok', 'version': '0.2.0'}   # any dict becomes JSON automatically

@app.post('/triage', response_model=TriageResult)
async def triage_endpoint(bug: BugReport, db: sqlite3.Connection = Depends(get_db)):
    try:
        result = await triage_bug(bug)
        # Save the report + triage result together as one row in the defects table.
        db.execute(
            '''INSERT INTO defects
               (id, title, description, severity, reporter, status, created_at,
                category, suggested_severity, suggested_assignee, explanation, confidence)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
            (bug.id, bug.title, bug.description, bug.severity, bug.reporter,
             'open', bug.created_at.isoformat(),
             result.category, result.suggested_severity, result.suggested_assignee,
             result.explanation, result.confidence)
        )
        db.commit()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))   # proper error

@app.get('/defects', response_model=list[Defect])
async def list_defects(severity: Optional[str] = None,   # ?severity=high
                       status: Optional[str] = None,     # ?status=open
                       db: sqlite3.Connection = Depends(get_db)):
    # Build the query, adding a filter only for the parameters that were sent.
    query = 'SELECT * FROM defects'
    conditions, params = [], []
    if severity:
        conditions.append('severity = ?'); params.append(severity)
    if status:
        conditions.append('status = ?'); params.append(status)
    if conditions:
        query += ' WHERE ' + ' AND '.join(conditions)
    query += ' ORDER BY created_at DESC'
    rows = db.execute(query, params).fetchall()
    return [dict(row) for row in rows]   # sqlite3.Row -> dict -> validated by Defect

@app.get('/defects/{defect_id}', response_model=Defect)
async def get_defect(defect_id: str, db: sqlite3.Connection = Depends(get_db)):
    row = db.execute('SELECT * FROM defects WHERE id = ?', (defect_id,)).fetchone()
    if row is None:
        raise HTTPException(status_code=404, detail=f'Defect {defect_id} not found')
    return dict(row)

@app.put('/defects/{defect_id}', response_model=Defect)
async def update_defect(defect_id: str, updates: DefectUpdate,
                        db: sqlite3.Connection = Depends(get_db)):
    row = db.execute('SELECT * FROM defects WHERE id = ?', (defect_id,)).fetchone()
    if row is None:
        raise HTTPException(status_code=404, detail=f'Defect {defect_id} not found')

    # exclude_unset = only the fields the caller actually sent get changed.
    # The keys come from DefectUpdate's fixed field set (not raw user text), so
    # building the column list this way is safe; values stay parameterized.
    changes = updates.model_dump(exclude_unset=True)
    if changes:
        assignments = ', '.join(f'{field} = ?' for field in changes)
        params = list(changes.values()) + [defect_id]
        db.execute(f'UPDATE defects SET {assignments} WHERE id = ?', params)
        db.commit()

    updated = db.execute('SELECT * FROM defects WHERE id = ?', (defect_id,)).fetchone()
    return dict(updated)
