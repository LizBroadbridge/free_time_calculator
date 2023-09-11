import pandas as pd
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
                html.P(
                    children=(
                        html.Button("Check my free time!", id="check-button", className="time-check-button", n_clicks=0)
                    )
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
    Output("data-table", "data"),
    Input("check-button", "n_clicks"),
)
def update_output(n_clicks):
    if n_clicks == 0:
        return []

    else:
        result_dict = free_time_calc().to_dict("records")
        return result_dict

if __name__ == "__main__":
    app.run_server(debug=True)
