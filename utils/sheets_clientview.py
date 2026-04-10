import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import streamlit as st

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]

@st.cache_resource
def get_client():
    raw = st.secrets["GOOGLE_SERVICE_ACCOUNT_JSON"]
    info = json.loads(raw)
    creds = ServiceAccountCredentials.from_json_keyfile_dict(info, SCOPE)
    return gspread.authorize(creds)

def append_row(sheet_name, tab_name, row_values):
    gc = get_client()
    sh = gc.open(sheet_name)
    ws = sh.worksheet(tab_name)
    ws.append_row(row_values)

def load_sheet(sheet_name, tab_name):
    gc = get_client()
    sh = gc.open(sheet_name)
    ws = sh.worksheet(tab_name)
    return ws.get_all_records()
