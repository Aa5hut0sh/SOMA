import pandas as pd
import json
import os

def generate_heatmap_json(input_csv='static/boulder_data_clustered.csv', output_json='static/boulder_points.json'):
    """
    Converts clustered boulder CSV into a Leaflet-compatible heatmap JSON.
    Normalizes X and Y coordinates to a 0–1 scale and assigns fixed intensity.
    """
    if not os.path.exists(input_csv):
        print(f"[ERROR] Input CSV not found: {input_csv}")
        return False

    try:
        # Load the CSV file with explicit encoding
        df = pd.read_csv(input_csv, encoding='utf-8')

        # Validate necessary columns
        required_columns = {'X', 'Y'}
        if not required_columns.issubset(df.columns):
            missing_cols = required_columns - set(df.columns)
            raise ValueError(f"Missing required columns: {', '.join(missing_cols)}")

        # Drop rows with missing values in X or Y
        df = df.dropna(subset=['X', 'Y'])

        # Ensure there is data to process
        if df.empty:
            raise ValueError("No valid data available after dropping NaNs in 'X' and 'Y'.")

        # Normalize coordinates to 0–1 scale
        max_x, max_y = df['X'].max(), df['Y'].max()
        if max_x == 0 or max_y == 0:
            raise ValueError("Cannot normalize with zero max value for 'X' or 'Y'.")

        heat_data = [
            [round(y / max_y, 4), round(x / max_x, 4), 0.5]  # [normalized_y, normalized_x, intensity]
            for x, y in zip(df['X'], df['Y'])
        ]

        # Write the heatmap data to a JSON file with UTF-8 encoding
        os.makedirs(os.path.dirname(output_json), exist_ok=True)
        with open(output_json, 'w', encoding='utf-8') as f:
            json.dump(heat_data, f, indent=4, ensure_ascii=False)  # Ensure non-ASCII chars are handled

        print(f" Leaflet heatmap data written to: {output_json}")
        print(f" Total points: {len(heat_data)}")
        return True

    except Exception as e:
        # Handle encoding issues in exception messages
        safe_error = str(e).encode('utf-8', errors='replace').decode('utf-8')
        print(f"[ERROR] Failed to generate heatmap JSON: {safe_error}")
        return False
