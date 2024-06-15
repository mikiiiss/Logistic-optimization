import pandas as pd

# Read in the order and trip dataframes
order_df = pd.read_csv('Notebook/request.csv')
trip_df = pd.read_csv('Notebook/speed.csv')

# Merge the order and trip dataframes on 'order_id' and 'Trip ID'
merged_df = pd.merge(order_df, trip_df, left_on='order_id', right_on='Trip ID')

# Group the merged dataframe by 'order_id' and calculate the trip information
grouped_df = merged_df.groupby('order_id').agg({
    'Trip Origin': 'first',
    'Trip Destination': 'first',
    'Weekday': 'first',
    'Trip_Start_Date': 'first',
    'Holiday': 'first',
    'rain': 'first',
    'Distance': 'first',
    'Speed': 'first'
})

# Reset the index to get a column for 'order_id'
grouped_df = grouped_df.reset_index()

# Rename the columns to match the original order.csv dataframe
grouped_df = grouped_df.rename(columns={
    'Trip Origin': 'trip_origin',
    'Trip Destination': 'trip_destination',
    'Weekday': 'weekday',
    'Trip_Start_Date': 'trip_start_date',
    'Holiday': 'holiday',
    'rain': 'rain',
    'Distance': 'distance',
    'Speed': 'speed'
})

# Merge the original order dataframe with the grouped dataframe on 'order_id'
result_df = pd.merge(order_df, grouped_df, on='order_id', how='left')

# Save the resulting dataframe to a new CSV file
result_df.to_csv('merged_result.csv', index=False)

# Select the columns from the original order dataframe that you want to keep
order_df = order_df[['id', 'order_id', 'driver_id', 'driver_action', 'lat', 'lng']]

# Concatenate the original order dataframe with the new columns
order_df = pd.concat([order_df.iloc[:, :6], grouped_df], axis=1)

# Save the updated dataframe to a new CSV file
order_df.to_csv('order_with_trip_info.csv', index=False)