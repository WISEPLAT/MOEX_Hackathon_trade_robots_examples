# Официальный образ Python
FROM python:3.9-alpine

# Установка зависимостей
ADD requirements.txt /app/requirements.txt
RUN pip install --upgrade pip
RUN pip install -r /app/requirements.txt

# Копирование исходного кода
ADD . /app

# Рабочая директория
WORKDIR /app

# Запуск скрипта на Python
CMD ["python", "app/main.py"]