import os
from PIL import Image

# Function to crop the images in the specified folder
def crop_images_in_folder(input_folder, output_folder):
    # Create output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)
    
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
            labels = []
            
            # Calculate the number of crops
            x = 0
            crop_index = 0
            
            while x + crop_size <= width:
                # Define the crop area
                box = (x, 0, x + crop_size, crop_size)
                crop = img.crop(box)
                crops.append(crop)

                # Determine the label
                if crop_index == 4 or crop_index == 5:  # 5th and 6th crops
                    labels.append(1)
                else:
                    labels.append(0)

                # Move the x coordinate for the next crop
                x += crop_size - overlap
                crop_index += 1

            # Save crops and labels
            for i, crop in enumerate(crops):
                crop.save(os.path.join(output_folder, f"{os.path.splitext(image_name)[0]}_crop_{i + 1}.png"))

            # Save labels to a text file named after the image
            label_file = os.path.join(output_folder, f"{os.path.splitext(image_name)[0]}_labels.txt")
            with open(label_file, "w") as f:
                for label in labels:
                    f.write(f"{label}\n")

# Usage
input_folder = "Earh_Spectograms_japan/"  # Replace with your image folder path
output_folder = "augment/"  # Replace with your output folder path

crop_images_in_folder(input_folder, output_folder)
