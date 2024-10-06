import os
import glob

def erase_txt_files(folder_path):
    # Get all .txt files in the folder
    txt_files = glob.glob(os.path.join(folder_path, "*.txt"))
    
    # Loop through and remove each file
    for file_path in txt_files:
        try:
            os.remove(file_path)
            print(f"Deleted: {file_path}")
        except Exception as e:
            print(f"Error deleting {file_path}: {e}")

# Example usage
folder_path = 'lunar_augment/'  # Replace with the folder you want to erase .txt files from
erase_txt_files(folder_path)
