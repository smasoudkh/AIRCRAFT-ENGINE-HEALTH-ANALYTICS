import pandas as pd
import numpy as np

def analyze_engine_health(telemetry_data):
    df = pd.DataFrame(telemetry_data)
    
    # Calculate EGT Margin (Safety buffer between max limit and recorded temp)
    df['EGT_Margin_C'] = df['Max_Allowed_EGT_C'] - df['Recorded_EGT_C']
    
    # Calculate Oil Loss and Flight Duration between stations
    df['Oil_Loss'] = df['Oil_Quantity_Quarts'].diff().fillna(0) * -1
    df['Hours_Flown'] = df['Flight_Hours'].diff().fillna(0)
    
    # Calculate hourly oil consumption rate
    df['Oil_Consumption_Rate'] = np.where(df['Hours_Flown'] > 0, df['Oil_Loss'] / df['Hours_Flown'], 0)
    
    return df

# Simulated data for 7 consecutive Boeing 737 flights
flight_telemetry = {
    'Flight_Number': [101, 102, 103, 104, 105, 106, 107],
    'Flight_Hours': [1000, 1005, 1011, 1016, 1022, 1028, 1034],
    'Recorded_EGT_C': [580.0, 582.5, 595.0, 610.0, 635.5, 645.0, 648.2],
    'Max_Allowed_EGT_C': [660.0, 660.0, 660.0, 660.0, 660.0, 660.0, 660.0],
    'Oil_Quantity_Quarts': [16.0, 15.2, 14.5, 12.1, 11.0, 8.5, 7.2]
}

print("=== Azure Engine Health Core ===")
results = analyze_engine_health(flight_telemetry)

for idx, row in results.iterrows():
    print(f"Flight {int(row['Flight_Number'])} | EGT Margin: {row['EGT_Margin_C']}°C | Oil Burn Rate: {row['Oil_Consumption_Rate']:.3f} Qts/Hr")
    if row['EGT_Margin_C'] <= 15:
        print(" ⚠️ [ALERT] Critical EGT Margin! Triggering Compressor Wash/Borescope Inspection.")
    if row['Oil_Consumption_Rate'] > 0.3:
        print(" ⚠️ [ALERT] High Oil Consumption! Check Bearing Seals.")
    print("-" * 50)

