import argparse
import random

def init_seed():
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, default=None)
    args = parser.parse_args()

    if args.seed is not None:
        seed = args.seed
    else:
        seed = random.randint(0, 10_000_000)
        print(f"No seed provided. Using seed: {seed}")

    random.seed(seed)
    print(f"Seed set to: {seed}")