import pandas as pd
import base64
from dash import Dash, dcc, html, Output, Input, State, dash_table
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
                        'Drag and Drop or ',
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
                html.Div(id="output-div"),
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
                        "Delta vs previous CSV:"
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
    Output('data-table', 'data'),
    Output('delta-table', 'data'),
    Input('upload-data', 'contents'),
    prevent_initial_call=True
)
def update_output(contents):
    if contents is None:
        return None

    content_type, content_string = contents.split(',')

    if content_type != "data:text/csv;base64":
        print("Unexpected content_type")
        print(content_type) # TODO combine these prints, interpolate the content_type
        return ['An error occured while processing the file.'] # TODO this errors on render

    decoded = base64.b64decode(content_string)

    csv_string = decoded.decode('utf-8')

    global prev_contents

    result_df = free_time_calc(csv_string)

    delta_dict = None

    if prev_contents is not None:
        delta_df = prev_contents.copy()
        delta_df.iloc[:, 1:] = delta_df.iloc[:, 1:] - result_df.iloc[:, 1:]
        delta_df.iloc[:, 1:] = delta_df.iloc[:,1:].map(lambda x: f"{int(x // 60)}h{int(x % 60)}")
        delta_dict = delta_df.to_dict("records")

    prev_contents = result_df.copy()

    result_df.iloc[:,1:] = result_df.iloc[:,1:].map(lambda x: f"{int(x // 60)}h{int(x % 60)}")

    result_dict = result_df.to_dict("records")

    return result_dict, delta_dict

if __name__ == "__main__":
    app.run_server(debug=True)
