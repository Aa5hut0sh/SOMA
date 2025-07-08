import pandas as pd
import cv2
import numpy as np
from sklearn.linear_model import LinearRegression

def estimate_source(
    csv_path='static/boulder_data_clustered.csv',
    image_path='static/boulders_detected.jpg',
    output_path='static/boulders_with_source.jpg'
):
    # Load boulder data
    df = pd.read_csv(csv_path)
    df.columns = df.columns.str.strip()

    # Use correct columns (adjust as needed)
    X_coords = df['X'].values.reshape(-1, 1)
    Y_coords = df['Y'].values

    # Fit linear regression (boulder flow direction)
    model = LinearRegression()
    model.fit(X_coords, Y_coords)
    slope = model.coef_[0]
    intercept = model.intercept_

    # Project "uphill" to estimate the source point
    min_x = int(np.min(X_coords)) - 50
    estimated_source_x = min_x
    estimated_source_y = int(slope * estimated_source_x + intercept)

    # Load detection image
    img = cv2.imread(image_path)
    if img is not None:
        # Draw a single red dot at the source
        cv2.circle(img, (estimated_source_x, estimated_source_y), 30, (255, 0, 0), -1)  # 🔵 blue

        cv2.putText(img, 'Estimated Source', (estimated_source_x + 15, estimated_source_y - 10),
            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)  # 🔵 blue label

        cv2.imwrite(output_path, img)

    return (estimated_source_x, estimated_source_y)
