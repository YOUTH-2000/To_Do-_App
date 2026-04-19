from create_db import db_connection, create_database

create_database()
def add_task():
    task_name = input("Enter task name: ")

    conn = db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERRT INTO tasks (name) VALUES (%s)", (task_name,))

    conn.commit()
    conn.close()
    cursor.close()

def view_tasks():
    conn = db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tasks")
    tasks = cursor.fetchall()
    if not tasks:
        print("No tasks to show.")
    else:
        for i, task in enumerate(tasks):
            status = "✅ Done" if task["done"] else "❌ Undone"
            print(f"{i + 1}. {task['name']} - {status}")
     
    conn.close()
    cursor.close()

def update_task():
    task_number = int(input("Enter task number to update: "))
    new_name = input("Enter new task name: ")

    conn = db_connection()
    cursor = conn.cursor()
    cursor.execute("UDATE tasks SET name = %s WHERE id = %d", (new_name, task_number))

    conn.commit()
    conn.close()
    cursor.close()
     
def mark_task():
    mark_number = int(input("Enter task number to mark (Done/Undone): "))

    conn = db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT done FOM tasks WHERRE id = %d", (mark_number))
    current_status = cursor.fetchone()
    if current_status:
        new_status = not current_status[0]
        cursor.execute("UPDATE tasks SET done = %s WHERE id = %d", (new_status, mark_number))
        conn.commit()
        
        status = "✅ Done" if new_status else "❌ Undone"
        print(f"Task {mark_number} markes as {status}.")
    else:
        print("Task not found.")

    conn.close()
    cursor.close()

def delete_task():
    delete_number  = int(input("Enter task number to delete: "))

    conn = db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tasks WHERE id = %d", (delete_number,))

    conn.commit()
    conn.close()
    cursor.close()

def main():
    while True:
        print("\n------ To-Do-List ------")
        print("1. Add Task")
        print("2. View Tasks")
        print("3. Update Task")
        print("4. Mark Task (Done/Undone)")
        print("5. Delete Task")
        print("6. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            add_task()
        elif choice == '2':
            view_tasks()
        elif choice == '3':
            update_task()
        elif choice == '4':
            mark_task()
        elif choice == '5':
            delete_task()
        elif choice == '6':
            print("Existing the program. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")
                

if __name__ == "__main__":
    tasks = []  
    main()


