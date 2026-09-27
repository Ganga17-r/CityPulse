import random
import csv
import os
from datetime import datetime, timedelta

# City zones
zones = [
    "Zone_A",
    "Zone_B",
    "Zone_C",
    "Zone_D",
    "Zone_E"
]

# Different characteristics for each simulated zone
zone_profiles = {
    "Zone_A": {
        "traffic": 1.15,
        "activity": 1.10,
        "energy": 1.05,
        "aqi": 1.00
    },
    "Zone_B": {
        "traffic": 0.85,
        "activity": 0.90,
        "energy": 0.95,
        "aqi": 0.90
    },
    "Zone_C": {
        "traffic": 1.05,
        "activity": 1.00,
        "energy": 1.10,
        "aqi": 1.20
    },
    "Zone_D": {
        "traffic": 1.25,
        "activity": 1.20,
        "energy": 1.10,
        "aqi": 1.10
    },
    "Zone_E": {
        "traffic": 0.95,
        "activity": 1.00,
        "energy": 1.00,
        "aqi": 1.00
    }
}

# Output file
file_path = "Data/raw/city_data.csv"

# Create output folder if needed
os.makedirs("Data/raw", exist_ok=True)

# One year of data
start_date = datetime(2026, 1, 1, 0, 0)
end_date = datetime(2027, 1, 1, 0, 0)

# Small seasonal temperature variation
seasonal_adjustment = {
    1: -2,
    2: -1,
    3: 0,
    4: 1,
    5: 2,
    6: 1,
    7: 0,
    8: 0,
    9: 0,
    10: 0,
    11: -1,
    12: -2
}

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
        month = current_time.month
        weekday = current_time.weekday()

        # Weekend adjustment
        if weekday >= 5:
            weekend_factor = 0.82
            weekend_energy_factor = 0.92
        else:
            weekend_factor = 1.0
            weekend_energy_factor = 1.0

        # Time-based city behavior
        if 7 <= hour <= 9:
            traffic_range = (750, 950)
            temperature_range = (25, 30)
            aqi_range = (70, 100)
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

            profile = zone_profiles[zone]

            # Traffic
            traffic = int(
                random.randint(*traffic_range)
                * profile["traffic"]
                * weekend_factor
            )

            # Activity
            activity = int(
                random.randint(*activity_range)
                * profile["activity"]
                * weekend_factor
            )

            # Energy depends partly on activity
            energy = int(
                random.randint(*energy_range)
                * profile["energy"]
                * weekend_energy_factor
                * (0.80 + activity / 4000)
            )

            # Temperature
            temperature = (
                random.randint(*temperature_range)
                + seasonal_adjustment[month]
            )

            # AQI influenced slightly by traffic
            aqi = int(
                random.randint(*aqi_range)
                * profile["aqi"]
                + max(0, (traffic - 500) // 60)
            )

            # --------------------------------------------------
            # OCCASIONAL EXTREME EVENT
            # --------------------------------------------------

            if random.random() < 0.001:

                event_type = random.choice([
                    "traffic",
                    "aqi",
                    "activity"
                ])

                if event_type == "traffic":
                    traffic = random.randint(2500, 4000)

                elif event_type == "aqi":
                    aqi = random.randint(140, 200)

                elif event_type == "activity":
                    activity = random.randint(2000, 3500)

            # Write record
            writer.writerow([
                current_time.strftime("%Y-%m-%d %H:%M:%S"),
                zone,
                traffic,
                temperature,
                aqi,
                energy,
                activity
            ])

        # Move to next 5-minute interval
        current_time += timedelta(minutes=5)

print("CityPulse V2 dataset generated successfully!")
print("File:", file_path)
print("Records: 525,600")