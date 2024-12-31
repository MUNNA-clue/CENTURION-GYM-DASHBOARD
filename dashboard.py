import dash
from dash import dcc, html, Input, Output
import dash_table
import pandas as pd
import plotly.express as px

# Load data
file_path = "Gym_Management_Dashboard_Data.xlsx"
members_df = pd.read_excel(file_path, sheet_name="Members")
attendance_df = pd.read_excel(file_path, sheet_name="Attendance")

# Initialize Dash app
app = dash.Dash(__name__)
app.title = "Gym Management Dashboard"

# App layout
app.layout = html.Div([
    html.H1("Gym Management Dashboard", style={"textAlign": "center", "marginBottom": "20px"}),

    # Dropdown to select ERP
    html.Div([
        html.Label("Select ERP:", style={"fontWeight": "bold"}),
        dcc.Dropdown(
            id="erp-dropdown",
            options=[{"label": erp, "value": erp} for erp in members_df["ERP"].unique()],
            placeholder="Select an ERP",
            style={"width": "300px"}
        )
    ], style={"marginBottom": "20px"}),

    # Attendance table
    html.Div([
        html.Label("Attendance Table:", style={"fontWeight": "bold", "fontSize": "18px"}),
        dash_table.DataTable(
            id="attendance-table",
            columns=[
                {"name": "Month", "id": "Month"},
                {"name": "Day", "id": "Day"},
                {"name": "Present", "id": "Present"},
                {"name": "Workout", "id": "Workout"}
            ],
            style_table={"overflowX": "auto"},
            style_cell={"textAlign": "center", "padding": "5px"},
            style_header={"backgroundColor": "#f4f4f4", "fontWeight": "bold"},
        )
    ], style={"marginBottom": "40px"}),

    # Charts
    html.Div([
        html.Div([
            dcc.Graph(id="attendance-line-plot")
        ], style={"width": "48%", "display": "inline-block"}),

        html.Div([
            dcc.Graph(id="workout-pie-chart")
        ], style={"width": "48%", "display": "inline-block"})
    ])
], style={"padding": "20px", "fontFamily": "Arial"})

# Callbacks
@app.callback(
    [
        Output("attendance-table", "data"),
        Output("attendance-line-plot", "figure"),
        Output("workout-pie-chart", "figure")
    ],
    [Input("erp-dropdown", "value")]
)
def update_dashboard(selected_erp):
    if not selected_erp:
        return [], {}, {}

    # Filter attendance data for the selected ERP
    filtered_data = attendance_df[attendance_df["ERP"] == selected_erp]

    # Prepare data for the line plot
    monthly_attendance = filtered_data.groupby("Month")["Present"].sum().reset_index()
    line_fig = px.line(
        monthly_attendance,
        x="Month",
        y="Present",
        title="Monthly Attendance Trend",
        labels={"Present": "Attendance Count", "Month": "Month"},
        markers=True
    )

    # Prepare data for the pie chart
    workout_distribution = filtered_data[filtered_data["Workout"].notna()]
    workout_counts = workout_distribution["Workout"].value_counts().reset_index()
    workout_counts.columns = ["Workout", "Count"]
    pie_fig = px.pie(
        workout_counts,
        names="Workout",
        values="Count",
        title="Workout Distribution"
    )

    return filtered_data.to_dict("records"), line_fig, pie_fig

# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)
