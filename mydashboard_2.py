import dash
from dash.dependencies import Input, Output
from dash import dcc, html
import pandas as pd
import plotly.express as px
import json

with open('splitted_PE.json', 'r') as fichier_json:
    data = json.load(fichier_json)
df = pd.DataFrame(data)

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# ------------------------------------------------------------------------------
# App layout
app.layout = html.Div([
  html.H1('Besoin d\'un nouveau poste !', style={'textAlign': 'center', 'color': '8A90CC'}),
  html.H2('MY Job Market', style={'textAlign': 'center', 'color': 'Periwinkle'}),
  html.Div(dcc.Dropdown(id = 'Dropdown',
                        options= [{'label': 'dureeTravailLibelleConverti', 'value': 'duree de travail'},
                                  {'label': 'lieuTravail_codepostal', 'value': 'lieu de travail - codepostal'},
                                  {'label': 'typeContrat', 'value': 'type de contrat'},
                                  {'label': 'natureContrat', 'value': 'nature de contrat'}],
                        multi= False,
                        value= 'nature du contrat',
                        style={'width': "40%"}
  )),
  html.Div(dcc.Slider(id = 'slider_1',
                      min = df['salaire_max'].min(),
                      max = df['salaire_max'].max(),
                      marks={nbr: nbr for nbr in df['salaire_max'].unique()},step = None)),
  html.Div(dcc.Graph(id='graph_1')),
  html.Div(id='output_container', children=[]),
  html.Br(),
  html.Graph(id='trouver un poste en France',figure={})
], style = {'background' : 'beige'})

# ------------------------------------------------------------------------------
# Connect the Plotly graphs with Dash Components
@app.callback(Output(component_id='graph_1', component_property='figure'),
              Output(component_id='output_container', component_property='children'),
              [Input(component_id='Dropdown', component_property='value'),
               Input(component_id='slider_1', component_property='value')])
def update_graph(indicator):
    # Création de la figure plotly
    fig = px.scatter(df, x="intitule",
                        y=indicator,
                        color="qualificationCode",
                        hover_name="description")
    return fig


# ------------------------------------------------------------------------------
if __name__ == '__main__':
  app.run_server(debug=True,host = '0.0.0.0')