import os
import pandas as pd
from obspy import read
from tqdm import tqdm

def generate_event_times_csv(mseed_dir, output_csv):
    """
    Generate a CSV file with the midpoint of each MSEED file as the event time.

    Parameters:
    mseed_dir (str): Directory containing MSEED files
    output_csv (str): Path to save the CSV file
    """
    event_data = []

    # Iterate over each file in the directory
    for mseed_file in tqdm(os.listdir(mseed_dir)):
        if mseed_file.endswith('.mseed'):
            try:
                # Read the MSEED file
                st = read(os.path.join(mseed_dir, mseed_file))
                tr = st[0]
                
                # Calculate the midpoint of the trace
                n_samples = len(tr.data)
                midpoint = n_samples / 2
                event_time = midpoint / tr.stats.sampling_rate  # Convert sample index to time in seconds
                
                # Append to the event data
                event_data.append({'filename': mseed_file, 'event_time': event_time})
            
            except Exception as e:
                print(f"Error processing {mseed_file}: {str(e)}")

    # Create a DataFrame and save it as a CSV
    event_df = pd.DataFrame(event_data)
    event_df.to_csv(output_csv, index=False)

    print(f"Event times CSV saved to {output_csv}")

# Example usage:
mseed_dir = 'pyweed_new'
output_csv = 'event_times.csv'

generate_event_times_csv(mseed_dir, output_csv)
