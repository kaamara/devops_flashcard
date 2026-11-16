FROM python:3.13-slim
WORKDIR /app
RUN useradd --create-home app
RUN apt-get update && apt-get upgrade -y
RUN python -m pip install --upgrade pip setuptools
COPY requirements.txt .
RUN pip install -r requirements.txt
RUN pip uninstall -y pip
COPY app ./app
USER app
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "app.main:create_app()"]