from analisis import *
import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedStyle
import pandas as pd
import plotly.express as px
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def mostrar_mapa(datafile='globalterrorismdb-0522dist.csv'):
    # Leer los datos desde el archivo CSV
    df = pd.read_csv(datafile, dtype={'summary': str})

    # Filtrar los datos: Obtener eventos a partir del año 2000 con al menos una víctima mortal
    df = df[df['iyear'] >= 2000]
    df = df[df['nkill'] > 0]

    # Verificar si las columnas existen en el DataFrame
    columns = ['attacktype1_txt', 'targtype1_txt', 'weaptype1_txt', 'gname', 'country_txt', 'region_txt', 'city', 'resolution', 'location']
    for column in columns:
        if column not in df.columns:
            print(f"La columna {column} no existe en el DataFrame.")
            return

    # Rellenar los valores NaN con una cadena vacía
    df[columns] = df[columns].fillna('')

    # Agregar columnas personalizadas
    df['custom_info'] = df['attacktype1_txt'] + "<br>" + \
                       df['targtype1_txt'] + "<br>" + \
                       df['weaptype1_txt'] + "<br>" + \
                       df['gname'] + "<br>" + \
                       df['country_txt'] + "<br>" + \
                       df['region_txt'] + "<br>" + \
                       df['city'] + "<br>" + \
                       df['resolution'] + "<br>" + \
                       df['location']

    # Crear la figura con el estilo personalizado
    fig = px.scatter_mapbox(df, lat="latitude", lon="longitude", hover_name="nkill", hover_data=["custom_info"], zoom=10, color="attacktype1_txt",
                            size=df['nkill'], size_max=20, color_continuous_scale=px.colors.sequential.Plasma)

    # Configuración del mapa
    fig.update_layout(
        mapbox_style="open-street-map",
        margin={"r": 0, "t": 0, "l": 0, "b": 0},
        hovermode='closest',  # Resalta el punto más cercano al pasar el cursor
        mapbox=dict(
            bearing=0,  # Dirección inicial del mapa
            pitch=0,    # Ángulo de inclinación
        )
    )

    # Mostrar la figura
    fig.show()


def relacion_importaciones_atentados():
    # Leer los datos de importaciones de armas y atentados
    importaciones = pd.read_csv('TIV-Import-All-1970-2022.csv', index_col=0)
    atentados = pd.read_csv('globalterrorismdb-0522dist.csv', encoding='ISO-8859-1')

    # Renombrar la columna 'Total'
    importaciones = importaciones.rename(columns={'Total': 'importaciones'})

    # Convertir el índice a una columna
    importaciones.reset_index(inplace=True)
    importaciones = importaciones.rename(columns={'index': 'country_txt'})

    atentados = atentados[['country_txt', 'nkill']]

    # Combinar los datos en un solo DataFrame
    datos_combinados = importaciones.merge(atentados, on='country_txt', how='inner')

    # Crear un gráfico de dispersión
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.scatter(datos_combinados['importaciones'], datos_combinados['nkill'])
    ax.set_xlabel('Importaciones de armas')
    ax.set_ylabel('Número de atentados')
    ax.set_title('Relación entre las importaciones de armas y el número de atentados')

    # Crear una ventana de Tkinter y embeber el gráfico en ella
    root = tk.Tk()
    root.title('Gráfico de Relación Importaciones-Atentados')

    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.get_tk_widget().pack()

    root.mainloop()


def actualizar_resumen():
    # Obtener el país, el año, el mes y el día seleccionados
    pais = pais_seleccionado.get()
    anio = int(anio_seleccionado.get())
    mes = int(mes_seleccionado.get())
    dia = int(dia_seleccionado.get())

    # Filtrar los datos por país, año, mes y día
    ataques = data[(data['country_txt'] == pais) & (data['iyear'] == anio) & (data['imonth'] == mes) & (data['iday'] == dia)]

    # Mostrar el resumen del ataque seleccionado en el cuadro de texto
    resumen_texto.delete('1.0', tk.END)

    if len(ataques) > 0:
        # Permitir al usuario seleccionar un ataque de la lista
        selected_attack = ataques.sample(n=1)  # Aquí seleccionamos un ataque aleatorio, puedes personalizar esto
        resumen_texto.insert(tk.END, selected_attack.iloc[0]['summary'])
    else:
        resumen_texto.insert(tk.END, "No se encontraron ataques para el país, año, mes y día seleccionados.")

# Función para mostrar datos en una ventana Tkinter
def mostrar_datos():
    # Crear una ventana Tkinter para mostrar los datos
    datos_window = tk.Toplevel(root)
    datos_window.title("Datos de Armamento")
    Df = pd.read_csv('TIV_of_arms_exports_to_all_1970-2022.csv', encoding='ISO-8859-1', delimiter=';')

    # Crear un Frame para contener la barra de desplazamiento y el Treeview
    frame = tk.Frame(datos_window)
    frame.pack()

    # Crear una barra de desplazamiento horizontal
    scroll_x = tk.Scrollbar(frame, orient="horizontal")

    # Crear un Treeview para mostrar los datos en una tabla
    tree = ttk.Treeview(frame, columns=list(Df.columns), show="headings", xscrollcommand=scroll_x.set)

    # Configurar las columnas
    for column in Df.columns:
        tree.heading(column, text=column)
        tree.column(column, width=100)  # Ajusta el ancho de las columnas según tus necesidades

    # Insertar los datos en la tabla
    for i, row in Df.iterrows():
        tree.insert("", "end", values=list(row))

    # Configurar la barra de desplazamiento para desplazarse junto al Treeview
    scroll_x.config(command=tree.xview)

    # Empacar la barra de desplazamiento y el Treeview
    scroll_x.pack(side="bottom", fill="x")
    tree.pack()

# Cargar los datos desde el archivo CSV
data = pd.read_csv('globalterrorismdb-0522dist.csv', encoding='ISO-8859-1', low_memory=False)
root = tk.Tk()
root.title("Summary, Map info")

# Configurar el fondo con el color del tema "equilux"
equilux_background_color = "#3c3f41"  # Color de fondo de equilux
root.configure(background=equilux_background_color)

style = ThemedStyle(root)
style.set_theme("equilux")


# Crear una lista de países únicos, años únicos, meses únicos y días únicos
paises_unicos = data['country_txt'].unique()
paises_unicos.sort()
anios_unicos = data['iyear'].unique()
meses_unicos = data['imonth'].unique()
dias_unicos = data['iday'].unique()

# Crear variables de Tkinter para el país, el año, el mes y el día seleccionados
pais_seleccionado = tk.StringVar(root)
pais_seleccionado.set(paises_unicos[0])
anio_seleccionado = tk.StringVar(root)
anio_seleccionado.set(anios_unicos[0])
mes_seleccionado = tk.StringVar(root)
mes_seleccionado.set(meses_unicos[0])
dia_seleccionado = tk.StringVar(root)
dia_seleccionado.set(dias_unicos[0])

# Crear un Frame para los menús desplegables
menu_frame = ttk.Frame(root)
menu_frame.pack(pady=10)

# Crear un menú desplegable para seleccionar el país
pais_label = ttk.Label(menu_frame, text="País:")
pais_label.pack(side="left", padx=10)
pais_menu = ttk.OptionMenu(menu_frame, pais_seleccionado, *paises_unicos)
pais_menu.pack(side="left", padx=10)

# Crear un menú desplegable para seleccionar el año
anio_label = ttk.Label(menu_frame, text="Año:")
anio_label.pack(side="left", padx=10)
anio_menu = ttk.OptionMenu(menu_frame, anio_seleccionado, *anios_unicos)
anio_menu.pack(side="left", padx=10)

# Crear un menú desplegable para seleccionar el mes
mes_label = ttk.Label(menu_frame, text="Mes:")
mes_label.pack(side="left", padx=10)
mes_menu = ttk.OptionMenu(menu_frame, mes_seleccionado, *meses_unicos)
mes_menu.pack(side="left", padx=10)

# Crear un menú desplegable para seleccionar el día
dia_label = ttk.Label(menu_frame, text="Día:")
dia_label.pack(side="left", padx=10)
dia_menu = ttk.OptionMenu(menu_frame, dia_seleccionado, *dias_unicos)
dia_menu.pack(side="left", padx=10)

# Crear un cuadro de texto para mostrar el resumen del ataque seleccionado
resumen_frame = ttk.Frame(root)
resumen_frame.pack(pady=10)
resumen_label = ttk.Label(resumen_frame, text="Resumen:")
resumen_label.pack(side="left", padx=10)
resumen_texto = tk.Text(resumen_frame, height=10, width=80)
resumen_texto.pack(side="left", padx=10)



# Crear un botón con la imagen redimensionada
mostrar_grafico_boton = ttk.Button(root, text="Mostrar mapa", command=mostrar_mapa)
mostrar_grafico_boton.pack(pady=10)

# Botón para actualizar
actualizar_boton = ttk.Button(root, text="Actualizar", command=actualizar_resumen)
actualizar_boton.pack(pady=10)

# Ver armamento
ver_armamento = ttk.Button(root, text="Ver armamento", command=mostrar_datos)
ver_armamento.pack(pady=10)

# Crear radio buttons
radio_frame = ttk.Frame(root)
radio_frame.pack(pady=10)
radio_label = ttk.Label(radio_frame, text="Opciones:")
radio_label.pack(side="left", padx=10)

radio_1 = ttk.Radiobutton(radio_frame, text="Relación entre compras de armas y atentados", command=relacion_importaciones_atentados, value=1, variable=1)
radio_1.pack(side="left", padx=10)

radio_2 = ttk.Radiobutton(radio_frame, text="Atentados por tipo de arma", command=subarmas, value=2, variable=1)
radio_2.pack(side="left", padx=10)

radio_3 = ttk.Radiobutton(radio_frame, text="Atentados por grupo terrorista", command=group_attacks, value=3, variable=1)
radio_3.pack(side="left", padx=10)

radio_4 = ttk.Radiobutton(radio_frame, text="Atentados por pais", command=total_attacks_by_country, value=4, variable=1)
radio_4.pack(side="left", padx=10)

# Ejecutar la ventana de Tkinter
root.mainloop()