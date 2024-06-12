"""
Divani Shiomara Tovilla Barradas
11/06/2024
Creacion del dashboard 2
¿Cuál es el producto mas caro de cada categoria?
Deteccion de outliers (precios atipicos)
Top 10 productos mas baratos
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

def leer_datos_desde_sql(consulta_sql):
    conn = conectar()
    if conn is None:
        return pd.DataFrame() 
    try:
        cursor = conn.cursor()
        cursor.execute(consulta_sql)
        data = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        cursor.close()
        conn.close()

        df = pd.DataFrame(data, columns=columns)
        return df
    except Error as e:
        print("Error leyendo datos desde MySQL:", e)
        return pd.DataFrame()

#el producto mas caro de cada categoria
sql_consulta_caro = """
SELECT p.Id_cate, c.NombreCate, p.Precios, p.NombrePro
FROM Productos p
JOIN Categorias c ON p.Id_cate = c.Id_cate
WHERE (p.Id_cate, p.Precios) IN (
    SELECT Id_cate, MAX(Precios)
    FROM Productos
    GROUP BY Id_cate
)
"""

#los 10 productos mas baratos
sql_consulta_baratos = """
SELECT p.Id_cate, c.NombreCate, p.Precios, p.NombrePro
FROM Productos p
JOIN Categorias c ON p.Id_cate = c.Id_cate
ORDER BY p.Precios ASC
LIMIT 10
"""

#los precios atipicos por categoria
sql_consulta_outliers = """
SELECT p.Id_cate, c.NombreCate, p.Precios, p.NombrePro
FROM Productos p
JOIN Categorias c ON p.Id_cate = c.Id_cate
WHERE p.Precios > (SELECT AVG(Precios) + STDDEV(Precios) * 1.5 FROM Productos WHERE Id_cate = p.Id_cate)
OR p.Precios < (SELECT AVG(Precios) - STDDEV(Precios) * 1.5 FROM Productos WHERE Id_cate = p.Id_cate)
"""

datos_caro = leer_datos_desde_sql(sql_consulta_caro)
datos_baratos = leer_datos_desde_sql(sql_consulta_baratos)
datos_outliers = leer_datos_desde_sql(sql_consulta_outliers)

def tarjetas_filtro():
    control = dbc.Card(
        dbc.CardBody([
            html.H5("DATOS"),
            html.Div([
                dbc.Label("Categoria:"),
                dcc.Dropdown(
                    options=[{"label": "Todas", "value": "all"}] + [{"label": cat, "value": cat} for cat in datos_caro["NombreCate"].unique()],
                    id="ddlCategory",
                    value="all"
                )
            ]),
            html.Div([
                dbc.Label("Rango de Precios:", style={"color": "black"}),
                dcc.RangeSlider(
                    id='price-range-slider',
                    min=datos_caro['Precios'].min(),
                    max=datos_caro['Precios'].max(),
                    step=1,
                    value=[datos_caro['Precios'].min(), datos_caro['Precios'].max()],
                    marks={i: str(i) for i in range(int(datos_caro['Precios'].min()), int(datos_caro['Precios'].max()) + 1, 500)}
                )
            ])
        ])
    )
    return control

@callback(
    Output(component_id="figProducts", component_property="figure"),
    Input(component_id="ddlCategory", component_property="value"),
    Input(component_id='price-range-slider', component_property='value')
)
def actualizar_grafica(valor_categoria, rango_precio):
    datos_filtrados = datos_caro
    if valor_categoria != "all":
        datos_filtrados = datos_filtrados[datos_filtrados["NombreCate"] == valor_categoria]
    datos_filtrados = datos_filtrados[
        (datos_filtrados["Precios"] >= rango_precio[0]) & (datos_filtrados["Precios"] <= rango_precio[1])]

    fig = px.bar(datos_filtrados, x="NombrePro", y="Precios", color="NombreCate",
                 title="Productos más caros por categoría",
                 labels={"Precios": "Precio", "NombrePro": "Producto"}, hover_data=["NombrePro"],
                 color_discrete_sequence=['#FF5733', '#FF8C00', '#FFD700', '#FFA07A', '#E9967A', '#CD5C5C'])
    fig.update_layout(plot_bgcolor="white", paper_bgcolor="white", font={"color": "black"})

    return fig

def diseño_dash(datos_caro: pd.DataFrame, datos_baratos: pd.DataFrame, datos_outliers: pd.DataFrame):
    paleta = px.colors.sequential.Reds[::-1]

    fig_caro = px.bar(datos_caro, x="NombrePro", y="Precios", color="NombreCate", title="Productos mas caros por categoria",
                      labels={"Precios": "Precio", "NombrePro": "Producto"}, hover_data=["NombrePro"],
                      color_discrete_sequence=paleta)

    fig_baratos = px.pie(datos_baratos, names="NombrePro", values="Precios", title="Top 10 productos mas baratos",
                         color_discrete_sequence=paleta)

    fig_outliers = px.scatter(datos_outliers, x="NombrePro", y="Precios", color="NombreCate",
                              title="Deteccin de outliers (precios atipicos)",
                              labels={"Precios": "Precio", "NombrePro": "Producto"}, hover_data=["NombrePro"],
                              color_discrete_sequence=paleta)

    cuerpo = html.Div([
        html.H1("Producto mas caro de cada categoría",
                style={"textAlign": "center", "color": "#faf7f7", "background-color": "#bf1919"}),
        html.P("Mostrar los productos mas caros por categoria."),
        html.Hr(),

        dbc.Row([
            dbc.Col(tarjetas_filtro(), width=3),

            dbc.Col([
                dash_table.DataTable(data=datos_caro.to_dict("records"), page_size=10,
                                     style_table={'height': '300px', 'overflowY': 'auto'}),
                dcc.Graph(figure=fig_caro, id="figProducts")
            ], width=9)
        ]),

        html.Hr(),
        html.H1("Top 10 productos mas baratos",
                style={"textAlign": "center", "color": "#faf7f7", "background-color": "#bf1919"}),
        dcc.Graph(figure=fig_baratos),

        html.Hr(),
        html.H1("Deteccion de outliers (precios atipicos)",
                style={"textAlign": "center", "color": "#faf7f7", "background-color": "#bf1919"}),
        dcc.Graph(figure=fig_outliers)
    ])
    return cuerpo

if __name__ == "__main__":
    app = Dash(__name__, external_stylesheets=[dbc.themes.FLATLY])
    app.layout = diseño_dash(datos_caro, datos_baratos, datos_outliers)
    app.run_server(debug=True)



