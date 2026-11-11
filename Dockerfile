FROM python:3.13-slim
WORKDIR /app
RUN useradd app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY app ./app
USER app
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "app.main:create_app()"]