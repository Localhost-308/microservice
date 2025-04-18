FROM python:3.10.12-slim
WORKDIR /app
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt
COPY . /app/
EXPOSE 5000
ENV FLASK_APP=src.main.endpoint.app:app
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
