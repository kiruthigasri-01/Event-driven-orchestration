import psycopg2
import requests
import glob

# -----------------------------
# FETCH LATEST AIRFLOW LOG
# -----------------------------

log_files = glob.glob(
    r"C:\project\airflow_logs\*.log"
)

latest_log = max(log_files, key=lambda x: x)

with open(latest_log, "r") as f:
    error_log = f.read()

print("\n================ AIRFLOW LOG ================\n")
print(error_log)

# -----------------------------
# FETCH BUSINESS RULES
# -----------------------------

conn = psycopg2.connect(
    host="localhost",
    database="airflow_db",
    user="postgres",
    password="Dtsk2468@",
    port="5432"
)

cursor = conn.cursor()

cursor.execute("SELECT * FROM business_rules")

rules = cursor.fetchall()

business_context = "\n".join([str(rule) for rule in rules])

print("\n================ BUSINESS RULES ================\n")
print(business_context)

cursor.close()
conn.close()

# -----------------------------
# CREATE PROMPT
# -----------------------------

prompt = f"""
You are a senior DataOps engineer.

Analyze the ETL failure.

Airflow Error Log:
{error_log}

Business Rules:
{business_context}

Classify issue into:
1. DATA_QUALITY
2. BUSINESS_RULE_CHANGE
3. TECH_FAILURE

Return:
- classification
- reason
- suggested_fix
"""

print("\n================ LLM PROMPT ================\n")
print(prompt)

# -----------------------------
# CALL OLLAMA
# -----------------------------

response = requests.post(
    "http://localhost:11434/api/generate",
    json={
        "model": "llama3",
        "prompt": prompt,
        "stream": False
    }
)

result = response.json()

print("\n================ LLM RESPONSE ================\n")
print(result["response"])