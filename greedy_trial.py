import pandas as pd
import argparse
from code.classes import graph
from code.algorithms import greedy
from code.visualize import visualize as vis

def loop_greedy(input1, input2, iterations):
    lst_k_values = []
    for solution in range(iterations):
        # create a scenario
        test_graph = graph.Graph(input1, input2)

        weights = [1, 100]

        # see Dijkstra class for all parameters
        test_greedy = greedy.Greedy(test_graph, weights, 4)
        k = test_greedy.run_greedy()

        lst_k_values.append(k)
        if k >= max(lst_k_values):
            best_graph = test_greedy.graph

        if solution % 100 == 0:
            print(f'this is iteration: {solution}')

    return best_graph, lst_k_values


def main(input1, input2, iterations):
    best_graph, lst_k_values = loop_greedy(input1, input2, iterations)

    vis.bar_k(lst_k_values)
    vis.histogram_k(lst_k_values)
    vis.plot_connections(input1, input2, 'data/ne_10m_admin_0_countries/ne_10m_admin_0_countries.shp')
    vis.plot_routes(input1, input2, 'data/ne_10m_admin_0_countries/ne_10m_admin_0_countries.shp', best_graph.route_dict)
    best_graph.show_routes()

    print(max(lst_k_values))


if __name__ == "__main__":

        # Set-up parsing command line arguments
        parser = argparse.ArgumentParser(description = "read both input file name and writes to output file")

        parser.add_argument("input1", help = "input file 1 (csv)")
        parser.add_argument("input2", help = "input file 2 (csv)")


        # Read arguments from command line
        args = parser.parse_args()

        main(args.input1, args.input2, 1000)
