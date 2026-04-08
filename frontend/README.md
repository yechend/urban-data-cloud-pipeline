# Frontend

## Overview
This folder contains the frontend components for data visualisation and analysis.

The visualisation layer is implemented in Python using Jupyter-style workflows, with interactive elements (e.g., buttons and maps) to explore different urban data scenarios.

A combined interface integrates multiple visualisations into a unified interactive frontend.

---

## Scenarios & Visualisation Modules

### 1. Population Analysis (SUDO)
Generates bar charts and interactive maps showing regional population distribution.

**Files:**
populationVisual.py

---

### 2. Traffic Congestion
Visualises road congestion patterns and supports statistical analysis.

- `path1.py` – Displays congestion routes on an interactive map  
- `congestion_statistic.py` – Generates bar charts based on selected date and area ID  

> Note: Area IDs can be obtained from the map generated in `path1.py`

**Files:**
path1.py
congestion_statistic.py

---

### 3. Pedestrian Activity
Provides multiple visualisations for pedestrian movement across Melbourne.

- Hourly pedestrian counts  
- Sensor-based comparisons  
- Sensor location mapping  
- Spatial distribution visualisation  

**Files:**
ped_Visual.py

---

### 4. Social Media (Mastodon)
Performs statistical analysis on harvested social media data and generates visual outputs.

**Files:**
mastodon_helper.py

---

### 5. Train Service Analysis
Visualises train network and station-level information.

- Interactive maps for railway lines and station locations  
- Pre-generated plots stored in the `trainservice/` folder  

> Note: Visualisations are based on previously collected data due to infrastructure limitations during development.

**Files:**
trainservice/
all_station_info.html
line_railway.html

---

## Features

- Interactive visualisations using maps and charts  
- Scenario-based modular design  
- Integration of multiple data sources (population, traffic, transport, social media)  
- Support for exploratory data analysis  

---

## Notes

- Visualisations are designed to work with data processed by the backend pipeline  
- Some outputs rely on precomputed datasets due to infrastructure constraints  
- The frontend focuses on **insight generation and user interaction**