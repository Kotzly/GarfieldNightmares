import argparse

def run_experiment_parser():
    parser = argparse.ArgumentParser(description='Experiment command line interface.')
    parser.add_argument('command', type=str, help="Command to run. Can be 'md' or 'experiment'.")
    return parser
