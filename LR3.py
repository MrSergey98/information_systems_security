import tkinter as tk
from tkinter import filedialog, messagebox

alphabet: str = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ ,.!?*+=—-\"`\n"

# Функция шифрования текста
def encode(text: str, a: int = 1, b: int = 1, c: int = 1) -> str:
    decode: str = ""
    for position, symbol in enumerate(text):
        k: int = (a * position**2) + (b * position) + c
        index: int = (alphabet.index(symbol.upper()) - k) % len(alphabet)
        decode += alphabet[index] if symbol.isupper() else alphabet[index].lower()
    return decode


# Функция дешифрования текста
def decode(text: str, a: int = 1, b: int = 1, c: int = 1) -> str:
    encode: str = ""
    for position, symbol in enumerate(text):
        k: int = (a * position**2) + (b * position) + c
        index: int = (alphabet.index(symbol.upper()) + k) % len(alphabet)
        encode += alphabet[index] if symbol.isupper() else alphabet[index].lower()
    return encode


# Функция для шифрования текста с интерфейса
def encrypt_text():
    message = text_input.get("1.0", tk.END).strip()
    if message:
        encrypted_msg = encode(message)
        text_output.delete("1.0", tk.END)
        text_output.insert(tk.END, str(encrypted_msg))
    else:
        messagebox.showwarning("Ошибка", "Поле ввода пусто!")


# Функция для дешифрования текста с интерфейса
def decrypt_text():
    encrypted_message = text_output.get("1.0", tk.END).strip()
    if encrypted_message:
        try:
            decrypted_msg = decode(encrypted_message)
            decrypted_output.delete("1.0", tk.END)
            decrypted_output.insert(tk.END, decrypted_msg)
        except:
            messagebox.showwarning("Ошибка", "Неправильный формат зашифрованного текста!")
    else:
        messagebox.showwarning("Ошибка", "Поле для зашифрованного текста пусто!")


# Функция для загрузки текста из файла
def load_from_file():
    filepath = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
    if filepath:
        with open(filepath, 'r', encoding='utf-8') as file:
            file_content = file.read()
            text_input.delete("1.0", tk.END)
            text_input.insert(tk.END, file_content)


# Функции для работы с контекстным меню
def create_context_menu(widget):
    menu = tk.Menu(widget, tearoff=0)
    menu.add_command(label="Копировать", command=lambda: widget.event_generate("<<Copy>>"))
    menu.add_command(label="Вставить", command=lambda: widget.event_generate("<<Paste>>"))
    menu.add_command(label="Вырезать", command=lambda: widget.event_generate("<<Cut>>"))
    widget.bind("<Button-3>", lambda event: menu.tk_popup(event.x_root, event.y_root))


# Создание окна интерфейса
root = tk.Tk()
root.title("Шифрование и Дешифрование методом Трисемуса")
root['bg'] = '#3c85fa'

# Поле для ввода текста
text_input_label = tk.Label(root, text="Введите текст для шифрования:")
text_input_label.pack(pady=5)

# Кнопка для загрузки текста из файла
load_button = tk.Button(root, text="Загрузить текст из файла", command=load_from_file)
load_button.pack(pady=5)

TEXT_BACKGROUND_COLOR = '#78a6f0'
TEXT_FONT = 18

# Поле для ввода текста
text_input = tk.Text(root, height=10, width=50, background=TEXT_BACKGROUND_COLOR, font=TEXT_FONT)
text_input.pack(pady=5)
create_context_menu(text_input)  # Добавление контекстного меню

# Кнопки шифрования и дешифрования
encrypt_button = tk.Button(root, text="Зашифровать", command=encrypt_text)
encrypt_button.pack(pady=5)

decrypt_button = tk.Button(root, text="Расшифровать", command=decrypt_text)
decrypt_button.pack(pady=5)

# Поле для вывода зашифрованного текста
text_output_label = tk.Label(root, text="Зашифрованный текст:")
text_output_label.pack(pady=5)

text_output = tk.Text(root, height=10, width=50, background=TEXT_BACKGROUND_COLOR, font=TEXT_FONT)
text_output.pack(pady=5)
create_context_menu(text_output)  # Добавление контекстного меню

# Поле для вывода расшифрованного текста
decrypted_output_label = tk.Label(root, text="Расшифрованный текст:")
decrypted_output_label.pack(pady=5)

decrypted_output = tk.Text(root, height=10, width=50, background=TEXT_BACKGROUND_COLOR, font=TEXT_FONT)
decrypted_output.pack(pady=5)
create_context_menu(decrypted_output)  # Добавление контекстного меню

# Запуск окна
root.mainloop()
