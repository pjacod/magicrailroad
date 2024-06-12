import pandas as pd
import argparse
from code.classes import graph
from code.visualize import visualize as vis
from code.algorithms import randomise


def main(input1, input2, output_file, iterations):

    lst_costs = []

    for solution in range(iterations):
        # create a scenario
        test_graph = graph.Graph(input1, input2)

        # add a route to scenario
        test_graph.add_routes(7)

        # use randomise to choose itinerary for route
        randomise.random_routes(test_graph.route_dict)

        # calculate cost of traject
        lst_costs.append(test_graph.calculate_k())

    vis.histogram_k(lst_costs)

    vis.visualize_station_percentage(test_graph)
    test_graph.show_routes()
    test_graph.write_output(output_file)

if __name__ == "__main__":
    # Set-up parsing command line arguments
    parser = argparse.ArgumentParser(description = "read both input file name and writes to output file")

    parser.add_argument("input1", help = "input file 1 (csv)")
    parser.add_argument("input2", help = "input file 2 (csv)")
    parser.add_argument("output_file", help="output file (csv)")

    # Read arguments from command line
    args = parser.parse_args()

    main(args.input1, args.input2, args.output_file, 10)
