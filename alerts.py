def get_alerts(row):
    alerts = []

    if row["heart_rate"] > 110:
        alerts.append("⚠ High Heart Rate")

    if row["temperature"] > 37.5:
        alerts.append("🌡 Fever Risk")

    if row["water_intake"] < 800:
        alerts.append("💧 Low Water Intake")

    if row["sleep_hours"] < 6:
        alerts.append("😴 Poor Sleep")

    return alerts