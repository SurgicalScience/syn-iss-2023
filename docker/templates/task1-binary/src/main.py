import sys

if len(sys.argv) != 3:
    raise(RuntimeError(f"Expected 2 arguments, was provided {len(sys.argv)-1} argument(s)."))

input_dir_path = sys.argv[1]
output_dir_path = sys.argv[2]

print("="*30)
print("Running binary segmentation:")
print(f"  Using images under {input_dir_path}")
print(f"  Storing predictions under {output_dir_path}")
print("="*30)

