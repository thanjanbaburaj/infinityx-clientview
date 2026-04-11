import streamlit as st
import pandas as pd
from utils.sheets_clientview import load_sheet
from datetime import datetime

st.set_page_config(page_title="Review Summary", page_icon="🧭", layout="wide")

def safe_get(row, key, default=""):
    v = row.get(key, default)
    return v if v not in ["", None] else default

def now_str():
    return datetime.now().strftime("%d %b %Y, %I:%M %p")

def build_client_friendly_summary(name, arch_points, focus_points, next_steps):
    lines = []
    lines.append(f"Review Summary for {name}")
    lines.append(f"Date: {now_str()}")
    lines.append("")
    lines.append("Your Financial Architecture:")
    for p in arch_points:
        lines.append(f"• {p}")
    lines.append("")
    lines.append("What We Agreed to Focus On:")
    for p in focus_points:
        lines.append(f"• {p}")
    lines.append("")
    lines.append("Next Steps:")
    for p in next_steps:
        lines.append(f"• {p}")
    return "\n".join(lines)

st.title("🧭 Your Review Summary")
st.caption("A simple, visual review of your current plan and agreed next steps.")

query_params = st.query_params
client_id_from_url = query_params.get("client_id", "")

client_id = st.text_input("Your Client ID", value=client_id_from_url)
if not client_id:
    st.info("Please enter your Client ID to view your review summary.")
    st.stop()

records = load_sheet("Financial_Fact_Find")
df = pd.DataFrame(records)

row_match = df[df["ClientID"].astype(str) == str(client_id)]
if row_match.empty:
    st.error("We couldn’t find a review record for this Client ID.")
    st.stop()

client_row = row_match.iloc[0].to_dict()
client_name = safe_get(client_row, "FullName", "Client")

st.markdown(f"### Hello, **{client_name}**")

st.subheader("Your Financial Architecture")
must_points = ["Strengthen family protection", "Build emergency buffer"]
should_points = ["Improve CI protection", "Start education funding", "Improve retirement funding"]
could_points = ["Accelerate wealth building", "Explore legacy planning"]

col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("#### MUST")
    for p in must_points:
        st.write(f"• {p}")
with col2:
    st.markdown("#### SHOULD")
    for p in should_points:
        st.write(f"• {p}")
with col3:
    st.markdown("#### COULD")
    for p in could_points:
        st.write(f"• {p}")

st.subheader("Next Steps")
next_steps = ["Review options", "Confirm priorities", "Implement plan"]
for p in next_steps:
    st.write(f"• {p}")

summary_text = build_client_friendly_summary(
    name=client_name,
    arch_points=must_points + should_points + could_points,
    focus_points=should_points,
    next_steps=next_steps
)

st.subheader("WhatsApp Summary")
st.text_area("Copy this summary:", summary_text, height=260)
