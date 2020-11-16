"""
This app creates a simple sidebar layout using inline style arguments and the
dbc.Nav component.

dcc.Location is used to track the current location. There are two callbacks,
one uses the current location to render the appropriate page content, the other
uses the current location to toggle the "active" properties of the navigation
links.

For more details on building multi-page Dash applications, check out the Dash
documentation: https://dash.plot.ly/urls
"""
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import csv
import plotly.graph_objs as go
import numpy as np
import plotly.express as px
from modelos import predictModel1, loadImage,predictModel2

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

# the style arguments for the sidebar. We use position:fixed and a fixed width
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

# the styles for the main content position it to the right of the sidebar and
# add some padding.
CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

sidebar = html.Div(
    [
        html.H2("Bone Age App", className="display-4"),
        html.Hr(),
        html.P(
            "RSNA Bone Age Predict Age from X-Rays", className="lead"
        ),
        dbc.Nav(
            [
                dbc.NavLink("Inicio", href="/page-1", id="page-1-link"),
                dbc.NavLink("Análisis de datos",
                            href="/page-2", id="page-2-link"),
                dbc.NavLink("Predicción", href="/page-3", id="page-3-link"),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)

imagePicker = html.Div([
    dcc.Upload(
        id='upload-image',
        children=html.Div([
            'Drag and Drop or ',
            html.A('Select Files')
        ]),
        style={
            'width': '100%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px'
        },
        # Allow multiple files to be uploaded
        multiple=True
    ),
    html.Div(id='output-image-upload'),
])

content = html.Div(id="page-content", style=CONTENT_STYLE)

app.layout = html.Div([dcc.Location(id="url"), sidebar, content])

###########################################Page No.1############################################################


markdown_titel = " # Acerca del proyecto"
markdown_text = '''
Existen dos procesos biológicos íntimamente relacionados de un individuo los cuales no necesariamente van paralelos a lo largo de la infancia y adolescencia, estos dos procesos son el crecimiento y la maduración. Cada niño madura a distinta velocidad, es decir que la edad no es un buen indicativo para ello (Pérez, 2011). 

La edad ósea (EO) es la mejor forma de expresar la edad biológica de una persona, y es de suma importancia en el campo de la medicina dado que muchos tratamientos y procedimientos deben ser cuidadosamente basados en la edad del individuo. Esto también permite evaluar la maduración ósea que, según medios, es "es un fenómeno biológico a través del cual los seres vivos incrementan su masa adquiriendo progresivamente una maduración morfológica y funcional" (Europapress, 2015).

El principal problema se centra en que, a pesar de tener una radiografía presente y clara, no existe un proceso 100% automatizado que identifique la edad ósea de una persona. El procedimiento se centra siempre en el criterio de un experto y dado que es una tarea manual, existirá variabilidad interindividual. Esto abre lugar a resultados raramente precisos y expuestos a un porcentaje de error humano (Abad. D, 2011).

Las computadoras y el uso de algoritmos complejos, junto con las aplicaciones de inteligencia artificial (como lo es machine learning y deep learning), han presentado resultados prontos y exactos. Esto da lugar a un aumento de eficiencia y confiabilidad en los resultados, por lo que obtener un modelo capaz de predecir la edad ósea de un individuo es sumamente conveniente.
'''

page1 = html.Div([
    dcc.Markdown(
        children=markdown_titel,
        style={
            'textAlign': 'justify',
            'padding': '25px 50px 25px',
        },
    ),
    dcc.Markdown(
        children=markdown_text,
        style={
            'textAlign': 'justify',
            'padding': '25px 50px 75px',
        },
    )
])

##################################################################################################################

import pandas as pd 
df = pd.read_csv('boneage-training-dataset.csv')
print(df.head())
print(df.groupby(['male']).size().reset_index(name='counts'))

fig = px.bar(
    df.groupby(['boneage']).size().reset_index(name='count')
    , title ="Cantidad de imágenes por cantidad de meses"
    , x = 'boneage'
    , y = 'count'
    ,labels = {"boneage": "Edad Ósea (meses)", "count": "Cantidad de imágenes"}
    )

fig2 = px.pie(
    df.groupby(['male']).size().reset_index(name='count')
    , values = 'count'
    , title ="Cantidad de imágenes por género"
    , width = 200
    , names='male'
    )

page2 = html.Div([
    dcc.Graph(
            id='example-graph-1',
            figure=fig
        ),
    dcc.Graph(
            id='example-graph-2',
            figure=fig2
        )
], #style={
   #         'display': 'flex',
   #         'flexDirection': 'row'
   #     }
)





###################################################################################################################v
def parse_contents(contents, filename, date):
    # print(contents)

    return html.Div([
        # html.H5(filename),
        # html.H6(datetime.datetime.fromtimestamp(date)),

        # HTML images accept base64 encoded strings in the same format
        # that is supplied by the upload
        html.Img(src=contents, style={'height':'35%', 'width':'35%'}),
        html.Hr(),
        html.Div('Predicciones: '),
        html.Pre("Modelo 1: "+str(predictModel1(loadImage(contents))), style={
            'whiteSpace': 'pre-wrap',
            'wordBreak': 'break-all'
        }),
        html.Pre("Modelo 2: "+str(predictModel2(loadImage(contents))), style={
            'whiteSpace': 'pre-wrap',
            'wordBreak': 'break-all'
        })
    ])

@app.callback(Output('output-image-upload', 'children'),
              [Input('upload-image', 'contents')],
              [State('upload-image', 'filename'),
               State('upload-image', 'last_modified')])
def update_output(list_of_contents, list_of_names, list_of_dates):
    if list_of_contents is not None:
        children = [
            parse_contents(c, n, d) for c, n, d in
            zip(list_of_contents, list_of_names, list_of_dates)]
        return children

# this callback uses the current pathname to set the active state of the
# corresponding nav link to true, allowing users to tell see page they are on
@app.callback(
    [Output(f"page-{i}-link", "active") for i in range(1, 4)],
    [Input("url", "pathname")],
)
def toggle_active_links(pathname):
    if pathname == "/":
        # Treat page 1 as the homepage / index
        return True, False, False
    return [pathname == f"/page-{i}" for i in range(1, 4)]


@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
    if pathname in ["/", "/page-1"]:
        return page1
        #return html.P("Contenido del !")
    elif pathname == "/page-2":
        return page2
    elif pathname == "/page-3":
        return imagePicker
        #return html.P("Contenido de la prediccion")
    # If the user tries to reach a different page, return a 404 message
    return dbc.Jumbotron(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ]
    )


if __name__ == "__main__":
    app.run_server(port=8888)
