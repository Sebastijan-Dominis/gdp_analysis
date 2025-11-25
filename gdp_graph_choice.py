import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc
from dash import Dash, html, dcc
from dash.dependencies import Output, Input
from dash.exceptions import PreventUpdate
from dash_bootstrap_templates import load_figure_template

gdp_pc_data = pd.read_csv("./gdp_pc_data.csv", header=2, usecols=["Country Name"] + [str(x) for x in range(1960, 2024)]).set_index("Country Name").T

app = Dash(__name__, external_stylesheets=[dbc.themes.SLATE])

load_figure_template("SLATE")

app.layout = html.Div([
    html.H1("GDP per capita Plotter", style={"textAlign": "center", "marginTop": 20}),
    dbc.Card([
        html.Label("Select countries:", style={"marginBottom": 10, "fontSize": 20, "textAlign": "center"}),
        dcc.Dropdown(
            options = gdp_pc_data.columns.unique(),
            id="country_input",
            value=["United States"],
            multi=True
        ),
        html.Br(),
        html.Label("Select year range:", style={"marginBottom": 10, "fontSize": 20, "textAlign": "center"}),
        dcc.RangeSlider(
            min=1960,
            max=2024,
            step=1,
            value=[1960, 2024],
            marks={year: str(year) for year in range(1960, 2024, 5)},
            id="year_slider"
        )
    ], style={"padding": 20, "width": "70%", "margin": "auto", "marginTop": 20}),
    dbc.Card([dcc.Graph(id="country_output")], style={"width": "70%", "margin": "auto", "marginTop": 50}),
    # TODO: Add a clear button to reset selections
    dbc.Button("Clear Selections", id="clear_button", color="secondary", style={"display": "block", "margin": "20px auto"})
])

@app.callback(
    Output("country_output", "figure"),
    Input("country_input", "value"),
    Input("year_slider", "value")
)
def show_gdp_pc(countries, year_range):
    if not countries:
        raise PreventUpdate

    start_year, end_year = year_range

    df = gdp_pc_data.loc[str(start_year):str(end_year), countries].copy()
    df["Year"] = df.index

    df_long = df.melt(
        id_vars="Year",
        var_name="Country",
        value_name="GDP per capita"
    )

    fig = px.line(
        df_long,
        x="Year",
        y="GDP per capita",
        color="Country",
        title=f"GDP per capita ({start_year}–{end_year})"
    )

    return fig

@app.callback(
    Output("country_input", "value"),
    Output("year_slider", "value"),
    Input("clear_button", "n_clicks"),
    prevent_initial_call=True
)
def clear_selections(n_clicks):
    if n_clicks:
        return [], [1960, 2024], 
    raise PreventUpdate

if __name__ == "__main__":
    app.run()