import os
import shutil
from flask import Flask, request, render_template, send_file
from werkzeug.utils import secure_filename
from random import random
from PIL import Image
import glob
from datetime import datetime

from modules.detect_boulders import detect_boulders
from modules.cluster_boulders import cluster_boulders
from modules.generate_stats import generate_stats
from modules.generate_heatmap import generate_heatmap
from modules.estimate_source import estimate_source
from modules.generate_pdf_report import generate_pdf
from modules.generate_heatmap_json import generate_heatmap_json
from modules.detect_landslides import detect_landslides

# App Initialization
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['STATIC_FOLDER'] = 'static'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['STATIC_FOLDER'], exist_ok=True)

def cleanup_previous_results():
    """
    Clean up previous analysis results to ensure fresh results for new uploads
    """
    try:
        # List of files to clean up
        files_to_remove = [
            'preview.jpg',
            'boulders_detected.jpg',
            'landslides_detected.jpg',
            'clustered_boulders_plot.jpg',
            'risk_heatmap.jpg',
            'boulders_with_source.jpg',
            'report.pdf',
            'boulder_data_clustered.csv',
            'boulder_points.json',
            'stats_summary.txt'
        ]
        
        # Remove old result files
        for filename in files_to_remove:
            filepath = os.path.join(app.config['STATIC_FOLDER'], filename)
            if os.path.exists(filepath):
                os.remove(filepath)
                print(f"[🗑️] Removed old file: {filename}")
        
        # Also clean up any CSV files in the root directory
        csv_files = glob.glob("boulder_data*.csv")
        for csv_file in csv_files:
            if os.path.exists(csv_file):
                os.remove(csv_file)
                print(f"[🗑️] Removed old CSV: {csv_file}")
                
        print("[✅] Cleanup completed successfully")
        
    except Exception as e:
        print(f"[⚠️] Error during cleanup: {str(e)}")

def convert_tif_to_jpg(image_path):
    """
    Converts a .tif image to .jpg and returns the converted file path.
    """
    if image_path.lower().endswith('.tif'):
        try:
            img = Image.open(image_path)
            
            # Convert to RGB if necessary
            if img.mode != 'RGB':
                img = img.convert('RGB')
            
            converted_path = os.path.join(app.config['UPLOAD_FOLDER'], 'converted_image.jpg')
            img.save(converted_path, "JPEG")
            print(f"[✅] Converted .tif to .jpg: {converted_path}")
            return converted_path
        except Exception as e:
            print(f"[ERROR] Unable to convert .tif image: {e}")
            return None
    return image_path

@app.route('/', methods=['GET', 'POST'])
def index():
    stats_text = "No stats available yet. Upload an image to generate results."

    # ✅ Clean up on fresh GET request
    if request.method == 'GET':
        print("[🌙] GET request received — cleaning previous results")
        cleanup_previous_results()

    if request.method == 'POST':
        if 'image' not in request.files:
            return "Error: No file part in the request."
        file = request.files['image']
        
        if not file.filename:
            return "Error: No file selected for upload."
        
        if file:
            try:
                # STEP 1: Clean up again for good measure (you may skip this if done above)
                print("[🧹] Cleaning up previous analysis results...")
                cleanup_previous_results()
                
                # STEP 2: Save uploaded image
                filename = secure_filename(file.filename)
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)
                print(f"[📁] Saved uploaded file: {filepath}")
                
                # STEP 3: Handle .tif conversion if needed
                processed_filepath = convert_tif_to_jpg(filepath)
                if not processed_filepath:
                    return "Error: Failed to process .tif image."
                
                # STEP 4: Generate a preview image for the UI
                preview_path = os.path.join(app.config['STATIC_FOLDER'], 'preview.jpg')
                shutil.copy(processed_filepath, preview_path)
                print(f"[🖼️] Created preview: {preview_path}")
                
                # STEP 5: Run Full Detection Pipeline
                print("[🔬] Starting analysis pipeline...")
                detect_boulders(processed_filepath)
                cluster_boulders()
                generate_stats()
                generate_heatmap()
                estimate_source()
                detect_landslides(processed_filepath)
                generate_pdf()
                generate_heatmap_json()
                
                print("[✅] Analysis pipeline completed")
                
                # STEP 6: Load fresh stats
                stats_file = os.path.join(app.config['STATIC_FOLDER'], 'stats_summary.txt')
                if os.path.exists(stats_file):
                    with open(stats_file, 'r', encoding='utf-8') as f:
                        stats_text = f.read()
                    print("[📊] Loaded fresh statistics")
                else:
                    print("[⚠️] Stats file not found after analysis")
                
            except Exception as e:
                print(f"[💥] Pipeline Error: {str(e)}")
                return f"Pipeline Error: {str(e)}"
    
    return render_template('index.html', stats_text=stats_text, random=random)


@app.route('/download-report')
def download_report():
    report_path = os.path.join(app.config['STATIC_FOLDER'], 'report.pdf')
    if os.path.exists(report_path):
        return send_file(report_path, as_attachment=True)
    return "Error: Report file not found."

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)