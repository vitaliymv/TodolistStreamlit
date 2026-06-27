import streamlit as st
from tasks import render_tasks_tab
from analytics import render_analytics_tab
import json
st.set_page_config(page_title="Todo manager", layout="wide")

st.title("Todo manager")
st.caption("Manage your tasks easy")

tabs = st.tabs(["Tasks", "Analytics", "Achievements", "Export", "Heatmap"])

def render_export_tasks(tasks):
    st.subheader("Export to JSON")
    if not tasks:
        st.info("No tasks to export")
        return
    st.write(f"Ready to export {len(tasks)} tasks")
    json_data = json.dumps(tasks, ensure_ascii=False, indent=4)
    st.download_button(
        "Download JSON",
        json_data,
        "tasks.json",
        "application/json",
        use_container_width=True
    )

with tabs[0]:
    render_tasks_tab()

with tabs[1]:
    render_analytics_tab(st.session_state.tasks)

with tabs[3]:
    render_export_tasks(st.session_state.tasks)