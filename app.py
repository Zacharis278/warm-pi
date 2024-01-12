from dash import Dash, html, dcc, callback, Output, Input
import dash_daq as daq
import plotly.express as px
import pandas as pd

from database import Connection


app = Dash(__name__)

connection = None

def serve_layout():
    reading_data = fetch_data()
    current_temp = int(reading_data[-1].value)
    df = pd.DataFrame(reading_data)
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s')
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
                        value=current_temp,
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
                        html.H1(f'{current_temp} F', style={'font-size': '80px'}),
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

def fetch_data():
    connection = Connection('Test.db')
    return connection.get_readings(0, 0)

app.layout = serve_layout

if __name__ == '__main__':
    app.run(debug=True)
