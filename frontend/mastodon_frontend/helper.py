"""
File: helper.py
Author: Yechen Deng
Date: 21/05/2024
Description: This program serves as a helper files of functions for the main front-end deployement.
"""
import pandas as pd
import requests
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from sklearn.linear_model import LinearRegression

# Fetch the data from API - ElasticSearch
def fetch_data(url, df_name):
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        df = pd.DataFrame.from_dict(data, orient='index')
        df.reset_index(inplace=True)
        df.rename(columns={'index': 'timestamp'}, inplace=True)
        df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')
        print(f"{df_name} load succeeded.")
        return df
    else:
        print(f"Request failed: {response.status_code}")
        return None

# Plot temporal analysis of average sentiment score and total number of toots
def plot_count_and_sentiment(df):
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    fig, ax1 = plt.subplots(figsize=(15, 7))

    bars = ax1.bar(df['timestamp'].astype(str), df['doc_count'], color='tab:blue', label='Doc Count', width=0.5, align='center')
    ax1.set_xlabel('Timestamp')
    ax1.set_ylabel('Document Count', color='tab:blue')
    ax1.tick_params(axis='y', labelcolor='tab:blue')

    for bar in bars:
        yval = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2, yval + 100, int(yval), ha='center', va='bottom', color='black')

    ax2 = ax1.twinx()
    ax2.plot(df['timestamp'].astype(str), df['average_sentiment'], 'go-', markersize=5, label='Average Sentiment')
    ax2.set_ylabel('Average Sentiment', color='tab:green')
    ax2.tick_params(axis='y', labelcolor='tab:green')

    ax1.set_xticks(df['timestamp'].astype(str))
    ax1.set_xticklabels(df['timestamp'].dt.strftime('%Y-%m-%d %H:%M'), rotation=45, ha='right')

    ax1.grid(True)
    ax1.legend(loc='center left')
    ax2.legend(loc='center right')

    plt.title('Document Count and Average Sentiment Over Time')
    plt.tight_layout()
    plt.show()

# Plot pie charts to analyse each summarised categories
def plot_cumulative_pie_charts(df):
    total_weather = df['cumulative_weather'].sum()
    total_airquality = df['cumulative_airquality'].sum()
    total_traffic = df['cumulative_traffic'].sum()

    total_cumulative = total_weather + total_airquality + total_traffic
    total_doc_count = df['doc_count'].sum()
    total_others = total_doc_count - total_cumulative

    labels_cumulative = ['Weather', 'Air Quality', 'Traffic']
    sizes_cumulative = [
        total_weather / total_cumulative * 100 if total_cumulative > 0 else 0,
        total_airquality / total_cumulative * 100 if total_cumulative > 0 else 0,
        total_traffic / total_cumulative * 100 if total_cumulative > 0 else 0
    ]
    colors = ['skyblue', 'lightgreen', 'lightcoral']

    labels_total = ['Weather', 'Air Quality', 'Traffic', 'Others']
    sizes_total = [
        total_weather / total_doc_count * 100 if total_doc_count > 0 else 0,
        total_airquality / total_doc_count * 100 if total_doc_count > 0 else 0,
        total_traffic / total_doc_count * 100 if total_doc_count > 0 else 0,
        total_others / total_doc_count * 100 if total_doc_count > 0 else 0
    ]
    colors_total = ['skyblue', 'lightgreen', 'lightcoral', 'lightgrey']

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 7))

    ax1.pie(sizes_cumulative, labels=labels_cumulative, colors=colors, autopct='%1.1f%%', startangle=140)
    ax1.axis('equal')
    ax1.set_title('Percentage of Each Category')

    ax2.pie(sizes_total, labels=labels_total, colors=colors_total, autopct='%1.1f%%', startangle=140)
    ax2.axis('equal')
    ax2.set_title('Percentage of Each Category in Total Number of Toots')

    plt.show()

# Plot comparison between two servers
def plot_comparision_bar(df1, df2):
    totals_df1 = {
        "Weather": df1['cumulative_weather'].sum(),
        "Air Quality": df1['cumulative_airquality'].sum(),
        "Traffic": df1['cumulative_traffic'].sum(),
        "Total #of Toots": df1['doc_count'].sum()
    }

    totals_df2 = {
        "Weather": df2['cumulative_weather'].sum(),
        "Air Quality": df2['cumulative_airquality'].sum(),
        "Traffic": df2['cumulative_traffic'].sum(),
        "Total #of Toots": df2['doc_count'].sum()
    }

    total_data = pd.DataFrame([totals_df1, totals_df2], index=["mastodon.au", "au.social"])

    ax = total_data.plot(kind="bar", color=['skyblue', 'lightgreen', 'salmon', 'lightgrey'], figsize=(10, 6))
    ax.set_title("Comparison of Each Category Between Two Servers")
    ax.set_ylabel("Total # of Counts")
    ax.set_xlabel("Servers")
    plt.xticks(rotation=0)
    for p in ax.patches:
        ax.annotate(str(p.get_height()), (p.get_x() + p.get_width() / 2., p.get_height()), ha='center', va='bottom')
    plt.show()

# Correlation analysis of numeric features
def plot_correlation_matrix(df, df_name):
    df_internal = df.copy()
    df_internal['weather_ratio'] = df_internal['cumulative_weather'] / df_internal['doc_count']
    df_internal['airquality_ratio'] = df_internal['cumulative_airquality'] / df_internal['doc_count']
    df_internal['traffic_ratio'] = df_internal['cumulative_traffic'] / df_internal['doc_count']

    numeric_columns = [
        'weather_ratio',
        'airquality_ratio',
        'traffic_ratio',
        'average_sentiment'
    ]
    correlation_matrix = df_internal[numeric_columns].corr()

    plt.figure(figsize=(8, 6))

    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f", linewidths=0.5)

    plt.title(f'Correlation Matrix - {df_name.capitalize()}')
    plt.show()

    return df_internal

# Build linear regression model and evaluate via residual plot
def evaluate_linear_regression(df):
    required_columns = ['weather_ratio', 'airquality_ratio', 'traffic_ratio', 'average_sentiment']
    if all(col in df.columns for col in required_columns):
        # Fit linear regression model
        X = df[['weather_ratio', 'airquality_ratio', 'traffic_ratio']]
        y = df['average_sentiment']
        model = LinearRegression().fit(X, y)
        # Print coefficients in the model
        print('Intercept:', model.intercept_)
        print('Coefficients:', model.coef_)

        predicted_values = model.predict(X)
        residuals = y - predicted_values

        # Plot residuals
        plt.figure(figsize=(8, 6))
        plt.scatter(predicted_values, residuals, alpha=0.5)
        plt.xlabel('Predicted Values')
        plt.ylabel('Residuals')
        plt.title('Residual Plot')
        plt.axhline(y=0, color='r', linestyle='--')  # Add a horizontal line at y=0
        plt.grid(True)
        plt.show()
    else:
        print("One or more of the specified columns do not exist in the DataFrame.")

# Visualise in 3D condition
def plot_3d_scatter_with_regression(df):
    required_columns = ['weather_ratio', 'airquality_ratio', 'traffic_ratio', 'average_sentiment']
    if all(col in df.columns for col in required_columns):

        # Create figure and 3D axis
        fig = plt.figure(figsize=(8, 6))
        ax = fig.add_subplot(111, projection='3d')

        # Scatter plot
        scatter = ax.scatter(df['weather_ratio'], df['airquality_ratio'], df['traffic_ratio'],
                             c=df['average_sentiment'], cmap='viridis', s=50)

        X = df[['weather_ratio', 'airquality_ratio', 'traffic_ratio']]
        y = df['average_sentiment']
        model = LinearRegression().fit(X, y)

        xx, yy = np.meshgrid(np.linspace(df['weather_ratio'].min(), df['weather_ratio'].max(), 10),
                             np.linspace(df['airquality_ratio'].min(), df['airquality_ratio'].max(), 10))
        zz = model.coef_[0] * xx + model.coef_[1] * yy + model.intercept_

        ax.plot_surface(xx, yy, zz, alpha=0.5, color='red')

        ax.set_xlabel('Weather Ratio')
        ax.set_ylabel('Airquality Ratio')
        ax.set_zlabel('Traffic Ratio')
        ax.set_title('3D Scatter Plot with Regression Plane')

        cbar = fig.colorbar(scatter)
        cbar.set_label('Average Sentiment')

        plt.show()
    else:
        print("One or more of the specified columns do not exist in the DataFrame.")