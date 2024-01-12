from dash import Dash, html, dcc, callback, Output, Input
import dash_daq as daq
import plotly.express as px
import pandas as pd


app = Dash(__name__)

def serve_layout():
    df = pd.read_csv('data/test.csv')
    return html.Div([
        html.Div(
            style={
                'display': 'flex',
            },
            children=[
                html.Div(
                    children=[daq.Gauge(
                        id='temp-gauge',
                        size=200,
                        value=550,
                        min=100,
                        max=900,
                        scale={
                            'start': 100,
                            'interval': 50
                        },
                        color={
                            'gradient': False,
                            'ranges': {
                                'yellow': [100, 330],  # theres a bug in the component that messes up scaling if the min is not 0
                                'orange': [330, 630],  # visually orange is 400-650
                                'red': [630, 900],
                            }
                        }
                    )],
                    style={
                        'flex': '1',
                    }
                ),
                html.Div(
                    children=[
                        html.H1('575° F', style={'font-size': '80px'}),
                    ],
                    style={
                        'flex': '1',
                        'padding-top': '50px',
                    }
                ),
            ]
        ),
        dcc.Graph(
            figure=px.line(df, x='timestamp', y='value', markers=True),
            id='graph-content',
        ),
    ])

app.layout = serve_layout

# @callback(
#     Output('graph-content', 'figure'),
# #     Input('dropdown-selection', 'value')
# )
# def update_graph():
#     dff = df[df.channel == 1]
#     return px.line(dff, x='timestamp', y='reading')

if __name__ == '__main__':
    app.run(debug=True)
