from matplotlib import pyplot as plt
import pandas as pd
from shapely.geometry import Point, LineString
import geopandas as gpd

def visualize_station_percentage(graph):
    """
    visualizes the percentage of stations used in the route.
    """
    graph.route_percentages = {}

    for route_number, route in graph.route_dict.items():

        used_stations = len(set(route.itinerary))
        total_stations = len(graph.station_dict)
        unused_stations = total_stations - used_stations

        # calculate percentages
        percentage_used = (used_stations / total_stations) * 100
        percentage_unused = (unused_stations / total_stations) * 100
        graph.route_percentages[route_number] = {'used': percentage_used, 'unused': percentage_unused}

        # data for pie chart
        sizes = [used_stations, unused_stations]
        labels = ['Used', 'Unused']

        plt.figure(figsize=(7, 7))
        plt.pie(sizes, labels=labels, colors=['red', 'blue'], autopct='%1.1f%%')
        plt.title(f'Percentage of stations used in route {route_number}')
        plt.show()

def bar_k(k_values):
    """
    generates a bar chart of k values per attempt.
    """
    iterations = range(1, len(k_values) + 1)

    plt.title('k values per iteration')
    plt.xlabel('attempts')
    plt.ylabel('k value')
    plt.bar(iterations, k_values)
    plt.grid(True)
    plt.show()

def histogram_k(k_values):
    """
    generates a histogram visualizing the distribution of k values.
    """
    plt.title('frequency per k_value')
    plt.xlabel('k_value')
    plt.ylabel('frequency')
    plt.hist(k_values, bins = 10)
    plt.grid(True)
    plt.show()

def plot_stations(stations_df, ax):
    """
    locates the train stations in Noord and Zuid Holland.
    """
    geometry = [Point(xy) for xy in zip(stations_df['x'], stations_df['y'])]
    stations_gdf = gpd.GeoDataFrame(stations_df, geometry = geometry)
    stations_gdf.plot(ax = ax, color = 'blue')

    for i, row in stations_gdf.iterrows():
        if row['station'] in ['Rotterdam Centraal', 'Amsterdam Centraal', 'Amsterdam Amstel']:
            plt.annotate(text = row['station'], xy = (row['geometry'].x, row['geometry'].y),
                         xytext = (5, 5), textcoords = 'offset points', ha = 'left')
        elif row['station'] == 'Amsterdam Sloterdijk':
            plt.annotate(text = 'Ams Sl', xy = (row['geometry'].x, row['geometry'].y),
                         xytext = (5, 5), textcoords = 'offset points', ha = 'left')
        else:
            plt.annotate(text = row['station'], xy = (row['geometry'].x, row['geometry'].y),
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
    netherlands = world[world['NAME'] == 'Netherlands']
    netherlands.plot(ax = ax, color = 'grey')

    # plot train stations
    stations_gdf = plot_stations(stations_df, ax)

    # geodf for connections
    connections = []
    for index, row in connections_df.iterrows():
        station1 = row['station1']
        station2 = row['station2']
        distance = row['distance']

        coordinates = [(stations_gdf.loc[stations_gdf['station'] == station1, 'geometry'].squeeze().x,
                        stations_gdf.loc[stations_gdf['station'] == station1, 'geometry'].squeeze().y),
                       (stations_gdf.loc[stations_gdf['station'] == station2, 'geometry'].squeeze().x,
                        stations_gdf.loc[stations_gdf['station'] == station2, 'geometry'].squeeze().y)]
        connections.append((LineString(coordinates), distance))

    for line, distance in connections:
        gpd.GeoSeries([line]).plot(ax = ax, color = 'red')

    plt.title('Train stations and connections in Noord- and Zuid-Holland')
    ax.set_xlim(4.0, 5.1)
    ax.set_ylim(51.75, 53.1)
    plt.tight_layout()
    plt.show()


def plot_routes(stations_file, connections_file, shape_file, routes):
    """
    visualizes the programmed routes in Noord and Zuid Holland.
    """
    stations_df = pd.read_csv(stations_file)

    fig, ax = plt.subplots(figsize=(10, 10))

    # shapefile path
    world = gpd.read_file(shape_file)
    netherlands = world[world['NAME'] == 'Netherlands']
    netherlands.plot(ax = ax, color = 'grey')

    # plot train stations
    stations_gdf = plot_stations(stations_df, ax)

    # plot routes
    for route_number, route in routes.items():
        route_coords = [(station.location[0], station.location[1]) for station in route.itinerary]
        route_line = LineString(route_coords)
        gpd.GeoSeries([route_line]).plot(ax = ax, color = 'yellow', linewidth = 3, alpha = 0.5)

    plt.title('Programmed routes in Noord- and Zuid-Holland')
    ax.set_xlim(4.0, 5.1)
    ax.set_ylim(51.75, 53.1)
    plt.tight_layout()
    plt.show()
