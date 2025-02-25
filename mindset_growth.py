import streamlit as st
import pandas as pd

import os
from io import BytesIO

st.set_page_config(page_title= "Data Sweaper", layout="wide")

# custome css 
st.markdown(
    """
<style>
 .stApp{
    background-color : black;
    color: white
 }
</style>
    """,
    unsafe_allow_html=True
)

# title and  description

st.title("Data Sweeper Sterling Integrator")
st.write("Transform Your Files between CSV and Excel formates with build in data")

# file uploader 

uploaded_files = st.file_uploader("Upload Your files (accepts CSV or Excel):", type=["csv","xlsx"], accept_multiple_files=(True))

if uploaded_files:
    for file in uploaded_files:
        file_ext = os.path.splitext(file.name)[-1].lower()

        if file_ext == ".csv":
            df = pd.read_csv(file)
        elif file_ext == ".xlsx":
            df = pd.read_excel(file)
        else:
            st.error(f"unsupported file type: {file_ext}")
            continue

        # file detailes 
        st.write("Preview the head of a data frame")
        st.dataframe(df.head())

        # data cleaning option
        st.subheader("Data Cleaning Option")
        if st.checkbox(f"clean data for {file.name}"):
            col1, col2 = st.columns(2)

            with col1:
                if st.button(f"Remove duplicates from the file: {file.name}"):
                    df.drop_duplicates(inplace=True)
                    st.write("duplicate removed!")

                    with col2:
                        if st.button(f"Fill missing values for {file.name}"):
                           numeric_cols = df.select_dtypes(include=['number']).columns
                           df[numeric_cols] = df [numeric_cols].filln(df[numeric_cols].mean())
                           st.write("Missing values have been filled!")
                st.subheader("Select colomns to keep")
                columns = st.multiselect(f"Choose columns for {file.name}", df.columns, default=df.columns)
                df = df[columns]

                # data visualization
                st.subheader("Data Visualization")
                if st.checkbox(f"Show visualition for {file.name}"):
                    st.bar_chart(df.select_dtypes(include="number").iloc[:,:2])



                # conversation option

                st.subheader("Conversation Option")
                conversation_type = st.radion(f"Conver {file.name} to: ",["CSV" , "Excel"], key=file.name)
                if st.button(f"Convert{file.name}"):
                    buffer = BytesIO()
                    if conversation_type == "CSV":
                        df.to_csv(buffer, index=False)
                        file_name = file.name.replace(file_ext,)
                        mime_type = "text/csv"

                    elif conversation_type == "Excel":
                        df.to_excel(buffer, index=False)
                        file_name = file.name.replace(file_ext, ".xlsk")
                        mime_type = "application/vnd.openformates-officedocument.spreadsheetml.sheet"
                        buffer.seek(0)

                        st.download_button(
                            label=f"Download {file.name} as {conversation_type}",
                            data=buffer,
                            file_name=file_name,
                            mime=mime_type
                        )
st.success("All Files proceed successfully")
