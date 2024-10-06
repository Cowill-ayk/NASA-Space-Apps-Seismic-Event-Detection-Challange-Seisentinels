import os
import pandas as pd
from PIL import Image
from datetime import datetime, timedelta

# Function to handle date parsing with or without microseconds
def parse_time_abs(time_str):
    try:
        # Try to parse with microseconds first
        return datetime.strptime(time_str, '%Y-%m-%dT%H:%M:%S.%f')
    except ValueError:
        # If that fails, parse without microseconds
        return datetime.strptime(time_str, '%Y-%m-%dT%H:%M:%S')

# Function to extract hour and minute from the raw time
def extract_hour_minute(rel_time_str):
    try:
        dt = datetime.strptime(rel_time_str, '%Y-%m-%dT%H:%M:%S.%f')
        return dt.hour, dt.minute
    except ValueError:
        return None, None  # Handle parsing errors

# Function to crop the images in the specified folder
def crop_images_in_folder(input_folder, output_folder, csv_file):
    # Load the CSV file into a DataFrame
    events_df = pd.read_csv(csv_file)

    # Create output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)

    # Ensure 'time_abs(%Y-%m-%dT%H:%M:%S.%f)' column exists
    time_column_name = 'time_abs(%Y-%m-%dT%H:%M:%S.%f)'
    if time_column_name not in events_df.columns:
        raise ValueError(f"Column '{time_column_name}' not found in the CSV file.")

    # Parse the start time of the day from the first event in the CSV
    day_start_time = parse_time_abs(events_df[time_column_name].iloc[0])
    day_end_time = day_start_time + timedelta(days=1)

    # Define total seconds in a day and segment duration
    total_seconds_in_day = 86400
    segment_duration = total_seconds_in_day / 10  # Each segment is 2.4 hours

    # Calculate the time segments
    time_segments = [day_start_time + timedelta(seconds=i * segment_duration) for i in range(11)]

    # Print time segments for debugging
    print("Time Segments:")
    for i, segment in enumerate(time_segments[:-1]):
        print(f"Segment {i}: {segment} to {time_segments[i + 1]}")

    # Process each image in the input folder
    for image_name in os.listdir(input_folder):
        image_path = os.path.join(input_folder, image_name)

        if image_path.lower().endswith(('.png', '.jpg', '.jpeg')):
            img = Image.open(image_path)
            width, height = img.size
            crop_size = 224
            overlap = 5
            crops = []
            labels = []

            x = 0
            while x + crop_size <= width:
                box = (x, 0, x + crop_size, crop_size)
                crop = img.crop(box)
                crops.append(crop)

                # Determine the time corresponding to the current crop
                crop_time = day_start_time + timedelta(seconds=(x / width) * total_seconds_in_day)
                crop_label = 0  # Default label

                # Print crop time for debugging
                print(f"Crop Time: {crop_time}")

                # Check which segment the crop falls into
                for segment_index in range(len(time_segments) - 1):
                    if time_segments[segment_index] <= crop_time < time_segments[segment_index + 1]:
                        # Print segment match
                        print(f"Crop Time {crop_time} falls into Segment {segment_index}")

                        for _, row in events_df.iterrows():
                            event_time = parse_time_abs(row[time_column_name])
                            event_segment_index = int((event_time - day_start_time).total_seconds() // segment_duration)

                            # Print event time and segment
                            print(f"Event Time: {event_time}, Segment Index: {event_segment_index}")

                            # Label this crop if the event falls into the same segment
                            if event_segment_index == segment_index:
                                crop_label = 1
                                print(f"Labeling crop as 1 due to event at {event_time}")
                                break

                        break  # Break after finding the correct segment

                x += crop_size - overlap

                # Save the crops and labels
                crop.save(os.path.join(output_folder, f"{os.path.splitext(image_name)[0]}_crop_{len(crops)}.png"))
                labels.append(crop_label)

            # Save labels to a text file named after the image
            label_file = os.path.join(output_folder, f"{os.path.splitext(image_name)[0]}_labels.txt")
            with open(label_file, "w") as f:
                for label in labels:
                    f.write(f"{segment_index}\n")

# Usage example
input_folder = "space_apps_2024_seismic_detection/data/lunar/training/spectrograms"  # Replace with your folder
output_folder = "lunar_augment/"  # Replace with your output folder
csv_file = "space_apps_2024_seismic_detection/data/lunar/training/catalogs/apollo12_catalog_GradeA_final.csv"

crop_images_in_folder(input_folder, output_folder, csv_file)
