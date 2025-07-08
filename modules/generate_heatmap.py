import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import os

def generate_heatmap(csv_path='static/boulder_data_clustered.csv', output_path='static/risk_heatmap.jpg'):
    """
    Generates a KDE heatmap from boulder data CSV.
    """
    # Step 1: Check if the input file exists
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"[ERROR] Input CSV not found: {csv_path}")

    try:
        # Step 2: Load data with explicit encoding
        df = pd.read_csv(csv_path, encoding='utf-8')

        # Step 3: Trim column names and validate required columns
        df.columns = df.columns.str.strip()
        required_columns = {'X', 'Y'}
        if not required_columns.issubset(df.columns):
            raise ValueError(f"[ERROR] Missing required columns: {required_columns - set(df.columns)}")

        # Step 4: Check for empty data
        if df.empty:
            raise ValueError("[ERROR] CSV file is empty. No data available for heatmap generation.")

        # Step 5: Handle NaN values in required columns
        if df['X'].isna().any() or df['Y'].isna().any():
            raise ValueError("[ERROR] X or Y contains NaN values. Please clean the data.")

        # Step 6: Generate KDE heatmap
        plt.figure(figsize=(12, 10))  # Slightly larger figure for better visualization
        sns.kdeplot(
            x=df['X'], y=df['Y'],
            cmap="Reds", fill=True, bw_adjust=0.7, levels=50, thresh=0.02
        )

        # Step 7: Axis formatting and inversion
        plt.gca().invert_yaxis()
        plt.title('Boulder Risk Heatmap', fontsize=18, weight='bold')
        plt.xlabel('X Coordinate', fontsize=14)
        plt.ylabel('Y Coordinate', fontsize=14)

        # Step 8: Save the heatmap to file
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        plt.tight_layout()
        plt.savefig(output_path, dpi=300)
        plt.close()

        # Step 9: Success logging
        print(f"[✅] Heatmap saved to: {output_path}")
        print(f"[ℹ️] Dataset contains {len(df)} entries.")
        print(df.head())

    except Exception as e:
        # Step 10: Exception handling
        print(f"[ERROR] Failed to generate heatmap: {e}")
