import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


# Create an empty DataFrame to store the cloud coverage data


def plot_cloud(lat, long, all_data, image_dir, town, selected_years=np.arange(2020, 2024), selected_days=[8,9]):

    cloud_coverage_data = pd.DataFrame(columns=['Year', 'Day', 'Hour', 'Cloud Cover'])



    # Iterate over the selected years and days
    for year in selected_years:
        for day in selected_days:
            # Filter the data for the selected year and day
            selected_data = all_data[((all_data['date'].dt.year == year) & (all_data['date'].dt.day == day))]
            
            # Append the cloud coverage data to the DataFrame
            cloud_coverage_data = cloud_coverage_data.append(selected_data[['date', 'cloud_cover']].rename(columns={'date': 'Hour', 'cloud_cover': 'Cloud Cover'}))
            
    # Reset the index of the DataFrame
    cloud_coverage_data.reset_index(drop=True, inplace=True)


    # Group the data by year
    grouped_data = cloud_coverage_data.groupby(cloud_coverage_data['Hour'].dt.year)

    fig = plt.figure(figsize=(12, 6))

    for year, group in grouped_data:
        x = group['Hour'].dt.strftime('%d:%Hh')  # Format the x-axis as day:hour
        plt.plot(x, group['Cloud Cover'], label=str(year))

    plt.xlabel('Day and Hour')
    plt.ylabel('Cloud Cover')
    plt.legend(bbox_to_anchor=(1.01, 1), loc=2, borderaxespad=0.)
    # Rotate the x-axis labels by 90 degrees
    plt.xticks(rotation=90)

    # Get the x values for the shaded area
    x_values = grouped_data.get_group(2022)['Hour'].dt.strftime('%d:%Hh')

    # Set the start and end indices for the shaded area
    start_index = x_values.tolist().index('0%s:12h'%selected_days[0])
    end_index = x_values.tolist().index('0%s:16h'%selected_days[0])

    # Shade the area between the start and end indices
    plt.fill_between(x_values[start_index:end_index+1], 0, 100, alpha=0.3)

    # Add latitude and longitude to the plot
    plt.text(0.9, 0.95, f'Latitude: {lat:.2f}, Longitude: {long:.2f}', transform=plt.gca().transAxes, ha='right')
    plt.text(0.9, 0.95, f'Latitude: {lat:.2f}, Longitude: {long:.2f}', transform=plt.gca().transAxes, ha='right')

    # Draw a rectangle around the latitude and longitude
    #rect = plt.Rectangle((0.98, 0.009), 0., 0.03, fill=False, edgecolor='red', linewidth=2)
    #plt.Rectangle
    #plt.gca().add_patch(rect)
    fig.savefig(image_dir + '/cloud-cover-%s.png'%town,
            dpi=600,format='png',bbox_inches='tight')
    plt.show()

