import csv
import sys
from bokeh.sampledata import us_counties, unemployment
from bokeh.plotting import *
from cassandra.cluster import Cluster

# The county code is a tuple (state ID, county ID). 
# The "patches" graph is an array of arrays. Each element is a set of
# lat/lon points that represents a polygon. 
# Then for each element, we assign a color to that polygon.

colors = ['#993355',
          '#3333FF',
          '#3399FF',
          '#33FFFF',
          '#33FF99',
          '#33FF33',
          '#99FF33',
          '#FFFF33',
          '#FF9933',
          '#FF3333']

def _connect_to_cassandra(keyspace):
    """
    Connect to the Cassandra cluster and return the session.
    """

    if 'BACKEND_STORAGE_IP' in os.environ:
        host = os.environ['BACKEND_STORAGE_IP']
    else:
        host = 'localhost'

    cluster = Cluster([host])
    session = cluster.connect(keyspace)

    return session

def _get_econ_data(state_abbr):
    highest_median = -1
    median_econ_data = {}
    county_xs=[]
    county_ys=[]

    query = """SELECT * FROM sensor_data
               WHERE sensor_id=%(sensor)s
               and time>%(time)s
               ORDER BY time DESC"""

    values = { 'time': ts,
               'sensor': sensor }

    rows = session.execute(query, values)

    return county_xs, county_ys, median_econ_data, highest_median

def _color_econ_data(state_abbr, county_xs, county_ys, median_econ_data, highest_median):
    county_colors = []
    for county_id in us_counties.data:
        if us_counties.data[county_id]['state'] != state_abbr:
            continue

        try:
            rate = float(median_econ_data[county_id]) / float(highest_median)
            idx = min(int(10 * rate), 9)
            county_colors.append(colors[idx])
        except KeyError:
            county_colors.append("black")

    return county_colors

def _output_econ_data(county_xs, county_ys, county_colors, width=500, height=200):
    patches(county_xs, county_ys, fill_color=county_colors, fill_alpha=0.7,
            line_color="white", line_width=0.5, plot_height=height, plot_width=width, title="Median Income")
    grid().grid_line_color = None
    axis().axis_line_color = None
    axis().major_tick_line_color = None
    show()

state_name = sys.argv[1]
state_abbr = sys.argv[2]
data_file = sys.argv[3]
template_dir = sys.argv[4]

output_file(template_dir + '/' + state_name + '.html')

county_xs, county_ys, econ_data, highest_median = _get_econ_data(data_file, state_abbr)
county_colors = _color_econ_data(state_abbr, county_xs, county_ys, econ_data, highest_median)
_output_econ_data(county_xs, county_ys, county_colors, 500, 250)
