import sys
import os
import glob
from os.path import join as osjoin
import csv

if len(sys.argv) != 4:
    raise(RuntimeError(f"Expected 3 arguments, was provided {len(sys.argv)-1} argument(s)."))

test_csv_path = sys.argv[1]
input_dir_path = sys.argv[2]
output_dir_path = sys.argv[3]

print("="*30)
print("Running binary segmentation:")
print(f"  For IDs listed in {test_csv_path}")
print(f"  Using images under {input_dir_path}")
print(f"  Storing predictions under {output_dir_path}")
print("="*30)

# check csv file
if not os.path.exists(test_csv_path):
    raise(FileNotFoundError(f"Could not find csv file: {test_csv_path}"))

# check folders
if not os.path.exists(input_dir_path):
    raise(NotADirectoryError(f"Could not find directory: {input_dir_path}"))

if not os.path.exists(output_dir_path):
    os.makedirs(output_dir_path)

