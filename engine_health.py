import os
import urllib
import numpy as np
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine

# Load environment variables from secure .env file
load_dotenv()

# ==========================================
# ☁️ SECURE AZURE DATABASE CONFIGURATION
# ==========================================
SERVER = os.getenv('AZURE_SERVER')
DATABASE = os.getenv('AZURE_DATABASE')
USERNAME = os.getenv('AZURE_USERNAME')
PASSWORD = os.getenv('AZURE_PASSWORD')
DRIVER = '{ODBC Driver 17 for SQL Server}'

# Create secure connection string for SQLAlchemy
params = urllib.parse.quote_plus(
    f"DRIVER={DRIVER};SERVER={SERVER};DATABASE={DATABASE};"
    f"UID={USERNAME};PWD={PASSWORD}"
)
engine = create_engine(f"mssql+pyodbc:///?odbc_connect={params}")

def fetch_telemetry_from_azure():
    """Uses SQL queries to pull raw telemetry data from Azure SQL Cloud."""
    query = "SELECT * FROM Flight_Telemetry_Raw"
    return pd.read_sql(query, engine)

def analyze_engine_health(df):
    """Performs aviation engineering calculations and anomaly detection."""
    df = df.sort_values(by='Flight_Number').reset_index(drop=True)
    
    # Calculate EGT Margin (Safety buffer)
    df['EGT_Margin_C'] = df['Max_Allowed_EGT_C'] - df['Recorded_EGT_C']
    
    # Calculate Oil Loss and Flight Duration between stations
    df['Oil_Loss'] = df['Oil_Quantity_Quarts'].diff().fillna(0) * -1
    df['Hours_Flown'] = df['Flight_Hours'].diff().fillna(0)
    
    # Calculate hourly oil consumption rate
    df['Oil_Consumption_Rate'] = np.where(
        df['Hours_Flown'] > 0, df['Oil_Loss'] / df['Hours_Flown'], 0
    )
    
    # Determine automated MRO maintenance alerts
    df['Maintenance_Alert'] = 'NORMAL'
    
    # Standard shortened lines to pass PEP8 / E501 checks
    df.loc[df['EGT_Margin_C'] <= 15, 'Maintenance_Alert'] = \
        'CRITICAL EGT - Trigger Borescope'
    df.loc[df['Oil_Consumption_Rate'] > 0.3, 'Maintenance_Alert'] = \
        'HIGH OIL BURN - Check Bearing Seals'
    df.loc[(df['EGT_Margin_C'] <= 15) & (df['Oil_Consumption_Rate'] > 0.3), 
           'Maintenance_Alert'] = 'EMERGENCY - Ground Aircraft'
    
    return df

def save_analysis_to_azure(df):
    """Saves processed diagnostics and alerts into Azure cloud table."""
    df.to_sql('Engine_Health_Results', engine, if_exists='replace', index=False)
    print("✅ Analysis successfully synced and saved to Azure SQL Database.")

if __name__ == "__main__":
    print("=== Starting Azure Engine Health Pipeline ===")
    try:
        raw_data = fetch_telemetry_from_azure()
        processed_results = analyze_engine_health(raw_data)
        save_analysis_to_azure(processed_results)
    except Exception as e:
        print(f"❌ Connection or Processing Error: {e}")
