import pandas as pd
from code.classes import graph
from code.algorithms import randomise




def main(input1, input2):

    # create a scenario
    scenario = Scenario(input1, input2)

    # add a route to scenario
    scenario.add_route("1")
    scenario.show_routes()

if __name__ == "__main__":
    # Set-up parsing command line arguments
    parser = argparse.ArgumentParser(description = "read both input file name")

    parser.add_argument("input1", help = "input file 1 (csv)")
    parser.add_argument("input2", help = "input file 2 (csv)")

    # Read arguments from command line
    args = parser.parse_args()

    main(args.input1, args.input2)
