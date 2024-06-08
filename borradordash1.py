"""
Araceli Garcia Diaz
07/06/2024
Dashboad: ¿Qué productos tienen los precios más altos en cada categoría?"
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

def tarjetas_filtro():
    control = dbc.Card(
        dbc.CardBody([
            html.H5("FILTROS DE DATOS"),
            html.Div([
                dbc.Label("Categoría:"),
                dcc.Dropdown(
                    options=[{"label": "Todas", "value": "all"}] + [{"label": cat, "value": cat} for cat in data["NombreCate"].unique()],
                    id="ddlCategory",
                    value="all"
                )
            ])
        ])
    )
    return control

@callback(
    Output(component_id="figProducts", component_property="figure"),
    Input(component_id="ddlCategory", component_property="value")
)
def update_grafica(value_category):
    if value_category == "all":
        filtered_data = data
    else:
        filtered_data = data[data["NombreCate"] == value_category]

    # Convertir la columna de precios a un tipo numérico
    filtered_data['Precios'] = pd.to_numeric(filtered_data['Precios'])

    fig = px.scatter(filtered_data, x="NombrePro", y="Precios", color="NombreCate", size="Precios",
                     title="Precio de Productos por Categoría", labels={"Precios": "Precio", "NombrePro": "Producto"},
                     hover_data=["NombrePro"])
    fig.update_layout(plot_bgcolor="black", paper_bgcolor="black", font={"color": "black"})
    fig.update_traces(marker=dict(opacity=0.7, sizemode='area'))

    return fig

def dash_layout(data: pd.DataFrame):
    # Convertir la columna de precios a un tipo numérico
    data['Precios'] = pd.to_numeric(data['Precios'])

    fig = px.scatter(data, x="NombrePro", y="Precios", color="NombreCate", size="Precios",
                     title="Precio de Productos por Categoría", labels={"Precios": "Precio", "NombrePro": "Producto"},
                     hover_data=["NombrePro"])

    body = html.Div([
        html.H1("Datos de Productos", style={"textAlign": "center", "color": "#FFA62F", "background-color": "#FFE8C8"}),
        html.P("Objetivo Dashboard: Mostrar los productos por categoría."),
        html.Hr(),

        dbc.Row([
            dbc.Col(tarjetas_filtro(), width=3),

            dbc.Col([
                dash_table.DataTable(data=data.to_dict("records"), page_size=10),
                dcc.Graph(figure=fig, id="figProducts")
            ], width=9)
        ])
    ])
    return body

if __name__ == "__main__":
    app = Dash(__name__, external_stylesheets=[dbc.themes.FLATLY])
    app.layout = dash_layout(data)
    app.run(debug=True)
