import matplotlib.pyplot as plt
import requests

def plot_traffic_congestion(date, area_id):
    api_url = f"http://127.0.0.1:9090/traffic/days/{date}/id/{area_id}"

    # Parsing JSON data
    response = requests.get(api_url)
    response.raise_for_status()  # Check response status
    traffic_data = response.json()  # Get JSON data directly

    # Extracting time and congestion data
    times = [entry["Time"].split()[1][:5] for entry in traffic_data]
    congestion = [entry["average_congestion_per_hour"] for entry in traffic_data]

    # Plotting the line chart
    plt.figure(figsize=(10, 6))
    plt.plot(times, congestion, marker='o', linestyle='-', color='b')

    # Adding title and labels
    plt.title(f'Traffic Congestion on {date} for Area {area_id}')
    plt.xlabel('Time (Hour)')
    plt.ylabel('Average Congestion per Hour')
    plt.xticks(rotation=45)
    plt.grid(True)

    # Displaying the chart
    plt.tight_layout()
    plt.show()
    #plt.savefig('traffic_congestion_chart.png')
    #print("save successfully")
    #plt.close()

# Example usage
plot_traffic_congestion("2024-05-28", 2644)
