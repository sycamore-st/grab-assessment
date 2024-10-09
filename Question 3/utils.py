import os
from os.path import dirname, realpath

get_display_str = lambda x: x.replace('_', ' ').title()


def get_output_dir(file_path):
    output_dir = dirname(realpath(file_path)) + os.sep + 'output' + os.sep
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    return output_dir


OUTPUT_DIR = get_output_dir(__file__)

LINE_PLOT_ARGS = dict(
    lw=3,
    zorder=12,
    alpha=0.7,
    legend=True,
    marker='o'
)
