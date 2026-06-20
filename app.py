import streamlit as st

st.set_page_config(page_title="Todo manager", layout="wide")

st.title("Todo manager")
st.caption("Manage your tasks easy")

tabs = st.tabs(["Tasks", "Analytics", "Achievements", "Export", "Heatmap"])
