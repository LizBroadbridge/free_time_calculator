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
            ],
            className="header",
        )
    ]
)

@app.callback(
    Output('data-table', 'data'),
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

    try:
        csv_string = decoded.decode('utf-8')
        result_dict = free_time_calc(csv_string).to_dict("records")
        return result_dict
    except Exception as e:
        print(e)
        return ['An error occurred while processing the file.'] # TODO this errors on render

if __name__ == "__main__":
    app.run_server(debug=True)
