import numpy as np
import pandas as pd
from sksurv.datasets import load_veterans_lung_cancer
from sksurv.nonparametric import kaplan_meier_estimator

# Load the dataset
data_x_raw, data_y_raw = load_veterans_lung_cancer()

# Convert to structured array with ('event', 'duration') format
data_y = np.array([
    (bool(status), time)
    for status, time in zip(data_y_raw["Status"], data_y_raw["Survival_in_days"])
], dtype=[('status', 'bool'), ('time', 'f8')])

# Add 'cell_type' as a categorical feature (grouping by cell type)
data_x_raw['cell_type'] = data_x_raw['cell_type'].astype(str)  # Convert to string for grouping

# Prepare the data frame to store survival curves by group
survival_data = []

# Loop through each group (e.g., different cell types)
for cell_type in data_x_raw['cell_type'].unique():
    # Filter data by cell type
    group_indices = data_x_raw[data_x_raw['cell_type'] == cell_type].index
    group_survival_time = data_y['time'][group_indices]
    group_status = data_y['status'][group_indices]
    
    # Compute Kaplan-Meier for this group
    time_km, prob_km = kaplan_meier_estimator(group_status, group_survival_time)
    
    # Store results in the list
    survival_data.append({
        'cell_type': cell_type,
        'time': time_km,
        'survival_prob': prob_km
    })

# Now we have survival data for each cell type
# Convert the data into a DataFrame format
survival_df = pd.DataFrame(columns=["cell_type", "time", "survival_prob"])

for group in survival_data:
    for time, prob in zip(group['time'], group['survival_prob']):
        survival_df = survival_df.append({
            "cell_type": group['cell_type'],
            "time": time,
            "survival_prob": prob
        }, ignore_index=True)

# Save the DataFrame to a CSV file
survival_df.to_csv("survival_curve_by_group.csv", index=False)
print("Saved survival_curve_by_group.csv")