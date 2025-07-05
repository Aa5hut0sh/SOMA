
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
- 🖥️ **Modern UI** for visualization and image upload

---


---

## 🛠 Technologies Used

### 🔧 Backend
| Tool | Purpose |
|------|---------|
| Python | Core logic and orchestration |
| OpenCV | Image processing & segmentation |
| NumPy / SciPy | Elevation matrix analysis |
| Matplotlib | Plotting and visualization |
| Rasterio / GDAL (optional) | Elevation/DTM data loading |

### 🎨 Frontend
| Tool | Purpose |
|------|---------|
| HTML/CSS | Web page structure and styling |
| JavaScript | Client-side interactivity |
| Flask | Web framework to connect backend and frontend |
| Bootstrap (optional) | UI framework for responsive design |

---


---

## 🧪 How to Use locally

```bash
git clone https://github.com/your-username/SOMA-main.git
cd SOMA
pip install -r requirements.txt
python app.py
```


---

## 📈 Outputs

- `boulders.png`: Detected boulders with dimension annotations
- `landslides.png`: Highlighted regions of potential mass movement
- `heatmap.png`: Risk map showing active zones
- `boulder_stats.csv`: Diameter, area, position data for each boulder
- `report.pdf`: Pdf file containing all stats and generated images

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

## 📊 Estimated Implementation Cost

- Open-source tools only (Python, Flask, OpenCV, etc.)
- ₹0 for local execution
- Optional ₹1,000/month for Google Colab Pro (for training or cloud compute)
- Chandrayaan datasets available from ISRO archive

---

## 🧑‍💻 Contributors

- Ashutosh Sharma – Team Leader
- Gurpreet Arora
- Suryansh
- Saumya Ganeshe

---
