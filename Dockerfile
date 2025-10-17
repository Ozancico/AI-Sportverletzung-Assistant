FROM python:3.12-slim
ENV PYTHONDONTWRITEBYTECODE=1     PYTHONUNBUFFERED=1
WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt &&     pip install --no-cache-dir gunicorn
COPY . .
ENV PORT=8080
EXPOSE 8080
CMD gunicorn -w 2 -k gthread -t 120 -b 0.0.0.0: app:app
