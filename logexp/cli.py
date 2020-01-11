import argparse

from logexp.version import VERSION


def main():
    parser = argparse.ArgumentParser("logexp: simple logging tool for machine learning")
    parser.add_argument("--version", action="store_true")

    args = parser.parse_args()

    if args.version:
        print(VERSION)
