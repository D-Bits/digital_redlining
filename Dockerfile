FROM apache/airflow:3.0.1


# Add requirements.txt
COPY requirements.txt /requirements.txt

# Install any additional Python packages if needed
RUN pip install --no-cache-dir -r /requirements.txt

# Copy your DAGs, plugins, or other files if needed
# COPY dags/ /opt/airflow/dags/
# COPY plugins/ /opt/airflow/plugins/

# Set environment variables if needed
# ENV AIRFLOW__CORE__LOAD_EXAMPLES=False

# Expose Airflow webserver port
EXPOSE 8080

# Default command (optional, Airflow base image already sets entrypoint)
# CMD ["webserver"]