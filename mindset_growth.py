import streamlit as st
import pandas as pd
import os
from io import BytesIO

st.set_page_config(page_title="Data Sweeper", layout="wide")

# Custom CSS for a sleek UI
st.markdown(
    """
    <style>
        body {
            background-color: #0d1117;
            color: white;
        }
        .stApp {
            background: linear-gradient(to right, #141e30, #243b55);
            color: white;
        }
        .css-1d391kg { 
            background-color: #161b22 !important; 
            border-radius: 10px;
            padding: 20px;
            box-shadow: 2px 2px 10px rgba(0, 255, 255, 0.2);
        }
        .stButton > button {
            background-color: #00adb5;
            color: black;
            font-size: 16px;
            border-radius: 10px;
            padding: 10px;
            transition: 0.3s;
        }
        .stButton > button:hover {
            background-color: #008b8b;
            color: white;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Title & Description
st.markdown("""
    <h1 style='text-align: center; color: cyan;'>🧹 Data Sweeper</h1>
    <h3 style='text-align: center; color: lightgray;'>Transform and Clean Your Data Instantly</h3>
""", unsafe_allow_html=True)

# File Uploader
uploaded_files = st.file_uploader("📂 Upload CSV or Excel files:", type=["csv", "xlsx"], accept_multiple_files=True)

if uploaded_files:
    for file in uploaded_files:
        file_ext = os.path.splitext(file.name)[-1].lower()
        
        try:
            if file_ext == ".csv":
                df = pd.read_csv(file, encoding="utf-8")
            elif file_ext == ".xlsx":
                df = pd.read_excel(file)
            else:
                st.error(f"🚫 Unsupported file type: {file_ext}")
                continue
        except Exception as e:
            st.error(f"❌ Error reading file {file.name}: {str(e)}")
            continue

        # Display File Preview
        st.markdown(f"### 📜 Preview of {file.name}")
        st.dataframe(df.head())

        # Data Cleaning Options
        with st.expander(f"🧹 Data Cleaning for {file.name}"):
            col1, col2 = st.columns(2)

            with col1:
                if st.button(f"🗑 Remove Duplicates - {file.name}"):
                    df.drop_duplicates(inplace=True)
                    st.success("Duplicates removed!")

            with col2:
                if st.button(f"🛠 Fill Missing Values - {file.name}"):
                    numeric_cols = df.select_dtypes(include=['number']).columns
                    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                    st.success("Missing values filled!")

            columns = st.multiselect(f"📌 Select Columns for {file.name}", df.columns, default=df.columns)
            df = df[columns]

        # Data Visualization
        with st.expander(f"📊 Visualization for {file.name}"):
            st.bar_chart(df.select_dtypes(include="number").iloc[:, :2])

        # Conversion Options
        with st.expander(f"🔄 Convert {file.name}"):
            conversion_type = st.radio(f"Convert {file.name} to:", ["CSV", "Excel"], key=file.name)
            if st.button(f"💾 Convert {file.name}"):
                buffer = BytesIO()
                if conversion_type == "CSV":
                    df.to_csv(buffer, index=False)
                    file_name = file.name.replace(file_ext, ".csv")
                    mime_type = "text/csv"
                elif conversion_type == "Excel":
                    df.to_excel(buffer, index=False, engine="openpyxl")
                    file_name = file.name.replace(file_ext, ".xlsx")
                    mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                buffer.seek(0)
                st.download_button(
                    label=f"📥 Download {file.name} as {conversion_type}",
                    data=buffer,
                    file_name=file_name,
                    mime=mime_type
                )

st.success("✅ All files processed successfully!")
