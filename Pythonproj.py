import sqlite3
import tkinter as tk
from tkinter import messagebox

# Database Setup
def initialize_db():
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task TEXT NOT NULL,
            status TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

# Function to add task
def add_task():
    task = task_entry.get()
    if task:
        conn = sqlite3.connect("tasks.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO tasks (task, status) VALUES (?, ?)", (task, "Pending"))
        conn.commit()
        conn.close()
        task_entry.delete(0, tk.END)
        load_tasks()
    else:
        messagebox.showwarning("Warning", "Task cannot be empty!")

# Function to load tasks
def load_tasks():
    task_list.delete(0, tk.END)
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tasks")
    tasks = cursor.fetchall()
    conn.close()
    for task in tasks:
        task_list.insert(tk.END, f"{task[0]} - {task[1]} ({task[2]})")

# Function to mark task as complete
def complete_task():
    try:
        selected = task_list.get(task_list.curselection())
        task_id = selected.split(" - ")[0]
        conn = sqlite3.connect("tasks.db")
        cursor = conn.cursor()
        cursor.execute("UPDATE tasks SET status = ? WHERE id = ?", ("Completed", task_id))
        conn.commit()
        conn.close()
        load_tasks()
    except:
        messagebox.showwarning("Warning", "Please select a task to complete!")

# Function to delete task
def delete_task():
    try:
        selected = task_list.get(task_list.curselection())
        task_id = selected.split(" - ")[0]
        conn = sqlite3.connect("tasks.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        conn.commit()
        conn.close()
        load_tasks()
    except:
        messagebox.showwarning("Warning", "Please select a task to delete!")

# GUI Setup
root = tk.Tk()
root.title("Task Manager")
root.geometry("400x500")

task_entry = tk.Entry(root, width=40)
task_entry.pack(pady=10)

add_button = tk.Button(root, text="Add Task", command=add_task)
add_button.pack()

task_list = tk.Listbox(root, width=50, height=15)
task_list.pack(pady=10)

complete_button = tk.Button(root, text="Mark Complete", command=complete_task)
complete_button.pack()

delete_button = tk.Button(root, text="Delete Task", command=delete_task)
delete_button.pack()

initialize_db()
load_tasks()
root.mainloop()
