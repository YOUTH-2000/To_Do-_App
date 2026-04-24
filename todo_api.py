from fastapi import FastAPI, HTTPException
from create_db import db_connection, create_database

app = FastAPI()

create_database()

# Home
@app.get("/")
def home():
    return {"message": "To-Do API is running"}

# Get all tasks
@app.get("/tasks")
def get_tasks():
    conn = db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM tasks")
    tasks = cursor.fetchall()

    cursor.close()
    conn.close()

    return tasks

# Get single task
@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    conn = db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM tasks WHERE id = %s", (task_id,))
    task = cursor.fetchone()

    cursor.close()
    conn.close()

    if not task:
        raise HTTPException(status_code = 404, detail = "Task not found")
    
    return task

# Add a new task
@app.post("/tasks")
def add_task(task_name: str):
    conn = db_connection()
    cursor = conn.cursor()

    cursor.execute("INSERT INTO tasks (name) VALUES (%s)", (task_name,))
    conn.commit()

    cursor.close()
    conn.close()

    return {"message": "Task added successfully1!"}

#Update a task
@app.put("/tasks/{task_id}")
def update_task(task_id: int, new_name: str):
    conn = db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            "UPDATE tasks SET name = %s WHERE id =%s", 
            (new_name, task_id)
        )
        conn.commit()

        if cursor.rowcount == 0:
            raise HTTPException(status_code = 404, detail = "Task not found")
        
        return {"message": "Task updated successfully!"}

        
    finally:
        cursor.close()
        conn.close()

# Mark a task as done/undone
@app.patch("/tasks/{task_id}/mark")
def mark_task(task_id: int):
    conn = db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT done FROM tasks WHERE id = %s", (task_id,))
        current_status = cursor.fetchone()

        if not current_status:
            raise HTTPException(status_code = 404, detail = "Task not found")

        new_status = not current_status[0]

        cursor.execute(
            "UPDATE tasks SET done = %s WHERE id =%s", 
            (new_status, task_id)
        )
        conn.commit()

        status = "✅ Done" if new_status else "❌ Undone"

        return {"message": f"Task {task_id} marked as {status}."}

    finally:
        cursor.close()
        conn.close()  
        
# Delete a task
@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    conn = db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("DELETE FROM tasks WHERE id =%s", (task_id,))
        conn.commit()

        if cursor.rowcount == 0:
            raise HTTPException(status_code = 404, detail = "Task not found")
        
        return {"message": "Task deleted successfully!"}

    finally:
        cursor.close()
        conn.close()
   

if __name__ == "__main__":
    import uvicorn
    uvicorn.runapp (app, host="0.0.0.0", port = 8000)

