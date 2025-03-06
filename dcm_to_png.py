import os
import pydicom
import numpy as np
from PIL import Image
import shutil  # Optional: For copying non-DICOM files if needed

def convert_dcm_to_png(dcm_file, output_file):
    # Read the DICOM file
    ds = pydicom.dcmread(dcm_file)
    
    # Access the pixel array and convert to float for normalization
    image = ds.pixel_array.astype(np.float32)
    
    # Normalize the pixel values to 0-255
    image -= np.min(image)
    if np.max(image) != 0:  # Avoid division by zero
        image /= np.max(image)
    image *= 255.0
    
    # Convert to uint8
    image = image.astype(np.uint8)
    
    # Save using PIL
    im = Image.fromarray(image)
    im.save(output_file)

def process_directory(input_directory, output_directory, copy_non_dcm=False):
    """
    Traverse the input_directory tree and convert all .dcm files to .png in the output_directory,
    preserving the same directory structure.
    If copy_non_dcm is True, other files will be copied to the corresponding output location.
    """
    for root, dirs, files in os.walk(input_directory):
        # Determine the relative directory path from the input_directory
        relative_path = os.path.relpath(root, input_directory)
        target_dir = os.path.join(output_directory, relative_path)
        os.makedirs(target_dir, exist_ok=True)

        for file in files:
            input_file_path = os.path.join(root, file)
            
            # Check for DICOM files
            if file.lower().endswith('.dcm'):
                output_file_name = file.replace('.dcm', '.png')
                output_file_path = os.path.join(target_dir, output_file_name)
                try:
                    convert_dcm_to_png(input_file_path, output_file_path)
                    print(f"Converted {input_file_path} to {output_file_path}")
                except Exception as e:
                    print(f"Failed to convert {input_file_path}: {e}")
            elif copy_non_dcm:
                # Optionally, copy non-DICOM files (like metadata or other necessary files)
                shutil.copy2(input_file_path, target_dir)
                print(f"Copied {input_file_path} to {target_dir}")

input_directory = './manifest-1741257512125'      
output_directory = './converted'      


os.makedirs(output_directory, exist_ok=True)

process_directory(input_directory, output_directory, copy_non_dcm=False)
