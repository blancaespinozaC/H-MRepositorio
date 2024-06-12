from dash import dash_table
import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc
from dash import dcc, html, Dash, Input, Output
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
        datos = cursor.fetchall()
        columnas = [desc[0] for desc in cursor.description]
        cursor.close()
        conn.close()

        df = pd.DataFrame(datos, columns=columnas)
        return df
    except Error as e:
        print("Error leyendo datos desde MySQL:", e)
        return pd.DataFrame()


consulta_sql = """
SELECT p.Id_cate, c.NombreCate, p.Precios, p.NombrePro 
FROM Productos p 
JOIN Categorias c ON p.Id_cate = c.Id_cate
"""

datos = leer_datos_desde_sql(consulta_sql)

colores_categoria = {
    "Mujer": "#FFB6C1",
    "Hombre": "#87CEFA",
    "Ninos": "#66CDAA",
    "Home": "#BC8F8F",
    "Sport": "#778899",
    "Beauty": "#DDA0DD",
    "Bebe": "#FFDEAD"
}

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

def diseño_dash(data):
    controls = dbc.Card(
        [
            html.Div(
                [
                    dbc.Label("Categoría", style={'font-weight': 'bold'}),
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
                    dbc.Label("Número de Productos", style={'font-weight': 'bold'}),
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

    products_line_chart = dbc.Card(
        dbc.CardBody(
            [
                html.H5("Productos más Repetidos en Todas las Categorías", className="card-title"),
                dcc.Graph(id="products-line-chart", style={"height": "60vh", "border": "4px solid #FF69B4"})
            ]
        ),
        style={"width": "100%", "marginTop": "20px", "background-color": "#EE99C2"}
    )

    layout = dbc.Container(
        [
            html.H1("Precio Promedio de Productos por Categoría", style={"textAlign": "center", "backgroundColor": "#D8BFD8", "color": "white", 'font-weight': 'bold'}),
            html.P("Objetivo del Dashboard: Mostrar el precio promedio de los productos en cada categoría",style={"color":"#E59BE9","font-family":"cursive", 'font-weight': 'bold'}),
            html.Hr(),
            dbc.Row(
                [
                    dbc.Col(controls, md=4),
                    dbc.Col(dcc.Graph(id="scatter-plot", style={"height": "80vh", "border": "4px solid #FF69B4","font-weight": "bold"}), md=8),
                ],
                align="center",
            ),
            dbc.Row(
                [
                    dbc.Col(md=4),
                    dbc.Col(dcc.Graph(id="density-plot", style={"height": "80vh", "border": "4px solid #FF69B4","font-weight": "bold"}) ,md=8),
                ],
                align="center",
            ),
            dbc.Row(
                [
                    dbc.Col(products_line_chart, md=6)
                ],
                align="center"
            )
        ],
        fluid=True,
        style={"backgroundColor": "#F8F9D7"}
    )

    return layout

def productos_mas_repetidos(datos):
    productos_repetidos = datos['NombrePro'].value_counts().sort_values(ascending=False)
    return productos_repetidos.head(10)  # Mostrar los 10 productos más repetidos

@app.callback(
    Output("scatter-plot", "figure"),
    Output("precio-promedio-general", "children"),
    Input("dropdown-categoria", "value"),
    Input("num-products", "value")
)
def Actualiza_grafica(categoria, num_productos):
    datos_filtrados = datos[datos['NombreCate'] == categoria]
    datos_filtrados = datos_filtrados.head(num_productos)

    if not datos_filtrados.empty:
        fig = px.scatter(datos_filtrados, x='NombrePro', y='Precios', color='NombreCate',
                         title=f'Precio Promedio en la Categoría {categoria}', labels={"Precios": "Precio Promedio", "NombrePro": "Producto"},
                         color_discrete_map=colores_categoria)
        fig.update_traces(marker=dict(size=22))

        fig.update_layout(
            plot_bgcolor='#FFFAFA',
            paper_bgcolor='#FFFAFA',
            xaxis=dict(linecolor='#C0C0C0'),
            yaxis=dict(linecolor='#C0C0C0'),
        )

        precio_promedio_general = f"${datos_filtrados['Precios'].mean():.2f}"
    else:
        fig = px.scatter(title="No hay datos disponibles")
        precio_promedio_general = "No disponible"

    return fig, precio_promedio_general

@app.callback(
    Output("density-plot", "figure"),
    Input("dropdown-categoria", "value")
)
def Actualiza_Densidad(categoria):
    datos_filtrados = datos[datos['NombreCate'] == categoria]

    if not datos_filtrados.empty:
        fig = px.histogram(datos_filtrados, x='Precios', color='NombreCate', marginal='rug', histnorm='probability density',
                           title=f'Distribución de Precios en la Categoría {categoria}', labels={"Precios": "Precio", "NombreCate": "Densidad"},
                           color_discrete_map=colores_categoria)
        fig.update_traces(opacity=0.6)

        fig.update_layout(
            plot_bgcolor='#FFFAFA',
            paper_bgcolor='#FFFAFA',
            xaxis=dict(linecolor='#C0C0C0'),
            yaxis=dict(linecolor='#C0C0C0'),
        )
    else:
        fig = px.histogram(title="No hay datos disponibles")

    return fig

@app.callback(
    Output("products-line-chart", "figure"),
    Input("dropdown-categoria", "value"),
    Input("num-products", "value")
)
def Actualiza_Linea(categoria, num_productos):
    datos_filtrados = datos.head(num_productos)

    if not datos_filtrados.empty:
        productos_repetidos = productos_mas_repetidos(datos_filtrados)
        fig = px.line(x=productos_repetidos.index, y=productos_repetidos.values, labels={"x": "Producto", "y": "Cantidad"},
                      title="Productos más Repetidos en Todas las Categorías")
        fig.update_xaxes(categoryorder='total descending')
        fig.update_traces(mode='lines+markers')

        return fig
    else:
        fig = px.line(title="No hay datos disponibles")
        return fig

if __name__ == "__main__":
    app.layout = diseño_dash(datos)
    app.run_server(debug=True, port=8888)

