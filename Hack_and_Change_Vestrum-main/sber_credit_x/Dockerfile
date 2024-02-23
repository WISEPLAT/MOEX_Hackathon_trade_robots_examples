# Используйте официальный образ Python как базовый
FROM python:3.11-slim

# Создание рабочей директории
WORKDIR /code

# Копирование файлов проекта и файла окружения
COPY main /code/
COPY .env.docker /code/.env

# Установка зависимостей
RUN pip install --no-cache-dir -r requirements.txt

# Сбор статических файлов
RUN python manage.py collectstatic --noinput

# Команда для запуска сервера с Gunicorn
CMD ["gunicorn", "sber_credit_x.wsgi:application", "-b", "0.0.0.0:8000"]
