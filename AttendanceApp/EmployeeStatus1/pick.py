import re

# Читаем данные из файла
with open("aaa.txt", "r", encoding="utf-8") as f:
    hex_data = f.read().strip()  # Убираем пробелы и переносы строк

# Оставляем только HEX-цифры (0-9, A-F, a-f)
hex_data = re.sub(r'[^0-9A-Fa-f]', '', hex_data)

# Проверяем длину строки
print(f"Очищенная длина строки: {len(hex_data)}")
print(f"Последние 100 символов:\n{hex_data[-100:]}")

# Проверяем последний символ (нет ли там мусора)
if len(hex_data) % 2 != 0 or not hex_data[-1].isalnum():
    print(f"⚠️ Удаляем последний символ: {hex_data[-1]}")
    hex_data = hex_data[:-1]  # Удаляем последний символ

# Преобразуем HEX в бинарный файл
try:
    binary_data = bytes.fromhex(hex_data)  # Конвертируем в бинарные данные
    with open("photo.bmp", "wb") as img:
        img.write(binary_data)  # Записываем в файл
    print("✅ Файл успешно декодирован!")
except ValueError as e:
    print(f"❌ Ошибка конвертации: {e}")
