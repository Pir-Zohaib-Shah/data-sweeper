import streamlit as st
import pandas as pd
import os
from io import BytesIO

st.set_page_config(page_title="💿 Data Sweeper by Zohaib Shah", layout="wide")
st.title("💿 Data Sweeper by Zohaib Shah")
st.write("Transform your files between CSV and Excel formats with built-in data cleaning and visualization!.")

uploaded_files = st.file_uploader("Upload your files here (CSV or Excel)", type=["csv", "xlsx"], accept_multiple_files=True)

if uploaded_files:
    for file in uploaded_files:
        file_ext = os.path.splitext(file.name)[-1].lower()
        
        # Process the file
        if file_ext == ".csv":
            df = pd.read_csv(file)
        elif file_ext == ".xlsx":
            df = pd.read_excel(file)
        else:
            st.error(f"Unsupported file type: {file_ext}. Please upload a CSV or Excel file.")
            continue

        # Show file information
        st.write(f"**File Name:** {file.name}")
        st.write(f"**File Size:** {file.size/1000} KB")
        st.write(f"**File Type:** {file_ext}")

        # Show preview of the data
        st.write("**Preview of the Head of Data:**")
        st.dataframe(df.head())

        # Data Cleaning Options
        st.subheader("Data Cleaning Options")
        if st.checkbox("Data Cleaning Options"):
            col1, col2 = st.columns(2)

            with col1:
                if st.button(f"Remove Duplicates from {file.name}"):
                    df = df.drop_duplicates(inplace=False)
                    st.success(f"Duplicates removed from {file.name}")

            with col2:
                if st.button(f"Fill Missing Values in {file.name}"):
                    numeric_cols = df.select_dtypes(include=['number']).columns
                    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                    st.success(f"Missing values filled in {file.name} ✔")

        # Select Columns to Keep or Convert
        st.subheader("Select Columns to Keep or Convert")
        columns = st.multiselect(f"Choose Columns for {file.name}", df.columns, default=df.columns)
        df = df[columns]

        # Data Visualization
        st.subheader("📊 Data Visualization")
        if st.checkbox(f"Show Visualizations for {file.name}"):
            st.bar_chart(df.select_dtypes(include='number').iloc[:, :2])

        # Convert the file (CSV to Excel or vice versa)
        st.subheader("🔄 Conversion Options")
        conversion_type = st.radio(f"Convert {file.name} to:", ["CSV", "Excel"], key=file.name)
        if st.button(f"Convert {file.name}"):
            buffer = BytesIO()
            if conversion_type == "CSV":
                df.to_csv(buffer, index=False)
                file_name = file.name.replace(file_ext, ".csv")
                mime_type = "text/csv"

            elif conversion_type == "Excel":
                df.to_excel(buffer, index=False)
                file_name = file.name.replace(file_ext, ".xlsx")
                mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            buffer.seek(0)

            # Downloading the converted file
            st.download_button(
                label=f"⬇ Download {file_name}",
                data=buffer,
                file_name=file_name,
                mime=mime_type
            )
