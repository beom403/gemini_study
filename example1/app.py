import streamlit as st
import pandas as pd
import json
import os
import altair as alt

st.set_page_config(page_title="Firmware Test Results", layout="wide")

st.title("📟 Firmware Version Test Dashboard")
st.markdown("---")

# Load data from the 'data' directory relative to this script
current_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(current_dir, 'data')
json_files = [f for f in os.listdir(data_dir) if f.endswith('.json')]
json_files.sort(reverse=True)

# Map version to filename for easy lookup
ver_to_file = {}
for f in json_files:
    with open(os.path.join(data_dir, f), 'r') as jf:
        d = json.load(jf)
        ver_to_file[d['firmware_version']] = f

# Initialize session state for the selected file
if 'selected_file' not in st.session_state:
    st.session_state.selected_file = json_files[0]

# Historical Pass Rate Chart
st.write("### 📈 Pass Rate Trend")
st.info("💡 Click a bar in the chart to see detailed test results for that version.")

all_data = []
for f in json_files:
    with open(os.path.join(data_dir, f), 'r') as jf:
        d = json.load(jf)
        res = d['results']
        pass_rate = (len([r for r in res if r['status'] == 'Pass']) / len(res)) * 100
        all_data.append({
            "Version": d['firmware_version'], 
            "Pass Rate (%)": pass_rate
        })

chart_df = pd.DataFrame(all_data).sort_values("Version")

# Altair Chart with Selection
# Highlight the bar if it matches the current selection in session state
selection = alt.selection_point(fields=['Version'], name='selector')

chart = alt.Chart(chart_df).mark_bar().encode(
    x=alt.X('Version:N', sort='ascending'),
    y='Pass Rate (%):Q',
    color=alt.condition(
        alt.datum.Version == (st.session_state.selected_file.replace('test_v', '').replace('.json', '')),
        alt.value('steelblue'),
        alt.value('lightgray')
    ),
    tooltip=['Version', 'Pass Rate (%)']
).add_params(
    selection
).properties(
    height=300
)

# Handle chart selection
event_dict = st.altair_chart(chart, use_container_width=True, on_select="rerun")

# If a bar is clicked, update session state
if event_dict and "selection" in event_dict and "selector" in event_dict["selection"]:
    selected_points = event_dict["selection"]["selector"]
    if selected_points:
        clicked_version = selected_points[0].get("Version")
        if clicked_version in ver_to_file:
            st.session_state.selected_file = ver_to_file[clicked_version]
            st.rerun()

# Sidebar selection
st.sidebar.header("Filter")

# Selectbox uses session state
selected_file = st.sidebar.selectbox(
    "Select Firmware Version", 
    json_files, 
    index=json_files.index(st.session_state.selected_file),
    key="selectbox_sync"
)

# If sidebar changes, update session state
if selected_file != st.session_state.selected_file:
    st.session_state.selected_file = selected_file
    st.rerun()

st.markdown("---")

# Display Details
if st.session_state.selected_file:
    file_path = os.path.join(data_dir, st.session_state.selected_file)
    with open(file_path, 'r') as f:
        data = json.load(f)

    # Header Information
    col1, col2 = st.columns(2)
    with col1:
        st.subheader(f"Version: {data['firmware_version']}")
    with col2:
        st.subheader(f"Test Date: {data['test_date']}")

    # Results Table
    st.write("### 📋 Test Details")
    df = pd.DataFrame(data['results'])
    
    # Styling the status column
    def color_status(val):
        color = 'green' if val == 'Pass' else 'red'
        return f'color: {color}; font-weight: bold'

    st.table(df.style.applymap(color_status, subset=['status']))

    # Statistics Summary
    total_tests = len(df)
    pass_count = len(df[df['status'] == 'Pass'])
    fail_count = len(df[df['status'] == 'Fail'])

    st.write("---")
    sc1, sc2, sc3 = st.columns(3)
    sc1.metric("Total Tests", total_tests)
    sc2.metric("Pass ✅", pass_count)
    sc3.metric("Fail ❌", fail_count)
else:
    st.info("No test results found in the data directory.")
