import csv
import sys
from typing import List, Dict


def read_clients_from_csv(file_path: str) -> List[Dict[str, str]]:
#Загружаем файл в словарь
    clients: List[Dict[str, str]] = []

    with open(file_path, "r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            clients.append(row)

    return clients


def normalize(value: str) -> str:
#Нормализуем вид
    if value is None:
        return ""
    return str(value).strip().lower()


def parse_int(value) -> int:
#Нормализует к целому числу
    if value is None:
        return 0

    text = str(value).strip().replace(",", ".")
    if text == "":
        return 0

    try:
        return int(float(text))
    except ValueError:
        return 0


def sex_to_russian(sex: str) -> str:
#Определяет гендер
    s = normalize(sex)
    if s == "female":
        return "женского"
    if s == "male":
        return "мужского"
    return "неопределённого"


def verb_for_sex(sex: str) -> str:
#Возвращает правильную форму глагола в зависимости от пола
    s = normalize(sex)
    if s == "female":
        return "совершила"
    if s == "male":
        return "совершил"
    return "совершил(а)"


def device_phrase(device_type: str, browser: str) -> str:
#Формирует фразу про устройство + браузер.

    t = normalize(device_type)
    browser_name = browser.strip()

    if t == "mobile":
        return f"мобильного браузера {browser_name}"
    if t == "tablet":
        return f"планшета через браузер {browser_name}"
    if t in ("laptop", "notebook"):
        return f"ноутбука через браузер {browser_name}"
    if t in ("pc", "desktop", "computer"):
        return f"компьютера через браузер {browser_name}"

    # запасной вариант, если в данных встретится что-то необычное
    original = device_type.strip() if device_type is not None else "устройства"
    return f"устройства ({original}) через браузер {browser_name}"


def build_description(row: Dict[str, str]) -> str:
#Преобразование данных и формирование текстового описания по шаблону.
    name = (row.get("name") or "").strip()
    sex = row.get("sex") or ""
    age_raw = row.get("age")
    bill_raw = row.get("bill")
    device_type = row.get("device_type") or ""
    browser = row.get("browser") or ""
    region = (row.get("region") or "").strip()

    age = parse_int(age_raw)
    bill = parse_int(bill_raw)

    sex_word = sex_to_russian(sex)  # 'женского / мужского пола'
    verb = verb_for_sex(sex)
    device_part = device_phrase(device_type, browser)

    description = (
        f"Пользователь {name} {sex_word} пола, {age} лет {verb} покупку "
        f"на {bill} у.е. с {device_part}. "
        f"Регион, из которого совершалась покупка: {region}."
    )

    return description


def write_descriptions_to_txt(descriptions: List[str], file_path: str) -> None:
#Запись всех описаний в единый TXT-файл (по одному в строке)
    with open(file_path, "w", encoding="utf-8") as f:
        for line in descriptions:
            f.write(line + "\n")


def main() -> None:
#Точка входа и запуск программы
    if len(sys.argv) >= 3:
        input_csv = sys.argv[1]
        output_txt = sys.argv[2]
    else:
        input_csv = input("Введите путь к входному CSV-файлу: ").strip()
        output_txt = input("Введите путь к выходному TXT-файлу: ").strip()

    clients = read_clients_from_csv(input_csv)

    descriptions: List[str] = []
    for row in clients:
        description = build_description(row)
        descriptions.append(description)

    write_descriptions_to_txt(descriptions, output_txt)
    print(f"Готово. В файл '{output_txt}' записано {len(descriptions)} строк(и).")


if __name__ == "__main__":
    main()

""" 
Путь к исходному файлу: resources/web_clients_correct-старое.csv
Путь к новому файлу: resources/output.txt
"""