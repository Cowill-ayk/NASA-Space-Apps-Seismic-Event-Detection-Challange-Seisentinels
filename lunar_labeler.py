import os
import pandas as pd

# Folder containing your images
image_folder = 'lunar_augment/'  # Replace with your image folder path

# Load the CSV file with filename and segment information
csv_file = r'time_periods.csv'
df = pd.read_csv(csv_file)

# Rename the 'time_abs' column if needed
df.rename(columns={'time_abs(%Y-%m-%dT%H:%M:%S.%f)': 'time_abs'}, inplace=True)

# Loop through each row in the CSV file
for index, row in df.iterrows():
    filename = row['filename']  # The base filename
    segment = row['segment']  # Segment number

    # Loop through 10 image files corresponding to each filename
    for i in range(1, 11):
        old_filename = f"{filename}_colored_spectrogram_crop_{i}.png"
        old_file_path = os.path.join(image_folder, old_filename)

        # Check if the file exists
        if os.path.exists(old_file_path):
            # If the current file is the one for the segment, rename it
            if i == segment:
                new_filename = f"{filename}_colored_spectrogram_crop_{i}EVENT.png"
                new_file_path = os.path.join(image_folder, new_filename)
                os.rename(old_file_path, new_file_path)
                print(f"Renamed: {old_filename} -> {new_filename}")
        else:
            print(f"File not found: {old_filename}")
