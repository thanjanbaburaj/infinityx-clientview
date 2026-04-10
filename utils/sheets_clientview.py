import json
import gspread
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials
import streamlit as st

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]

@st.cache_resource
def get_gspread_client():
    raw = st.secrets["GOOGLE_SERVICE_ACCOUNT_JSON"]
    info = json.loads(raw)
    creds = ServiceAccountCredentials.from_json_keyfile_dict(info, SCOPE)
    return gspread.authorize(creds)

@st.cache_data
def load_sheet_as_df(spreadsheet_name: str, tab_name: str):
    gc = get_gspread_client()
    sh = gc.open(spreadsheet_name)
    ws = sh.worksheet(tab_name)
    data = ws.get_all_records()
    if not data:
        return pd.DataFrame()
    return pd.DataFrame(data)

def append_row(spreadsheet_name: str, tab_name: str, row_values: list):
    gc = get_gspread_client()
    sh = gc.open(spreadsheet_name)
    ws = sh.worksheet(tab_name)
    ws.append_row(row_values)
