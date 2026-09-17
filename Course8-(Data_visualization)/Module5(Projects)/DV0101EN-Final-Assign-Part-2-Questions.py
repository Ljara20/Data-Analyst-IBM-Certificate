#!/usr/bin/env python
# coding: utf-8

import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px

# Load the data
data = pd.read_csv(
    "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/"
    "d51iMGfp_t0QpO30Lym-dw/automobile-sales.csv"
)

# Initialize the Dash app
app = dash.Dash(__name__)
app.title = "Automobile Sales Statistics Dashboard"

# Dropdown options
dropdown_options = [
    {
        "label": "Yearly Statistics",
        "value": "Yearly Statistics"
    },
    {
        "label": "Recession Period Statistics",
        "value": "Recession Period Statistics"
    }
]

# List of years
year_list = list(range(1980, 2024))

# Application layout
app.layout = html.Div([

    # TASK 2.1: Dashboard title
    html.H1(
        "Automobile Sales Statistics Dashboard",
        style={
            "textAlign": "center",
            "color": "#503D36",
            "fontSize": 24
        }
    ),

    # TASK 2.2: Statistics dropdown
    html.Div([
        html.Label("Select Statistics:"),

        dcc.Dropdown(
            id="dropdown-statistics",
            options=dropdown_options,
            value=None,
            placeholder="Select a report type",
            style={
                "width": "80%",
                "padding": "3px",
                "fontSize": "20px",
                "textAlign": "center"
            }
        )
    ]),

    # Year dropdown
    html.Div([
        html.Label("Select Year:"),

        dcc.Dropdown(
            id="select-year",
            options=[
                {"label": year, "value": year}
                for year in year_list
            ],
            value=1980,
            placeholder="Select a year",
            disabled=True,
            style={
                "width": "80%",
                "padding": "3px",
                "fontSize": "20px",
                "textAlign": "center"
            }
        )
    ]),

    # TASK 2.3: Output container
    html.Div([
        html.Div(
            id="output-container",
            className="chart-grid",
            style={
                "display": "flex",
                "flexDirection": "column"
            }
        )
    ])
])


# TASK 2.4: Enable or disable the year dropdown
@app.callback(
    Output(
        component_id="select-year",
        component_property="disabled"
    ),
    Input(
        component_id="dropdown-statistics",
        component_property="value"
    )
)
def update_input_container(selected_statistics):
    if selected_statistics == "Yearly Statistics":
        return False

    return True


# Callback for displaying graphs
@app.callback(
    Output(
        component_id="output-container",
        component_property="children"
    ),
    [
        Input(
            component_id="dropdown-statistics",
            component_property="value"
        ),
        Input(
            component_id="select-year",
            component_property="value"
        )
    ]
)
def update_output_container(selected_statistics, input_year):

    # TASK 2.5: Recession Report Statistics
    if selected_statistics == "Recession Period Statistics":

        recession_data = data[data["Recession"] == 1]

        # Plot 1: Average sales by recession year
        yearly_rec = (
            recession_data
            .groupby("Year")["Automobile_Sales"]
            .mean()
            .reset_index()
        )

        R_chart1 = dcc.Graph(
            figure=px.line(
                yearly_rec,
                x="Year",
                y="Automobile_Sales",
                title=(
                    "Average Automobile Sales "
                    "Fluctuation over Recession Period"
                )
            )
        )

        # Plot 2: Average sales by vehicle type
        average_sales = (
            recession_data
            .groupby("Vehicle_Type")["Automobile_Sales"]
            .mean()
            .reset_index()
        )

        R_chart2 = dcc.Graph(
            figure=px.bar(
                average_sales,
                x="Vehicle_Type",
                y="Automobile_Sales",
                title=(
                    "Average Automobile Sales by Vehicle Type "
                    "during Recession"
                ),
                labels={
                    "Vehicle_Type": "Vehicle Type",
                    "Automobile_Sales": "Average Automobile Sales"
                }
            )
        )

        # Plot 3: Advertising expenditure by vehicle type
        exp_rec = (
            recession_data
            .groupby("Vehicle_Type")["Advertising_Expenditure"]
            .sum()
            .reset_index()
        )

        R_chart3 = dcc.Graph(
            figure=px.pie(
                exp_rec,
                values="Advertising_Expenditure",
                names="Vehicle_Type",
                title=(
                    "Advertising Expenditure Share by Vehicle "
                    "Type during Recession"
                )
            )
        )

        # Plot 4: Effect of unemployment on vehicle sales
        unemp_data = (
            recession_data
            .groupby(
                ["unemployment_rate", "Vehicle_Type"]
            )["Automobile_Sales"]
            .mean()
            .reset_index()
        )

        R_chart4 = dcc.Graph(
            figure=px.bar(
                unemp_data,
                x="unemployment_rate",
                y="Automobile_Sales",
                color="Vehicle_Type",
                labels={
                    "unemployment_rate": "Unemployment Rate",
                    "Automobile_Sales": "Average Automobile Sales",
                    "Vehicle_Type": "Vehicle Type"
                },
                title=(
                    "Effect of Unemployment Rate on "
                    "Vehicle Type and Sales"
                )
            )
        )

        return [
            html.Div(
                className="chart-item",
                children=[
                    html.Div(
                        children=R_chart1,
                        style={"width": "50%"}
                    ),
                    html.Div(
                        children=R_chart2,
                        style={"width": "50%"}
                    )
                ],
                style={"display": "flex"}
            ),

            html.Div(
                className="chart-item",
                children=[
                    html.Div(
                        children=R_chart3,
                        style={"width": "50%"}
                    ),
                    html.Div(
                        children=R_chart4,
                        style={"width": "50%"}
                    )
                ],
                style={"display": "flex"}
            )
        ]

    # TASK 2.6: Yearly Report Statistics
    elif (
        input_year
        and selected_statistics == "Yearly Statistics"
    ):

        yearly_data = data[data["Year"] == input_year]

        # Plot 1: Average yearly automobile sales
        yas = (
            data
            .groupby("Year")["Automobile_Sales"]
            .mean()
            .reset_index()
        )

        Y_chart1 = dcc.Graph(
            figure=px.line(
                yas,
                x="Year",
                y="Automobile_Sales",
                title="Yearly Average Automobile Sales",
                labels={
                    "Automobile_Sales": "Average Automobile Sales"
                }
            )
        )

        # Plot 2: Total monthly sales for selected year
        mas = (
            yearly_data
            .groupby("Month")["Automobile_Sales"]
            .sum()
            .reset_index()
        )

        Y_chart2 = dcc.Graph(
            figure=px.line(
                mas,
                x="Month",
                y="Automobile_Sales",
                title=(
                    f"Total Monthly Automobile Sales in {input_year}"
                ),
                labels={
                    "Automobile_Sales": "Total Automobile Sales"
                }
            )
        )

        # Plot 3: Average sales by vehicle type
        avr_vdata = (
            yearly_data
            .groupby("Vehicle_Type")["Automobile_Sales"]
            .mean()
            .reset_index()
        )

        Y_chart3 = dcc.Graph(
            figure=px.bar(
                avr_vdata,
                x="Vehicle_Type",
                y="Automobile_Sales",
                labels={
                    "Vehicle_Type": "Vehicle Type",
                    "Automobile_Sales": "Average Automobile Sales"
                },
                title=(
                    "Average Vehicles Sold by Vehicle Type "
                    f"in the Year {input_year}"
                )
            )
        )

        # Plot 4: Advertising expenditure by vehicle type
        exp_data = (
            yearly_data
            .groupby("Vehicle_Type")["Advertising_Expenditure"]
            .sum()
            .reset_index()
        )

        Y_chart4 = dcc.Graph(
            figure=px.pie(
                exp_data,
                values="Advertising_Expenditure",
                names="Vehicle_Type",
                title=(
                    "Total Advertisement Expenditure "
                    f"for Each Vehicle in {input_year}"
                )
            )
        )

        return [
            html.Div(
                className="chart-item",
                children=[
                    html.Div(
                        children=Y_chart1,
                        style={"width": "50%"}
                    ),
                    html.Div(
                        children=Y_chart2,
                        style={"width": "50%"}
                    )
                ],
                style={"display": "flex"}
            ),

            html.Div(
                className="chart-item",
                children=[
                    html.Div(
                        children=Y_chart3,
                        style={"width": "50%"}
                    ),
                    html.Div(
                        children=Y_chart4,
                        style={"width": "50%"}
                    )
                ],
                style={"display": "flex"}
            )
        ]

    return None


# Run the Dash application
if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8050, debug=False)