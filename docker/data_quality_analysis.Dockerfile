FROM python:3.11-slim

WORKDIR /app
ENV MPLCONFIGDIR=/tmp/matplotlib

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src ./src

CMD ["python", "src/data_quality_analysis.py"]
