import utils
import world_bank_api

from matplotlib.mlab import prctile_rank
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap as Basemap
import numpy as np
from matplotlib.colors import rgb2hex
from matplotlib.patches import Polygon


def decide_colors_and_countries(world_map, poverty_data):
    colors = {}
    country_names = []
    cmap = plt.cm.hot # use 'hot' colormap
    vmin = 0.0
    vmax = 450.0 # set range.
    for shapedict in world_map.countries_info:
        country_name = shapedict['NAME']
        if country_name not in poverty_data:
            poverty_rate = 0.0 # TODO
        else:
            poverty_rate = poverty_data[country_name]['poverty_rates']['3.10']['percent']

        if poverty_rate is None:
            poverty_rate = 0.0 #TODO

        poverty_rate = float(poverty_rate)

        # calling colormap with value between 0 and 1 returns
        # rgba value.  Invert color range (hot colors are high
        # population), take sqrt root to spread out colors more.
        color = cmap(1.-np.sqrt((poverty_rate-vmin)/(vmax-vmin)))[:3]
        colors[country_name] = color
        country_names.append(country_name)

    return colors, country_names

def create_map():
    poverty_data, error = world_bank_api.most_recent_poverty_data()
    if error is not None:
        print(error)
        return

    poverty_data = utils.dictify_list_of_dicts(poverty_data, 'country_name')

    world_map = Basemap()
    shape_info = world_map.readshapefile('borders', 'countries')
    country_to_color, country_names = decide_colors_and_countries(world_map, poverty_data)

    ax = plt.gca() # get current axes instance
    for nshape, seg in enumerate(world_map.countries):
        country_name = country_names[nshape]
        if country_name not in country_to_color:
            print('could not find: ' + country_name)
            continue
        color = rgb2hex(country_to_color[country_name])
        poly = Polygon(seg, facecolor=color, edgecolor=color)
        ax.add_patch(poly)

    # m.drawcoastlines()
    # m.fillcontinents()
    #m.drawcountries()
    plt.title('Countries by poverty rate')
    plt.show()

if __name__ == '__main__':
    create_map()
