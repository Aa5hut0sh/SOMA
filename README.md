
# 🌕 SOMA - Surface Observation and Mapping Algorithm

**Novel method to detect landslides and boulders on the Moon using Chandrayaan-1/2 imagery**

---

## 🚀 Overview

SOMA is a modular, open-source Python pipeline designed to detect **lunar landslides** and **boulders** using satellite imagery and terrain datasets from **Chandrayaan-1 and 2 missions**. It uses terrain modeling, image processing, and statistical feature extraction to highlight geological activities such as mass movements and boulder falls on the Moon.

---

## 🧩 Problem Statement

Landslides and boulder falls on the Moon are critical indicators of recent geological activities. Due to steep slopes and unique surface conditions, conventional Earth-based methods fall short in lunar scenarios.

This project addresses the challenge by proposing a **novel algorithm** capable of:
- Detecting landslides from DTM, OHRC, and TMC images.
- Detecting and measuring individual boulders.
- Highlighting active zones using terrain slope and imagery cues.
- Working across all lunar regions.

---

## 📸 Key Features

- ✅ **Automated Landslide Detection** using elevation slope and gradient analysis
- 🪨 **Boulder Detection & Measurement** using contour segmentation
- 📏 **Dimension Estimation** (diameter, bounding box, area)
- 🌋 **Mass Movement Source Decoding**
- 🔥 **Risk Heatmap Generation**
- 🌐 **Region-Agnostic (any part of the Moon)**
- 📊 **Detailed Metadata Output** (.csv/.json)

---

## 🛰️ Data Sources

| Dataset | Description | Source |
|---------|-------------|--------|
| TMC (Terrain Mapping Camera) | Panchromatic topographic images | Chandrayaan-1/2 |
| OHRC (Optical High Resolution Camera) | High-res surface imaging | Chandrayaan-2 |
| DTM (Digital Terrain Model) | Elevation map derived from TMC | ISRO Archives |

---

---

## 🛠 Technologies Used

| Tool | Purpose |
|------|---------|
| Python | Core logic and orchestration |
| OpenCV | Image processing & segmentation |
| NumPy / SciPy | Elevation matrix analysis |
| Matplotlib | Plotting and visualization |
| Rasterio / GDAL (optional) | Elevation/DTM data loading |
| QGIS (optional) | Manual validation and mapping |

---


---

## 🧪 How to Use

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Run App

```bash
python appn.py --input image in tif/jpg/png format --output data/output/boulders.png
```

---

## 📈 Outputs

- `boulders.png`: Detected boulders with dimension annotations
- `landslides.png`: Highlighted regions of potential mass movement
- `heatmap.png`: Risk map showing active zones
- `boulder_stats.csv`: Diameter, area, position data for each boulder
- `report.pdg` : Detailed pdf containg all the  iamges and sats

---

## 💡 Novel Contributions

SOMA is distinct because:

- It integrates **terrain slope + elevation + image morphology**
- It uses **object-based segmentation + pixel geometry** for boulder size estimation
- It includes a **source decoding module** to trace landslide origins
- It is **data-agnostic**: applicable to any Moon region with suitable imagery

---

## ✅ Deliverables Mapping

| Requirement from Hackathon | Addressed by SOMA |
|----------------------------|-------------------|
| Detect Landslides          | ✅ Terrain slope + elevation-based |
| Detect Boulders            | ✅ Contour + shadow segmentation |
| Estimate Boulder Stats     | ✅ Diameter, area, location |
| Annotated Map              | ✅ Images with overlays |
| Novel Algorithm            | ✅ Fusion of slope, shadow, terrain |
| Region-Agnostic            | ✅ Works globally on lunar surface |

---


## 🧑‍💻 Contributors

- Ashutosh Sharma
- Suryansh
- Gurpreet Arora
- Saumya Ganeshe

---

