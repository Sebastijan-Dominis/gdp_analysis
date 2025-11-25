import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc
import pycountry
from dash import Dash, html, dcc
from dash.dependencies import Output, Input
from dash.exceptions import PreventUpdate
from dash_bootstrap_templates import load_figure_template

gdp_pc_2024 = pd.read_csv("./gdp_pc_data.csv", header=2, usecols=["Country Name", "2024"]).dropna().reset_index(drop=True)

# Convert country names to ISO3 codes
def get_iso3(country_name):
    try:
        country = pycountry.countries.lookup(country_name)
        return country.alpha_3
    except LookupError:
        return None
    
gdp_pc_2024["ISO3"] = gdp_pc_2024["Country Name"].apply(get_iso3)
gdp_pc_2024 = gdp_pc_2024.dropna(subset=["ISO3"])

# Round the GDP per capita values to 2 decimal places
gdp_pc_2024["2024"] = gdp_pc_2024["2024"].round(2)

app = Dash(__name__, external_stylesheets=[dbc.themes.SLATE])

load_figure_template("SLATE")

def make_choropleth(scope, title, range_color, tickvals, ticktext):
    fig = px.choropleth(
        data_frame=gdp_pc_2024,
        locations="ISO3",
        locationmode="ISO-3",
        color="2024",
        custom_data=["Country Name", "2024"],
        color_continuous_scale="RdYlGn",
        scope=scope,
        range_color=range_color
    )

    fig.update_layout(
        width=1400,
        height=700,
        margin=dict(l=0, r=20, t=60, b=20),
        title=dict(
            text=title,
            x=0.5,
            font=dict(weight=650, color="whitesmoke", size=20),
        )
    )

    fig.update_coloraxes(
        colorbar=dict(title="", tickvals=tickvals, ticktext=ticktext)
    )

    fig.update_traces(
        hovertemplate="<b>    %{customdata[0]}</b><br>" +
                    "    $%{customdata[1]:,}<extra></extra>"
        )

    return fig

tab_configs = {
    "europe": {
        "label": "Europe",
        "scope": "europe",
        "range_color": (0, 80000),
        "tickvals": [0,10000,20000,30000,40000,50000,60000,70000,80000],
        "ticktext": ["0","10k","20k","30k","40k","50k","60k","70k","≥80k"]
    },
    "north_america": {
        "label": "North America",
        "scope": "north america",
        "range_color": (0, 30000),
        "tickvals": [0,5000,10000,15000,20000,25000,30000],
        "ticktext": ["0","5k","10k","15k","20k","25k","≥30k"]
    },
    "asia": {
        "label": "Asia",
        "scope": "asia",
        "range_color": (0, 50000),
        "tickvals": [0,10000,20000,30000,40000,50000],
        "ticktext": ["0","10k","20k","30k","40k","50k+"]
    },
    "south_america": {
        "label": "South America",
        "scope": "south america",
        "range_color": (0, 30000),
        "tickvals": [0,5000,10000,15000,20000,25000,30000],
        "ticktext": ["0","5k","10k","15k","20k","25k","30k+"]
    },
    "africa": {
        "label": "Africa",
        "scope": "africa",
        "range_color": (0, 8000),
        "tickvals": [0,1000,2000,3000,4000,5000,6000,7000,8000],
        "ticktext": ["0","1k","2k","3k","4k","5k","6k","7k","8k+"]
    }
}

app.layout = dbc.Container(
    [
        html.H1("GDP per capita (nominal USD) Interactive Maps (2024 data)", style={"margin-top": "20px", "textAlign": "center"}),
        dcc.Tabs(
            id="tabs",
            value="europe",
            children=[
                dcc.Tab(
                    label=config["label"],
                    value=name,
                    children=[
                        dcc.Graph(
                            id=f"{name}-gdp-map",
                            figure=make_choropleth(
                                scope=config["scope"],
                                title=f"{config['label']} Countries by GDP per capita (nominal USD)",
                                range_color=config["range_color"],
                                tickvals=config["tickvals"],
                                ticktext=config["ticktext"],
                            ),
                            style={"margin-top": "40px"}
                        )
                    ]
                )
                for name, config in tab_configs.items()
            ],
            className="custom-tabs",
            style={"margin-top": "45px"}
        )
    ]
)

if __name__ == "__main__":
    app.run()