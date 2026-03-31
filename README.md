# Hyrox Data Analysis

## Table of Contents
- [General Info](#general-info)
- [Technologies Used](#technologies-used)
- [Features](#features)
- [Setup](#setup)
- [Usage](#usage)
- [Project Status](#project-status)
- [Room for Improvement](#room-for-improvement)
- [Contact](#contact)

## General Info
This project analyzes Hyrox athletes’ results, focusing on **total time** in the **Open** and **Pro** categories for both men and women.  
The goal is to show the differences between the **Top 10% performers** and the rest of the participants, and to visualize the results.

## Technologies Used
- Python 3.x  
- pandas  
- matplotlib  
- seaborn  

## Features
- Load data from a CSV and select relevant columns (`gender`, `division`, `total_time`).  
- Convert total time to seconds and calculate the Top 10% in each category (gender + division).  
- Display a pivot table showing average times of Top vs. Rest performers.  
- Generate bar charts comparing Top 10% and the rest of participants for Male and Female in Open and Pro.

## Setup
1. Install Python 3.x on your computer.  
2. Install required libraries:  
```bash
pip install pandas matplotlib seaborn
``` 
3. Place your CSV file in the folder `data/RawData.csv`.  

## Usage
1. Run `load_and_plot.py` to load the data, calculate the Top 10%, display the pivot table, and generate the charts.  
2. Results will appear in the console, and the plots will open in a matplotlib window.  
3. Note: The project uses two scripts:  
   - `load_data.py` — loads the CSV, prepares the data, calculates Top 10%.  
   - `plot_top_vs_rest.py` — generates the pivot table and bar charts for visualization.

## Project Status
The project is ready to use and demonstrates basic analysis of Hyrox results.  
It is suitable for a **Data Analyst / Data QA portfolio**.

## Room for Improvement
- Add percentage difference labels above bars.  
- Save plots as PNG files.  
- Analyze data by station/segment (if available).  
- Extend analysis to more categories or compare men vs women across different events.

## Contact
- GitHub: [Your GitHub](https://github.com/damiankiwi)