import streamlit as st

achievements = [
    {"threshold": 10, "title": "Novice", "icon": "🥉"},
    {"threshold": 25, "title": "Productivity", "icon": "🥈"},
    {"threshold": 50, "title": "Master", "icon": "🥇"},
    {"threshold": 100, "title": "Legend", "icon": "🏆"},
]

def get_unlocked_achievement(done_count):
    return [a for a in achievements if done_count >= a["threshold"]]

def get_next_achievement(done_count):
    for a in achievements:
        if done_count >= a["threshold"]:
            return a
    return None

def render_achievement_tab(tasks):
    st.subheader("Achievements")
    done_count = len([t for t in tasks if t["done"]])
    st.write(f"Completed tasks: {done_count}")

    unlocked = get_unlocked_achievement(done_count)
    next_ach = get_next_achievement(done_count)
    cols = st.columns(len(achievements))

    for col, achievement in zip(cols, achievements):
        is_unlocked = achievement in unlocked
        with col:
            if is_unlocked:
                st.markdown(f"""
                    <div style='text-align: center; 
                        padding: 15px; 
                        border-radius: 10px; 
                        background-color: lightgreen'>
                        <div style="font-size: 40px;">
                            {achievement['icon']}
                        </div>
                        <b>{achievement['title']}</b>
                        <small>{achievement['threshold']} tasks</small>
                    </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                    <div style='text-align: center; 
                        padding: 15px; 
                        border-radius: 10px; 
                        background-color: gray'>
                        <div style="font-size: 40px;">
                            🔒
                        </div>
                        <b>{achievement['title']}</b>
                        <small>{achievement['threshold']} tasks</small>
                    </div>
                """, unsafe_allow_html=True)

    if next_ach:
        remaining = next_ach["threshold"] - done_count
        progress = done_count / next_ach["threshold"]
        st.markdown(f"To achievement: {next_ach['title']} "
                    f"Remaining {remaining} tasks")
        st.progress(min(progress, 1.0))
    else:
        st.success("All achievement unlocked")