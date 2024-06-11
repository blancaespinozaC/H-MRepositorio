"""
Araceli Garcia Diaz
07/06/2024
Creacion del dashboad 1:
¿Cuál es la distribución de precios por categoría de productos?
"""

import dash_table
import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc
from dash import dcc, html, Dash, callback, Input, Output
from mysql.connector import connect, Error

# Función para conectar a la base de datos
def conectar():
    try:
        conexiondb = connect(host="localhost", user="root", password="", database="HYM")
        return conexiondb
    except Error as e:
        print(e)
        return None

def leerDatos(sql_query):
    conn = conectar()
    if conn is None:
        return pd.DataFrame()
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


data = leerDatos(sql_query)

def tarjetas_filtro():
    control = dbc.Card(
        dbc.CardBody([
            html.H5("Filtros de Datos"),
            html.Div([
                dbc.Label("Categoría:"),
                dcc.Dropdown(
                    options=[{"label": "Todas", "value": "all"}] + [{"label": cat, "value": cat} for cat in data["NombreCate"].unique()],
                    id="categoria",
                    value="all",
                    style={"background-color": "#FEAE6F","font-family":"fantasy"}
                )
            ]),
            html.Div([
                dbc.Label("Rango de Precios:"),
                dcc.RadioItems(
                    options=[
                        {"label": "100 - 500", "value": "100-500"},
                        {"label": "501 - 1000", "value": "501-1000"},
                        {"label": "1001 - 1500", "value": "1001-1500"}
                    ],
                    id='precio',
                    value="100-500",
                    inline=True
                )
            ])
        ])
    )
    return control

@callback(
    Output(component_id="Productos", component_property="figure"),
    Input(component_id="categoria", component_property="value"),
    Input(component_id='precio', component_property='value')
)
def update_grafica(value_category, price_range):
    filtered_data = data
    if value_category != "all":
        filtered_data = filtered_data[filtered_data["NombreCate"] == value_category]

    # Convertir el valor del rango de precios seleccionado en rangos numéricos
    price_ranges = {
        "100-500": (100, 500),
        "501-1000": (501, 1000),
        "1001-1500": (1001, 1500)
    }

    filtered_data = filtered_data[
        (filtered_data["Precios"] >= price_ranges[price_range][0]) &
        (filtered_data["Precios"] <= price_ranges[price_range][1])
    ]

    # Convertir la columna de precios a un tipo numérico
    filtered_data['Precios'] = pd.to_numeric(filtered_data['Precios'])

    fig = px.violin(filtered_data, y="Precios", x="NombreCate", color="NombreCate",
                    box=True, points="all",
                    title="Distribución de precios por categoría de productos",
                    labels={"Precios": "Precio", "NombreCate": "Categoría"})
    fig.update_layout(plot_bgcolor="white", paper_bgcolor="white", font={"color": "black"})

    return fig

def dash_layout(data: pd.DataFrame):
    # Convertir la columna de precios a un tipo numérico
    data['Precios'] = pd.to_numeric(data['Precios'])

    fig = px.violin(data, y="Precios", x="NombreCate", color="NombreCate",
                    box=True, points="all",
                    title="Distribución de precios por categoría de productos",
                    labels={"Precios": "Precio", "NombreCate": "Categoría"})

    body = html.Div([
        html.H1("¿Cuál es la distribución de precios por categoría de productos?", style={"textAlign": "center", "color": "#FFA62F", "background-color": "#FFE8C8","font-family":"fantasy"}),
        html.P("Objetivo del Dashboard: Mostrar la distribución de precios por categoría de productos.",style={"color":"orange","font-family":"cursive"}),
        html.Hr(),

        dbc.Row([
            dbc.Col(tarjetas_filtro(), width=3),

            dbc.Col([
                dcc.Graph(figure=fig, id="Productos")
            ], width=9)
        ]),

        dbc.Row([
            dbc.Col(html.Div("Tabla de datos", style={"background-color": "orange","font-family":"fantasy"}), width=12)
        ]),

        dbc.Row([
            dbc.Col(dash_table.DataTable(data=data.to_dict("records"), page_size=10), width=12)
        ])
    ],style={"background-color": "#FEFAF6"})
    return body

if __name__ == "__main__":
    app = Dash(__name__, external_stylesheets=[dbc.themes.FLATLY])
    app.layout = dash_layout(data)
    app.run(debug=True)
