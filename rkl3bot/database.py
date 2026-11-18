import sqlite3,os,datetime
from config import DB_PATH,DATA_DIR
def get_conn():
    os.makedirs(DATA_DIR,exist_ok=True)
    c=sqlite3.connect(DB_PATH); c.row_factory=sqlite3.Row; return c
def init_db():
    with get_conn() as c:
        c.executescript("""
CREATE TABLE IF NOT EXISTS users(user_id INTEGER PRIMARY KEY,username TEXT,first_name TEXT,created_at TEXT);
CREATE TABLE IF NOT EXISTS notes(id INTEGER PRIMARY KEY AUTOINCREMENT,user_id INTEGER,text TEXT,created_at TEXT);
CREATE TABLE IF NOT EXISTS homework(id INTEGER PRIMARY KEY AUTOINCREMENT,user_id INTEGER,text TEXT,due_date TEXT,created_at TEXT,done INTEGER DEFAULT 0);
CREATE TABLE IF NOT EXISTS schedule_cache(id INTEGER PRIMARY KEY CHECK(id=1),payload TEXT,updated_at TEXT);
CREATE TABLE IF NOT EXISTS schedule_history(date TEXT PRIMARY KEY,payload TEXT,saved_at TEXT);
CREATE TABLE IF NOT EXISTS morning_sent(date TEXT,user_id INTEGER,UNIQUE(date,user_id));
CREATE TABLE IF NOT EXISTS lesson_notifications(date TEXT,user_id INTEGER,lesson_no INTEGER,UNIQUE(date,user_id,lesson_no));
""")
def upsert_user(u):
    with get_conn() as c:
        c.execute("INSERT INTO users(user_id,username,first_name,created_at) VALUES(?,?,?,?) ON CONFLICT(user_id) DO UPDATE SET username=excluded.username,first_name=excluded.first_name",(u.id,u.username,u.first_name,datetime.datetime.now().isoformat()))
def add_note(uid,text):
    with get_conn() as c: c.execute("INSERT INTO notes(user_id,text,created_at) VALUES(?,?,?)",(uid,text,datetime.datetime.now().isoformat()))
def get_notes(uid):
    with get_conn() as c: return c.execute("SELECT id,text,created_at FROM notes WHERE user_id=? ORDER BY id DESC",(uid,)).fetchall()
def delete_note(uid,nid):
    with get_conn() as c:
        cur=c.execute("DELETE FROM notes WHERE id=? AND user_id=?",(nid,uid)); return cur.rowcount>0
def add_homework(uid,text,due):
    with get_conn() as c: c.execute("INSERT INTO homework(user_id,text,due_date,created_at) VALUES(?,?,?,?)",(uid,text,due,datetime.datetime.now().isoformat()))
def get_homework(uid,done=None):
    q="SELECT id,text,due_date,created_at,done FROM homework WHERE user_id=?"; a=[uid]
    if done is not None: q+=" AND done=?"; a.append(done)
    q+=" ORDER BY id DESC"
    with get_conn() as c: return c.execute(q,a).fetchall()
def set_homework_done(uid,nid,done):
    with get_conn() as c:
        cur=c.execute("UPDATE homework SET done=? WHERE id=? AND user_id=?",(done,nid,uid)); return cur.rowcount>0
def delete_homework(uid,nid):
    with get_conn() as c:
        cur=c.execute("DELETE FROM homework WHERE id=? AND user_id=?",(nid,uid)); return cur.rowcount>0
def get_cache():
    with get_conn() as c: return c.execute("SELECT payload,updated_at FROM schedule_cache WHERE id=1").fetchone()
def set_cache(payload):
    with get_conn() as c: c.execute("INSERT INTO schedule_cache(id,payload,updated_at) VALUES(1,?,?) ON CONFLICT(id) DO UPDATE SET payload=excluded.payload,updated_at=excluded.updated_at",(payload,datetime.datetime.now().isoformat()))
def clear_cache():
    with get_conn() as c: c.execute("DELETE FROM schedule_cache WHERE id=1")
def save_history(date,payload):
    with get_conn() as c: c.execute("INSERT INTO schedule_history(date,payload,saved_at) VALUES(?,?,?) ON CONFLICT(date) DO UPDATE SET payload=excluded.payload,saved_at=excluded.saved_at",(date,payload,datetime.datetime.now().isoformat()))
def get_history(date):
    with get_conn() as c: return c.execute("SELECT payload FROM schedule_history WHERE date=?",(date,)).fetchone()
def mark_morning(date,uid):
    with get_conn() as c:
        try: c.execute("INSERT INTO morning_sent(date,user_id) VALUES(?,?)",(date,uid)); return True
        except Exception: return False
def get_users():
    with get_conn() as c: return c.execute("SELECT user_id FROM users").fetchall()
def mark_lesson_notified(date,uid,no):
    with get_conn() as c:
        try: c.execute("INSERT INTO lesson_notifications(date,user_id,lesson_no) VALUES(?,?,?)",(date,uid,no)); return True
        except Exception: return False
