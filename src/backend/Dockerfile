FROM tiangolo/uvicorn-gunicorn:python3.9

RUN mkdir -p /opt/api
WORKDIR /opt/api

COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY main.py .
COPY data/ data/
COPY ml/ ml/
COPY data/ data/
COPY fhir/data_ingest.py .
COPY fhir/fhir_data_access.py .
COPY fhir/data_ingest_csv.py .

EXPOSE 5000

# https://fastapi.tiangolo.com/deployment/server-workers/
ENTRYPOINT ["gunicorn" , "-k uvicorn.workers.UvicornWorker", "--bind=0.0.0.0:5000", "--threads=2", "--workers=1", "main:app"]