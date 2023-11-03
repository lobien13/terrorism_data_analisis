import pandas as pd

def cargar_procesar_datos():
    # Cargar el archivo CSV en un DataFrame
    df = pd.read_csv('globalterrorismdb-0522dist.csv', encoding='ISO-8859-1')

    # Seleccionar las columnas deseadas en un nuevo DataFrame
    columns_to_keep = ['iyear', 'imonth', 'iday', 'country_txt', 'attacktype1_txt', 'targtype1_txt',
                       'targsubtype1_txt', 'weaptype1_txt', 'weapsubtype1_txt', 'nkill', 'nwound',
                       'gname', 'success', 'suicide', 'ishostkid','eventid']

    df = df[columns_to_keep]

    # Eliminar las filas con valores nulos en el DataFrame resultante
    df.dropna(inplace=True)

    # Eliminar las filas que contienen "unknown" en la columna gname
    # Eliminar las filas que contienen "unknown" en la columna 'gname'
    df = df[df['gname'] != 'Unknown']

    return df

def look_up():
    # Llama a la función cargar_procesar_datos() para obtener el DataFrame procesado
    df_procesado = cargar_procesar_datos()
    
    # Devuelve el DataFrame procesado
    return df_procesado