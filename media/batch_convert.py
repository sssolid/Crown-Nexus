#!/usr/bin/env python3
import os
from PIL import Image

def convert_webp_to_png(source_dir, output_dir):
    """
    Converts all .webp images in the source_dir to .png format and saves them in output_dir.
    """
    # Create the output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Process each file in the source directory
    for filename in os.listdir(source_dir):
        if filename.lower().endswith(".webp"):
            input_path = os.path.join(source_dir, filename)
            output_filename = os.path.splitext(filename)[0] + ".png"
            output_path = os.path.join(output_dir, output_filename)

            try:
                # Open the image and save it in PNG format
                with Image.open(input_path) as img:
                    img.save(output_path, "PNG")
                print(f"Converted {filename} to {output_filename}")
            except Exception as e:
                print(f"Error converting {filename}: {e}")

if __name__ == "__main__":
    # Specify the source directory containing .webp images
    source_directory = "."  # Change this path as needed
    # Specify the output directory where .png images will be saved
    output_directory = "png"   # Change this path as needed

    convert_webp_to_png(source_directory, output_directory)
