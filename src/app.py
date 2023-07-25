import dash
import dash_html_components as html
import dash_core_components as dcc
# from dash import html, dcc
import plotly.graph_objects as go
import pandas as pd
from dash.dependencies import Input, Output

import os.path as path

two_up =  path.abspath(path.join(__file__ ,"../"))
# Load data
df = pd.read_csv(two_up + '/data/wa_marathon_ranking.csv', index_col=0, parse_dates=True)
df.index = pd.to_datetime(df.index)

# Initialize the app
app = dash.Dash(__name__)
server = app.server
app.config.suppress_callback_exceptions = True


def get_options(list_competitors):
    dict_list = []
    for i in list_competitors:
        dict_list.append({'label': i, 'value': i})

    return dict_list


app.layout = html.Div(
    children=[
        html.Div(className='row',
                 children=[
                    html.Div(className='four columns div-user-controls',
                             children=[
                                 html.H2('DASH - World Athletics Marathon Ranking'),
                                 html.P('From 2019 until 2023'),
                                 html.P('Pick one or more runners from the dropdown below.'),
                                 html.Div(
                                     className='div-for-dropdown',
                                     children=[
                                         dcc.Dropdown(id='competitorselector', options=get_options(df['competitors'].unique()),
                                                      multi=True, value=[df['competitors'].sort_values()[0]],
                                                      style={'backgroundColor': '#1E1E1E'},
                                                      className='competitorselector'
                                                      ),
                                     ],
                                     style={'color': '#1E1E1E'})
                                ]
                             ),
                    html.Div(className='eight columns div-for-charts bg-grey',
                             children=[
                                 dcc.Graph(id='timeseries',
                                     config={'displayModeBar': False},
                                     animate=True),
                                 dcc.Graph(id='change',
                                     config={'displayModeBar': False},
                                     animate=True),
                             ])
                              ])
        ]

)


# Callback for timeseries
@app.callback(Output('timeseries', 'figure'),
              [Input('competitorselector', 'value')])
def update_timeseries(selected_dropdown_value):
    ''' Draw traces of the feature 'score' based one the currently selected runners '''
    # STEP 1
    trace = []
    df_sub = df
    # STEP 2
    # Draw and append traces for each runner
    for runner in selected_dropdown_value:
        trace.append(go.Scatter(x=df_sub[df_sub['competitors'] == runner].index,
                                 y=df_sub[df_sub['competitors'] == runner]['score'],
                                 mode='lines',
                                 opacity=0.7,
                                 name=runner,
                                 textposition='bottom center'))
    # STEP 3
    traces = [trace]
    data = [val for sublist in traces for val in sublist]
    # Define Figure
    # STEP 4
    figure = {'data': data,
              'layout': go.Layout(
                  colorway=["#5E0DAC", '#FF4F00', '#375CB1', '#FF7400', '#FFF400', '#FF0056'],
                  template='plotly_dark',
                  paper_bgcolor='rgba(0, 0, 0, 0)',
                  plot_bgcolor='rgba(0, 0, 0, 0)',
                  margin={'b': 15},
                  hovermode='x',
                  autosize=True,
                  title={'text': 'Scores', 'font': {'color': 'white'}, 'x': 0.5},
                  xaxis={'range': [df_sub.index.min(), df_sub.index.max()]},
              ),
              }

    return figure


@app.callback(Output('change', 'figure'),
              [Input('competitorselector', 'value')])
def update_change(selected_dropdown_value):
    ''' Draw traces of the feature 'rank' based one the currently selected stocks '''
    trace = []
    df_sub = df
    # Draw and append traces for each stock
    for runner in selected_dropdown_value:
        trace.append(go.Scatter(x=df_sub[df_sub['competitors'] == runner].index,
                                 y=df_sub[df_sub['competitors'] == runner]['rank'],
                                 mode='lines',
                                 opacity=0.7,
                                 name=runner,
                                 textposition='bottom center'))
    traces = [trace]
    data = [val for sublist in traces for val in sublist]
    # Define Figure
    figure = {'data': data,
              'layout': go.Layout(
                  colorway=["#5E0DAC", '#FF4F00', '#375CB1', '#FF7400', '#FFF400', '#FF0056'],
                  template='plotly_dark',
                  paper_bgcolor='rgba(0, 0, 0, 0)',
                  plot_bgcolor='rgba(0, 0, 0, 0)',
                  margin={'t': 50},
                  height=500,
                  hovermode='x',
                  yaxis = dict(autorange="reversed"),
                  autosize=True,
                  title={'text': 'Ranking', 'font': {'color': 'white'}, 'x': 0.5},
                  xaxis={'showticklabels': False, 'range': [df_sub.index.min(), df_sub.index.max()]},
              ),
              }

    return figure


if __name__ == '__main__':
    app.run_server(debug=True)