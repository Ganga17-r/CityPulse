from pyspark.sql import SparkSession
from pyspark.sql.functions import avg, stddev, col, round, abs
import csv
import os

spark = SparkSession.builder \
    .appName("CityPulse Big Data Analysis") \
    .master("local[*]") \
    .getOrCreate()

# Read the large CityPulse dataset
df = spark.read.csv(
    "Data/raw/city_data.csv",
    header=True,
    inferSchema=True
)

print("\n=== CITYPULSE DATASET ===")
print("Total records:", df.count())

# --------------------------------------------------
# 1. CITY ZONE SUMMARY
# --------------------------------------------------

zone_summary = df.groupBy("zone").agg(
    round(avg("traffic"), 2).alias("avg_traffic"),
    round(avg("temperature"), 2).alias("avg_temperature"),
    round(avg("aqi"), 2).alias("avg_aqi"),
    round(avg("energy"), 2).alias("avg_energy"),
    round(avg("activity"), 2).alias("avg_activity")
)

print("\n=== CITYPULSE ZONE SUMMARY ===")
zone_summary.show()

# --------------------------------------------------
# 2. CALCULATE NORMAL VALUES
# --------------------------------------------------

stats = df.select(
    avg("traffic").alias("traffic_mean"),
    stddev("traffic").alias("traffic_std"),
    avg("aqi").alias("aqi_mean"),
    stddev("aqi").alias("aqi_std"),
    avg("activity").alias("activity_mean"),
    stddev("activity").alias("activity_std")
).collect()[0]

traffic_mean = stats["traffic_mean"]
traffic_std = stats["traffic_std"]

aqi_mean = stats["aqi_mean"]
aqi_std = stats["aqi_std"]

activity_mean = stats["activity_mean"]
activity_std = stats["activity_std"]

# --------------------------------------------------
# 3. DETECT ANOMALIES
# --------------------------------------------------

anomalies = df.filter(
    (col("traffic") >= 2500) |
    (col("aqi") >= 140) |
    (col("activity") >= 2000)
)
print("\n=== ANOMALIES DETECTED ===")
print("Total anomalies:", anomalies.count())

anomalies.select(
    "timestamp",
    "zone",
    "traffic",
    "temperature",
    "aqi",
    "energy",
    "activity"
).show(10)

# --------------------------------------------------
# 4. SAVE RESULTS USING PYTHON
# --------------------------------------------------

os.makedirs("Data/processed", exist_ok=True)

# Save zone summary
zone_rows = zone_summary.collect()

with open(
    "Data/processed/zone_summary.csv",
    "w",
    newline=""
) as file:

    writer = csv.writer(file)

    writer.writerow([
        "zone",
        "avg_traffic",
        "avg_temperature",
        "avg_aqi",
        "avg_energy",
        "avg_activity"
    ])

    for row in zone_rows:
        writer.writerow([
            row["zone"],
            row["avg_traffic"],
            row["avg_temperature"],
            row["avg_aqi"],
            row["avg_energy"],
            row["avg_activity"]
        ])

# Save anomalies
anomaly_rows = anomalies.collect()

with open(
    "Data/processed/anomalies.csv",
    "w",
    newline=""
) as file:

    writer = csv.writer(file)

    writer.writerow([
        "timestamp",
        "zone",
        "traffic",
        "temperature",
        "aqi",
        "energy",
        "activity"
    ])

    for row in anomaly_rows:
        writer.writerow([
            row["timestamp"],
            row["zone"],
            row["traffic"],
            row["temperature"],
            row["aqi"],
            row["energy"],
            row["activity"]
        ])

print("\n=== RESULTS SAVED ===")
print("Data/processed/zone_summary.csv")
print("Data/processed/anomalies.csv")

spark.stop()