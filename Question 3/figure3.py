from matplotlib import pyplot as plt
import seaborn as sns

from random_data import random_delivery_data
from utils import OUTPUT_DIR, LINE_PLOT_ARGS, get_display_str

min_year = 2024
region = ['Central', 'East']
x = 'order_hour'
y = 'waiting_time'

display_x = get_display_str(x)
display_y = get_display_str(y)

# Filter for recent orders:
# filter the dataset to include only orders from 2024 onwards to focus on recent trends in certain region.
latest_data = random_delivery_data[
    (random_delivery_data['year'] >= 2024) &
    (random_delivery_data['region'].isin(region))
]

# Calculate average delivery time by hour:
# The average delivery time is calculated by grouping the data by order_hour
# and taking the mean of the waiting_time for each hour.
avg_deliver_time = latest_data.groupby(
    ['order_hour', 'region']
)['waiting_time'].mean().reset_index()

# Plotting:
# A line plot is generated to visualize the trend of average delivery time across different hours of the
# day in different region.
fig, ax = plt.subplots(figsize=(10, 6))
sns.lineplot(
    data=avg_deliver_time,
    x="order_hour",
    y="waiting_time",
    hue="region",
    ax=ax,
    **LINE_PLOT_ARGS
)

ax.set_xlabel(display_x)
ax.set_ylabel(display_y)

plt.suptitle(
    'Sample Figure 3 Average Delivery by Time Hour and Region In A Day',
    fontsize=14,
    fontweight='bold'
)

plt.savefig(
    OUTPUT_DIR + 'sample_figure_3_avg_deliver_time_by_hour_and_region.png',
    dpi=300
)
plt.close()