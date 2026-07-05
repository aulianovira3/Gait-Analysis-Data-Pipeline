# End-to-End Project: Gait Analysis Data Pipeline & Dashboard

![Dashboard Preview](assets/dashboard_screenshot.png) *(Note: Replace this path if your screenshot is named differently, or remove this line if not using an image)*

🔗 **[Link to Interactive Looker Studio Dashboard][https://datastudio.google.com/u/0/reporting/47751361-d6fc-4936-9f71-53a858f6d0e4/page/60g2F/edit]**

## 1. Executive Summary
This project aims to build an end-to-end data pipeline architecture to process, analyze, and visualize interdisciplinary Gait Analysis data. By leveraging a combination of Data Engineering techniques using Python and SQL, alongside Data Visualization through Google Looker Studio, this project successfully processed large-scale data (**Big Data**) consisting of **15,974,882 rows** of raw signal data originating from 31 test subjects (Record ID S01 to S31).

The primary focus of this analysis is to prove the phenomenon of muscle electrical asymmetry (Muscle Asymmetry) and perform gait biomechanics validation to produce an accurate, intuitive clinical report that is ready for remote reporting needs.

---

## 2. Tech Stack Summary (Technology Matrix)
Below are the primary technologies utilized throughout the data lifecycle of this project:

| Core Function | Technology | Project Implementation |
| :--- | :--- | :--- |
| **Data Engineering & Cleansing** | Python (Pandas, NumPy, Glob) | Automated batch file extraction, noise removal, and implementation of *Min-Max Normalization* on sEMG signals. |
| **Data Storage & Aggregation** | SQL (SQLite) | Structured architecture storage (15+ million rows) and writing aggregation queries for subject-level summary extraction. |
| **Data Visualization & UI/UX** | Google Looker Studio | Interactive dashboard design, time-series visualization, and unified axis scaling adjustments for actionable insights. |

---

## 3. Data Pipeline Architecture
The data workflow in this project is divided into three distinct, structured stages:

1. **Data Extraction & Engineering (Python):** The stage of reading time-based raw signal files, performing initial data cleaning, and applying mathematical transformations such as sensor amplitude normalization.
2. **Data Storage & Transformation (SQL/SQLite):** Loading the processed data into the relational database `gait_analysis_bigdata.db` and executing advanced aggregation queries to summarize macro features per subject.
3. **Data Visualization & UI/UX Design (Looker Studio):** Connecting the relational database to the visualization platform to build an interactive dashboard for clinical and management stakeholders.

---

## 4. Stage 1: Raw Signal Extraction and Processing (Sensor Fusion)

### 4.1 Sensor Component Description
This project implements the concept of *Sensor Fusion* by unifying three types of physical sensors that record subject activity simultaneously:
* **Surface Electromyography (sEMG):** Captures micro-volt electrical signals from muscles to measure the contraction intensity of the front thigh muscle (Rectus Femoris / REC) and rear thigh muscle (Hamstring / HAM) on both the left (LT) and right (RT) legs.
* **Goniometer (Gonio):** Measures joint kinematics in the form of real-time rotational angle changes at the right knee joint (`gonio RT KNEE`) and right hip joint (`gonio RT HIP`).
* **Basograph (Baso):** Plantar pressure sensors attached to the left foot sole (`baso LT FOOT`) and right foot sole (`baso RT FOOT`) to detect physical foot contact with the floor during the gait cycle.

### 4.2 sEMG Signal Amplitude Normalization
Raw sEMG electrical signals have baseline amplitude variations that are heavily influenced by skin thickness and physiological conditions across individuals. To ensure a fair comparison, a *Min-Max Normalization* technique was executed using a Python script to map all signal values into a uniform scale of 0.0 to 1.0 (where 0.0 represents complete relaxation and 1.0 represents Maximum Voluntary Contraction/MVC). 

```text
Signal_Norm = (Signal - Signal_Min) / (Signal_Max - Signal_Min)
