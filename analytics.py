import streamlit as st
import pandas as pd
import plotly.express as px

def render_metrics(tasks):
    total = len(tasks)
    done = len([t for t in tasks if t["done"]])
    percent = round((done / total) * 100, 1) if total > 0 else 0

    c1, c2, c3 = st.columns(3)
    c1.metric("Total tasks", total)
    c2.metric("Done tasks", done)
    c3.metric("Percent of completed tasks", f"{percent}%")

def render_charts(tasks):
    if not tasks:
        st.info("No data for chart")
        return
    df = pd.DataFrame(tasks)
    df["status"] = df["done"].apply(lambda t: "Completed" if t else "Not completed")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("#### Tasks by category")
        category_counts = df["category"].value_counts().reset_index()
        category_counts.columns = ["category", "count"]
        fig_cat = px.pie(
            category_counts,
            "category",
            "count",
            hole=0.6
        )
        st.plotly_chart(fig_cat, use_container_width=True)
    with c2:
        st.markdown("#### Tasks by status")
        status_counts = df["status"].value_counts().reset_index()
        status_counts.columns = ["status", "count"]
        fig_stat = px.pie(
            status_counts,
            "status",
            "count",
            hole=0.6,
            color="status",
            color_discrete_map={"Completed": "lightgreen", "Not completed": "coral"}
        )
        st.plotly_chart(fig_stat, use_container_width=True)

    st.markdown("#### Tasks by priority")
    priority_order = ["Low", "Medium", "High"]
    priority_counts = df[
        "priority"
    ].value_counts().reindex(priority_order, fill_value=0).reset_index()
    priority_counts.columns = ["priority", "count"]
    fig_pr = px.bar(
        priority_counts,
        "priority",
        "count",
        color="priority",
        color_discrete_map={
            "Low": "lightgreen",
            "Medium": "coral",
            "High": "crimson"
        },
        labels={
            "priority": "Priority",
            "count": "Tasks count"
        }
    )
    st.plotly_chart(
        fig_pr,
        use_container_width=True
    )

def render_analytics_tab(tasks):
    st.subheader("Analytics")
    render_metrics(tasks)
    st.divider()
    render_charts(tasks)