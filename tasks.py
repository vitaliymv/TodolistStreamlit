import streamlit as st
from datetime import date
from utils import load_tasks, save_tasks, generate_task_id, today_str

categories = ["Work", "Myself", "Learning", "House", "Hobbies"]
priorities = ["Low", "Medium", "High"]

priority_colors = {
    "Low": "🟢",
    "Medium": "🟠",
    "High": "🔴"
}

def init_tasks_state():
    if "tasks" not in st.session_state:
        st.session_state.tasks = load_tasks()

def add_task(title, category, priority, deadline):
    tasks = st.session_state.tasks
    new_task = {
        "id": generate_task_id(tasks),
        "title": title,
        "category": category,
        "priority": priority,
        "deadline": deadline.isoformat(),
        "done": False,
        "completed_date": None
    }
    tasks.append(new_task)
    save_tasks(tasks)

def update_task(task_id, **fields):
    tasks = st.session_state.tasks
    for task in tasks:
        if task["id"] == task_id:
            was_done = task["done"]
            task.update(fields)
            if "done" in fields:
                if fields["done"] and not was_done:
                    task["completed_date"] = today_str()
                elif not fields["done"]:
                    task["completed_date"] = None
            break

    save_tasks(tasks)

def delete_task(task_id):
    tasks = st.session_state.tasks
    st.session_state.tasks = [t for t in tasks if t["id"] != task_id]
    save_tasks(st.session_state.tasks)

def render_create_form():
    st.subheader("New task")
    with st.form("new_task_form", clear_on_submit=True):
        col1, col2 = st.columns(2)

        with col1:
            title = st.text_input("Task title")
            category = st.selectbox("Category", categories)

        with col2:
            priority = st.selectbox("Priority", priorities)
            deadline = st.date_input("Deadline", value=date.today())

        submitted = st.form_submit_button("Add task", use_container_width=True)
        if submitted:
            if title.strip():
                add_task(title.strip(), category, priority, deadline)
                st.success("Task added")
                st.rerun()
            else:
                st.warning("Write task title")

def render_tasks_tab():
    init_tasks_state()
    render_create_form()
    st.divider()