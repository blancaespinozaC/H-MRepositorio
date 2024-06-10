"""
Divani Shiomara Tovilla Barradas
07/06/2024
Creacion del dashboad 2
¿Cual es el producto mas caro de cada categoria?"
"""

import dash_table
import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc
from dash import dcc, html, Dash, callback, Input, Output
from mysql.connector import connect, Error

# Funcion para conectar a la base de datos
def conectar():
    try:
        conexiondb = connect(host="localhost", user="root", password="", database="HYM")
        return conexiondb
    except Error as e:
        print(e)
        return None

# Funcion para leer datos desde la base de datos
def read_data_from_sql(sql_query):
    conn = conectar()
    if conn is None:
        return pd.DataFrame()  # Devolver un DataFrame vacio si la conexion falla
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
WHERE (p.Id_cate, p.Precios) IN (
    SELECT Id_cate, MAX(Precios)
    FROM Productos
    GROUP BY Id_cate
)
"""

# Leer los datos desde la base de datos
data = read_data_from_sql(sql_query)

def tarjetas_filtro():
    control = dbc.Card(
        dbc.CardBody([
            html.H5("DATOS"),
            html.Div([
                dbc.Label("Categoria:"),
                dcc.Dropdown(
                    options=[{"label": "Todas", "value": "all"}] + [{"label": cat, "value": cat} for cat in data["NombreCate"].unique()],
                    id="ddlCategory",
                    value="all",
                    style={"font-family": "fantasy"}
                )
            ]),
            html.Div([
                dbc.Label("Rango de Precios:", style={"color": "black"}),
                dcc.RangeSlider(
                    id='price-range-slider',
                    min=data['Precios'].min(),
                    max=data['Precios'].max(),
                    step=1,
                    value=[data['Precios'].min(), data['Precios'].max()],
                    marks={i: str(i) for i in range(int(data['Precios'].min()), int(data['Precios'].max()) + 1, 500)}
                )
            ])
        ])
    ,style={"background-color": "#FF70AB", "font-family": "cursive"})
    return control


@callback(
    Output(component_id="figProducts", component_property="figure"),
    Input(component_id="ddlCategory", component_property="value"),
    Input(component_id='price-range-slider', component_property='value')
)
def update_grafica(value_category, price_range):
    filtered_data = data
    if value_category != "all":
        filtered_data = filtered_data[filtered_data["NombreCate"] == value_category]
    filtered_data = filtered_data[
        (filtered_data["Precios"] >= price_range[0]) & (filtered_data["Precios"] <= price_range[1])]

    fig = px.bar(filtered_data, x="NombrePro", y="Precios", color="NombreCate",
                 title="Productos mas caros por categoria",
                 labels={"Precios": "Precio", "NombrePro": "Producto"}, hover_data=["NombrePro"])
    fig.update_layout(plot_bgcolor="white", paper_bgcolor="white", font={"color": "black"})

    return fig


def dash_layout(data: pd.DataFrame):
    fig = px.bar(data, x="NombrePro", y="Precios", color="NombreCate", title="Productos mas caros por categoria",
                 labels={"Precios": "Precio", "NombrePro": "Producto"}, hover_data=["NombrePro"])

    body = html.Div([
        html.H1("Producto mas caro de cada categoria", style={"textAlign": "center", "color": "#faf7f7", "background-color": "#bf1919", "font-family":"fantasy"}),
        html.P("Objetivo Dashboard: Mostrar los productos más caros por categoría.",style={"color":"black","font-family":"cursive"}),
        html.Hr(),

        dbc.Row([
            dbc.Col(tarjetas_filtro(), width=3),

            dbc.Col([
                dash_table.DataTable(data=data.to_dict("records"), page_size=10, style_table={'height': '300px', 'overflowY': 'auto'}),
                dcc.Graph(figure=fig, id="figProducts")
            ], width=9)
        ])
    ],style={"background-color": "#FFD0D0"})
    return body


if __name__ == "__main__":
    app = Dash(__name__, external_stylesheets=[dbc.themes.FLATLY])
    app.layout = dash_layout(data)
    app.run(debug=True)
