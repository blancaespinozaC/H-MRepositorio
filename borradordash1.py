from dash import Dash, dcc, html, Input, Output
import dash_table
import pandas as pd
from mysql.connector import connect, Error
import plotly.express as px

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
        cursor.close()
        conn.close()

        columns = [desc[0] for desc in cursor.description]
        df = pd.DataFrame(data, columns=columns)
        return df
    except Error as e:
        print("Error leyendo datos desde MySQL:", e)
        return pd.DataFrame()

# Consulta SQL para obtener los datos
sql_query = """
SELECT p.Id_cate, c.NombreCate, p.Precios 
FROM Productos p 
JOIN Categorias c ON p.Id_cate = c.Id_cate
"""

# Leer los datos desde la base de datos
df = read_data_from_sql(sql_query)

# Inicializar la app
app = Dash(__name__)

# Layout de la app
app.layout = html.Div([
    html.H1('¿Qué categoría tiene el producto más caro?'),
    html.Hr(),
    html.H5("Rango de Precios"),
    dcc.RadioItems(options=["500-400", "300-200", "150-100"], value='lifeExp', id='controls-and-radio-item'),
    dash_table.DataTable(data=df.to_dict('records'), columns=[{"name": i, "id": i} for i in df.columns], page_size=10),
    dcc.Graph(id='controls-and-graph')  # Eliminamos 'figure={}' aquí
])

@app.callback(
    Output(component_id='controls-and-graph', component_property='figure'),
    Input(component_id='controls-and-radio-item', component_property='value')
)
def update_graph(col_chosen):
    # Actualizamos el DataFrame según el valor de col_chosen (aunque aquí parece que no lo estás usando)
    # En este caso, simplemente usaremos df como está
    return px.bar(df, x='NombreCate', y='Precios', title='Precio Promedio por Categoría',
                  labels={'Precios': 'Precio Promedio', 'NombreCate': 'Categoría'})

# Ejecutar la app
if __name__ == '__main__':
    app.run(debug=True)
