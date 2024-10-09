from matplotlib import pyplot as plt
from datetime import datetime
import seaborn as sns

from random_data import random_delivery_data
from utils import OUTPUT_DIR, LINE_PLOT_ARGS, get_display_str

x = 'order_date_index'
y = 'waiting_time'

display_x = get_display_str(x)
display_y = get_display_str(y)

# Take monthly averages:
# The data is resampled by taking the average delivery time for each month
# to smooth out noise and better observe trends over time.
random_delivery_data['order_date_index'] = random_delivery_data['order_date'].apply(
    lambda a: datetime(a.year, a.month, 1)
)

# Calculate monthly average waiting time:
# The average waiting time is calculated by grouping the data by month (order_date_index)
# and then taking the mean of the waiting_time for each group.
avg_deliver_time = random_delivery_data.groupby(
    'order_date_index'
)['waiting_time'].mean().reset_index()


# Plotting:
# A line plot is generated to visualize the trend in average delivery time across time,
# with each data point representing a month.
fig, ax = plt.subplots(figsize=(10, 6))
sns.lineplot(
    data=avg_deliver_time,
    x=x,
    y=y,
    ax=ax,
    **LINE_PLOT_ARGS
)

plt.suptitle(
    'Sample Figure 1: Average Delivery Time Across Time',
    fontsize=14,
    fontweight='bold'
)
ax.set_xlabel(display_x)
ax.set_ylabel(display_y)

plt.savefig(
    OUTPUT_DIR + 'sample_figure_1_avg_deliver_time_across_time.png',
    dpi=300
)