import streamlit as st
import pandas as pd
import json
import os

st.set_page_config(page_title="Firmware Test Results", layout="wide")

st.title("📟 Firmware Version Test Dashboard")
st.markdown("---")

# Load data from the 'data' directory relative to this script
current_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(current_dir, 'data')
json_files = [f for f in os.listdir(data_dir) if f.endswith('.json')]
json_files.sort(reverse=True)

# Historical Pass Rate Chart at the Top
st.write("### 📈 Pass Rate Trend")
all_data = []
for f in json_files:
    with open(os.path.join(data_dir, f), 'r') as jf:
        d = json.load(jf)
        res = d['results']
        pass_rate = (len([r for r in res if r['status'] == 'Pass']) / len(res)) * 100
        all_data.append({"Version": d['firmware_version'], "Pass Rate (%)": pass_rate})

chart_df = pd.DataFrame(all_data).sort_values("Version")
st.bar_chart(chart_df.set_index("Version"))
st.markdown("---")

# Select firmware version
st.sidebar.header("Filter")
selected_file = st.sidebar.selectbox("Select Firmware Version", json_files)

if selected_file:
    file_path = os.path.join(data_dir, selected_file)
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
