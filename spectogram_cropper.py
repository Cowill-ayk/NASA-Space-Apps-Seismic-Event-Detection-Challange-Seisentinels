import os
import pandas as pd
from PIL import Image
from datetime import datetime, timedelta

# Function to crop the images in the specified folder
def crop_images_in_folder(input_folder, output_folder, csv_file):
    # Load the CSV file into a DataFrame
    events_df = pd.read_csv(csv_file)

    # Create output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)

    # Get the start time of the day from the first row of the DataFrame
    day_start_time = datetime.strptime(events_df['time_abs(%Y-%m-%dT%H:%M:%S.%f)'].iloc[0], '%Y-%m-%dT%H:%M:%S.%f')
    day_end_time = day_start_time + timedelta(days=1)

    # Calculate total seconds in a day
    total_seconds_in_day = 86400

    # Define time segments
    time_segments = [day_start_time + timedelta(seconds=(i * total_seconds_in_day / 10)) for i in range(11)]

    # Process each image in the input folder
    for image_name in os.listdir(input_folder):
        # Construct full image path
        image_path = os.path.join(input_folder, image_name)

        # Check if it is an image file
        if image_path.lower().endswith(('.png', '.jpg', '.jpeg')):
            # Load the image
            img = Image.open(image_path)
            width, height = img.size
            
            # Initialize parameters
            crop_size = 224
            overlap = 5
            crops = []
            labels = [0] * 10  # Initialize labels for 10 segments
            
            # Calculate the number of crops
            x = 0
            
            while x + crop_size <= width:
                # Define the crop area
                box = (x, 0, x + crop_size, crop_size)
                crop = img.crop(box)
                crops.append(crop)

                # Determine the time of the current crop
                crop_time = day_start_time + timedelta(seconds=(x / width) * total_seconds_in_day)

                # Determine the label based on whether the crop time is within an event
                for index, row in events_df.iterrows():
                    event_time = datetime.strptime(row['time_abs(%Y-%m-%dT%H:%M:%S.%f)'], '%Y-%m-%dT%H:%M:%S.%f')
                    
                    # Check which segment the event time falls into
                    segment_index = int((event_time - day_start_time).total_seconds() // (total_seconds_in_day / 10))

                    # Ensure the segment index is within the bounds (0 to 9)
                    if 0 <= segment_index < 10:
                        # If the current crop time falls within the segment's time range
                        if time_segments[segment_index] <= crop_time < time_segments[segment_index + 1]:
                            labels[segment_index] = 1  # Label the corresponding segment as 1
                            break

                # Move the x coordinate for the next crop
                x += crop_size - overlap

            # Save crops and labels
            for i, crop in enumerate(crops):
                crop.save(os.path.join(output_folder, f"{os.path.splitext(image_name)[0]}_crop_{i + 1}.png"))

            # Save labels to a text file named after the image
            label_file = os.path.join(output_folder, f"{os.path.splitext(image_name)[0]}_labels.txt")
            with open(label_file, "w") as f:
                for label in labels:
                    f.write(f"{label}\n")

# Usage
input_folder = r"space_apps_2024_seismic_detection\data\lunar\test\data\S16_GradeBspec"  # Replace with your image folder path
output_folder = r"space_apps_2024_seismic_detection\data\lunar\test\data\S16_GradeBspecCrop"  # Replace with your output folder path
csv_file = "space_apps_2024_seismic_detection/data/lunar/training/catalogs/apollo12_catalog_GradeA_final.csv"  # Replace with the path to your CSV file

crop_images_in_folder(input_folder, output_folder, csv_file)
