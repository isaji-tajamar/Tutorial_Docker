import os
import psycopg2
from fastapi import FastAPI
from pydantic import BaseModel, Field

class NoteCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)

app = FastAPI(title="Compose Demo API")

def get_conn():
    return psycopg2.connect(
        host=os.getenv("DB_HOST", "db"),
        port=int(os.getenv("DB_PORT", "5432")),
        dbname=os.getenv("DB_NAME", "appdb"),
        user=os.getenv("DB_USER", "app"),
        password=os.getenv("DB_PASSWORD", "pass"),
    )

@app.on_event("startup")
def init_db():
    # Crea tabla y mete datos si está vacía
    conn = get_conn()
    try:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS notes (
                    id SERIAL PRIMARY KEY,
                    title TEXT NOT NULL
                );
            """)
            cur.execute("SELECT COUNT(*) FROM notes;")
            (count,) = cur.fetchone()
            if count == 0:
                cur.execute("INSERT INTO notes (title) VALUES (%s), (%s), (%s);",
                            ("Hola Docker Compose", "FastAPI + Postgres", "Nginx sirviendo la web"))
        conn.commit()
    finally:
        conn.close()

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/notes")
def list_notes():
    conn = get_conn()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT id, title FROM notes ORDER BY id;")
            rows = cur.fetchall()
        return [{"id": r[0], "title": r[1]} for r in rows]
    finally:
        conn.close()
        
@app.post("/notes", status_code=201)
def create_note(note: NoteCreate):
    title = note.title.strip()
    if not title:
        return {"error": "title vacío"}

    conn = get_conn()
    try:
        with conn.cursor() as cur:
            cur.execute("INSERT INTO notes (title) VALUES (%s) RETURNING id, title;", (title,))
            row = cur.fetchone()
        conn.commit()
        return {"id": row[0], "title": row[1]}
    finally:
        conn.close()

