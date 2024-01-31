import os
import re

# Set the path to the directory containing the files
directory_path = "D:\\Work\\Supercloud\\RBC_shear_flow\\espresso\\supercloud_runs\\stretching\\original_params\\output\\vtk\\sim34_0.00723404255319149vtk"

# List all files in the directory
files = os.listdir(directory_path)

# Define the pattern to match the original filenames
pattern = re.compile(r'stretch(\d+)\.vtk')

# Rename files
for index, file in enumerate(files):
    match = pattern.match(file)
    if match:
        # Extract the number from the original filename
        number = match.group(1)

        # Construct the new filename
        new_filename = f'stretch{index}.vtk'

        # Rename the file
        old_path = os.path.join(directory_path, file)
        new_path = os.path.join(directory_path, new_filename)
        os.rename(old_path, new_path)

print("Files renamed successfully.")
