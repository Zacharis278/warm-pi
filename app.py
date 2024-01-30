from dash import Dash, html, dcc, callback, Output, Input
from datetime import datetime, timedelta
import numpy as np
import plotly.graph_objects as go
import pandas as pd
from scipy.stats import linregress

from database import Connection


app = Dash(__name__)

connection = None

reading_data = []

# todo: these need some refactoring into components
def gauge_figure(current_temp, delta_ref, ref_units):
    return go.Figure(
        data=go.Indicator(
        domain={'x': [0, 1], 'y': [0, 1]},
        value=current_temp,
        mode="gauge+number+delta",
        delta={
            'suffix': ref_units,
            'reference': delta_ref,
            'valueformat': '.2f',
        },
        gauge={
            'bar': {'color': "green"},
            'axis': {'range': [100, 800]},
            'steps' : [
                {'range': [0, 325], 'color': "yellow"},
                {'range': [325, 550], 'color': "orange"},
                {'range': [550, 800], 'color': "red"},
            ],
        }),
        layout=go.Layout(
            paper_bgcolor='lightgray',
        ),
    )

def graph_figure(df):
    return go.Figure(
        data=go.Scatter(
            x=df['timestamp'],
            y=df['value'],
            mode='lines',
        ),
        layout=go.Layout(
            xaxis={
                'title': None,
                'showgrid': False,
            },
            yaxis=None,
            margin={'l': 0, 'r': 0, 't': 0, 'b': 0},
            paper_bgcolor='lightgray',
            plot_bgcolor='lightgray',
        ),
    )

def serve_layout():
    reading_data = fetch_data()
    current_temp = int(reading_data[-1].value)
    delta_ref = int(reading_data[-1].value)
    df = pd.DataFrame(reading_data)
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s')
    df['timestamp'] = pd.to_datetime(df['timestamp'], format='%H:%M')
    return html.Div([
        dcc.Graph(
            id='gauge',
        ),
        dcc.Graph(
            id='graph',
        ),
        dcc.Interval(
            id='interval-component',
            interval=5*1000, # in milliseconds
            n_intervals=0
        ),
    ])

@callback(Output('gauge', 'figure'), [Input('interval-component', 'n_intervals')])
def update_gauge(n):
    reading_data = get_readings()
    current_temp = int(reading_data[-1].value)
    df = pd.DataFrame(reading_data)
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s')
    df['timestamp'] = pd.to_datetime(df['timestamp'], format='%H:%M')

    tail = df.tail(60)
    x = np.arange(len(tail))
    y = tail['value'].values
    slope, intercept, r_value, p_value, std_err = linregress(x, y)
    if False: # abs(slope) < .5:
        ref = round(current_temp-slope*5)
        ref_units = '° F/5min'
    else:
        ref = round(current_temp-slope, 2)
        ref_units = '° F/min'
    
    return gauge_figure(current_temp, ref, ref_units)

@callback(Output('graph', 'figure'), [Input('interval-component', 'n_intervals')])
def update_graph(n):
    reading_data = get_readings()
    df = pd.DataFrame(reading_data)
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s')
    df['timestamp'] = pd.to_datetime(df['timestamp'], format='%H:%M')
    return graph_figure(df)

def get_readings():
    global reading_data
    last_updated = datetime.fromtimestamp(reading_data[-1].timestamp) if len(reading_data) else None
    if (
        last_updated is None or 
        datetime.now() - last_updated > timedelta(seconds=5)
    ):
        reading_data = fetch_data()
    return reading_data

def fetch_data():
    connection = Connection('Test.db')

    readings = connection.get_readings(
        datetime.now() - timedelta(hours=2),
        datetime.now()
    )
    connection.connection.close()
    return readings

app.layout = serve_layout

if __name__ == '__main__':
    app.run(host= '0.0.0.0', debug=False)
    # app.run(debug=True)
