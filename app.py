from dash import Dash, html, dcc, callback, Output, Input
import datetime
import plotly.graph_objects as go
import pandas as pd

from database import Connection


app = Dash(__name__)

connection = None

def serve_layout():
    reading_data = fetch_data()
    current_temp = int(reading_data[-1].value)
    delta_ref = int(reading_data[-12].value)
    df = pd.DataFrame(reading_data)
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s')
    df['timestamp'] = pd.to_datetime(df['timestamp'], format='%H:%M')
    return html.Div([
        dcc.Graph(
            figure=go.Figure(
                data=go.Indicator(
                domain={'x': [0, 1], 'y': [0, 1]},
                value=current_temp,
                mode="gauge+number+delta",
                delta={
                    'suffix': '° F/min',
                    'reference': delta_ref,
                },
                gauge={
                    'bar': {'color': "green"},
                    'axis': {'range': [100, 900]},
                    'steps' : [
                        {'range': [0, 400], 'color': "yellow"},
                        {'range': [400, 650], 'color': "orange"},
                        {'range': [650, 900], 'color': "red"},
                    ],
                }),
                layout=go.Layout(
                    paper_bgcolor='lightgray',
                ),
            ),
        ),
        dcc.Graph(
            figure=go.Figure(
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
            ),
        ),
    ])

def fetch_data():
    connection = Connection('Test.db')

    readings = connection.get_readings(
        datetime.datetime.now() - datetime.timedelta(hours=6),
        datetime.datetime.now()
    )
    connection.connection.close()
    return readings

app.layout = serve_layout

if __name__ == '__main__':
    app.run_server(host= '0.0.0.0', debug=False)
    # app.run(debug=True)
