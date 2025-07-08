import cv2
import numpy as np
import os

def detect_landslides(image_path):
    """
    Detects potential landslide regions in an input image and saves a visualized output.

    Args:
        image_path (str): Path to the input image.

    Returns:
        list: A list of dictionaries containing properties of detected landslide regions.
    """
    try:
        # Check if the image path exists
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Input image not found: {image_path}")

        # Load image
        img = cv2.imread(image_path)
        if img is None:
            raise ValueError(f"Unable to read image from path: {image_path}")

        # Convert to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Step 1: Histogram equalization for contrast enhancement
        equalized = cv2.equalizeHist(gray)

        # Step 2: Apply Gaussian blur to reduce noise
        blurred = cv2.GaussianBlur(equalized, (5, 5), 0)

        # Step 3: Edge detection to highlight slope breaks
        edges = cv2.Canny(blurred, threshold1=50, threshold2=150)

        # Step 4: Morphological operations to close gaps in edges
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
        closed = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernel)

        # Step 5: Find contours in the processed image
        contours, _ = cv2.findContours(closed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        landslide_candidates = []
        landslide_img = img.copy()

        for cnt in contours:
            area = cv2.contourArea(cnt)
            if area > 500:  # Filter small areas (noise)
                # Approximate shape and calculate bounding box
                approx = cv2.approxPolyDP(cnt, 0.02 * cv2.arcLength(cnt, True), True)
                x, y, w, h = cv2.boundingRect(approx)

                # Aspect ratio (optional filtering can be applied here)
                aspect_ratio = w / h if h != 0 else 0

                # Draw contour on the visualization image
                cv2.drawContours(landslide_img, [cnt], -1, (255, 0, 0), 2)

                # Append candidate properties
                landslide_candidates.append({
                    'x': int(x),
                    'y': int(y),
                    'width': int(w),
                    'height': int(h),
                    'area': round(area, 2),
                    'aspect_ratio': round(aspect_ratio, 2)
                })

        # Save visualization
        os.makedirs('static', exist_ok=True)
        output_path = 'static/landslides_detected.jpg'
        cv2.imwrite(output_path, landslide_img)

        print(f" Landslides detected and saved to {output_path}")
        print(f"Total landslide candidates detected: {len(landslide_candidates)}")

        return landslide_candidates

    except Exception as e:
        # Ensure error messages handle any character encoding issues
        print(f"[ERROR] Failed to detect landslides: {str(e).encode('utf-8', 'replace').decode('utf-8')}")
        return []
