import os
import pickle
import pandas as pd
import numpy as np

def load_dataset_files(dataset_path):
    """Loads dataset files from the given path into a structured dictionary."""
    dataset = {}
    keys_file = os.path.join(dataset_path, 'keys.txt')
    plaintexts_file = os.path.join(dataset_path, 'plaintexts.txt')

    # Check if keys exist and load them
    if os.path.exists(keys_file):
        try:
            dataset['keys'] = pd.read_csv(keys_file, header=None, sep=r"\s+")
        except Exception as e:
            print(f"Error loading keys file: {e}")
    else:
        print(f"Warning: Keys file not found in {dataset_path}")

    # Load plaintexts
    if os.path.exists(plaintexts_file):
        try:
            dataset['plaintexts'] = pd.read_csv(plaintexts_file, header=None, sep=r"\s+")
        except Exception as e:
            print(f"Error loading plaintexts file: {e}")
    else:
        print(f"Warning: Plaintexts file not found in {dataset_path}")

    # Load all traces (trace_0.txt, trace_1.txt, ...)
    dataset['traces'] = {}
    for file in os.listdir(dataset_path):
        if file.startswith('trace_') and file.endswith('.txt'):
            trace_id = file.split('.')[0]
            try:
                dataset['traces'][trace_id] = pd.read_csv(os.path.join(dataset_path, file), header=None, sep=r"\s+")
            except Exception as e:
                print(f"Error loading trace file {file}: {e}")

    return dataset


def load_dataset_files_with_cache(dataset_path, cache_path=f"../datasets/cache/dataset_cache.pkl"):
    """Loads dataset files with caching to avoid reloading every time."""
    # Check if cache exists
    print(f"Checking for cache at: {cache_path}")
    if os.path.exists(cache_path):
        print(f"Loading datasets from cache: {cache_path}")
        with open(cache_path, "rb") as cache_file:
            return pickle.load(cache_file)

    # If cache doesn't exist, load datasets from files
    print("Cache not found. Loading datasets from files...")
    dataset = load_dataset_files(dataset_path)

    # Save to cache
    with open(cache_path, "wb") as cache_file:
        pickle.dump(dataset, cache_file)
        print(f"Datasets cached to: {cache_path}")

    return dataset


def clear_cache(cache_path="{DATASETS_PATH}/cache/dataset_cache.pkl"):
    """Clears the dataset cache."""
    if os.path.exists(cache_path):
        os.remove(cache_path)
        print(f"Cache cleared: {cache_path}")
    else:
        print(f"No cache found at: {cache_path}")


def get_trace_matrix(dataset):
    """
    Converts trace dict into a matrix (n_traces x n_samples).
    Assumes trace keys are like 'trace_0', 'trace_1', ...
    """
    trace_keys = sorted(dataset['traces'].keys(), key=lambda x: int(x.split('_')[1]))
    trace_list = [dataset['traces'][k].values.flatten() for k in trace_keys]
    return np.vstack(trace_list)