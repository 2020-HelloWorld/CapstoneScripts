import json
import numpy as np
from scipy.stats import gaussian_kde,mode
import matplotlib.pyplot as plt
from scipy.signal import argrelextrema

# Read packet data from the JSON file created during packet sniffing
with open("packet_data.json", "r") as json_file:
    packet_data = [json.loads(line) for line in json_file]

# Create a dictionary to store flow information and IAT values
flow_iat = {}

# Extract packet data and calculate IAT values for each flow
for packet in packet_data:
    src_ip = packet["source_ip"]
    dst_ip = packet["destination_ip"]
    timestamp_sec = packet["timestamp_sec"]
    timestamp_us = packet["timestamp_us"]

    flow_id = src_ip,"-",dst_ip
    
    if flow_id not in flow_iat:
        flow_iat[flow_id] = {"timestamps": []}
    
    total_timestamp = timestamp_sec + (timestamp_us//1000) / 1000
    flow_iat[flow_id]["timestamps"].append(total_timestamp)

# Calculate the fields for each flow
results = []
for flow_id, data in flow_iat.items():
    timestamps = data["timestamps"]
    if len(timestamps)<=2:
        continue
    iat_values = np.round(np.diff(timestamps),3)
    print("IAT",iat_values)
    print("TS",timestamps)
    print("*****")

    unique_iat = len(np.unique(iat_values)) #done
    kde_peaks = 0

    density = gaussian_kde(iat_values)

# Evaluate KDE at a range of x values
    x_values = np.linspace(min(iat_values), max(iat_values), 1000)
    kde_estimate = density.evaluate(x_values)

    # Find local maxima indices
    local_maxima_indices = argrelextrema(kde_estimate, np.greater)
    kde_peaks=len(local_maxima_indices[0])

    # Plot the original data and KDE
    plt.figure(figsize=(10, 6))

    # Plot the histogram of the original data
    plt.hist(iat_values, bins=20, density=True, alpha=0.5, label="Data Histogram")

    # Plot the KDE estimate
    plt.plot(x_values, kde_estimate, label="KDE")

    # Highlight the identified peaks using local maxima
    plt.scatter(x_values[local_maxima_indices], kde_estimate[local_maxima_indices], color='red', label="Local Maxima")

    plt.xlabel("Values")
    plt.ylabel("Density")
    plt.title("Data and KDE with Local Maxima as Peaks")
    plt.legend()

    s="output/"+str(len(local_maxima_indices[0]))+str(flow_id)+".png"

    plt.savefig(s)











    symbols = len(set(iat_values))
    peak_std_mean = np.mean(density.covariance)
    autocorr_sum = np.sum(np.correlate(iat_values, iat_values, mode='full'))
    covert_bytes = 100 * len(iat_values)
    # Calculate the mode of IAT values using scipy.stats.mode()
    mode_result = mode(iat_values)
    mode_iat = mode_result.mode[0]

    p_mode = np.count_nonzero(iat_values == mode_iat) / len(iat_values)


    num_packets = len(timestamps)

    result = {
        "flow_id": flow_id,
        "unique": unique_iat,
        "multimod": kde_peaks,
        "multimod2": symbols,
        "widthave": peak_std_mean,
        "autocorr": autocorr_sum,
        "c": covert_bytes,
        "nrPacketsMode": p_mode,
        "nrPackets": num_packets
    }
    results.append(result)

# Store the results in a JSON file
output_filename = "flow_analysis.json"
with open(output_filename, "w") as json_file:
    json.dump(results, json_file, indent=4)

print("Results stored in 'flow_analysis.json'")

