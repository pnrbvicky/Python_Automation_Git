# import sqlite3
# import pandas as pd
# import streamlit as st
# import os

# st.set_page_config(page_title="Merlin Orders Dashboard", layout="wide")

# st.title("📦 Merlin Orders Dashboard")
# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# DB_PATH = os.path.join(BASE_DIR, "output", "merlin.db")

# st.write("📁 DB Path:", DB_PATH)  

# # DB connection
# conn = sqlite3.connect(DB_PATH)


# df = pd.read_sql("""
#     SELECT merlin_order_no,
#            merlin_sku,
#            merlin_qty,
#            merlin_unit_price,
#            merlin_total_price,
#            merlin_city,
#            status,
#            error_message,
#            created_at
#     FROM merlin_sales
#     ORDER BY created_at DESC
# """, conn)

# conn.close()

# # KPIs
# col1, col2, col3 = st.columns(3)

# col1.metric("Total Orders", len(df))
# col2.metric("✅ Success", len(df[df["status"] == "SUCCESS"]))
# col3.metric("❌ Failed", len(df[df["status"] == "FAILED"]))

# # Filter
# status_filter = st.selectbox(
#     "Filter by status",
#     ["ALL", "PENDING", "SUCCESS", "FAILED"]
# )

# if status_filter != "ALL":
#     df = df[df["status"] == status_filter]

# st.dataframe(df, use_container_width=True)
import sqlite3
import pandas as pd
import streamlit as st
import os
from streamlit_autorefresh import st_autorefresh

# ---------------- CONFIG ----------------
# DB_PATH = r"G:\SaleOrderAutomation_Python\project\output\merlin.db"

st.set_page_config(page_title="Merlin Orders Dashboard", layout="wide")

st.title("📊 Merlin Orders Dashboard")
# 🔄 Auto refresh every 5 seconds
st_autorefresh(interval=5000, key="merlin_refresh")

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "output", "merlin.db")

# ---------------- LOAD DATA ----------------

def load_data():
    if not os.path.exists(DB_PATH):
        return pd.DataFrame()

    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql("SELECT * FROM merlin_sales", conn)
    conn.close()
    return df

df = load_data()

if df.empty:
    st.warning("No data available in Merlin DB")
    st.stop()

# ---------------- KPI METRICS ----------------
total_count = len(df)
pending_count = len(df[df["status"] == "PENDING"])
success_count = len(df[df["status"] == "SUCCESS"])
failed_count = len(df[df["status"] == "FAILED"])

col1, col2, col3, col4 = st.columns(4)
col1.metric("📦 Total Orders", total_count)
col2.metric("⏳ Pending", pending_count)
col3.metric("✅ Success", success_count)
col4.metric("❌ Failed", failed_count)

st.divider()

# ---------------- STATUS FILTER ----------------
status_filter = st.selectbox(
    "Filter orders by status",
    ["ALL", "PENDING", "SUCCESS", "FAILED"]
)

if status_filter != "ALL":
    df = df[df["status"] == status_filter]

# ---------------- DATA TABLE ----------------
st.subheader("📋 Order Details")

st.dataframe(
    df.sort_values("created_at", ascending=False),
    use_container_width=True
)

# ---------------- FOOTER ----------------
st.caption("🔄 Live data from Merlin DB")
