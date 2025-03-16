import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import numpy as np
import random
import json
from datetime import datetime
from fpdf import FPDF

# Initialize the app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = "Smart City Simulation Model"

# Generate simulated data
np.random.seed(42)
days = pd.date_range(start="2025-01-01", periods=30)
energy_consumption = np.random.randint(100, 500, size=30)
optimized_consumption = energy_consumption - np.random.randint(10, 50, size=30)
energy_data = pd.DataFrame({"Date": days, "Energy Consumption (kWh)": energy_consumption, "Optimized Consumption (kWh)": optimized_consumption})

waste_types = ['Organic', 'Plastic', 'Metal', 'Glass', 'Paper']
waste_quantities = [random.randint(50, 200) for _ in waste_types]
optimized_waste = [round(q * 0.7) for q in waste_quantities]
waste_data = pd.DataFrame({"Waste Type": waste_types, "Generated Waste (kg)": waste_quantities, "Recycled Waste (kg)": optimized_waste})

pollution_zones = ['Residential', 'Industrial', 'Commercial', 'Urban Park', 'Suburban']
air_quality_index = [random.randint(50, 200) for _ in pollution_zones]
water_quality_index = [random.randint(30, 100) for _ in pollution_zones]
pollution_data = pd.DataFrame({"Zone": pollution_zones, "Air Quality Index (AQI)": air_quality_index, "Water Quality Index (WQI)": water_quality_index})

locations = ['Area A', 'Area B', 'Area C', 'Area D', 'Area E']
congestion_level = [random.randint(20, 100) for _ in locations]
traffic_data = pd.DataFrame({"Location": locations, "Congestion Level (%)": congestion_level})

# Define app layout
app.layout = dbc.Container([
    html.H1("Smart City Simulation Model", style={'textAlign': 'center', 'color': '#2E86C1'}),
    html.Hr(),
    
    dbc.Tabs([
        dbc.Tab(label="Energy Analysis", tab_id="energy"),
        dbc.Tab(label="Waste Management", tab_id="waste"),
        dbc.Tab(label="Pollution Control", tab_id="pollution"),
        dbc.Tab(label="Traffic Control", tab_id="traffic")
    ], id="tabs", active_tab="energy"),
    
    html.Div(id="tab-content", style={'padding': '20px'}),
    dbc.Button("Generate PDF Report", id="generate-report", color="primary", className="mt-3"),
    dcc.Download(id="download-report")
])

# Callback to update tabs
@app.callback(Output('tab-content', 'children'),
              Input('tabs', 'active_tab'))
def render_content(tab):
    if tab == 'energy':
        fig = px.line(energy_data, x="Date", y=["Energy Consumption (kWh)", "Optimized Consumption (kWh)"], 
                      title="Energy Analysis", template="plotly_dark")
        return dcc.Graph(figure=fig)
    
    elif tab == 'waste':
        fig = px.pie(waste_data, names='Waste Type', values='Generated Waste (kg)', title="Waste Distribution", template="plotly_dark")
        return dcc.Graph(figure=fig)
    
    elif tab == 'pollution':
        fig = px.bar(pollution_data, x='Zone', y='Air Quality Index (AQI)', title="Air Quality Index by Zone", template="plotly_dark")
        return dcc.Graph(figure=fig)
    
    elif tab == 'traffic':
        fig = px.density_heatmap(traffic_data, x="Location", y="Congestion Level (%)", title="Traffic Congestion Heatmap", template="plotly_dark")
        return dcc.Graph(figure=fig)

# Report Generation Callback
@app.callback(
    Output("download-report", "data"),
    Input("generate-report", "n_clicks")
)
def generate_pdf_report(n_clicks):
    if n_clicks:
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.set_text_color(0, 0, 0)
        
        # Add title
        pdf.set_font("Arial", 'B', 16)
        pdf.cell(200, 10, txt="Smart City Simulation Model Report", ln=True, align='C')
        pdf.ln(10)
        
        # Energy Analysis
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(0, 10, 'Energy Analysis', ln=True)
        pdf.set_font("Arial", size=12)
        pdf.multi_cell(0, 10, f"Energy Data: \n{energy_data.to_string(index=False)}")
        
        pdf.ln(5)
        
        # Waste Management
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(0, 10, 'Waste Management', ln=True)
        pdf.set_font("Arial", size=12)
        pdf.multi_cell(0, 10, f"Waste Data: \n{waste_data.to_string(index=False)}")
        
        pdf.ln(5)
        
        # Pollution Control
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(0, 10, 'Pollution Control', ln=True)
        pdf.set_font("Arial", size=12)
        pdf.multi_cell(0, 10, f"Pollution Data: \n{pollution_data.to_string(index=False)}")
        
        pdf.ln(5)
        
        # Traffic Control
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(0, 10, 'Traffic Control', ln=True)
        pdf.set_font("Arial", size=12)
        pdf.multi_cell(0, 10, f"Traffic Data: \n{traffic_data.to_string(index=False)}")
        
        # Save the PDF file
        pdf_file = "Smart_City_Simulation_Report.pdf"
        pdf.output(pdf_file)
        
        return dcc.send_file(pdf_file)

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)