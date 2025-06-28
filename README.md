# 🌐 Web Performance Analyzer for High-Traffic E-commerce Websites

**Goal:** Monitor and analyze Core Web Vitals and PageSpeed Insights of top e-commerce websites hourly over 7 days to identify performance bottlenecks and traffic load patterns.

---

## 🚀 Overview

In the digital economy, **site performance is revenue-critical**. This project leverages the [Google PageSpeed Insights API](https://developers.google.com/speed/docs/insights/v5/get-started) to track Core Web Vitals like LCP, FID, and CLS for high-traffic e-commerce websites.  

As a Data Analyst, this project demonstrates:
- Real-world use of data pipelines with **Airflow**
- **Hourly monitoring** for 7-day window
- Storage in **MySQL** with Docker orchestration
- Insights and reporting in **Power BI** 

---

## 📊 Key Metrics Tracked

| Metric              | Description                                       |
|---------------------|---------------------------------------------------|
| `performance`       | Overall performance score by Lighthouse           |
| `accessibility`     | Usability for all users                           |
| `best_practices`    | Industry coding and delivery best practices       |
| `seo`               | Optimization for search engines                   |
| `lcp`               | Largest Contentful Paint (load responsiveness)    |
| `fid`               | First Input Delay (interactivity)                 |
| `cls`               | Cumulative Layout Shift (visual stability)        |
| `fetch_time`        | Timestamp of API call                             |

---

## ⚙️ Tech Stack

| Layer            | Tools                            |
|------------------|----------------------------------|
| **Orchestration**| Apache Airflow (Dockerized)      |
| **ETL**          | Python, MySQL Connector           |
| **Database**     | MySQL 8 (Docker container)        |
| **Monitoring**   | PageSpeed Insights API            |
| **Visualization**| Power BI    |
| **Deployment**   | Docker Compose                    |

---

## 🧠 Project Structure

```bash
web-performance-analyzer/
│
├── dags/                    # Airflow DAG definition
│   └── pagespeed_collection_dag.py
│
├── docker/                  # Docker + Airflow setup
│   └── docker-compose.yaml
│
├── data/                    # Saved JSON + raw logs
├── scripts/
│   └─ extract.py           # Data extraction from DB
│   
├── dashboard/              # Power BI dashboard
│
├── .env                     # API keys and DB credentials
├── requirements.txt
└── README.md
