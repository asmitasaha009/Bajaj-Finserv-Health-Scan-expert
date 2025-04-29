import os
from main import extract_lab_tests

# This gets the current directory where run_extract.py is located
current_dir = os.path.dirname(__file__)

# If your report images are directly in lbmaske/, use current_dir
image_folder = current_dir

# Loop through all image files in lbmaske/
for filename in os.listdir(image_folder):
    if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
        file_path = os.path.join(image_folder, filename)
        with open(file_path, 'rb') as f:
            img_bytes = f.read()
            result = extract_lab_tests(img_bytes)
            print(f"Results for {filename}:\n", result)
            print("="*60)
