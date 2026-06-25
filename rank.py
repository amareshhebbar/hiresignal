#!/usr/bin/env python3
import argparse
from src import run

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--candidates", required=True)
    parser.add_argument("--out", required=True)
    args = parser.parse_args()
    run(args.candidates, args.out)
