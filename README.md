# 🌾 Optimal Agricultural Crop Planning

**Operations Research: Linear & Goal Programming Approach**

This repository contains the First Review and Final Implementation files for our Agricultural Operations Research project. The project aims to build a mathematical decision-support system that helps farmers optimally allocate cultivable land among various crops while strictly adhering to resource limitations (land, fertilizer, pesticide).

## 📖 Repository Description
This repository serves as the complete codebase and documentation for our **Operations Research (OR) Project: Optimal Agricultural Crop Planning**. 

Agriculture in India is highly constrained by limited cultivable land, strict fertilizer budgets, and environmental pesticide limits. Instead of relying on traditional farming intuition, this project treats crop planning as a strict mathematical optimization problem. By leveraging **Linear Programming (LP)** and **Goal Programming (GP)** algorithms on 23 years of historical crop yield data, this system mathematically determines the absolute best way to allocate land to different crops. 

The ultimate goal of this repository is to provide a deployable **Decision-Support System (via Streamlit)** that empowers farmers and agricultural planners to maximize their crop production while safely balancing environmental and resource limits.

## 📊 About the Data & Optimization
Traditional crop planning often relies on intuition. By using **Operations Research (OR)**, we can mathematically guarantee the most efficient use of resources. We use 23 years of historical Indian agricultural data to extract yield and resource parameters. 

Our optimization engine utilizes:
1. **Linear Programming (LP):** To find the absolute maximum theoretical production.
2. **Goal Programming (GP):** To balance multiple, often conflicting real-world targets (e.g., hitting a specific production quota while strictly minimizing chemical/pesticide usage).

## 🚀 Live Dashboard
An interactive Streamlit dashboard is built to make the optimization accessible to non-technical users.
- View Exploratory Data Analysis (EDA)
- Run the LP and GP Solvers (Final Review)
- Compare Resource Utilization tradeoffs interactively

## 👥 Meet the Team
This project is a collaborative effort by our team. Each member is responsible for a core module of the pipeline:

| Team Member | GitHub Profile | Core Focus & Responsibilities |
| :--- | :--- | :--- |
| **Vignesh V S** | [@VigneshVS2005](https://github.com/VigneshVS2005) | Linear Programming Model, Decision Variables, Objective Functions & LP Solver Code |
| **Karthick Ruban** | [@Karthickruban](https://github.com/Karthickruban) | Goal Programming Model, Deviation Variables, Goal Weighting & GP Solver Code |
| **Hariprakash** | [@Hariprakash024](https://github.com/Hariprakash024) | Streamlit UI Development, Plotly Visualizations, System Integration & Dashboard |
| **Sanjay Senthil** | [@sanjaysenthil17](https://github.com/sanjaysenthil17) | Dataset Acquisition, Data Cleaning, Exploratory Data Analysis & Parameter Calculations |

Please see [CONTRIBUTORS.md](CONTRIBUTORS.md) for more details.

## 🛠️ Tech Stack
- **Languages:** Python
- **Data Processing:** Pandas, NumPy
- **Operations Research Solvers:** PuLP / Google OR-Tools
- **UI & Visualization:** Streamlit, Plotly Express
