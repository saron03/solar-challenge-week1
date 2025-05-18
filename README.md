# Strategic Solar Investment Analysis  
*Week 0 Challenge – Solar Data Discovery*

## Project Summary

<<<<<<< HEAD
This project supports **MoonLight Energy Solutions** in identifying promising locations for solar energy investments across Benin, Sierra Leone, and Togo. By analyzing environmental and solar sensor data, the goal is to provide data-driven insights to guide sustainable and efficient solar panel deployment.

---

## Business Objective

- Analyze solar irradiance, temperature, humidity, wind, and related environmental data.
- Identify high-potential regions for solar panel installations.
- Help MoonLight optimize their investment strategy and operational sustainability.

---

## Dataset Overview

Datasets include hourly measurements of:

- Solar irradiance (GHI, DNI, DHI)
- Module sensor data (ModA, ModB)
- Weather variables (temperature, humidity, wind speed/direction, pressure, precipitation)
- Sensor cleaning flags
- Timestamped records

Files analyzed:  
`benin-malanville.csv`, `sierraleone-bumbuna.csv`, `togo-dapaong_qc.csv` (stored locally and gitignored).

---

## Project Structure & Workflow

- **Task 1:** Git setup, Python environment, CI/CD, and project organization.  
- **Task 2:** Data profiling, cleaning, and exploratory analysis per country using Jupyter notebooks.  
- **Task 3:** (In progress) Cross-country comparison with statistical analysis and visual summaries.  
- **Bonus:** Planned Streamlit dashboard for interactive data exploration.

---

## Getting Started

1. Clone repo and enter directory:  
   ```
   git clone https://github.com/saron03/solar-challenge-week1.git
   cd solar-challenge-week1
   ```
2. Create and activate Python virtual environment:
    ```
    python -m venv .venv
    source .venv/bin/activate  # Windows: .venv\Scripts\activate
    ```
3. Install dependencies:
    ```
    pip install -r requirements.txt
    ```
4. Place raw CSV data in a local data/ folder (not tracked by git).
5. Launch Jupyter to explore notebooks:
    ```
    jupyter notebook notebooks/
    ```
## Next Steps
- Complete cross-country comparison analysis.

- Develop and deploy the interactive Streamlit dashboard.

- Compile final reports with strategic recommendations.
