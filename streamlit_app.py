import base64
import io
import streamlit as st
import pandas as pd
from processing_helper import (
    process_resumen,
    process_uploaded_file
)



def main():
    st.title('Herramienta de control de tasas')

    uploaded_file = st.file_uploader("Sube un listado de producción", type='xlsx')

    if st.button('Generar reporte'):
        with st.spinner('Procesando...'):
            df = process_uploaded_file(uploaded_file)
            df_resumen = process_resumen(df)

        st.dataframe(df, hide_index=True)
        st.dataframe(df_resumen, hide_index=True)

        towrite = io.BytesIO()
        with pd.ExcelWriter(towrite, engine='openpyxl', mode='xlsx') as writer:
            df.to_excel(writer, index=False, sheet_name='Data')
            df_resumen.to_excel(writer, index=False, sheet_name='Resumen')
        
        towrite.seek(0)
        b64 = base64.b64encode(towrite.read()).decode()
        st.download_button(
            label='Download Data and Resumen',
            data=towrite,
            file_name='processed_data.xlsx',
            mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )

if __name__ == "__main__":
    main()