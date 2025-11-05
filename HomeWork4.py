documents = [
    {'type': 'passport', 'number': '2207 876234', 'name': 'Василий Гупкин'},
    {'type': 'invoice',  'number': '11-2',        'name': 'Геннадий Покемонов'},
    {'type': 'insurance','number': '10006',       'name': 'Аристарх Павлов'},
]

directories = {
    '1': ['2207 876234', '11-2'],
    '2': ['10006'],
    '3': []
}

#Логика
def get_owner_by_number(doc_number: str, docs: list[dict]) -> str | None:
    doc_number = doc_number.strip()
    for doc in docs:
        if doc.get('number') == doc_number:
            return doc.get('name')
    return None

def get_shelf_by_number(doc_number: str, dirs: dict[str, list[str]]) -> str | None:
    doc_number = doc_number.strip()
    for shelf, numbers in dirs.items():
        if doc_number in numbers:
            return shelf
    return None

def handle_command_p() -> None:
    doc_number = input("\nВведите номер документа:\n").strip()
    owner = get_owner_by_number(doc_number, documents)
    if owner:
        print(f"\nРезультат:\nВладелец документа: {owner}")
    else:
        print("\nРезультат:\nДокумент с таким номером не найден.")

def handle_command_s() -> None:
    doc_number = input("\nВведите номер документа:\n").strip()
    shelf = get_shelf_by_number(doc_number, directories)
    if shelf:
        print(f"\nРезультат:\nДокумент хранится на полке: {shelf}")
    else:
        print("\nРезультат:\nДокумент с таким номером не найден на полках.")

def main_loop() -> None:
    HELP = (
        "\nДоступные команды:\n"
        "  p  — владелец по номеру документа\n"
        "  s  — (необяз.) полка по номеру документа\n"
        "  h  — помощь\n"
        "  q  — выход\n"
    )
    print(HELP)
    while True:
        cmd = input("\nВведите команду:\n").strip().lower()
        if cmd == 'q':
            print("Выход. Пока!")
            break
        elif cmd == 'p':
            handle_command_p()
        elif cmd == 's':
            handle_command_s()
        elif cmd == 'h' or cmd == 'help':
            print(HELP)
        else:
            print("Неизвестная команда. Наберите 'h' для помощи.")

if __name__ == "__main__":
    main_loop()
