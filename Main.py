import json
import os
from datetime import datetime

# Имя файла, в котором будут храниться заметки
NOTES_FILE = "notes.json"


def load_notes():
    """Загрузка заметок из файла"""
    if not os.path.exists(NOTES_FILE):
        return []
    with open(NOTES_FILE, "r") as file:
        return json.load(file)


def save_notes(notes):
    """Сохранение заметок в файл"""
    with open(NOTES_FILE, "w") as file:
        json.dump(notes, file, ensure_ascii=False, indent=4)


def add_note():
    """Добавление новой заметки"""
    title = input("Введите заголовок заметки: ")
    body = input("Введите тело заметки: ")
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    notes = load_notes()
    note = {"id": len(notes) + 1, "title": title, "body": body, "timestamp": timestamp}
    notes.append(note)
    save_notes(notes)
    print("Заметка успешно сохранена")


def list_notes():
    """Вывод списка всех заметок"""
    notes = load_notes()
    for note in notes:
        print(f"{note['id']}. {note['title']} ({note['timestamp']})")
    if not notes:
        print("Список заметок пуст.")


def view_note():
    """Просмотр отдельной заметки"""
    note_id = int(input("Введите номер заметки для просмотра: "))
    notes = load_notes()
    for note in notes:
        if note["id"] == note_id:
            print(f"Заголовок: {note['title']}")
            print(f"Тело заметки: {note['body']}")
            print(f"Дата создания/изменения: {note['timestamp']}")
            return
    print("Заметка с таким номером не найдена.")


def edit_note():
    """Редактирование заметки"""
    note_id = int(input("Введите номер заметки для редактирования: "))
    notes = load_notes()
    for i, note in enumerate(notes):
        if note["id"] == note_id:
            title = input("Введите новый заголовок заметки: ")
            body = input("Введите новое тело заметки: ")
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            notes[i] = {
                "id": note_id,
                "title": title,
                "body": body,
                "timestamp": timestamp,
            }
            save_notes(notes)
            print("Заметка успешно отредактирована.")
            return
    print("Заметка с таким номером не найдена.")


def delete_note():
    """Удаление заметки"""
    note_id = int(input("Введите номер заметки для удаления: "))
    notes = load_notes()
    for i, note in enumerate(notes):
        if note["id"] == note_id:
            del notes[i]
            save_notes(notes)
            print("Заметка успешно удалена.")
            return
    print("Заметка с таким номером не найдена.")


def filter_notes_by_date():
    """Фильтрация заметок по дате"""
    date_str = input("Введите дату (гггг-мм-дд), чтобы отфильтровать заметки: ")
    try:
        target_date = datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        print("Некорректный формат даты. Пожалуйста, используйте гггг-мм-дд.")
        return

    notes = load_notes()
    filtered_notes = [
        note
        for note in notes
        if datetime.strptime(note["timestamp"], "%Y-%m-%d %H:%M:%S").date()
        == target_date.date()
    ]

    if not filtered_notes:
        print("Заметок за указанную дату не найдено.")
    else:
        for note in filtered_notes:
            print(f"{note['id']}. {note['title']} ({note['timestamp']})")


def main():
    commands = {
        "add": add_note,
        "list": list_notes,
        "view": view_note,
        "edit": edit_note,
        "delete": delete_note,
        "filter": filter_notes_by_date,
        "exit": exit,
    }

    while True:
        print("\nДоступные команды:")
        print("add - добавить заметку")
        print("list - вывести список заметок")
        print("view - просмотреть отдельную заметку")
        print("edit - редактировать заметку")
        print("delete - удалить заметку")
        print("filter - фильтровать заметки по дате")
        print("exit - выход из программы")

        user_input = input("Введите команду: ").strip().lower()

        if user_input in commands:
            commands[user_input]()
        else:
            print("Некорректная команда. Попробуйте ещё раз.")


main()
