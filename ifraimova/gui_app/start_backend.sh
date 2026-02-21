#!/bin/bash
# Скрипт для запуска бэкенда

cd "$(dirname "$0")"

echo "Активация виртуального окружения..."
source venv/bin/activate

echo "Проверка Python..."
which python3

echo "Запуск сервера..."
cd backend
python3 server.py