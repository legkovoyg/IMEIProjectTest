# Используем официальный образ Python 3.12-slim
FROM python:3.12-slim

# Устанавливаем системные зависимости, необходимые для сборки пакетов (например, psycopg2)
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app

# Копируем файлы poetry (pyproject.toml и poetry.lock) для кэширования установки зависимостей
COPY pyproject.toml poetry.lock* /app/

# Устанавливаем Poetry и обновляем pip
RUN pip install --upgrade pip && pip install poetry

# Отключаем создание виртуального окружения (чтобы зависимости устанавливались глобально)
RUN poetry config virtualenvs.create false

# Устанавливаем зависимости без dev-пакетов
RUN poetry install --no-root

# Копируем оставшийся исходный код в контейнер
COPY . /app

# Если вам нужен .env-файл, можно его также скопировать:
#COPY .env /app/

# Открываем порт 8002, на котором будет работать ваше FastAPI-приложение
EXPOSE 8002

# Запускаем приложение через uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8002"]
