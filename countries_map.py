import utils
import world_bank_api

from matplotlib.mlab import prctile_rank
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap as Basemap
import matplotlib.patches as mpatches
import numpy
from matplotlib.colors import rgb2hex
from matplotlib.patches import Polygon


def calculate_color(rate):
    '''
    calling colormap with value between 0 and 1 returns
    rgba value.  Invert color range (hot colors are high
    population), take sqrt root to spread out colors more.
    '''
    cmap = plt.cm.hot # use 'hot' colormap
    vmin = 0.0
    vmax = 100.0 # set range.
    if rate != 0.0:
        color = cmap(1.-numpy.sqrt((rate-vmin)/(vmax-vmin)))[:3]
        color = rgb2hex(color)
    else:
        color = 'grey'
    return color

def decide_colors_and_countries(world_map, poverty_data):
    found_countries = set()
    missing_countries = set()
    colors = {}
    country_names = []
    for shapedict in world_map.countries_info:
        country_code = shapedict['ISO2']
        country_name = shapedict['NAME']
        if country_code not in poverty_data:
            poverty_rate = 0.0 # TODO
            missing_countries.add(country_name)
        else:
            poverty_rate = poverty_data[country_code]['poverty_rates']['3.10']['percent']
            found_countries.add(country_name)
            if poverty_rate is None:
                poverty_rate = 0.0 #TODO
            else:
                pass

        poverty_rate = float(poverty_rate)
        color = calculate_color(poverty_rate)
        colors[country_name] = color
        country_names.append(country_name)


    print('list of places included in the map but that do not map to world bank data. Usually these are oversees territories but there are some really messed up ones like Taiwan. In additon the world bank lists many countries that it does not have data for.')
    print(missing_countries)
    return colors, country_names

def create_map():
    poverty_data, error = world_bank_api.most_recent_poverty_data()
    if error is not None:
        print(error)
        return

    poverty_data = utils.dictify_list_of_dicts(poverty_data, 'country_code')

    world_map = Basemap()
    world_map.readshapefile('borders', 'countries')
    country_to_color, country_names = decide_colors_and_countries(world_map, poverty_data)

    axes = plt.gca() # get current axes instance
    for nshape, seg in enumerate(world_map.countries):
        country_name = country_names[nshape]
        if country_name not in country_to_color:
            print('could not find: ' + country_name)
            continue
        color = country_to_color[country_name]
        poly = Polygon(seg, facecolor=color, edgecolor=color)
        axes.add_patch(poly)

    # m.drawcoastlines()
    # m.fillcontinents()
    #m.drawcountries()
    add_legend()
    fig = plt.gcf()
    fig.set_size_inches(30, 15)

    plt.axis('off')
    fig.savefig('countries_by_poverty_rate_world_bank_data.png', dpi=100,
                bbox_inches='tight',
                pad_inches=0)
    # plt.savefig('poverty_map.png', bbox_inches='tight')
    # plt.show()

def add_legend():

    rates = [('0 or not available', 0.0,),
             ('20', 20.0,),
             ('40', 40.0,),
             ('60', 60.0,),
             ('80', 80.0,),
             ('100', 100.0,),]

    patches = []
    for rate_info, rate in rates:
        color = calculate_color(rate)
        patch = mpatches.Patch(facecolor=color, label=rate_info, edgecolor='black')
        patches.append(patch)
    plt.legend(handles=patches, loc='lower left',
               handlelength=2,
               fontsize=30)


if __name__ == '__main__':
    create_map()
