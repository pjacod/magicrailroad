import pandas as pd
import argparse
from code.visualize import visualize as vis
from code.algorithms import main_loop


def main(input1, input2, output_file, iterations):

    # perform  iterations and get k-values and graph
    lst_k_values, test_graph = main_loop.main_loop(input1, input2, iterations)

    vis.bar_k(lst_k_values)
    vis.histogram_k(lst_k_values)
    vis.visualize_station_percentage(test_graph)
    vis.plot_connections(input1, input2, 'data/ne_10m_admin_0_countries/ne_10m_admin_0_countries.shp')
    vis.plot_routes(input1, input2, 'data/ne_10m_admin_0_countries/ne_10m_admin_0_countries.shp', test_graph.route_dict)
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
