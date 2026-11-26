FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY task_manager/ ./task_manager/
COPY config.py ./
COPY migrations/ ./migrations/

CMD ["sh", "-c", "exec gunicorn --bind \"0.0.0.0:${PORT:-8000}\" 'task_manager:create_app()'"]