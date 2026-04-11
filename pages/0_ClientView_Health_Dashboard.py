import streamlit as st
import time
import pandas as pd
from utils.sheets_clientview import get_spreadsheet, load_sheet

st.set_page_config(
    page_title="ClientView Health Dashboard",
    page_icon="🩺",
    layout="wide",
)

st.title("🩺 Infinity‑X ClientView Health Dashboard")
st.caption("Checks data backbone for all ClientView pages: Fact Find, Gaps, Architecture, Blueprint, Review Summary.")

# -----------------------------
# 1️⃣ Service Account & Google Auth
# -----------------------------
st.header("1️⃣ Service Account & Google Auth")

ok_sa = False
ok_ss = False

with st.spinner("Checking service account and auth..."):
    try:
        ss = get_spreadsheet()
        ok_sa = True
        ok_ss = True
        st.success("✅ Service account & Google auth OK")
        st.write(f"Spreadsheet Title: **{ss.title}**")
    except Exception as e:
        st.error(f"❌ Failed to authenticate or open spreadsheet.\n\n{e}")

if not (ok_sa and ok_ss):
    st.stop()

# -----------------------------
# 2️⃣ Tab Health (ClientView‑relevant)
# -----------------------------
st.header("2️⃣ Worksheet (Tab) Health for ClientView")

expected_tabs = [
    "Clients",
    "Financial_Fact_Find",
    "Policies",
    "Policy_Funds",
    "Config",
]

tab_status = []

for tab in expected_tabs:
    try:
        ws = ss.worksheet(tab)
        headers = ws.row_values(1)
        tab_status.append((tab, True, len(headers)))
    except Exception:
        tab_status.append((tab, False, 0))

col1, col2 = st.columns(2)
with col1:
    for tab, exists, header_len in tab_status:
        if exists:
            st.markdown(f"✅ **{tab}** — Exists — {header_len} header columns")
        else:
            st.markdown(f"❌ **{tab}** — Missing")

# -----------------------------
# 3️⃣ Column Schema Health
# -----------------------------
st.header("3️⃣ Column Schema Health (ClientView‑critical)")

expected_schema = {
    "Clients": [
        "ClientID", "FullName", "Mobile", "Email", "Salary",
        "Status", "ClientScore", "NextReviewDate", "ReferralAsked",
    ],
    "Financial_Fact_Find": [
        "ClientID", "FullName", "Income", "Expenses", "Assets",
        "Liabilities", "Dependents", "Catalyst",
        "CoverLife", "CoverCI", "CoverDisability",
        "RetirementAge", "EducationGoal", "LastUpdated",
    ],
    "Policies": [
        "PolicyID", "ClientID", "FullName", "Product", "Premium", "Frequency",
        "Status", "IssueDate", "PaidToDate", "NextPremiumDue",
        "CommissionRate", "ExpectedAnnualCommission",
        "LifeCover", "CICover", "DisabilityCover", "CurrentValue",
        "PolicyType", "Carrier", "PolicyNumber",
    ],
    "Policy_Funds": [
        "FundID", "PolicyID", "ClientID", "FullName", "Carrier",
        "FundName", "ISIN", "AllocationPercent", "UnitsHeld",
        "UnitPrice_Carrier", "UnitPrice_YF", "CurrentValue", "LastUpdated",
    ],
    "Config": [
        "LeadSources", "TriggerTypes", "StatusOptions",
        "PaymentFrequencies", "OutcomeTags",
    ],
}

for tab, expected_cols in expected_schema.items():
    st.markdown(f"#### 🧾 {tab}")
    try:
        records = load_sheet(tab)
        df = pd.DataFrame(records)
        actual_cols = list(df.columns)
    except Exception as e:
        st.error(f"❌ Could not load '{tab}': {e}")
        continue

    missing = [c for c in expected_cols if c not in actual_cols]
    extra = [c for c in actual_cols if c not in expected_cols]

    if not missing and not extra:
        st.success("✅ Columns match expected schema.")
    else:
        if missing:
            st.error(f"❌ Missing columns: {missing}")
        if extra:
            st.markdown(f"🟡 Extra / enhancement columns: {extra}")

# -----------------------------
# 4️⃣ Read Latency
# -----------------------------
st.header("4️⃣ Read Latency Test")

start = time.time()
_ = load_sheet("Financial_Fact_Find")
latency = (time.time() - start) * 1000
st.success(f"✅ Read latency: {latency:.2f} ms")

# -----------------------------
# 5️⃣ Page Dependency Map
# -----------------------------
st.header("5️⃣ ClientView Page Dependency Map")

st.markdown("""
**1_Fact_Find.py**
- Uses: `Clients`, `Financial_Fact_Find`
- Breaks if: `ClientID`, `FullName`, income/expense/asset/liability fields are missing.

**2_Gap_Engine.py**
- Uses: `Financial_Fact_Find`, `Policies`
- Breaks if: cover fields, retirement fields, or policy coverage/value fields are missing.

**3_Architecture.py**
- Uses: `Financial_Fact_Find`, derived gaps (no extra sheets).
- Breaks if: core Fact Find fields are missing.

**4_Blueprint.py**
- Uses: same data as Architecture + gaps.
- Breaks if: Fact Find or gap logic fails.

**5_Review_Summary.py**
- Uses: `Financial_Fact_Find`, `Policies`, `Policy_Funds`, `Clients`
- Breaks if: portfolio fields or client identity fields are missing.
""")

st.info("If this dashboard is fully green (no red), ClientView is safe to use in live review meetings.")
