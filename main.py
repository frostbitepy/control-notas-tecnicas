import pandas as pd
from processing_helper import (
    updated_name_column,
    add_cobertura_basica_column,
    add_capital_seg_column,
    add_resp_civil_column,
    add_ovp_column,
    add_tipo_column,
    add_franquicia_column,
    add_importacion_column,
    add_segmento_column,
    add_segmento_casco_column,
    add_segmento_rc_column,
    add_segmento_ovp_column,
    add_final_casco_column,
    add_tasa_min_prima_pura_casco_column,
    add_tasa_min_prima_pura_rc_column,
    add_tasa_min_prima_pura_ovp_column,
    add_prima_min_cobertura_basica_casco_column,
    add_prima_min_rc_column,
    add_prima_min_ovp_column,
    add_dias_vigencia_column,
    add_prima_tecnica_art_column,
    add_min_prima_pura_cot_column,
    add_min_prima_tarifa_cot_column,
    add_tasa_max_prima_pura_casco_column,
    add_tasa_max_prima_pura_rc_column,
    add_tasa_max_prima_pura_ovp_column,
    add_prima_max_cobertura_basica_casco_column,
    add_prima_max_rc_column,
    add_prima_max_ovp_column,
    add_max_prima_pura_cot_column,
    add_max_prima_tarifa_cot_column,
    add_monto_diferencia_prima_pura_column,
    add_monto_diferencia_prima_tarifa_column,
    process_resumen
)



file_path = "AUTO.xlsx"

main_df = pd.read_excel(file_path)


df = main_df




print(df.columns)


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

print(df.head())

df.to_excel('listado_generado_plus.xlsx', index=False)


df_new = process_resumen(df)
df_new.to_excel('resumen_5.xlsx', index=False)


