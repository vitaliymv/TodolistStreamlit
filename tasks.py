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

def render_filters(tasks):
    st.subheader("Search and filters")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        search_query = st.text_input("Search by title")
    with col2:
        filter_category = st.selectbox("Category", ["All"] + categories)
    with col3:
        filter_status = st.selectbox("Status", ["All", "Completed", "Not completed"])
    with col4:
        filter_priority = st.selectbox("Priority", ["All"] + priorities)

    filtered = tasks
    if search_query.strip():
        filtered = [
            t for t in filtered if search_query.strip().lower() in t["title"].lower()
        ]
    if filter_category != "All":
        filtered = [
            t for t in filtered if t["category"] == filter_category
        ]
    if filter_status != "All":
        was_done = filter_status == "Completed"
        filtered = [t for t in tasks if t["done"] == was_done]

    if filter_priority != "All":
        filtered = [t for t in filtered if t["priority"] == filter_priority]

    return filtered

def render_task_list(tasks):
    st.subheader(f"Tasks {len(tasks)}")
    if not tasks:
        st.info("Not tasks found")
        return
    for task in tasks:
        status_icon = "✅" if task["done"] else "❌"
        pr_icon = priority_colors.get(task["priority"])
        with st.expander(
            f"{status_icon} {task['title']}\t"
            f"{task['category']}\t"
            f"{pr_icon}{task['priority']}\t"
            f"{task['deadline']}"
        ):
            edit_col1, edit_col2 = st.columns(2)
            with edit_col1:
                new_title = st.text_input(
                    "Task title",
                    value=task["title"],
                    key=f"title_{task['id']}"
                )
                new_category = st.selectbox(
                    "Category",
                    categories,
                    index=categories.index(task["category"]),
                    key=f"cat_{task['id']}"
                )
            with edit_col2:
                new_priority = st.selectbox(
                    "Priority",
                    priorities,
                    index=priorities.index(task["priority"]),
                    key=f"pr_{task['id']}"
                )
                new_done = st.checkbox(
                    "Complete", value=task["done"], key=f"done_{task['id']}"
                )

            btn_col1, btn_col2 = st.columns(2)
            with btn_col1:
                if st.button("Save", key=f"save_{task['id']}", use_container_width=True):
                    update_task(
                        task["id"],
                        title=new_title.strip() if new_title.strip else task["title"],
                        category=new_category,
                        priority=new_priority,
                        done=new_done
                    )
                    st.rerun()
            with btn_col2:
                if st.button("Delete", key=f"delete_{task['id']}", use_container_width=True):
                    delete_task(task["id"])
                    st.rerun()


def render_tasks_tab():
    init_tasks_state()
    render_create_form()
    st.divider()
    filtered_tasks = render_filters(st.session_state.tasks)
    st.divider()
    render_task_list(filtered_tasks)