import sqlite3
from typing import List
import datetime
from model import Todo
from typing import Optional

# Establish the database connection
conn = sqlite3.connect('todos.db')
c = conn.cursor()

def create_table():
    c.execute("""
        CREATE TABLE IF NOT EXISTS todos (
            task TEXT,
            category TEXT,
            date_added TEXT,
            date_completed TEXT,
            status INTEGER,
            id INTEGER PRIMARY KEY AUTOINCREMENT
        )
    """)

create_table()

def deleteall_data():
    # Connect to the database
    conn = sqlite3.connect('todos.db')
    c = conn.cursor()

    # Execute the DELETE command
    c.execute('DELETE FROM todos')

    # Commit changes and close the connection
    c.execute("DELETE FROM sqlite_sequence WHERE name='todos'")
    conn.commit()
    conn.close()

def insert_todo(todo: Todo):
    with conn:
        c.execute("""
                INSERT INTO todos (task, category, date_added, date_completed, status)
                VALUES (:task, :category, :date_added, :date_completed, :status)
                """, 
                {
                    'task': todo.task,
                    'category': todo.category,
                    'date_added': todo.date_added,
                    'date_completed': todo.date_completed,
                    'status': todo.status
                })
        todo.id = c.lastrowid
        # print(f"Inserted todo with ID: {todo.id}")
        return todo

def get_all_todo() -> List[Todo]:
    c.execute('SELECT * FROM todos')
    results = c.fetchall()
    todos = []
    for result in results:
        todos.append(Todo(*result))
    return todos

def delete_todo(id: int):
    with conn:
        c.execute("""
            DELETE FROM todos
            WHERE id = :id
            """, 
            {'id': id})

        # Check if the table is empty
        c.execute("SELECT COUNT(*) FROM todos")
        count = c.fetchone()[0]

        if count == 0:
            # Reset the auto-increment ID counter
            c.execute("DELETE FROM sqlite_sequence WHERE name='todos'")

def update_todo(id: int, task: Optional[str] = None, category: Optional[str] = None):
    with conn:
        if task is not None and category is not None:
            c.execute("""
                UPDATE todos
                SET task = :task, 
                    category = :category
                WHERE id = :id
                """, 
                {
                    'id': id,
                    'task': task,
                    'category': category
                })

        elif task is not None:
            c.execute("""
                UPDATE todos
                SET task = :task
                WHERE id = :id
                """, 
                {
                    'id': id,
                    'task': task
                })

        elif category is not None:
            c.execute("""
                UPDATE todos
                SET category = :category
                WHERE id = :id
                """, 
                {
                    'id': id,
                    'category': category
                })
        conn.commit()

def complete_todo(id: int):
    with conn:
        c.execute("""
            UPDATE todos
            SET status = 2,
                date_completed = :date_completed
            WHERE id = :id
            """, 
            {
                'id': id,
                'date_completed': datetime.datetime.now().isoformat()
            })
