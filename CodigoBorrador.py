from dash import dash_table
from dash.dash_table.Format import Group
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


# Consulta SQL para obtener los datos de todos los productos
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
            html.H5("DATOS"),
            html.Div([
                dbc.Label("Categoria:"),
                dcc.Dropdown(
                    options=[{"label": "Todas", "value": "all"}] + [{"label": cat, "value": cat} for cat in
                                                                    data["NombreCate"].unique()],
                    id="ddlCategory",
                    value="all"
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
    )
    return control


@callback(
    Output(component_id="figProducts", component_property="figure"),
    Output(component_id="figPie", component_property="figure"),
    Input(component_id="ddlCategory", component_property="value"),
    Input(component_id='price-range-slider', component_property='value')
)
def update_grafica(value_category, price_range):
    filtered_data = data
    if value_category != "all":
        filtered_data = filtered_data[filtered_data["NombreCate"] == value_category]

    fig_bar = px.bar(filtered_data, x="NombreCate", title="Proporción de Productos por Categoría",
                     labels={"NombreCate": "Categoría", "count": "Número de Productos"})
    fig_pie = px.pie(filtered_data, names="NombreCate", title="Proporción de Productos por Categoría")

    return fig_bar, fig_pie


def dash_layout(data: pd.DataFrame):
    # Creamos un diccionario para asignar colores a cada categoría
    colors = px.colors.qualitative.Set3

    fig_bar = px.bar(data, x="NombreCate", title="Proporción de Productos por Categoría",
                     labels={"NombreCate": "Categoría", "count": "Número de Productos"})

    # Creamos el gráfico de pie con colores asignados a cada categoría
    fig_pie = px.pie(data, names="NombreCate", title="Proporción de Productos por Categoría",
                     color_discrete_sequence=colors)

    body = html.Div([
        html.H1("Rango de precios de productos en la tienda",
                style={"textAlign": "center", "color": "#faf7f7", "background-color": "#bf1919"}),
        html.P("Objetivo Dashboard: Mostrar el rango de precios de todos los productos en la tienda."),
        html.Hr(),

        dbc.Row([
            dbc.Col(tarjetas_filtro(), width=3),

            dbc.Col([
                dcc.Graph(figure=fig_bar, id="figProducts"),
                dcc.Graph(figure=fig_pie, id="figPie"),
                dash_table.DataTable(data=data.to_dict("records"), page_size=10,
                                     style_table={'height': '300px', 'overflowY': 'auto'}),
            ], width=9)
        ])
    ])
    return body


if __name__ == "__main__":
    app = Dash(__name__, external_stylesheets=[dbc.themes.FLATLY])
    app.layout = dash_layout(data)
    app.run_server(debug=True)

