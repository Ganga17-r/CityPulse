import random
import csv
from datetime import datetime, timedelta

# City areas
zones = ["Zone_A", "Zone_B", "Zone_C", "Zone_D", "Zone_E"]

# Output file
file_path = "Data/raw/city_data.csv"

# Start date
start_date = datetime(2026, 1, 1, 0, 0)

# Generate 1 year of data at 5-minute intervals
end_date = start_date + timedelta(days=365)

with open(file_path, "w", newline="") as file:

    writer = csv.writer(file)

    # CSV header
    writer.writerow([
        "timestamp",
        "zone",
        "traffic",
        "temperature",
        "aqi",
        "energy",
        "activity"
    ])

    current_time = start_date

    while current_time < end_date:

        hour = current_time.hour

        # Decide the normal pattern based on time
        if 7 <= hour <= 9:
            traffic_range = (700, 900)
            temperature_range = (25, 30)
            aqi_range = (60, 100)
            energy_range = (350, 500)
            activity_range = (800, 1200)

        elif 12 <= hour <= 15:
            traffic_range = (400, 600)
            temperature_range = (30, 36)
            aqi_range = (70, 120)
            energy_range = (400, 550)
            activity_range = (500, 800)

        elif 17 <= hour <= 20:
            traffic_range = (800, 1000)
            temperature_range = (27, 32)
            aqi_range = (65, 110)
            energy_range = (500, 700)
            activity_range = (900, 1400)

        else:
            traffic_range = (100, 300)
            temperature_range = (22, 27)
            aqi_range = (50, 90)
            energy_range = (200, 350)
            activity_range = (100, 400)

        # Generate data for every zone
        for zone in zones:

            traffic = random.randint(*traffic_range)
            temperature = random.randint(*temperature_range)
            aqi = random.randint(*aqi_range)
            energy = random.randint(*energy_range)
            activity = random.randint(*activity_range)

            # Create occasional unusual events
            if random.random() < 0.01:
                traffic *= random.randint(2, 4)
                activity *= random.randint(2, 3)
                aqi += random.randint(30, 80)

            writer.writerow([
                current_time.strftime("%Y-%m-%d %H:%M:%S"),
                zone,
                traffic,
                temperature,
                aqi,
                energy,
                activity
            ])

        # Move to the next 5-minute interval
        current_time += timedelta(minutes=5)

print("CityPulse dataset generated successfully!")