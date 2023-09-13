import pandas as pd
import base64
from dash import Dash, dcc, html, Output, Input, State, dash_table, no_update
import dash_bootstrap_components as dbc
from free_time_calculations import free_time_calc

external_stylesheets = [
    {
        "href": "https://fonts.googleapis.com/css?family=Rubik",
        "rel": "stylesheet",
    },
]

app = Dash(__name__, external_stylesheets=external_stylesheets)
app.title = "Free Time Calculator"

app.layout = html.Div(
    children=[
        html.Div(
            children=[
                html.H1(
                    children="Free Time Calculator", className="header-title"
                ),
                html.P(
                    children=(
                        "Check your free time!"
                    ),
                    className="header-description",
                ),
                dcc.Upload(
                    id='upload-data',
                    children=html.Div([
                        'Schedule A: Drag and Drop or ',
                        html.A('Select a File')
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
                    multiple=False
                ),
                dcc.Upload(
                    id='upload-data-b',
                    children=html.Div([
                        'Schedule B: Drag and Drop or ',
                        html.A('Select a File')
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
                    multiple=False
                ),
                dbc.Button(
                    "Compare",
                    id="compare-button",
                ),
                dcc.Dropdown(
                    id='dropdown-toggle',
                    options=[
                        {'label': 'Show DataTable', 'value': 'show'},
                        {'label': 'Hide DataTable', 'value': 'hide'}
                    ],
                    value='hide'
                ),
                html.P(
                    children=(
                        "Schedule A:"
                    ),
                ),
                dcc.Loading(
                    id="loading-table",
                    children=[
                        html.Div(
                            [
                                dash_table.DataTable(
                                    id="data-table",
                                    columns=[
                                        {"name": col, "id": col}
                                        for col in [
                                            "Day",
                                            "Free",
                                            "Free (at Gymnastics)",
                                            "Free (boys at home)",
                                            "Free (boys in bed)",
                                            "Free (with Milo at home)",
                                            "Total",
                                        ]
                                    ],
                                ),
                            ]
                        ),
                    ],
                    type="default",
                ),
                html.P(
                    children=(
                        "Schedule B:"
                    ),
                ),
                dcc.Loading(
                    id="loading-table-b",
                    children=[
                        html.Div(
                            [
                                dash_table.DataTable(
                                    id="data-table-b",
                                    columns=[
                                        {"name": col, "id": col}
                                        for col in [
                                            "Day",
                                            "Free",
                                            "Free (at Gymnastics)",
                                            "Free (boys at home)",
                                            "Free (boys in bed)",
                                            "Free (with Milo at home)",
                                            "Total",
                                        ]
                                    ],
                                ),
                            ]
                        ),
                    ],
                    type="default",
                ),
                html.P(
                    children=(
                        "Delta:"
                    ),
                ),
                dcc.Loading(
                    id="loading-delta-table",
                    children=[
                        html.Div(
                            [
                                dash_table.DataTable(
                                    id="delta-table",
                                    columns=[
                                        {"name": col, "id": col}
                                        for col in [
                                            "Day",
                                            "Free",
                                            "Free (at Gymnastics)",
                                            "Free (boys at home)",
                                            "Free (boys in bed)",
                                            "Free (with Milo at home)",
                                            "Total",
                                        ]
                                    ],
                                ),
                            ]
                        ),
                    ],
                    type="default",
                ),
            ],
            className="header",
        )
    ]
)

prev_contents = None

@app.callback(
    Output('upload-data', 'style'),
    Output('upload-data-b', 'style'),
    Output('data-table', 'data'),
    Output('data-table-b', 'data'),
    Output('delta-table', 'data'),
    State('upload-data', 'contents'),
    State('upload-data-b', 'contents'),
    Input('upload-data', 'filename'),
    Input('upload-data-b', 'filename'),
    Input('compare-button', 'n_clicks'),
    Input('dropdown-toggle', 'value'),
    prevent_initial_call=True
)
def update_output(contents, contents_b, filename, filename_b, n_clicks, value):
    style = no_update
    style_b = no_update

    if filename is not None:
        style = {'display': 'none'}

    if filename_b is not None:
        style_b = {'display': 'none'}

    if n_clicks is None:
        return style, style_b, [], [], []

    content_type, content_string = contents.split(',')

    if content_type != "data:text/csv;base64":
        print("Unexpected content_type")
        print(content_type) # TODO combine these prints, interpolate the content_type
        return ['An error occured while processing the file.'] # TODO this errors on render

    decoded = base64.b64decode(content_string)

    csv_string = decoded.decode('utf-8')

    #

    content_type, content_string = contents_b.split(',')

    if content_type != "data:text/csv;base64":
        print("Unexpected content_type")
        print(content_type) # TODO combine these prints, interpolate the content_type
        return ['An error occured while processing the file.'] # TODO this errors on render

    decoded = base64.b64decode(content_string)

    csv_string_b = decoded.decode('utf-8')

    #

    result_df = free_time_calc(csv_string)

    result_df_b = free_time_calc(csv_string_b)

    delta_dict = None

    delta_df = result_df.copy()
    delta_df.iloc[:, 1:] = result_df_b.iloc[:, 1:] - delta_df.iloc[:, 1:]
    delta_df.iloc[:, 1:] = delta_df.iloc[:,1:].map(lambda x: f"{int(x // 60)}h{int(x % 60)}")
    delta_df.replace("0h0", '-', inplace=True)

    result_df.iloc[:,1:] = result_df.iloc[:,1:].map(lambda x: f"{int(x // 60)}h{int(x % 60)}")
    result_df_b.iloc[:,1:] = result_df_b.iloc[:,1:].map(lambda x: f"{int(x // 60)}h{int(x % 60)}")

    if value == "hide":
        result_df = result_df.tail(1)
        result_df_b = result_df_b.tail(1)
        delta_df = delta_df.tail(1)

    delta_dict = delta_df.to_dict("records")
    result_dict = result_df.to_dict("records")
    result_dict_b = result_df_b.to_dict("records")

    return style, style_b, result_dict, result_dict_b, delta_dict

if __name__ == "__main__":
    app.run_server(debug=True)
