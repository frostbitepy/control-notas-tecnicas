import pandas as pd
import openpyxl
from setup_data import (
    tasas, via_importacion, tipo_vhl, seg_casco,
    seg_rc, seg_ovp, tasa_rc_min, tasa_rc_max, tasa_ovp_min,
    tasa_ovp_max, recargo_ptf, products_data)


def updated_name_column(df):
    df['Updated Nombre Producto'] = df['Nombre Producto'].map(products_data)
    return df


def add_cobertura_basica_column(df):
    df["Cobertura Básica / Casco"] = df["Auto Cober. Básica 1"] + df["Auto Cober. Básica 2"] + df["Auto Accesorios"]
    return df


def round_to_million(n):
    if n > 150000000:
        return 150000000
    elif n <= 10000000:
        return 10000000
    else:
        return (n // 1000000) * 1000000


def add_capital_seg_column(df):
    df["Capital seg"] = df["Cobertura Básica / Casco"].apply(round_to_million)
    return df


def add_resp_civil_column(df):
    df["Resp. Civil"] = df["Auto Lesión 2 o más Per."] + df["Auto Daños Material a Ter."]
    return df


def add_ovp_column(df):
    df["OVP"] = (df["Auto Muerte/Incap."] + df["Auto Asist. Médica"]) *  df["Cant. Ocupantes"]
    return df


def add_franquicia_column(df):
    def map_franquicia(value):
        if value < 500000:
            return "General"
        elif value == 500000:
            return "Franquicia 500mil"
        else:
            return "Franquicia 1 millón"

    df["Franquicia"] = df["Franquicia Monto Fijo"].apply(map_franquicia)
    return df


def add_importacion_column(df):
    df["Importacion"] = df["Via Importación"].map(via_importacion)
    return df


def add_tipo_column(df):
    df['Tipo'] = df['Tipo Vehiculo'].map(tipo_vhl)
    return df


def add_segmento_column(df):
    df['Segmento'] = df['Tipo'] + df['Franquicia'] + df['Importacion']
    return df

def add_segmento_casco_column(df):
    df['Segmento Casco'] = df['Segmento'].map(seg_casco)
    return df

def add_segmento_rc_column(df):
    df['Segmento RC'] = df['Segmento'].map(seg_rc)
    return df

def add_segmento_ovp_column(df):
    df['Segmento OVP'] = df['Segmento'].map(seg_ovp)
    return df


def add_final_casco_column(df):
    df['Final Casco'] = df['Segmento Casco'] + "-" + df['Capital seg'].astype(str) 
    return df


def add_tasa_min_prima_pura_casco_column(df):
    df['Tasa MIN Prima Pura Casco'] = df['Final Casco'].map(lambda x: tasas.get(x, {}).get('min'))
    return df 

def add_tasa_min_prima_pura_rc_column(df):
    df['Tasa MIN Prima Pura RC'] = df['Segmento RC'].map(tasa_rc_min)
    return df

def add_tasa_min_prima_pura_ovp_column(df ):
    df['Tasa MIN Prima Pura OVP'] = df['Segmento OVP'].map(tasa_ovp_min)
    return df


def add_prima_min_cobertura_basica_casco_column(df):
    df['Prima MIN Cobertura Basica / Casco'] = df['Cobertura Básica / Casco'] * df['Tasa MIN Prima Pura Casco']
    return df
    
def add_prima_min_rc_column(df):
    df['Prima MIN RC'] = df["Resp. Civil"] * df["Tasa MIN Prima Pura RC"]
    return df

def add_prima_min_ovp_column(df):
    df['Prima MIN OVP'] = df["OVP"] * df["Tasa MIN Prima Pura OVP"]
    return df

def add_dias_vigencia_column(df):
    df['Dias Vigencia'] = (df['Fec. Hasta'] - df['Fec. Desde']).dt.days + 1
    return df

def add_prima_tecnica_art_column(df):
    df['Prima Tecnica Art.'] = df['Prima Técnica Art.'] / df['Dias Vigencia'] * 365
    return df

def add_min_prima_pura_cot_column(df):
    df['MIN Prima Pura Cot'] = df['Prima MIN Cobertura Basica / Casco'] + df['Prima MIN RC'] + df['Prima MIN OVP']
    return df

def add_min_prima_tarifa_cot_column(df):
    df['MIN Prima Tarifa Cot'] = df['MIN Prima Pura Cot'] * recargo_ptf
    return df

def add_tasa_max_prima_pura_casco_column(df):
    df['Tasa MAX Prima Pura Casco'] = df['Final Casco'].map(lambda x: tasas.get(x, {}).get('max'))
    return df 

def add_tasa_max_prima_pura_rc_column(df):
    df['Tasa MAX Prima Pura RC'] = df['Segmento RC'].map(tasa_rc_max)
    return df

def add_tasa_max_prima_pura_ovp_column(df ):
    df['Tasa MAX Prima Pura OVP'] = df['Segmento OVP'].map(tasa_ovp_max)
    return df


def add_prima_max_cobertura_basica_casco_column(df):
    df['Prima MAX Cobertura Basica / Casco'] = df['Cobertura Básica / Casco'] * df['Tasa MAX Prima Pura Casco']
    return df
    
def add_prima_max_rc_column(df):
    df['Prima MAX RC'] = df["Resp. Civil"] * df["Tasa MAX Prima Pura RC"]
    return df

def add_prima_max_ovp_column(df):
    df['Prima MAX OVP'] = df["OVP"] * df["Tasa MAX Prima Pura OVP"]
    return df

def add_max_prima_pura_cot_column(df):
    df['MAX Prima Pura Cot'] = df['Prima MAX Cobertura Basica / Casco'] + df['Prima MAX RC'] + df['Prima MAX OVP']
    return df

def add_max_prima_tarifa_cot_column(df):
    df['MAX Prima Tarifa Cot'] = df['MAX Prima Pura Cot'] * recargo_ptf
    return df


def add_monto_diferencia_prima_pura_column(df):
    def calculate_difference(row):
        cx = row['Prima Tecnica Art.']
        da = row['MIN Prima Pura Cot']
        dj = row['MAX Prima Tarifa Cot']

        if cx < da:
            return cx - da
        elif cx > dj:
            return cx - dj
        else:
            return ""

    df['Monto Diferencia Prima Pura'] = df.apply(calculate_difference, axis=1)
    return df

def add_monto_diferencia_prima_tarifa_column(df):
    def calculate_difference(row):
        cx = row['Prima Tecnica Art.']
        da = row['MIN Prima Tarifa Cot']
        dj = row['MAX Prima Tarifa Cot']

        if cx < da:
            return cx - da
        elif cx > dj:
            return cx - dj
        else:
            return ""

    df['Monto Diferencia Prima Tarifa'] = df.apply(calculate_difference, axis=1)
    return df


def count_product_names_x(df):
    df['Mapped Nombre Producto'] = df['Nombre Producto'].map(products_data)
    df_count = df.groupby('Updated Nombre Producto').agg({
        'Mapped Nombre Producto': 'count',
        'Prima Tecnica Art.': 'sum',
        'MIN Prima Pura Cot': 'sum',
        'MIN Prima Tarifa Cot': 'sum',
        'MAX Prima Pura Cot': 'sum'
    }).reset_index()
    df_count.columns = ['PRODUCTO', 'CANTIDAD', 'PRIMA TECNICA ART', 'MIN PRIMA PURA COT', 'MIN PRIMA TARIFA COT', 'MAX PRIMA PURA COT']
    return df_count

def count_product_names_x2(df):
    # Convert columns to numeric type and round to 2 decimal places
    numeric_columns = ['Prima Tecnica Art.', 'MIN Prima Pura Cot', 'MIN Prima Tarifa Cot', 'MAX Prima Pura Cot', 'Monto Diferencia Prima Pura', 'Monto Diferencia Prima Tarifa']
    for col in numeric_columns:
        df[col] = pd.to_numeric(df[col], errors='coerce').round(2)

    df['Mapped Nombre Producto'] = df['Nombre Producto'].map(products_data)
    df_grouped = df.groupby('Updated Nombre Producto').agg({
        'Mapped Nombre Producto': 'count',
        'Prima Tecnica Art.': 'sum',
        'MIN Prima Pura Cot': 'sum',
        'MIN Prima Tarifa Cot': 'sum',
        'MAX Prima Pura Cot': 'sum',
        'Monto Diferencia Prima Pura': 'sum',
        'Monto Diferencia Prima Tarifa': 'sum'
    }).reset_index()

    df_grouped.columns = ['PRODUCTO', 'CANTIDAD', 'PRIMA TECNICA ART', 'MIN PRIMA PURA COT', 'MIN PRIMA TARIFA COT', 'MAX PRIMA PURA COT', 'Total Monto Diferencia Prima Pura', 'Total Monto Diferencia Prima Tarifa']
    return df_grouped


def process_resumen_deprecated(df):
    # Convert columns to numeric type and round to 2 decimal places
    numeric_columns = ['Prima Tecnica Art.', 'MIN Prima Pura Cot', 'MIN Prima Tarifa Cot', 'MAX Prima Pura Cot', 'Monto Diferencia Prima Pura', 'Monto Diferencia Prima Tarifa']
    for col in numeric_columns:
        df[col] = pd.to_numeric(df[col], errors='coerce').round(2)

    df['Mapped Nombre Producto'] = df['Nombre Producto'].map(products_data)
    df_grouped = df.groupby('Updated Nombre Producto').agg({
        'Mapped Nombre Producto': 'count',
        'Prima Tecnica Art.': 'sum',
        'MIN Prima Pura Cot': 'sum',
        'MIN Prima Tarifa Cot': 'sum',
        'MAX Prima Pura Cot': 'sum',
        'Monto Diferencia Prima Pura': ['sum', 'count'],
        'Monto Diferencia Prima Tarifa': ['sum', 'count']
    }).reset_index()

    df_grouped.columns = ['PRODUCTO', 'CANTIDAD', 'PRIMA TÉCNICA ART', 'MIN PRIMA PURA COT', 'MIN PRIMA TARIFA COT', 'MAX PRIMA PURA COT', 'Total Monto Diferencia Prima Pura', 'Count Prima Pura', 'Total Monto Diferencia Prima Tarifa', 'Count Prima Tarifa']
    return df_grouped


def process_resumen(df):
    # Convert columns to numeric type and round to 2 decimal places
    numeric_columns = ['Prima Tecnica Art.', 'MIN Prima Pura Cot', 'MIN Prima Tarifa Cot', 'MAX Prima Pura Cot', 'Monto Diferencia Prima Pura', 'Monto Diferencia Prima Tarifa']
    for col in numeric_columns:
        df[col] = pd.to_numeric(df[col], errors='coerce').round(2)

    df['Mapped Nombre Producto'] = df['Nombre Producto'].map(products_data)

    # Custom aggregation functions
    sum_negatives = lambda x: x[x < 0].sum()
    count_negatives = lambda x: (x < 0).sum()

    df_grouped = df.groupby('Updated Nombre Producto').agg({
        'Mapped Nombre Producto': 'count',
        'Prima Tecnica Art.': 'sum',
        'MIN Prima Pura Cot': 'sum',
        'MIN Prima Tarifa Cot': 'sum',
        'MAX Prima Pura Cot': 'sum',
        'Monto Diferencia Prima Pura': [sum_negatives, count_negatives],
        'Monto Diferencia Prima Tarifa': [sum_negatives, count_negatives]
    }).reset_index()

    df_grouped.columns = ['PRODUCTO', 'CANTIDAD', 'PRIMA TÉCNICA ART', 'MIN PRIMA PURA COT', 'MIN PRIMA TARIFA COT', 'MAX PRIMA PURA COT', 'Total Monto Diferencia Prima Pura', 'Count Prima Pura', 'Total Monto Diferencia Prima Tarifa', 'Count Prima Tarifa']
    return df_grouped


def process_uploaded_file(uploaded_file):
    if uploaded_file is not None:
        df = pd.read_excel(uploaded_file)
        
        df = updated_name_column(df)
        df = add_cobertura_basica_column(df)
        df = add_capital_seg_column(df)
        df = add_resp_civil_column(df)
        df = add_ovp_column(df)
        df = add_tipo_column(df)
        df = add_franquicia_column(df)
        df = add_importacion_column(df)
        df = add_segmento_column(df)
        df = add_segmento_casco_column(df)
        df = add_segmento_rc_column(df)
        df = add_segmento_ovp_column(df)
        df = add_final_casco_column(df)
        df = add_tasa_min_prima_pura_casco_column(df)
        df = add_tasa_min_prima_pura_rc_column(df)
        df = add_tasa_min_prima_pura_ovp_column(df)
        df = add_prima_min_cobertura_basica_casco_column(df)
        df = add_prima_min_rc_column(df)
        df = add_prima_min_ovp_column(df)
        df = add_dias_vigencia_column(df)
        df = add_prima_tecnica_art_column(df)
        df = add_min_prima_pura_cot_column(df)
        df = add_min_prima_tarifa_cot_column(df)
        df = add_tasa_max_prima_pura_casco_column(df)
        df = add_tasa_max_prima_pura_rc_column(df)
        df = add_tasa_max_prima_pura_ovp_column(df)
        df = add_prima_max_cobertura_basica_casco_column(df)
        df = add_prima_max_rc_column(df)
        df = add_prima_max_ovp_column(df)
        df = add_max_prima_pura_cot_column(df)
        df = add_max_prima_tarifa_cot_column(df)
        df = add_monto_diferencia_prima_pura_column(df)
        df = add_monto_diferencia_prima_tarifa_column(df)

    return df