
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta


# Generating timestamps for 30 days with 30-minute intervals
#start_date = datetime(2024, 12, 1, 0, 0)
#end_date = start_date + timedelta(days=30)
#timestamps = []
#current_time = start_date
#while current_time < end_date:
    #timestamps.append(current_time)
    #current_time += timedelta(minutes=30)

# baseline smart meter readings with some error
#baseline_consumption = np.random.uniform(1, 5, len(timestamps))
#noise = np.random.normal(0, 0.5, len(timestamps))  # Add some noise
#smart_meter_readings = baseline_consumption + noise

# Introducing anomalies
#anomaly_indices = np.random.choice(len(timestamps), size=5, replace=False)  # Introduce 5 anomalies
#smart_meter_readings[anomaly_indices] += np.random.uniform(5, 15, 5)  # Increase readings at anomaly points

#  DataFrame
#data = {'Timestamp': timestamps, 'Smart_Meter_Reading': smart_meter_readings}
df = pd.read_excel("C:\data analytics smart meters\meterdatanew.xlsx")

# Simple anomaly detection (using standard deviation)
threshold = 2.5  # Adjust as needed

rolling_mean = df['Smart_Meter_Reading'].rolling(window=24).mean() #24 hours as we have readings every 30 minutes
rolling_std = df['Smart_Meter_Reading'].rolling(window=24).std()
df['Anomaly'] = 0
#df.loc[df['Smart_Meter_Reading'] > rolling_mean + threshold * rolling_std, 'Anomaly'] = 1
#df.loc[df['Smart_Meter_Reading'] > rolling_mean - threshold * rolling_std, 'Anomaly'] = 1
df.loc[(df['Smart_Meter_Reading'] > rolling_mean + threshold * rolling_std) |
       (df['Smart_Meter_Reading'] < rolling_mean - threshold * rolling_std), 'Anomaly'] = 1



# Visualization

average_consumption = df['Smart_Meter_Reading'].mean()
plt.figure(figsize=(15, 6))
sns.lineplot(x='Timestamp', y='Smart_Meter_Reading', data=df, label='Consumption')
sns.scatterplot(x='Timestamp', y='Smart_Meter_Reading', data=df[df['Anomaly'] == 1], color='red', label='Anomaly')

# Add average consumption line
plt.axhline(y=average_consumption, color='green', linestyle='--', label=f'Average: {average_consumption:.2f}')

plt.title('Smart Meter Readings with Anomalies and Average Consumption')
plt.xlabel('Date and Time')
plt.ylabel('Smart Meter Reading')
plt.xticks(rotation=45)
plt.legend()
plt.show()

# Displaying anomaly timestamps
anomalies_df = df[df['Anomaly'] == 1]
print("Anomalies:")
print(anomalies_df[['Timestamp', 'Smart_Meter_Reading']])


#Save the Dataframe
#df.to_csv("meterdatanew.csv", index=False)
#df.to_excel("meterdatanew.xlsx", index=False)

#plt.axhline(y=average_consumption, color='green', linestyle='--', label=f'Average Consumption: {average_consumption:.2f}')
total_anomalies = df['Anomaly'].sum()
anomalies_per_day = df[df['Anomaly'] == 1].groupby(df['Timestamp'].dt.date).size()



plt.figure(figsize=(10, 6))
anomalies_per_day.plot(kind='bar', color='orange', alpha=0.7)
plt.title('Number of Anomalies Detected Per Day')
plt.xlabel('Date')
plt.ylabel('Count of Anomalies')
plt.xticks(rotation=45)
plt.tight_layout()

# Add total anomaly count as an annotation
plt.text(0.95, 0.9, f'Total Anomalies: {total_anomalies}',
         transform=plt.gca().transAxes, fontsize=12, color='blue',
         bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=0.5'))

plt.show()
