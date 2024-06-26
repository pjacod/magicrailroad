from matplotlib import pyplot as plt
import pandas as pd
from shapely.geometry import Point, LineString
import geopandas as gpd
import time

# timestamp for each saved image
timestamp = time.strftime("%Y%m%d-%H%M")

def bar_k(k_values):
    """
    generates a bar chart of k values per attempt.
    """
    iterations = range(1, len(k_values) + 1)

    plt.title('k values per iteration', color = 'mediumblue')
    plt.xlabel('attempts', color = 'mediumblue')
    plt.ylabel('k value', color = 'mediumblue')
    plt.bar(iterations, k_values, color = 'mediumblue')
    plt.grid(True)
    plt.savefig(f'visualizations/bar_k_{timestamp}.png')
    plt.show()

def histogram_k(k_values):
    """
    generates a histogram visualizing the distribution of k values.
    """
    plt.title('frequency per k_value', color = 'mediumblue')
    plt.xlabel('k_value', color = 'mediumblue')
    plt.ylabel('frequency', color = 'mediumblue')
    plt.hist(k_values, bins = 100, color='mediumblue')
    plt.grid(True)
    plt.savefig(f'visualizations/histogram_k_{timestamp}.png')
    plt.show()

def boxplot_k(k_values):
    """
    generates a boxplot of k values.
    """
    plt.title('boxplot of k values', color = 'mediumblue')

    # all the properties of a box plot, costumizing the colors and with of properties
    plt.boxplot(k_values, patch_artist = True, medianprops = dict(color='mediumblue', linewidth = 2),
                    boxprops = dict(facecolor = 'gold', edgecolor = 'mediumblue', linewidth = 2),
                    whiskerprops = dict(color = 'mediumblue', linewidth = 2),
                    capprops = dict(color = 'mediumblue', linewidth = 2))
    plt.xlabel('k value', color = 'mediumblue')
    plt.grid(True)
    plt.savefig(f'visualizations/boxplot_k_{timestamp}.png')
    plt.show()

def plot_stations(stations_df, ax):
    """
    locates the train stations in Noord and Zuid Holland.
    """
    # point geometries from station coordinates
    geometry = [Point(xy) for xy in zip(stations_df['x'], stations_df['y'])]

    # geodataframe from the station df
    stations_gdf = gpd.GeoDataFrame(stations_df, geometry = geometry)

    # plot the stations
    stations_gdf.plot(ax = ax, color = 'mediumblue')

    for i, row in stations_gdf.iterrows():

        # for these three stations:
        if row['station'] in ['Rotterdam Centraal', 'Amsterdam Centraal', 'Amsterdam Amstel']:
            plt.annotate(text = row['station'], xy = (row['geometry'].x, row['geometry'].y),

                        # these are displayed to the left of the mark (to avoid overlap)
                         xytext = (5, 5), textcoords = 'offset points', ha = 'left')

        # Amsterdam Sloterdijk
        elif row['station'] == 'Amsterdam Sloterdijk':

            # should be displayed as 'Ams Sl' and to the left to avoid overlap
            plt.annotate(text = 'Ams Sl', xy = (row['geometry'].x, row['geometry'].y),
                         xytext = (5, 5), textcoords = 'offset points', ha = 'left')

        # the rest of the stations
        else:
            plt.annotate(text = row['station'], xy = (row['geometry'].x, row['geometry'].y),

                        # are displayed to the right of the mark
                         xytext = (-5, 5), textcoords = 'offset points', ha = 'right')
    return stations_gdf

def plot_connections(stations_file, connections_file, shape_file):
    """
    visualizes the stations and connections in Noord and Zuid Holland.
    """
    stations_df = pd.read_csv(stations_file)
    connections_df = pd.read_csv(connections_file)

    fig, ax = plt.subplots(figsize = (10, 10))

    # shapefile path
    world = gpd.read_file(shape_file)

    # filter for the Netherlands
    netherlands = world[world['NAME'] == 'Netherlands']
    netherlands.plot(ax = ax, color = 'lightgrey')

    # plot train stations
    stations_gdf = plot_stations(stations_df, ax)

    # geodf for connections
    connections = []
    for index, row in connections_df.iterrows():
        station1 = row['station1']
        station2 = row['station2']
        distance = row['distance']

        #coordinates for each station
        coordinates = [(stations_gdf.loc[stations_gdf['station'] == station1, 'geometry'].squeeze().x,
                        stations_gdf.loc[stations_gdf['station'] == station1, 'geometry'].squeeze().y),
                       (stations_gdf.loc[stations_gdf['station'] == station2, 'geometry'].squeeze().x,
                        stations_gdf.loc[stations_gdf['station'] == station2, 'geometry'].squeeze().y)]

        # linestring for each connection
        connections.append((LineString(coordinates), distance))

    # plot connections as red strings
    for line, distance in connections:
        gpd.GeoSeries([line]).plot(ax = ax, color = 'red')


    # if for all of the Netherlands
    if stations_file == "data/StationsNationaal.csv":
        plt.title('Train stations and connections in the Netherlands', color = 'mediumblue')
        ax.set_xlim(3.3, 7.25)
        ax.set_ylim(50.7, 53.6)

    # if only for Noord- and Zuid-Holland
    if stations_file == "data/StationsHolland.csv":
        ax.set_xlim(4.0, 5.1)
        plt.title('Train stations and connections in  Noord- and Zuid-Holland', color = 'mediumblue')
        ax.set_ylim(51.75, 53.1)

    plt.show()


def plot_routes(stations_file, connections_file, shape_file, routes):
    """
    visualizes the programmed routes in Noord and Zuid Holland.
    """
    stations_df = pd.read_csv(stations_file)

    fig, ax = plt.subplots(figsize=(10,10))

    # shapefile path
    world = gpd.read_file(shape_file)

    # filter for the Netherlands
    netherlands = world[world['NAME'] == 'Netherlands']
    netherlands.plot(ax = ax, color = 'lightgrey')

    # plot train stations
    stations_gdf = plot_stations(stations_df, ax)

    # plot routes
    for route_number, route in routes.items():
        route_coords = [(station.location[0], station.location[1]) for station in route.itinerary]
        route_line = LineString(route_coords)
        gpd.GeoSeries([route_line]).plot(ax = ax, color = 'red', linewidth = 3, alpha = 0.5)

    # if for all of the Netherlands
    if stations_file == "data/StationsNationaal.csv":
        plt.title('Programmed routes in the Netherlands', color = 'mediumblue')
        ax.set_xlim(3.3, 7.25)
        ax.set_ylim(50.7, 53.6)

    # if only for Noord- and Zuid-Holland
    if stations_file == "data/StationsHolland.csv":
        plt.title('Train stations and connections in Noord- and Zuid-Holland', color = 'mediumblue')
        ax.set_xlim(4.0, 5.1)
        ax.set_ylim(51.75, 53.1)

    # save image to folder
    plt.savefig(f'visualizations/route_visualization_{timestamp}.png')
    plt.tight_layout()
    plt.show()
