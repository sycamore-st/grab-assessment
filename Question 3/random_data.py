import random
import pandas as pd
from dataclasses import dataclass
from datetime import timedelta, datetime

random.seed(42)


def generate_random_item_count(
        max_item_count: int = 10,
):
    return random.randint(1, max_item_count)


def generate_random_kitchen_processing_time(
        item_count: int,
        max_kitchen_processing_time: int = 60,
):
    return min(
        random.randint(5, 10) * item_count, max_kitchen_processing_time
    )


# Function to generate random delivery times (between 30 min and 60 min)
# Adjust based on year, peak hours, and region
def generate_random_delivery_time(year, hour, region):
    # Base delivery time range
    base_delivery_time = random.randint(30, 60)

    # Increase for more recent years
    year_adjustment = (year - 2019) * random.randint(0, 10)

    # Peak hour adjustment: increase during lunch (12 PM - 2 PM) and dinner (6 PM - 8 PM)
    if 12 <= hour <= 14 or 18 <= hour <= 20:
        peak_hour_adjustment = random.randint(0, 30)

        # Central region adjustment: increase more during peak hours in the Central region
        if region == 'Central':
            central_region_adjustment = random.randint(0, 20)

        else:
            central_region_adjustment = 0

    else:
        peak_hour_adjustment = 0
        central_region_adjustment = 0

    # Calculate final delivery time
    delivery_time = base_delivery_time + year_adjustment + peak_hour_adjustment + central_region_adjustment
    return delivery_time


# Function to generate random dates in the past 5 years and extract the year and hour
def generate_random_date():
    start_date = datetime.now() - timedelta(days=5 * 365)  # 5 years ago from today
    end_date = datetime.now()  # today
    random_date = start_date + (end_date - start_date) * random.random()
    return random_date, random_date.year, random_date.hour  # Return date, year, and hour


# Function to randomly select regions in Singapore
def generate_random_region():
    regions = ['Central', 'East', 'North', 'North-East', 'West']
    return random.choice(regions)


@dataclass
class Order:
    order_date: datetime
    item_count: int
    region: str
    processing_time: int
    delivery_time: int


# Generate a set of random data
def generate_random_delivery_data(num_records):
    data = []
    for _ in range(num_records):
        order_date, year, hour = generate_random_date()  # Random delivery date, year, and hour
        item_count = generate_random_item_count() # Random item count
        processing_time = generate_random_kitchen_processing_time(item_count) # Random processing time
        region = generate_random_region()  # Random region in Singapore
        delivery_time = generate_random_delivery_time(year, hour, region)  # Random delivery time based on conditions
        data += [
                Order(
                    order_date=order_date,
                    item_count=item_count,
                    region=region,
                    processing_time=processing_time,
                    delivery_time=delivery_time,
                )
            ]
    return pd.DataFrame(data)


# Generate 100 random delivery records
num_records = 10000
random_delivery_data = generate_random_delivery_data(num_records)
random_delivery_data['waiting_time'] = random_delivery_data['delivery_time'] + random_delivery_data['processing_time']

# Extract order year and hour:
# extract the year and hour from the order_date column to understand the delivery times by the hour of the day.
random_delivery_data['year'] = random_delivery_data['order_date'].dt.year
random_delivery_data['order_hour'] = random_delivery_data['order_date'].dt.hour