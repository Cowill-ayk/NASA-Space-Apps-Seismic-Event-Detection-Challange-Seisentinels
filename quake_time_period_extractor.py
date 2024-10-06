import pandas as pd
from datetime import datetime

# Load the CSV file
csv_file = r'space_apps_2024_seismic_detection\data\lunar\training\catalogs\apollo12_catalog_GradeA_final.csv'
df = pd.read_csv(csv_file)

# Rename the column for easier access
df.rename(columns={'time_abs(%Y-%m-%dT%H:%M:%S.%f)': 'time_abs'}, inplace=True)

# Function to determine which of the 10 divisions (2.4 hours each) the time falls into
def find_time_segment(time_str):
    time_obj = datetime.strptime(time_str, '%Y-%m-%dT%H:%M:%S.%f')
    seconds_since_midnight = time_obj.hour * 3600 + time_obj.minute * 60 + time_obj.second
    segment_size = 8640  # 2.4 hours = 8640 seconds
    segment = seconds_since_midnight // segment_size
    return (int(segment) + 1)

# Apply the function to the renamed 'time_abs' column
df['segment'] = df['time_abs'].apply(find_time_segment)

# Print the resulting dataframe
print(df)

# Save the output with the new 'segment' column
output_csv = 'time_periods.csv'
df.to_csv(output_csv, index=False)
