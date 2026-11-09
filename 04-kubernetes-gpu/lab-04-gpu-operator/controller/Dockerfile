FROM python:3.13-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY gpu_operator.py .
USER 65532:65532
ENTRYPOINT ["python", "-u", "gpu_operator.py"]
