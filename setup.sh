#!/bin/bash

# Цвета для вывода
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${GREEN}Настройка MOOSA AI...${NC}"

# Проверка наличия Python
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Python 3 не установлен. Пожалуйста, установите Python 3.${NC}"
    exit 1
fi

# Создание виртуального окружения
echo -e "${YELLOW}Создание виртуального окружения...${NC}"
python3 -m venv python_env

# Активация виртуального окружения
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    source python_env/Scripts/activate
else
    source python_env/bin/activate
fi

# Установка зависимостей
echo -e "${YELLOW}Установка зависимостей...${NC}"
pip install --upgrade pip
pip install -r requirements.txt

# Создание необходимых директорий
echo -e "${YELLOW}Создание директорий...${NC}"
mkdir -p data media output logs

# Копирование конфигурационных файлов
echo -e "${YELLOW}Настройка конфигурации...${NC}"
if [ ! -f .env ]; then
    cp config/.env.example .env
    echo -e "${GREEN}Создан файл .env. Пожалуйста, отредактируйте его, добавив необходимые переменные окружения.${NC}"
fi

# Проверка наличия Google Sheets credentials
if [ ! -f config/credentials.json ]; then
    if [ -f config/credentials.json.example ]; then
        cp config/credentials.json.example config/credentials.json
        echo -e "${YELLOW}Создан файл credentials.json. Пожалуйста, замените его на ваши учетные данные Google Sheets.${NC}"
    else
        echo -e "${YELLOW}Файл credentials.json.example не найден. Пожалуйста, добавьте ваши учетные данные Google Sheets в config/credentials.json${NC}"
    fi
fi

# Проверка наличия OpenAI API ключа
if ! grep -q "OPENAI_API_KEY" .env; then
    echo -e "${YELLOW}ВНИМАНИЕ: OPENAI_API_KEY не найден в .env файле. Добавьте его для использования AI-powered генерации контента.${NC}"
fi

# Установка прав на выполнение
chmod +x main.py
chmod +x scripts/*.py

echo -e "${GREEN}Настройка завершена!${NC}"
echo -e "${YELLOW}Для начала работы:${NC}"
echo "1. Активируйте виртуальное окружение:"
echo "   source python_env/bin/activate  # Linux/Mac"
echo "   python_env\\Scripts\\activate  # Windows"
echo "2. Запустите основной скрипт:"
echo "   python main.py"
echo -e "${YELLOW}Для получения дополнительной информации, обратитесь к документации в docs/ директории.${NC}" 