
# 🛰️ Moon Landslide & Boulder Detection Using Chandrayaan Imagery – Project Documentation

**Project Title:** Moon Surface Risk Analyzer  
**Hackathon Statement ID:** Problem Statement-11  
**Last Updated:** 2025-06-22

---

## 🚀 Overview

This project aims to detect **landslides** and **boulder falls** on the Moon using imagery from **Chandrayaan-1** and **Chandrayaan-2** missions. By analyzing **TMC, DTM, and OHRC** imagery, the goal is to develop a **novel detection algorithm** that not only detects and annotates boulders and landslides, but also extracts shape-based statistics, estimates risk zones, and predicts source origins.

---

## 🧠 Problem Understanding

- Landslides and boulder falls are indicators of recent lunar surface activity.
- The Moon has steep terrain making it prone to such hazards.
- Goal: Use ISRO Chandrayaan image data to detect, label, and analyze these phenomena in a novel, interpretable, and scalable manner.

---

## 🎯 Project Objectives

- Detect **boulders** and **landslides** in Moon images.
- Provide metadata: coordinates, diameter, shape metrics.
- Cluster similar boulders by size.
- Generate **heatmaps** and estimate likely **source points**.
- Annotate and export all findings in reports and interactive UI.
- Ensure that the approach works for *any region on the Moon*.

---

## 🧰 Tools, Technologies & Justifications

| Tool / Tech | Why Used | How Used |
|-------------|----------|----------|
| **Python** | Core backend logic | For image processing, detection algorithms, data clustering, and report generation. |
| **OpenCV** | Image analysis & contour detection | Used to preprocess grayscale images, detect boulders via thresholding and contour extraction. |
| **NumPy** | Fast numerical calculations | Calculates circularity, aspect ratios, and handles data arrays. |
| **Pandas** | Data analysis & CSV handling | Stores and processes shape descriptors and boulder metrics. |
| **Scikit-learn** | Clustering | Clusters boulders into small, medium, and large categories using KMeans. |
| **Matplotlib** | Plotting | Visualizes clustered boulders and saves annotated plots. |
| **Jinja2 (Flask templates)** | Dynamic HTML rendering | Embeds real-time data (images, stats, filenames) into the frontend. |
| **Flask** | Web framework | Powers the full backend + routing + file upload pipeline. |
| **Leaflet.js** | Interactive mapping | Renders zoomable boulder heatmaps directly over the analyzed image. |
| **Leaflet.heat plugin** | Visual heatmap layer | Displays boulder densities interactively. |
| **HTML/CSS/JavaScript** | UI/UX | Builds and styles the web-based user interface. |
| **QGIS** *(optional)* | Geospatial visualization | Used for advanced visualization (TMC/DTM overlay), not mandatory in current pipeline. |
| **LaTeX via ReportLab** | PDF report generation | Creates downloadable reports with all metadata and analysis. |
| **Shutil / OS** | File handling | For managing uploaded files and outputs in a structured directory. |

---

## 🧪 Detection Methodology

### 🔍 Boulder Detection Logic

1. Convert image to grayscale.
2. Apply **Gaussian blur** to remove noise.
3. Use **binary thresholding** to segment boulder-like shapes.
4. Use `cv2.findContours()` to extract shapes.
5. For each contour:
   - Fit **min enclosing circle**.
   - Compute:
     - Diameter
     - Area
     - Perimeter
     - Circularity = (4 * pi * Area) / (Perimeter^2)
     - Aspect Ratio (via ellipse fitting)
   - Classify shape as: **Round**, **Elongated**, or **Irregular**.
   - Annotate image with color-coded shapes.

6. Save data in `boulder_data.csv` and image in `boulders_detected.jpg`.

---

### 📊 Clustering Logic

- Cluster boulders using **KMeans (3 clusters)** on diameter values.
- Label as: **Small**, **Medium**, or **Large**.
- Use sorted means to determine cluster sizes (ensures consistent naming).
- Save results as `boulder_data_clustered.csv`.

---

### 🧠 Heatmap Generation

- Normalize X/Y coordinates of boulders to 0–1 scale.
- Format into a JSON format usable by **Leaflet.heat**.
- Layer this heatmap on top of `boulders_detected.jpg` using Leaflet.
- Blue shades = low density, Yellow = medium, Red = high boulder concentration.

---

### 🧭 Source Point Estimation

- Estimate most probable **landslide origin**:
  - Compute mean vector direction of boulder positions.
  - Trace “uphill” towards densest zone.
  - Mark source in `boulders_with_source.jpg`.

---

### 📄 PDF Report

- Summarizes:
  - Total boulders
  - Diameter ranges
  - Shape counts (Round/Elongated/Irregular)
  - Clustering summary
- Includes plots and stats.
- Downloadable via button.

---

### 🌐 Web UI Features

- Upload Moon image (`jpg`, `png`, `tif`, `img`).
- Shows:
  - Preview
  - Annotated detections
  - Cluster plot
  - Risk heatmap
  - Source point
  - Downloadable report
  - Boulder statistics
  - CSV download
- Built with **Flask** and **Jinja templates**.

---

## ✨ Novelty in Our Approach

- Combines **shape-based descriptors** (circularity, aspect ratio) into classification.
- Uses **elliptical fitting** for better shape analysis (vs bounding box).
- **Interactive heatmap** over image using Leaflet (rare in prior Moon analysis).
- Detects **source origin** based on centroid vectoring.
- Fully automated UI + report generator, easy to replicate.
- Works **in real-time** in browser without external GIS software.

---

## 🪨 Still to be Done / Ongoing

- Implement landslide detection (via slope & cluster gradients).
- Time series change detection (for “recent” landslides).
- Shape-based boulder group similarity analysis.
- Image registration with DTM/DEM data (via QGIS or raster APIs).

---

## 📁 Folder Structure

```
moon_boulder_app/
├── app.py
├── templates/
│   └── index.html
├── static/
│   ├── boulders_detected.jpg
│   ├── preview.jpg
│   ├── risk_heatmap.jpg
│   ├── report.pdf
│   └── boulder_data_clustered.csv
├── detect_boulders.py
├── cluster_boulders.py
├── generate_heatmap.py
├── estimate_source.py
├── generate_pdf_report.py
├── generate_stats.py
└── generate_heatmap_json.py
```

---

## 💬 Expected Deep Questions & Your Answers

| Question | How to Answer |
|---------|---------------|
| Why Gaussian blur? | Removes high-frequency noise to improve contour detection. |
| Why threshold 200? | We used it based on histogram testing of high-contrast lunar surfaces. Adjustable per image. |
| Why elliptical aspect ratio? | More accurate than bounding box for irregular moon rocks. |
| Why KMeans and 3 clusters? | Empirically, 3 sizes (S/M/L) cover natural distributions. KMeans offers unsupervised simplicity. |
| What if image is rotated? | We detect shapes independent of orientation using invariant features. |
| How does Leaflet work offline? | Leaflet.js is embedded from CDN, but we can host it locally too. |
| Can you align to latitude-longitude? | Yes, if we use QGIS/DTM and geo-tag the image. |
| What defines a landslide in image terms? | Sharp linear gradient, fan shape spread, clustered debris field. We aim to detect these in next phase. |

---

## 📌 Team Name: Clueless Coders  
**Institution:** Rajiv Gandhi Institute of Petroleum Technology  
**Tech Stack:** Python + OpenCV + Flask + JS (Leaflet) + Pandas + Matplotlib + Scikit-learn + HTML/CSS  
**Deployment:** Localhost (for now), can be deployed to Render/Heroku with minor changes.

---
