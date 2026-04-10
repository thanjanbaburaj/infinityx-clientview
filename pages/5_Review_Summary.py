import streamlit as st
import pandas as pd
from utils.sheets_clientview import load_sheet
from datetime import datetime

st.set_page_config(page_title="Review Summary", page_icon="🧭", layout="wide")

# -----------------------------
# Helpers
# -----------------------------
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
    lines.append("Your Financial Architecture (Simple View):")
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
    lines.append("")
    lines.append("Thank you for taking the time to review your plan. This puts you ahead of most people.")
    return "\n".join(lines)

# -----------------------------
# Load data
# -----------------------------
st.title("🧭 Your Review Summary")
st.caption("A simple, visual review of your current plan and agreed next steps.")

# Try to read ClientID from query params (if coming from a link)
query_params = st.experimental_get_query_params()
client_id_from_url = query_params.get("client_id", [""])[0]

client_id = st.text_input("Your Client ID", value=client_id_from_url)
if not client_id:
    st.info("Please enter your Client ID to view your review summary.")
    st.stop()

try:
    records = load_sheet("Financial_Fact_Find")
    df = pd.DataFrame(records)
except Exception as e:
    st.error("We’re unable to load your review data right now. Please try again later.")
    st.stop()

if df.empty or "ClientID" not in df.columns:
    st.error("We couldn’t find any review data linked to your profile yet.")
    st.stop()

row_match = df[df["ClientID"].astype(str) == str(client_id)]
if row_match.empty:
    st.error("We couldn’t find a review record for this Client ID.")
    st.stop()

client_row = row_match.iloc[0].to_dict()
client_name = safe_get(client_row, "FullName", "Client")

st.markdown(f"### Hello, **{client_name}**")
st.markdown("This page gives you a **clean, simple view** of your current setup and what we agreed to focus on.")

st.markdown("---")

# -----------------------------
# 1) Life & Goals Snapshot (soft, non‑numeric)
# -----------------------------
st.subheader("1️⃣ Life & Goals Snapshot")

col1, col2 = st.columns(2)
with col1:
    life_stage = safe_get(client_row, "LifeStage", "")
    main_goal = safe_get(client_row, "MainGoal", "")
    st.markdown("**Life Stage**")
    st.write(life_stage or "As discussed in our meeting.")
    st.markdown("**Main Goal Right Now**")
    st.write(main_goal or "The main goal we discussed together.")

with col2:
    dependents = safe_get(client_row, "Dependents", "")
    catalyst = safe_get(client_row, "ReviewTrigger", "")
    st.markdown("**Who Relies on You**")
    st.write(f"{dependents} dependents" if dependents else "As discussed in our meeting.")
    st.markdown("**Why We Reviewed Now**")
    st.write(catalyst or "The life change or reason you shared.")

st.markdown("---")

# -----------------------------
# 2) Architecture View (Must / Should / Could) – client‑friendly
# -----------------------------
st.subheader("2️⃣ Your Financial Architecture")

must_points = []
should_points = []
could_points = []

# These are descriptive, not numeric
has_life_cover_gap = safe_get(client_row, "HasLifeGap", "Yes") == "Yes"
has_ci_gap = safe_get(client_row, "HasCIGap", "Yes") == "Yes"
has_emergency_gap = safe_get(client_row, "HasEmergencyGap", "Yes") == "Yes"
has_retirement_gap = safe_get(client_row, "HasRetirementGap", "Yes") == "Yes"
has_education_gap = safe_get(client_row, "HasEducationGap", "Yes") == "Yes"

if has_life_cover_gap:
    must_points.append("Strengthen family protection in case income stops unexpectedly.")
if has_emergency_gap:
    must_points.append("Build a stronger emergency buffer for 3–6 months of expenses.")

if has_ci_gap:
    should_points.append("Add or improve critical illness protection for serious health events.")
if has_education_gap:
    should_points.append("Start or increase education funding for children’s future studies.")
if has_retirement_gap:
    should_points.append("Improve retirement funding so future lifestyle is protected.")

could_points.append("Accelerate wealth building once core protections and key goals are covered.")
could_points.append("Explore legacy or estate planning at a later stage if relevant.")

col_arch1, col_arch2, col_arch3 = st.columns(3)

with col_arch1:
    st.markdown("#### MUST")
    if must_points:
        for p in must_points:
            st.write(f"• {p}")
    else:
        st.write("• Your core protection looks reasonably on track based on our last review.")

with col_arch2:
    st.markdown("#### SHOULD")
    if should_points:
        for p in should_points:
            st.write(f"• {p}")
    else:
        st.write("• No major secondary gaps were highlighted in this review.")

with col_arch3:
    st.markdown("#### COULD")
    for p in could_points:
        st.write(f"• {p}")

st.markdown("---")

# -----------------------------
# 3) Focus Areas (what we agreed to prioritise)
# -----------------------------
st.subheader("3️⃣ What We Agreed to Focus On")

focus_1 = safe_get(client_row, "Priority1", "")
focus_2 = safe_get(client_row, "Priority2", "")
focus_3 = safe_get(client_row, "Priority3", "")

focus_points = []
if focus_1:
    focus_points.append(focus_1)
if focus_2:
    focus_points.append(focus_2)
if focus_3:
    focus_points.append(focus_3)

if not focus_points:
    st.write("We agreed to focus on a few key areas. Your advisor will confirm these with you directly.")
else:
    for p in focus_points:
        st.write(f"• {p}")

st.markdown("---")

# -----------------------------
# 4) Next Steps (client‑friendly)
# -----------------------------
st.subheader("4️⃣ Next Steps")

next_step_1 = safe_get(client_row, "NextStep1", "")
next_step_2 = safe_get(client_row, "NextStep2", "")
next_step_3 = safe_get(client_row, "NextStep3", "")

next_steps = []
if next_step_1:
    next_steps.append(next_step_1)
if next_step_2:
    next_steps.append(next_step_2)
if next_step_3:
    next_steps.append(next_step_3)

if not next_steps:
    st.write("Your advisor will share a short follow‑up message with the exact next steps.")
else:
    for p in next_steps:
        st.write(f"• {p}")

st.markdown("---")

# -----------------------------
# 5) WhatsApp‑ready summary
# -----------------------------
st.subheader("5️⃣ WhatsApp‑Ready Summary")

arch_points_for_text = must_points + should_points + could_points
summary_text = build_client_friendly_summary(
    name=client_name,
    arch_points=arch_points_for_text,
    focus_points=focus_points or ["As discussed in our review."],
    next_steps=next_steps or ["Your advisor will confirm the next steps with you shortly."]
)

st.text_area("You can copy this summary to share or keep for your records:", summary_text, height=260)
st.caption("Your advisor may also send you this (or a similar version) directly on WhatsApp.")

# -----------------------------
# 6) “PDF‑style” export (HTML/Markdown download)
# -----------------------------
st.subheader("6️⃣ Download Your Review Summary")

export_md = f"""# Review Summary for {client_name}

**Date:** {now_str()}

---

## Your Financial Architecture (Simple View)

""" + "\n".join([f"- {p}" for p in arch_points_for_text]) + """

---

## What We Agreed to Focus On

""" + "\n".join([f"- {p}" for p in (focus_points or ['As discussed in our review.'])]) + """

---

## Next Steps

""" + "\n".join([f"- {p}" for p in (next_steps or ['Your advisor will confirm the next steps with you shortly.'])]) + """

---

Thank you for taking the time to review your plan.
"""

st.download_button(
    label="Download Summary (Markdown/PDF‑ready)",
    data=export_md,
    file_name=f"Review_Summary_{client_name.replace(' ', '_')}.md",
    mime="text/markdown",
)
st.caption("You or your advisor can convert this file to PDF if needed, or keep it as a digital note.")
