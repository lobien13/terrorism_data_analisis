import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from clean_data import look_up

def total_attacks_by_year():
    df = pd.read_csv('globalterrorismdb-0522dist.csv', encoding='ISO-8859-1')
    columns_to_keep = ['iyear', 'eventid']
    df = df[columns_to_keep]
    df = df.groupby('iyear').count()
    df = df.rename(columns={'eventid': 'total_attacks'})
    df.plot(kind='bar', y='total_attacks', legend=False)
    plt.title('Total de ataques por año')
    plt.xlabel('Año')
    plt.ylabel('Número de ataques')
    plt.show()
    return df

def total_attacks_by_country():
    df = pd.read_csv('globalterrorismdb-0522dist.csv', encoding='ISO-8859-1')
    columns_to_keep = ['country_txt', 'eventid']
    df = df[columns_to_keep]
    df = df.groupby('country_txt').count()
    df = df.rename(columns={'eventid': 'total_attacks'})
    df.plot(kind='bar', y='total_attacks', legend=False)
    plt.title('Total de ataques por país')
    plt.xlabel('País')
    plt.ylabel('Número de ataques')
    plt.show()
    return df

def total_attacks_by_countryMAX():
    df = pd.read_csv('globalterrorismdb-0522dist.csv', encoding='ISO-8859-1')
    columns_to_keep = ['country_txt', 'eventid']
    df = df[columns_to_keep]
    df = df.groupby('country_txt').count()
    df = df.rename(columns={'eventid': 'total_attacks'})
    df = df[df['total_attacks'] > 1000]
    df.plot(kind='bar', y='total_attacks', legend=False)
    plt.title('Total de ataques por país')
    plt.xlabel('País')
    plt.ylabel('Número de ataques')
    plt.show()
    return df

def group_attacks():
    df = look_up()
    columns_to_keep = ['gname', 'eventid']
    df = df[columns_to_keep]
    df = df.groupby('gname').count()
    df = df.rename(columns={'eventid': 'total_attacks'})
    df = df[df['total_attacks'] > 1000]
    df = df.sort_values(by='total_attacks', ascending=True)
    df.plot(kind='barh', y='total_attacks', legend=False)
    plt.title('Total de ataques por grupo')
    plt.ylabel('Grupo')
    plt.xlabel('Número de ataques')
    plt.show()
    return df

def subarmas():
    df = pd.read_csv('globalterrorismdb-0522dist.csv', encoding='ISO-8859-1')
    columns_to_keep = ['iyear', 'weapsubtype1_txt']
    df = df[columns_to_keep]
    df = df.groupby('iyear').count()
    df = df.rename(columns={'weapsubtype1_txt': 'total_attacks'})
    df.plot(kind='line', y='total_attacks', legend=False)
    plt.title('Total de ataques por subarma')
    plt.xlabel('Año')
    plt.ylabel('Número de ataques')
    plt.show()
    return df

def tipos_subarmas_paises_top_10():
    df = pd.read_csv('globalterrorismdb-0522dist.csv', encoding='ISO-8859-1')
    top_10_paises = df['country_txt'].value_counts().head(10).index
    data_top_10 = df[df['country_txt'].isin(top_10_paises)]
    tipos_subarmas = data_top_10['weaptype1_txt'].value_counts()
    plt.figure(figsize=(12, 6))
    tipos_subarmas.plot(kind='bar')
    plt.title('Tipos de Subarmas más Utilizados en los 10 Países con más Subarmas')
    plt.xlabel('Tipo de Subarma')
    plt.ylabel('Número de Incidentes')
    plt.xticks(rotation=45)
    plt.show()
    return tipos_subarmas

def most_frequent_target_types():
    df = pd.read_csv('globalterrorismdb-0522dist.csv', encoding='ISO-8859-1')
    columns_to_keep = ['targtype1_txt', 'eventid']
    df = df[columns_to_keep]
    df = df.groupby('targtype1_txt').count()
    df = df.rename(columns={'eventid': 'total_attacks'})
    df = df[df['total_attacks'] > 0]
    df.plot(kind='bar', y='total_attacks', legend=False)
    plt.title('Most frequent target types')
    plt.xlabel('Target type')
    plt.ylabel('Number of attacks')
    plt.show()
    return df

def analizar_datos_terrorismo():
    df = pd.read_csv('globalterrorismdb-0522dist.csv', encoding='ISO-8859-1')
    num_filas, num_columnas = df.shape
    columnas = df.columns.tolist()
    estadisticas = df.describe()
    ataques_por_pais = df['country_txt'].value_counts()
    total_ataques = ataques_por_pais.sum()
    top_10_paises = ataques_por_pais.head(10)
    tipos_de_ataque = df['attacktype1_txt'].value_counts()
    print(f"Resumen de datos básicos:")
    print(f"Número de filas: {num_filas}")
    print(f"Número de columnas: {num_columnas}")
    print(f"Columnas disponibles: {', '.join(columnas)}")
    print(estadisticas)
    print("\nAnálisis por país:")
    print(f"Número total de ataques: {total_ataques}")
    print(f"Top 10 países con más ataques:")
    print(top_10_paises)
    print("\nTipos de ataque:")
    print(tipos_de_ataque)
    return df

def relacion_exito_tipo_de_ataque(df):
    success_by_attack = df.groupby('attacktype1_txt')['success'].mean()
    return success_by_attack

def grafico_relacion_exito_tipo_de_ataque(df):
    success_by_attack = df.groupby('attacktype1_txt')['success'].mean()
    plt.figure(figsize=(10, 6))
    success_by_attack.plot(kind='bar', color='lightcoral')
    plt.title('Relación entre el éxito y el tipo de ataque')
    plt.xlabel('Tipo de Ataque')
    plt.ylabel('Tasa de Éxito')
    plt.xticks(rotation=45)
    plt.ylim(0, 1)
    plt.show()

def mapa_de_calor_correlación(df):
    columns = df.select_dtypes(include=[int, float]).columns
    df_numeric = df[columns]
    corr_matrix = df_numeric.corr()
    plt.figure(figsize=(12, 8))
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', linewidths=0.5)
    plt.title('Mapa de Calor de Correlación entre Variables')
    plt.show()

def grafico_barras_apiladas_tipos_de_ataque_por_region(df):
    attack_type_by_region = df.groupby(['region_txt', 'attacktype1_txt']).size().unstack()
    attack_type_by_region.plot(kind='bar', stacked=True, colormap='viridis', figsize=(12, 6))
    plt.title('Tipos de Ataque por Región')
    plt.xlabel('Región')
    plt.ylabel('Número de Incidentes')
    plt.xticks(rotation=45)
    plt.legend(title='Tipo de Ataque', loc='upper right')
    plt.show()

def grafico_distribucion_victimas_por_año(df):
    df['iyear'] = df['iyear'].astype(int)
    df['nkill'] = df['nkill'].fillna(0).astype(int)
    plt.figure(figsize=(12, 6))
    sns.kdeplot(data=df, x='iyear', hue='nkill', common_norm=False, fill=True, palette='crest', alpha=.5, linewidth=0)
    plt.title('Distribución de Víctimas (Muertes) por Año')
    plt.xlabel('Año')
    plt.ylabel('Densidad')
    plt.show()

def distribucion_geografica(df):
    plt.figure(figsize=(12, 8))
    sns.scatterplot(data=df, x='longitude', y='latitude', hue='nkill', size='nkill', sizes=(10, 200), palette='coolwarm', alpha=0.7)
    plt.title('Distribución Geográfica de Ataques Terroristas')
    plt.xlabel('Longitud')
    plt.ylabel('Latitud')
    plt.show()





























