import argparse


def get_args(override_args=None):
    parser = argparse.ArgumentParser(description="Plan your trip places.")

    parser.add_argument('--add', help='Add a new place', action="store_true")
    parser.add_argument('--correct', action='store_true',
        help="Correct the information of a location. Defaults to the last one added if --id is not provided.")
    parser.add_argument('--create-map', action='store_true',
        help="Generate an interactive map with all locations.")
    parser.add_argument('--id', type=int, default=None,
        help="ID of the location to correct when using --correct.")
    parser.add_argument('--list', help='List all places', action="store_true")
    parser.add_argument('--name', help='Name of the place', type=str)

    if override_args is None:
        return parser.parse_args()
    return parser.parse_args(override_args)
