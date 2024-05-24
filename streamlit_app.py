import streamlit as st
import pandas as pd
from processing_helper import (
    process_resumen,
    process_uploaded_file
)



def main():
    uploaded_file = st.file_uploader("Choose an excel file", type='xlsx')

    if st.button('Process File'):
        with st.spinner('Processing...'):
            df = process_uploaded_file(uploaded_file)
            df_resumen = process_resumen(df)

        st.dataframe(df, hide_index=True)
        st.dataframe(df_resumen, hide_index=True)


if __name__ == "__main__":
    main()