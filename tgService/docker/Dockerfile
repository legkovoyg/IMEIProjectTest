FROM python:3.12-slim

RUN apt-get update && apt-get install -y build-essential && rm -rf /var/lib/apt/lists/*
WORKDIR /app
# Копируем файлы с зависимостями
COPY pyproject.toml poetry.lock ./
RUN pip install --upgrade pip && pip install poetry
RUN poetry config virtualenvs.create false
RUN poetry install --no-root



# Копируем исходный код проекта
COPY . .

EXPOSE 8003

CMD ["python", "main.py"]
