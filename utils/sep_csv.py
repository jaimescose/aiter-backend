import pandas as pd

# Import .csv file
df = pd.read_csv(r'C:\Users\Juan\Downloads\csv\Villareal_Apple.csv', low_memory=False)

# Get unique values in the first column
unique_values = df.iloc[:, 0].unique()

# Loop through the unique values and create a new DataFrame for each
for value in unique_values:
    # Filter the DataFrame
    new_df = df[df.iloc[:, 0] == value]
    
    # Save each DataFrame to a new CSV file
    new_df.to_csv(f'{value}.csv', index=False)