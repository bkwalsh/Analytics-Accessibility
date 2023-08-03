import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
import numpy as np
import os

def runColumnCorrelation(raw_data_stream, column):
    filename = 'columnCorrelation.model'
    model_file = os.environ.get('MODEL_FILE', filename)

    df = raw_data_stream

    def clean_columns(df, data_types, substrings):
        columns_to_remove = []

        for column in df.columns:
            if (df[column].dtype not in data_types) or (any(substring in column for substring in substrings)):
                columns_to_remove.append(column)

        df = df.drop(columns=columns_to_remove)

        nan_percentages = df.isna().mean()
        columns_to_remove = nan_percentages[nan_percentages > .2].index
        df = df.drop(columns=columns_to_remove, axis=1)
        df.drop(df.index[-1], inplace=True)
        return df

    def find_most_correlated_column(df, input_column):
        max_corr = 0  
        best_column = None  

        for column in df.columns:
            if column != input_column:
                corr = df[column].corr(df[input_column])
                if abs(corr) > abs(max_corr):
                    max_corr = corr
                    best_column = column

        return best_column

    df = clean_columns(df, ['int64', 'float64'], ['Id','Return'])
    most_Corr = find_most_correlated_column(df, column)

    new_df = df[[column, most_Corr]]
    df.sort_values(column, ascending=False)

    n_clusters = 1000
    kmeans = KMeans(n_clusters=n_clusters, random_state=0)
    kmeans.fit(new_df)
    centroids = kmeans.cluster_centers_
    reduced_data = pd.DataFrame(centroids, columns=new_df.columns)

    reduced_data_sorted = reduced_data.sort_values(by=most_Corr)
    plt.figure(figsize=(20, 12)) 
    plt.scatter(reduced_data[most_Corr], reduced_data[column])
    plt.xscale('log')
    plt.yscale('log')

    coefficients = np.polyfit(reduced_data_sorted[most_Corr], reduced_data_sorted[column], 1)
    trend_line = np.poly1d(coefficients)

    plt.plot(reduced_data_sorted[most_Corr], trend_line(reduced_data_sorted[most_Corr]), color='red', label='Trend Line')

    standard_deviation = np.std(reduced_data[column])
    plt.axhline(y=np.mean(reduced_data[column]), color='orange', linestyle='--', label='Mean')
    plt.axhline(y=np.mean(reduced_data[column]) + standard_deviation, color='green', linestyle='--', label='Mean + Std Dev')

    plt.title(column + ' correlation with ' + most_Corr + ' (' + str(n_clusters) + ' Most Relevant Clusters)')
    plt.xlabel(most_Corr)
    plt.ylabel(column)

    plt.legend()

    plt.savefig('correlation_plot.jpg', format='jpeg')

