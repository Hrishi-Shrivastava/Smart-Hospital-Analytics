# Smart Hospital Emergency Room Analytics System

## Overview
The Smart Hospital Emergency Room Analytics System is a data-driven decision-support application designed to optimize patient triage and medical resource allocation in high-volume medical facilities. Built entirely in Python, this system ingests patient data, applies a weighted priority algorithm for algorithmic triage, and utilizes statistical analysis to forecast real-time hospital resource requirements.

## Features
* **Automated Data Pipeline:** Generates, cleans, and validates synthetic patient records, handling anomalies such as missing values and biologically impossible vitals.
* **Algorithmic Patient Triage:** Calculates a composite Priority Score based on critical physiological thresholds (Oxygen, Heart Rate, Temperature, Age) to categorize patients into Normal, Moderate, High Priority, and Critical tiers.
* **Resource Forecasting:** Predicts daily and peak-hour staffing requirements (doctors) and ward bed occupancy based on patient inflow trends.
* **Emergency Alert Protocol:** Monitors hospital saturation and triggers automated alert levels (Green, Yellow, Orange, Red) based on the volume of critical patients.
* **Interactive Dashboard:** A live Streamlit interface that renders Key Performance Indicators (KPIs), clinical visualizations, and automated AI-driven administrative recommendations.
* **Automated Reporting:** Generates a comprehensive, multi-sheet Excel report (`hospital_analytics_report.xlsx`) detailing raw records, priority calculations, and resource requirements.

## Technologies Used
* **Language:** Python 3.x
* **Data Manipulation:** `pandas`, `numpy`
* **Data Visualization:** `matplotlib`, `seaborn`
* **Web Framework / UI:** `streamlit`
* **File I/O:** `openpyxl`

## Installation

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/your-username/your-repository-name.git](https://github.com/your-username/your-repository-name.git)
   cd your-repository-name
