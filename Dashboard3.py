"""
Blanca Isabel Espinoza Cruz
09/06/2024
Creacion del dashboad 3
¿Cuál es el precio promedio de los productos en la categoría?"
"""
from dash import dash_table
import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc
from dash import dcc, html, Dash, Input, Output
from mysql.connector import connect, Error

# Función para conectar a la base de datos
def conectar():
    try:
        conexiondb = connect(host="localhost", user="root", password="", database="HYM")
        return conexiondb
    except Error as e:
        print(e)
        return None

# Función para leer datos desde la base de datos
def read_data_from_sql(sql_query):
    conn = conectar()
    if conn is None:
        return pd.DataFrame()  # Devolver un DataFrame vacío si la conexión falla
    try:
        cursor = conn.cursor()
        cursor.execute(sql_query)
        data = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        cursor.close()
        conn.close()

        df = pd.DataFrame(data, columns=columns)
        return df
    except Error as e:
        print("Error leyendo datos desde MySQL:", e)
        return pd.DataFrame()

# Consulta SQL para obtener los datos
sql_query = """
SELECT p.Id_cate, c.NombreCate, p.Precios, p.NombrePro 
FROM Productos p 
JOIN Categorias c ON p.Id_cate = c.Id_cate
"""

# Leer los datos desde la base de datos
data = read_data_from_sql(sql_query)

# Colores para cada categoría
colores_categoria = {
    "Mujer": "#FFB6C1",
    "Hombre": "#87CEFA",
    "Ninos": "#66CDAA",
    "Home": "#BC8F8F",
    "Sport": "#778899",
    "Beauty": "#DDA0DD",
    "Bebe": "#FFDEAD"
}

# Crear la aplicación Dash
app = Dash(__name__, external_stylesheets=[dbc.themes.FLATLY])

controls = dbc.Card(
    [
        html.Div(
            [
                dbc.Label("Categoría"),
                dcc.Dropdown(
                    id="dropdown-categoria",
                    options=[
                        {"label": cat, "value": cat} for cat in data["NombreCate"].unique()
                    ],
                    value=data["NombreCate"].unique()[0],style={"background-color": "#E1AFD1","font-family":"fantasy"}
                ),
            ]
        ),
        html.Div(
            [
                dbc.Label("Número de Productos"),
                dbc.Input(id="num-products", type="number", value=10),
            ]
        ),
        dbc.Card(
            dbc.CardBody([
                html.H5("Precio Promedio de los Productos"),
                html.H2(id='precio-promedio-general', style={'textAlign': 'center', 'color': '#C738BD'}),
            ]),
            style={"width": "100%", "marginTop": "20px","background-color":"#EE99C2"}
        )
    ],
    body=True,
)

app.layout = dbc.Container(
    [
        html.H1("Precio Promedio de Productos por Categoría", style={"textAlign": "center", "backgroundColor": "#D8BFD8", "color": "white"}),
        html.P("Objetivo del Dashboard: Mostrar el precio promedio de los productos en cada categoría",style={"color":"#E59BE9","font-family":"cursive"}),
        html.Hr(),
        dbc.Row(
            [
                dbc.Col(controls, md=4),
                dbc.Col(dcc.Graph(id="scatter-plot", style={"height": "80vh"}), md=8),
            ],
            align="center",
        ),
    ],
    fluid=True,
    style={"backgroundColor": "#F8F9D7"}
)

@app.callback(
    Output("scatter-plot", "figure"),
    Output("precio-promedio-general", "children"),
    Input("dropdown-categoria", "value"),
    Input("num-products", "value")
)
def update_grafica(categoria, num_products):
    filtered_data = data[data['NombreCate'] == categoria]

    # Limitar el número de productos a mostrar
    filtered_data = filtered_data.head(num_products)

    if not filtered_data.empty:  # Verificar si filtered_data no está vacío
        fig = px.scatter(filtered_data, x='NombrePro', y='Precios', color='NombreCate',
                         title=f'Precio Promedio en la Categoría {categoria}', labels={"Precios": "Precio Promedio", "NombrePro": "Producto"},
                         color_discrete_map=colores_categoria)

        # Hacer las bolitas más grandes
        fig.update_traces(marker=dict(size=22))

        precio_promedio_general = f"${filtered_data['Precios'].mean():.2f}"
    else:
        # Si no hay datos para la categoría seleccionada, retornar un gráfico vacío y un mensaje indicando que no hay datos
        fig = px.scatter(title="No hay datos disponibles")
        precio_promedio_general = "No disponible"

    return fig, precio_promedio_general

if __name__ == "__main__":
    app.run_server(debug=True, port=8888)
