import argparse
import os
import json
import glob
import sys

def create_md():
    with open("info.json", "r") as file:
        info = json.load(file)
    text = []
    text.append(f"# {info['kind']} model")
    text.append(info["description"])
    text.append(info["detailed_description"])
    text.append(f"Run in {info['date']} at {info['time']}")
    text.append("# Examples")
    examples = glob.glob("./examples/image*")
    for i in range(5):
        try:
            text.append(f"![alt text]({examples[i]})")
        except:
            break
    
    with open("README.md", "w") as file:
        for txt in text:
            file.write(txt + "\n")

def run_experiment_parser():
    parser = argparse.ArgumentParser(description='Experiment command line interface.')
    parser.add_argument('command', type=str, help="Command to run. Can be 'md' or 'experiment'.")
    args = parser.parse_args()
    if args.command == 'md':
        create_md()
    elif args.command == 'experiment':
        os.system("python experiment.py")
    return parser

