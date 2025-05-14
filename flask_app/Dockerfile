FROM python:3.10


WORKDIR /app

COPY flask_app/requirements.txt ./requirements.txt

COPY flask_app/ ./

RUN pip install --no-cache-dir -r requirements.txt




ENV PYTHONPATH=/app
ENV FLASK_APP=flask_app.py


CMD ["python", "flask_app.py"]
