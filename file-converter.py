import streamlit as st
import pandas as pd
import os
from io import BytesIO

# App Config
st.set_page_config(page_title="File Converter", layout="wide")

# Custom CSS
st.markdown(
    """
    <style>
    .stApp {
        background-color: white;
        color: black;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# App Title and Instructions
st.title("File Converter & Cleaner")
st.write("Upload CSV or Excel files, clean data, and convert formats.")

# Upload Files
uploaded_files = st.file_uploader(
    "Upload CSV or Excel Files here.",
    type=["csv", "xlsx"],
    accept_multiple_files=True
)

# Processing Uploaded Files
if uploaded_files:
    for file in uploaded_files:
        file_ext = os.path.splitext(file.name)[-1].lower()

        # Read the File
        if file_ext == ".csv":
            df = pd.read_csv(file)
        elif file_ext == ".xlsx":
            df = pd.read_excel(file)
        else:
            st.error(f"Unsupported file type: {file_ext}")
            continue

        # File Preview
        st.subheader(f"{file.name} - Preview")
        st.dataframe(df.head())

        # Data Cleaning Section
        st.subheader("Data Cleaning Options")
        if st.checkbox(f"Clean data for {file.name}"):
            col1, col2 = st.columns(2)

            with col1:
                if st.button(f"Remove Duplicates: {file.name}"):
                    df.drop_duplicates(inplace=True)
                    st.write("Duplicates Removed Successfully!")

            with col2:
                if st.button(f"Fill Missing Values: {file.name}"):
                    numeric_cols = df.select_dtypes(include=["number"]).columns
                    if len(numeric_cols) > 0:
                        df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                        st.write("Missing Values Filled!")
                    else:
                        st.write("No numeric columns to fill.")

        # Column Selection Section
        st.subheader("Select Columns to Keep")
        columns = st.multiselect(
            f"Select columns for {file.name}",
            df.columns.tolist(),
            default=df.columns.tolist()
        )
        df = df[columns]

        # Visualization Section
        st.subheader("Data Visualization")
        if st.checkbox(f"Show Visualization Chart - {file.name}"):
            numeric_df = df.select_dtypes(include="number")
            if not numeric_df.empty:
                st.bar_chart(numeric_df.iloc[:, :2])
            else:
                st.write("No numeric data to display.")

        # Conversion Options Section
        st.subheader("Conversion Options")
        conversion_type = st.radio(
            f"Convert {file.name} to:",
            ["CSV", "Excel"],
            key=f"conversion_{file.name}"
        )

        if st.button(f"Convert {file.name}"):
            buffer = BytesIO()

            if conversion_type == "CSV":
                df.to_csv(buffer, index=False)
                new_file_name = file.name.replace(file_ext, ".csv")
                mime_type = "text/csv"

            elif conversion_type == "Excel":
                df.to_excel(buffer, index=False)
                new_file_name = file.name.replace(file_ext, ".xlsx")
                mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

            buffer.seek(0)

            # Download Button
            st.download_button(
                label=f"Download {new_file_name}",
                data=buffer,
                file_name=new_file_name,
                mime=mime_type
            )

        st.success(f"Processing Complete for {file.name}!")
