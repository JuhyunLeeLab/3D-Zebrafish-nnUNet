# Our Proprietary Tiff converter file 

import numpy as np
from PIL import Image
import tifffile as tiff
import os

# Define the input and output folder paths
input_folder = '/media/lee/ZebrafishDisk1/zebrafish_seg_2/zebrafish_seg/data/preprocessed/Dataset777_zebrafish_segv2/nnUNetPlans_3d_fullres'
output_folder = '/media/lee/ZebrafishDisk1/zebrafish_seg_2/zebrafish_seg/data/tiff_preprocessed/day04_new'

# Create the output folder if it doesn't exist
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Loop through all the .npz files in the input folder
for filename in os.listdir(input_folder):
    if filename.endswith('.npz'):
        # Construct full file paths
        npz_file = os.path.join(input_folder, filename)
        output_file = os.path.join(output_folder, filename.replace('.npz', '.tiff'))

        # Load the .npz file
        data = np.load(npz_file)

        # Extract image data (assume 'data' key stores image)
        image_array = data['data']

        # If 3D or 4D, save as a multi-page TIFF, or extract a 2D slice for a single image
        if image_array.ndim == 4:  # Assuming 4D (channels, z, y, x)
            image_slice = image_array[0, 0, :, :]  # Select first channel and slice (example)
        elif image_array.ndim == 3:  # Assuming 3D (z, y, x)
            image_slice = image_array[0, :, :]  # Select first slice (example)
        else:
            image_slice = image_array  # If already 2D

        # Save as TIFF using tifffile (multi-page TIFF for 3D data)
        if image_array.ndim > 2:
            tiff.imwrite(output_file, image_array.astype(np.uint8))  # Cast to uint8 if needed
        #    print(f"Converted {filename} to {output_file}")

print("Conversion completed for all .npz files.")
