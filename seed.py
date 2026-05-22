import argparse
import random

def init_seed():
    """Initialize game seed."""
    #parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, default=None)
    args = parser.parse_args()

    #check if arg exists
    if args.seed is not None:
        seed = args.seed
    else:
        #if seed not given generate new one
        seed = random.randint(0, 10_000_000)
        print(f"No seed provided. Using seed: {seed}")

    #set seed
    random.seed(seed)
    print(f"Seed set to: {seed}")