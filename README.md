# Aircraft-Engine-Health-Analytics

masoudkh
5:35 PM (0 minutes ago)
to me

# Aircraft Engine Predictive Maintenance & Health Analytics

An aviation-focused data analytics script written in Python to monitor **Boeing 737** engine health. This project demonstrates the intersection of **Aircraft Maintenance** and **Cloud Data Analytics**, focusing on predictive alerts for maintenance crews.

## ✈️ Aviation Core Concepts Implemented
- **EGT Margin Tracking:** Monitors the degradation of the engine compressor. Automatically triggers alerts for a **Compressor Wash** or **Borescope Inspection** when the margin drops below 15°C.
- **Oil Consumption Rate:** Calculates real-time fluid loss per flight hour. Triggers warning alerts if consumption exceeds **0.3 Qts/Hr**, indicating potential **Bearing Seal** failure.

## 🛠️ Tech Stack & Skills
- **Language:** Python 3
- **Data Libraries:** Pandas, NumPy
- **Cloud Use Case:** Ready for integration with cloud streaming telemetry (e.g., Azure IoT Hub or AWS IoT Core) to enable real-time fleet monitoring.

## 📊 Sample Output
The script processes multi-flight telemetry data and outputs critical maintenance logs:
`Flight 106 | EGT Margin: 15.0°C | Oil Burn Rate: 0.417 Qts/Hr`
`⚠️ [ALERT] Critical EGT Margin! Triggering Compressor Wash/Borescope Inspection.`
`⚠️ [ALERT] High Oil Consumption! Check Bearing Seals.`
