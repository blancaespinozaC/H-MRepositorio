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
        datos = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        cursor.close()
        conn.close()

        df = pd.DataFrame(datos, columns=columns)
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

datos = leerDatos(sql_query)

def tarjetas_filtro():
    control = dbc.Card(
        dbc.CardBody([
            html.H5("Filtros de Datos"),
            html.Div([
                dbc.Label("Categoría:"),
                dcc.Dropdown(
                    options=[{"label": "Todas", "value": "all"}] + [{"label": cat, "value": cat} for cat in datos["NombreCate"].unique()],
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

def graficaBarras(datos):
    datos["Cantidad"] = datos.groupby("NombreCate")["Precios"].transform("count")
    fig = px.bar(datos.drop_duplicates("NombreCate"), x="NombreCate", y="Cantidad", title="Número de productos por categoría",
                 labels={"NombreCate": "Categoría", "Cantidad": "Cantidad de productos"},
                 color="Cantidad", color_continuous_scale="Oranges")
    fig.update_layout(plot_bgcolor="#FFD39B")
    return fig

def graficoDispersion(datos):
    fig = px.scatter(datos, x="NombreCate", y="Precios", color="NombreCate",
                     title="Relación entre precios y categorías",
                     labels={"NombreCate": "Categoría", "Precios": "Precio"},
                     color_continuous_scale="Oranges")
    fig.update_layout(plot_bgcolor="#FFD39B")
    return fig

def graficaPastel(datos):
    datos["Cantidad"] = datos.groupby("NombreCate")["Precios"].transform("count")
    fig = px.pie(datos.drop_duplicates("NombreCate"), names="NombreCate", values="Cantidad",
                 title="Proporción de productos por categoría", color_discrete_sequence=['#FF5733', '#FF8C00', '#FFA500'])
    fig.update_layout(plot_bgcolor="#FFD39B")
    return fig


@callback(
    [Output("Productos", "figure"),
     Output("Barras", "figure"),
     Output("Dispersion", "figure"),
     Output("Pastel", "figure")],
    [Input("categoria", "value"),
     Input('precio', 'value')]
)
def update_graficas(valorCategorias, rangoPrecio):
    filtro = datos
    if valorCategorias != "all":
        filtro = filtro[filtro["NombreCate"] == valorCategorias]

    rango_precio_dict = {
        "100-500": (100, 500),
        "501-1000": (501, 1000),
        "1001-1500": (1001, 1500)
    }

    rango = rango_precio_dict[rangoPrecio]
    filtro = filtro[
        (filtro["Precios"] >= rango[0]) &
        (filtro["Precios"] <= rango[1])
    ]

    filtro["Precios"] = pd.to_numeric(filtro["Precios"])

    violin_fig = px.violin(filtro, y="Precios", x="NombreCate", color="NombreCate",
                           box=True, points="all",
                           title="Distribución de precios por categoría de productos",
                           labels={"Precios": "Precio", "NombreCate": "Categoría"})
    violin_fig.update_layout(plot_bgcolor="white", paper_bgcolor="white", font={"color": "black"})

    grafBarra = graficaBarras(filtro)
    dispersion = graficoDispersion(filtro)
    graficaPaastel = graficaPastel(filtro)

    return violin_fig, grafBarra, dispersion, graficaPaastel

def dash_layout(datos: pd.DataFrame):
    datos['Precios'] = pd.to_numeric(datos['Precios'])

    violin_fig = px.violin(datos, y="Precios", x="NombreCate", color="NombreCate",
                           box=True, points="all",
                           title="Distribución de precios por categoría de productos",
                           labels={"Precios": "Precio", "NombreCate": "Categoría"})

    grafBarra = graficaBarras(datos)
    dispersion = graficoDispersion(datos)
    graficaPaastel = graficaPastel(datos)

    body = html.Div([
        html.H1("¿Cuál es la distribución de precios por categoría de productos?", style={"textAlign": "center", "color": "#FFA62F", "background-color": "#FFE8C8","font-family":"fantasy"}),
        html.P("Objetivo del Dashboard: Mostrar la distribución de precios por categoría de productos.", style={"color": "orange", "font-family": "cursive"}),
        html.Hr(),

        dbc.Row([
            dbc.Col(tarjetas_filtro(), width=3),
            dbc.Col([
                dcc.Graph(figure=violin_fig, id="Productos"),
                dcc.Graph(figure=grafBarra, id="Barras"),
                dcc.Graph(figure=dispersion, id="Dispersion"),
                dcc.Graph(figure=graficaPaastel, id="Pastel")
            ], width=9)
        ]),

        dbc.Row([
            dbc.Col(html.Div("Tabla de datos", style={"background-color": "orange","font-family":"fantasy"}), width=12)
        ]),

        dbc.Row([
            dbc.Col(dash_table.DataTable(data=datos.to_dict("records"), page_size=10), width=12)
        ])
    ], style={"background-color": "#FEFFD2"})
    return body

if __name__ == "__main__":
    app = Dash(__name__, external_stylesheets=[dbc.themes.FLATLY])
    app.layout = dash_layout(datos)
    app.run(debug=True)
