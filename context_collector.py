import psycopg2
import glob
import os
import subprocess

# -----------------------------------
# DATABASE CONNECTION
# -----------------------------------

conn = psycopg2.connect(
    host="localhost",
    database="airflow_db",
    user="postgres",
    password="Dtsk2468@",
    port="5432"
)

cursor = conn.cursor()

# -----------------------------------
# FETCH BUSINESS RULES
# -----------------------------------

cursor.execute("SELECT * FROM business_rules")
business_rules = cursor.fetchall()

# -----------------------------------
# FETCH DAG METADATA
# -----------------------------------

cursor.execute("SELECT * FROM dag_metadata")
dag_metadata = cursor.fetchall()

# -----------------------------------
# FETCH INCIDENT HISTORY
# -----------------------------------

cursor.execute("SELECT * FROM incident_history")
incident_history = cursor.fetchall()


# -----------------------------------
# READ DAG CODE FROM DOCKER
# -----------------------------------

dag_code = {}

try:

    dag_list_command = [
        "docker",
        "exec",
        "airflow",
        "find",
        "/opt/airflow/dags",
        "-name",
        "*.py"
    ]

    dag_files = subprocess.check_output(
        dag_list_command
    ).decode().splitlines()

    for dag_file in dag_files:

        dag_name = dag_file.split("/")[-1]

        dag_command = [
            "docker",
            "exec",
            "airflow",
            "cat",
            dag_file
        ]

        dag_content = subprocess.check_output(
            dag_command
        ).decode()

        dag_code[dag_name] = dag_content

except Exception as e:

    dag_code = {
        "error": str(e)
    }

# -----------------------------------
# READ AIRFLOW LOGS
# -----------------------------------


# -----------------------------------
# READ AIRFLOW LOGS FROM DOCKER
# -----------------------------------

try:

    command = [
        "docker",
        "exec",
        "airflow",
        "find",
        "/opt/airflow/logs",
        "-name",
        "*.log"
    ]

    result = subprocess.check_output(command).decode()

    log_paths = result.strip().split("\n")

    latest_log = log_paths[-1]

    print("\nLATEST LOG FILE:\n")
    print(latest_log)

    log_command = [
        "docker",
        "exec",
        "airflow",
        "cat",
        latest_log
    ]

    airflow_logs = subprocess.check_output(
        log_command
    ).decode()

except Exception as e:

    airflow_logs = f"Error reading airflow logs: {e}"

# -----------------------------------
# BUILD CONTEXT OBJECT
# -----------------------------------

context = {
    "business_rules": business_rules,
    "dag_metadata": dag_metadata,
    "incident_history": incident_history,
    "dag_code": dag_code,
    "airflow_logs": airflow_logs
}

# -----------------------------------
# PRINT CONTEXT
# -----------------------------------

print("\n================ CONTEXT ================\n")

for key, value in context.items():

    print(f"\n----- {key.upper()} -----\n")

    print(value)

cursor.close()
conn.close()