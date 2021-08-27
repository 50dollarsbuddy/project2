import base64
import io

import dash
import dash_table
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html

import dash_daq as daq

import plotly.express as px

import pandas as pd


# external_stylesheets = ['https://codepen.io/50dollarsbuddy/pen/ExZzYWz.css']

# app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app = dash.Dash(__name__)

app.layout = html.Div([
    dcc.Store(id='mydatabase'),
    dcc.Upload(
        id='upload-data',
        children=html.Div([
            dcc.Input(id='input-file', placeholder='Select aFile to Upload'),
            html.Button('Browse')
        ]),
        style={
            'width': '100%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
        },
        # Allow multiple files to be uploaded
        multiple=True
    ),

    daq.BooleanSwitch(
        id='my-boolean-switch',
        on=False,
        label='Parse Data'
    ),

    html.Table(
        hidden=False,
        style={'width': '100%',
               'textAlign': 'center'},
        id='selectdata',
        children=[
                html.Tr(
                    children=[
                        html.Th('Column Name'),
                        html.Th('Data Type'),
                        html.Th('Ignore?')
                    ]
                ),
                html.Tr(
                    children=[
                        html.Th('Date'),
                        html.Td(children=[
                            dcc.Dropdown(
                                id='update_Date',
                                placeholder='Date-Time'
                            )
                        ]),
                        html.Td(children=[
                            dcc.Checklist(
                                id='ignore_Date',
                                options=[
                                    {'label': '', 'value': 'ignore'}
                                ]
                            )
                        ])
                    ]
                ),
                html.Tr(
                    children=[
                        html.Th('Volume'),
                        html.Td(children=[
                            dcc.Dropdown(
                                id='update_volume',
                                placeholder='Numerical'
                            )
                        ]),
                        html.Td(children=[
                            dcc.Checklist(
                                id='ignore_volume',
                                options=[
                                    {'label': '', 'value': 'ignore'}
                                ]
                            )
                        ])
                    ]
                ),
                html.Tr(
                    children=[
                        html.Th('Adj Close'),
                        html.Td(children=[
                            dcc.Dropdown(
                                id='update_Adj',
                                placeholder='Numerical'
                            )
                        ]),
                        html.Td(children=[
                            dcc.Checklist(
                                id='ignore_Adj',
                                options=[
                                    {'label': '', 'value': 'ignore'}
                                ]
                            )
                        ])
                    ]
                ),
                html.Tr(
                    children=[
                        html.Th('Stock'),
                        html.Td(children=[
                            dcc.Dropdown(
                                id='update_stock',
                                placeholder='String/Categorical',
                            )
                        ]),
                        html.Td(children=[
                            dcc.Checklist(
                                id='ignore_stock',
                                options=[
                                    {'label': '', 'value': 'ignore'}
                                ]
                            )
                        ])
                    ]
                ),
                html.Tr(
                    children=[
                        html.Th('Exchange'),
                        html.Td(children=[
                            dcc.Dropdown(
                                id='update_exchange',
                                placeholder='String/Categorical'
                            )
                        ]),
                        html.Td(children=[
                            dcc.Checklist(
                                id='ignore_exchange',
                                options=[
                                    {'label': '', 'value': 'ignore'}
                                ]
                            )
                        ])
                    ]
                )
        ]
    ),

    html.Div(id='my-table'),

    dcc.Dropdown(
        id='feature_name',
        options=[
            {'label': 'Volume', 'value': 'Volume'},
            {'label': 'Adj Close', 'value': 'Adj Close'}
        ]
    ),

    dcc.Dropdown(
        id='company_name',
        options=[
            {'label': 'AAPl', 'value': 'AAPL'},
            {'label': 'FB', 'value': 'FB'},
            {'label': 'GME', 'value': 'GME'},
            {'label': 'IBM', 'value': 'IBM'},
            {'label': 'INTC', 'value': 'INTC'},
            {'label': 'TSLA', 'value': 'TSLA'},
            {'label': '^DJI', 'value': '^DJI'}
        ],
        multi=True
    ),

    dcc.Graph(id='my_graph')
])


def load_file(contents, filename):
    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            # Assume that the user uploaded a CSV file
            df = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')))
        elif 'xls' in filename:
            # Assume that the user uploaded an excel file
            df = pd.read_excel(io.BytesIO(decoded))
    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing this file.'
        ])
    return df


@app.callback(Output('mydatabase', 'data'),
              Input('upload-data', 'contents'),
              State('upload-data', 'filename'))
def update_df(list_of_contents, list_of_names):
    if list_of_contents is not None:
        for c, n in zip(list_of_contents, list_of_names):
            df = load_file(c, n)
        return df.to_dict('records')

@app.callback(Output('selectdata', 'hidden'),
              Input('my-boolean-switch', 'on'),
              Input('selectdata', 'hidden')
              )
def parse(on, hidden):
    if not on:
        return not hidden

@app.callback(Output('update_Date', 'options'),
              # Output('ignore_Date', 'options'),
              Output('update_volume', 'options'),
              # Output('ignore_volume', 'options'),
              Output('update_Adj', 'options'),
              # Output('ignore_Adj', 'options'),
              Output('update_stock', 'options'),
              # Output('ignore_Stock', 'options'),
              Output('update_exchange', 'options'),
              # Output('ignore_exchange', 'options'),
              Input('mydatabase', 'data'))
              # Input('parsedata', 'n_clicks'))
def datatype(sd):
    df = pd.DataFrame.from_dict(sd)
    df['Date'] = pd.to_datetime(df['Date'])
    uDate_options = [
        {'label': Date, 'value': Date} for Date in pd.Categorical(df[df.columns[0]]).categories
    ]
    uVolume_options = [
        {'label': volume, 'value': volume} for volume in pd.Categorical(df[df.columns[1]]).categories
    ]
    uAdj_options = [
        {'label': adj, 'value': adj} for adj in pd.Categorical(df[df.columns[2]]).categories
    ]
    uStock_options = [
        {'label': stock, 'value': stock} for stock in pd.Categorical(df[df.columns[3]]).categories
    ]
    uExchange_options = [
        {'label': exchange, 'value': exchange} for exchange in pd.Categorical(df[df.columns[4]]).categories
    ]

    return uDate_options, uVolume_options, uAdj_options, uStock_options, uExchange_options

@app.callback(
    Output('my-table', 'children'),
    Input('update_Date', 'value'),
    Input('ignore_Date', 'value'),
    Input('update_volume', 'value'),
    Input('ignore_volume', 'value'),
    Input('update_Adj', 'value'),
    Input('ignore_Adj', 'value'),
    Input('update_stock', 'value'),
    Input('ignore_stock', 'value'),
    Input('update_exchange', 'value'),
    Input('ignore_exchange', 'value'),
    Input('mydatabase', 'data'),
)
def update_my_Datetable(update_Date,
                        ignore_Date,
                        update_volume,
                        ignore_volume,
                        update_Adj,
                        ignore_Adj,
                        update_stock,
                        ignore_stock,
                        update_exchange,
                        ignore_exchange,
                        df):
    my_df = pd.DataFrame.from_dict(df)
    my_df['Date'] = pd.to_datetime(my_df['Date'])

    if update_Date:
        my_df = my_df.loc[my_df['Date'] > update_Date]
    if ignore_Date:
        my_df = my_df.drop(['Date'], axis=1)
    if update_volume:
        my_df = my_df.loc[my_df['Volume'] > update_volume]
    if ignore_volume:
        my_df = my_df.drop(['Volume'], axis=1)
    if update_Adj:
        my_df = my_df.loc[my_df['Adj Close'] > update_Adj]
    if ignore_Adj:
        my_df = my_df.drop(['Adj Close'], axis=1)
    if update_stock:
        my_df = my_df.loc[my_df['Stock'] == update_stock]
    if ignore_stock:
        my_df = my_df.drop(['Stock'], axis=1)
    if update_exchange:
        my_df = my_df.loc[my_df['Exchange'] == update_exchange]
    if ignore_exchange:
        my_df = my_df.drop(['Exchange'], axis=1)


    children = [
        dash_table.DataTable(
            columns=[{'name': i, 'id': i} for i in my_df.columns],
            data = my_df.to_dict('records'),
            page_action='none',
            style_table={'height': '300px', 'overflowY': 'auto'},
            style_cell={'backgroundColor': 'transparent', 'textAlign': 'center'}
        )
    ]
    return children

@app.callback(
    Output('my_graph', 'figure'),
    Input('feature_name', 'value'),
    Input('company_name', 'value'),
    Input('mydatabase', 'data'),
)
def update_my_graph(feature, company, df):

    le = pd.DataFrame.from_dict(df)
    le['Date'] = pd.to_datetime(le['Date'])

    le = le.loc[le['Stock'].isin(company)]

    fig = px.line(le, x='Date', y=feature, color='Stock')

    return fig

if __name__ == '__main__':
    app.run_server(debug=True)