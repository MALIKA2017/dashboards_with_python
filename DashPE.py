import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.express as px

df = pd.read_json ('data_PE_splitted.json')

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP>app = dash.Dash(__name__, external_stylesheets=external_stylesh>
app.layout = html.Div([
  html.H1('Job Market', style={'textAlign': 'center', 'color': >  html.Div(dcc.Dropdown(id = 'Dropdown',
                        options= [{'label': 'dureeTravailLibell>                                  {'label': 'secteurActivite', >                        value= 'dureeTravailLibelleConverti'
  )),
  html.Div(dcc.Graph(id='graph_1')),

  html.Div(dcc.Slider(id = 'slider_1',
                      min = df['nombrePostes'].min(),
                      max = df['nombrePostes'].max(),
                      marks={str(nbr): str(nbr) for nbr in df['>                      step = None))
], style = {'background' : 'beige'})

@app.callback(Output(component_id='graph_1', component_property>            [Input(component_id='Dropdown', component_property=>def update_graph(indicator):
    # Création de la figure plotly
    fig = px.scatter(df_1, x="intitule",
                        y=indicator,
                        color="green",
                        hover_name="description")
    return fig

if __name__ == '__main__':
  app.run_server(debug=True,host = '0.0.0.0')
					  