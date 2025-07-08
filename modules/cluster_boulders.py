def cluster_boulders(df_path=None):
    """
    Clusters detected boulders based on their diameters and visualizes the results.
    """
    import pandas as pd
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    from sklearn.cluster import KMeans
    import os

    # Step 1: File paths
    input_file = df_path or "static/boulder_data.csv"
    output_file = "static/boulder_data_clustered.csv"
    plot_file = "static/clustered_boulders_plot.jpg"

    if not os.path.exists(input_file):
        raise FileNotFoundError(f"[ERROR] {input_file} not found. Run boulder detection first.")

    # Step 2: Load the data
    df = pd.read_csv(input_file)

    # Step 3: Validate required columns
    required_columns = {'Diameter (m)', 'X', 'Y'}
    if not required_columns.issubset(df.columns):
        raise ValueError(f"[ERROR] Input CSV must contain: {required_columns}")

    # Step 4: KMeans clustering based on diameter
    X = df[['Diameter (m)']]

    # Step 5: Handle compatibility for n_init
    try:
        kmeans = KMeans(n_clusters=3, random_state=0, n_init='auto')
    except TypeError:
        kmeans = KMeans(n_clusters=3, random_state=0, n_init=10)

    df['Cluster'] = kmeans.fit_predict(X)

    # Step 6: Assign size labels based on cluster means
    cluster_means = df.groupby("Cluster")["Diameter (m)"].mean().sort_values()
    cluster_map = {i: label for i, label in zip(cluster_means.index, ['Small', 'Medium', 'Large'])}
    df['SizeLabel'] = df['Cluster'].map(cluster_map)

    # Step 7: Save clustered data
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    df.to_csv(output_file, index=False)
    print(f"[✅] Clustered data saved to: {output_file}")

    # Step 8: Plot clusters
    plt.figure(figsize=(10, 8))
    cluster_colors = {'Small': 'green', 'Medium': 'orange', 'Large': 'red'}

    for label in ['Small', 'Medium', 'Large']:
        sub = df[df['SizeLabel'] == label]
        plt.scatter(
            sub['X'], sub['Y'], label=f"{label} Boulders",
            s=40, c=cluster_colors[label], edgecolors='k', alpha=0.7
        )

    plt.gca().invert_yaxis()
    plt.title("Boulder Clusters by Size", fontsize=16)
    plt.xlabel("X Coordinate", fontsize=12)
    plt.ylabel("Y Coordinate", fontsize=12)
    plt.legend(title="Boulder Size", fontsize=10, loc='upper right')

    # Step 9: Save the plot
    plt.savefig(plot_file, dpi=300)
    plt.close()
    print(f"[✅] Clustered plot saved to: {plot_file}")
