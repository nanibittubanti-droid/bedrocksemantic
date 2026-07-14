FROM python:3.12-slim

RUN adduser --disabled-password --gecos '' appuser
WORKDIR /home/appuser

COPY requirements.txt .
RUN python -m pip install --upgrade pip && \
    python -m pip install --no-cache-dir -r requirements.txt

COPY app ./app
RUN chown -R appuser:appuser /home/appuser
USER appuser

ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/home/appuser

ENTRYPOINT ["python", "-m", "app.main"]
