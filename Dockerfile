FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
ENV PYTHONPATH=/app/src
EXPOSE 8888

CMD ["python", "src/presentation/main.py"]