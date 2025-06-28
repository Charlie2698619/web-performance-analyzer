from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import requests
import mysql.connector
import logging
import json
import os
from dotenv import load_dotenv

load_dotenv() 

# Config from environment variables
API_KEY = os.environ.get("PAGESPEED_API_KEY", "")
URL_TO_PATH = "/opt/airflow/dags/urls.json"

def load_urls():
    with open(URL_TO_PATH, 'r') as f:
        return json.load(f)

DB_CONFIG = {
    'host': os.environ.get("MYSQL_HOST"),
    'database': os.environ.get("MYSQL_DB"),
    'user': os.environ.get("MYSQL_USER", "devcharlie"),
    'password': os.environ.get("MYSQL_PASSWORD", "devcharlie"),
    'port': int(os.environ.get("MYSQL_PORT", 3307))

}

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2025, 6, 16),
    'end_date': datetime(2025, 6, 24),
    'retries': 2,
    'retry_delay': timedelta(minutes=1),
    'email_on_failure': True,
    'email_on_retry': False,
    'email': ['devcharlie2698619@gmail.com']
}

dag = DAG(
    'pagespeed_collection_dag',
    default_args=default_args,
    description='Collect PageSpeed and Core Web Vitals data hourly for 7 days',
    schedule_interval='@hourly',
    catchup=True,
    tags=['performance', 'pagespeed'],
)

# Safe nested key getter
def safe_get(d, *keys):
    for key in keys:
        if isinstance(d, dict):
            d = d.get(key)
        else:
            return None
    return d

def fetch_pagespeed_metrics(url):
    endpoint = 'https://www.googleapis.com/pagespeedonline/v5/runPagespeed'
    params = {
        'url': url,
        'strategy': 'desktop',
        "category": ["performance", "accessibility", "best-practices", "seo"]
    }
    if API_KEY:
        params['key'] = API_KEY

    logging.info(f"📡 Fetching PageSpeed data for {url}")
    response = requests.get(endpoint, params=params)
    data = response.json()

    logging.info(f"🔍 Top-level keys from PageSpeed API: {list(data.keys())}")
    logging.info(f"🧪 Lighthouse sample: {json.dumps(data.get('lighthouseResult', {}), indent=2)[:1000]}...")

    metrics = {
        'url': url,
        'fetch_time': safe_get(data, 'lighthouseResult', 'fetchTime').replace('T', ' ').replace('Z', '') if safe_get(data, 'lighthouseResult', 'fetchTime') else None,
        'performance': safe_get(data, 'lighthouseResult', 'categories', 'performance', 'score'),
        'accessibility': safe_get(data, 'lighthouseResult', 'categories', 'accessibility', 'score'),
        'best_practices': safe_get(data, 'lighthouseResult', 'categories', 'best-practices', 'score'),
        'seo': safe_get(data, 'lighthouseResult', 'categories', 'seo', 'score'),
        'lcp': safe_get(data, 'loadingExperience', 'metrics', 'LARGEST_CONTENTFUL_PAINT_MS', 'percentile'),
        'fid': safe_get(data, 'loadingExperience', 'metrics', 'FIRST_INPUT_DELAY_MS', 'percentile'),
        'cls': safe_get(data, 'loadingExperience', 'metrics', 'CUMULATIVE_LAYOUT_SHIFT_SCORE', 'percentile'),
    }

    logging.info(f"📦 Collected metrics:\n{json.dumps(metrics, indent=2)}")
    return metrics

def store_metrics_in_db():
    

    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS pagespeed_results (
            id INT AUTO_INCREMENT PRIMARY KEY,
            url VARCHAR(255),
            fetch_time DATETIME,
            performance FLOAT,
            accessibility FLOAT,
            best_practices FLOAT,
            seo FLOAT,
            lcp FLOAT,
            fid FLOAT,
            cls FLOAT
        )
    """)

    insert_query = """
        INSERT INTO pagespeed_results (
            url, fetch_time, performance, accessibility, best_practices, seo, lcp, fid, cls
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    urls = load_urls()
    for url in urls:
        metrics = fetch_pagespeed_metrics(url)
        if metrics["fetch_time"] is None:
            logging.warning(f"⚠️ No fetch time for URL: {url}, skipping insertion.")
            continue

        cursor.execute(insert_query, (
            metrics['url'],
            metrics['fetch_time'],
            metrics['performance'],
            metrics['accessibility'],
            metrics['best_practices'],
            metrics['seo'],
            metrics['lcp'],
            metrics['fid'],
            metrics['cls'],
        ))                                                  

    conn.commit()
    cursor.close()
    conn.close()
    logging.info("✅ Data inserted into MySQL successfully.")

collect_task = PythonOperator(
    task_id='collect_and_store_pagespeed',
    python_callable=store_metrics_in_db,
    dag=dag,
)
