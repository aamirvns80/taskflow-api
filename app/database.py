import sqlite3
from pathlib import Path

DATABASE_PATH = Path(__file__).resolve().parent.parent/ "taskflow.db"

def get_connection(db_path=DATABASE_PATH):
    connection =sqlite3.connect(db_path)
    connection.row_factory=sqlite3.Row
    return connection

def create_tables():
    connection = get_connection()
    
    connection.execute("""
                       CREATE TABLE IF NOT EXISTS tasks(
                           id INTEGER PRIMARY KEY AUTOINCREMENT,
                           title TEXT NOT NULL,
                           description TEXT NOT NULL,
                           completed INTEGER NOT NULL DEFAULT 0
                       )
                       
                       
                       
                       
                       """)
    
    connection.commit()
    connection.close()
    
    
def add_task(title, description,completed,db_path=DATABASE_PATH):
    connection = get_connection(db_path)
    
    cursor=connection.execute("""
                       INSERT INTO tasks (title,description,completed) VALUES(?,?,?)
                       
                       """,
                       (title,description,int(completed)))
    
    connection.commit()
    task_id = cursor.lastrowid
    connection.close()
    return task_id
    
    
def get_all_tasks(db_path=DATABASE_PATH):
    connection = get_connection(db_path)
    cursor = connection.execute("""
                                SELECT * FROM tasks""")
    rows=cursor.fetchall()
    connection.close()
    return rows


def get_task_by_id(task_id,db_path=DATABASE_PATH):
    connection = get_connection(db_path)
    
    
    cursor = connection.execute("SELECT*FROM tasks WHERE id =?", (task_id,))
    
    row = cursor.fetchone()
    connection.close()
    
    return row

def update_task_status(task_id,completed,db_path=DATABASE_PATH):
    connection = get_connection(db_path)
    
    cursor = connection.execute("UPDATE tasks SET completed =? WHERE id =?",(int(completed),task_id))
    
    
    connection.commit()
    rows_updated = cursor.rowcount
    connection.close()
    return rows_updated

def delete_task_by_id(task_id,db_path=DATABASE_PATH):
    conn = get_connection(db_path)
    
    cursor = conn.execute("DELETE FROM tasks WHERE id =?", (task_id,))
    
    conn.commit()
    rows_deleted = cursor.rowcount
   
    
    conn.close()
    return rows_deleted


def patch_task(task_id,updates,db_path=DATABASE_PATH):
    allowed_fields = {"title","description","completed"}
    
    if not updates:
        raise ValueError("No fields provided for update")
    
    if not set(updates).issubset(allowed_fields):
        raise ValueError("Invalid update fields")
    
    connection = get_connection(db_path)
    fields = list(updates.keys())
    
    set_clause = ", ".join(f"{field}=?" for field in fields)
    
    values = list(updates.values())
    values.append(task_id)
    
    cursor = connection.execute(f"UPDATE tasks SET {set_clause} WHERE id =?", values)
    
    connection.commit()
    rows_updated = cursor.rowcount
    connection.close()
    
    return rows_updated
    