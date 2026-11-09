FROM python:3.13-slim
WORKDIR /app
COPY metrics.py .
USER 65532:65532
EXPOSE 9400
CMD ["python", "-u", "metrics.py"]
