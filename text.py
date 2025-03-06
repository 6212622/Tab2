import re

# Читаем данные из файла
with open("tt.txt", "r", encoding="utf-8") as f:
    hex_data = f.read()

# Преобразуем HEX в бинарный файл
try:
    binary_data = bytes.fromhex(hex_data)  # Конвертируем в бинарные данные
    with open("photo.bmp", "wb") as img:
        img.write(binary_data)  # Записываем в файл
    print("✅ Файл успешно декодирован!")
except ValueError as e:
    print(f"❌ Ошибка конвертации: {e}")
