import streamlit as st
import pandas as pd
from io import BytesIO

st.set_page_config(page_title="File Converter", layout="wide")
st.title("File Converter & Cleaner")
st.write("Upload CSV or Excel files, clean data, and convert formats.")

# Debugging: Print a message
st.write("App is running...")

files = st.file_uploader("Upload CSV or Excel Files here.", type=["csv","xlsx"], accept_multiple_files=True)

if files:
    st.write("File uploaded!")  # Debugging step
    for file in files:
        ext = file.name.split(".")[-1]
        st.write(f"Processing file: {file.name}")  # Debugging step

        # Try/Except block to catch errors
        try:
            df = pd.read_csv(file) if ext == "csv" else pd.read_excel(file)
            st.subheader(f"{file.name} - Preview")
            st.dataframe(df.head())
        except Exception as e:
            st.error(f"Error reading {file.name}: {e}")
