import pandas as pd
import argparse
from code.classes import graph
from code.algorithms import dijkstra
from code.visualize import visualize as vis


def main(input1, input2):
    test_graph = graph.Graph(input1, input2)

    weights = [1, 100]
    test_dijkstra = dijkstra.Dijkstra(test_graph, 300, 20, weights)
    test_dijkstra.run_dijkstra()

    vis.plot_connections(input1, input2, 'data/ne_10m_admin_0_countries/ne_10m_admin_0_countries.shp')
    vis.plot_routes(input1, input2, 'data/ne_10m_admin_0_countries/ne_10m_admin_0_countries.shp', test_dijkstra.graph.route_dict)


if __name__ == "__main__":

        # Set-up parsing command line arguments
        parser = argparse.ArgumentParser(description = "read both input file name and writes to output file")

        parser.add_argument("input1", help = "input file 1 (csv)")
        parser.add_argument("input2", help = "input file 2 (csv)")


        # Read arguments from command line
        args = parser.parse_args()

        main(args.input1, args.input2)
