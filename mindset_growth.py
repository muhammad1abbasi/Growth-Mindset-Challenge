import streamlit as st
import pandas as pd
import os
from io import BytesIO

st.set_page_config(page_title="Data Sweeper", layout="wide")

# Custom CSS for dark mode
st.markdown(
    """
    <style>
        .stApp {
            background-color: black;
            color: white;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Title and description
st.title("Data Sweeper Sterling Integrator")
st.write("Transform Your Files between CSV and Excel formats with built-in data processing.")

# File uploader
uploaded_files = st.file_uploader("Upload Your files (CSV or Excel only):", 
                                  type=["csv", "xlsx"], 
                                  accept_multiple_files=True)

if uploaded_files:
    for file in uploaded_files:
        file_ext = os.path.splitext(file.name)[-1].lower()

        try:
            if file_ext == ".csv":
                df = pd.read_csv(file, encoding="utf-8")  # ✅ Fixed Unicode issue
            elif file_ext == ".xlsx":
                df = pd.read_excel(file, engine="openpyxl")
            else:
                st.error(f"Unsupported file type: {file_ext}")
                continue
        except Exception as e:
            st.error(f"Error reading file {file.name}: {str(e)}")
            continue

        # File details and preview
        st.write(f"### Preview of {file.name}:")
        st.dataframe(df.head())

        # Data cleaning options
        st.subheader("Data Cleaning Options")
        if st.checkbox(f"Clean data for {file.name}"):
            col1, col2 = st.columns(2)

            with col1:
                if st.button(f"Remove Duplicates - {file.name}"):
                    df.drop_duplicates(inplace=True)
                    st.success("Duplicates removed!")

            with col2:
                if st.button(f"Fill Missing Values - {file.name}"):
                    numeric_cols = df.select_dtypes(include=['number']).columns
                    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())  # ✅ Fixed `.fillna`
                    st.success("Missing values filled!")

            st.subheader("Select Columns to Keep")
            selected_columns = st.multiselect(f"Choose columns for {file.name}", df.columns, default=df.columns)
            df = df[selected_columns]

        # Data visualization
        st.subheader("Data Visualization")
        if st.checkbox(f"Show Visualization for {file.name}"):
            numeric_cols = df.select_dtypes(include=["number"])
            if not numeric_cols.empty:
                st.bar_chart(numeric_cols.iloc[:, :2])
            else:
                st.warning("No numeric columns available for visualization.")

        # File conversion options
        st.subheader("Conversion Options")
        conversion_type = st.radio(f"Convert {file.name} to:", ["CSV", "Excel"], key=file.name)

        if st.button(f"Convert {file.name}"):
            buffer = BytesIO()
            if conversion_type == "CSV":
                df.to_csv(buffer, index=False)
                file_name = file.name.replace(file_ext, ".csv")
                mime_type = "text/csv"
            elif conversion_type == "Excel":
                df.to_excel(buffer, index=False, engine="openpyxl")  # ✅ Fixed `.xlsx` issue
                file_name = file.name.replace(file_ext, ".xlsx")
                mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

            buffer.seek(0)
            st.download_button(
                label=f"Download {file.name} as {conversion_type}",
                data=buffer,
                file_name=file_name,
                mime=mime_type
            )

st.success("All files processed successfully!")
