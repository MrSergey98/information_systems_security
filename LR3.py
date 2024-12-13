import tkinter as tk
from tkinter import *
from tkinter import filedialog, messagebox, ttk

alphabet: str = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ ,.!?*+=—-1234567890;:'	()\"`\n"


def encode_cipher(text, key=2):
    """
    Кодирование текста методом одиночной перестановки.

    Args:
        text (str): Исходный текст для шифрования
        key (int): Ключ (длина блока) для перестановки

    Returns:
        str: Зашифрованный текст
    """
    # Дополняем текст пробелами, если его длина не кратна ключу
    while len(text) % key != 0:
        text += " "

    # Разбиваем текст на блоки длиной key
    blocks = [text[i:i + key] for i in range(0, len(text), key)]

    # Выполняем перестановку в каждом блоке
    encoded_blocks = []
    for block in blocks:
        # Переворачиваем порядок символов в блоке
        encoded_block = block[::-1]
        encoded_blocks.append(encoded_block)

    # Объединяем зашифрованные блоки в одну строку
    return "".join(encoded_blocks)


def decode_cipher(encoded_text, key=2):
    """
    Декодирование текста, зашифрованного методом одиночной перестановки.

    Args:
        encoded_text (str): Зашифрованный текст
        key (int): Ключ (длина блока) для перестановки

    Returns:
        str: Расшифрованный текст
    """
    # Разбиваем текст на блоки длиной key
    blocks = [encoded_text[i:i + key] for i in range(0, len(encoded_text), key)]

    # Выполняем обратную перестановку в каждом блоке
    decoded_blocks = []
    for block in blocks:
        # Переворачиваем порядок символов в блоке обратно
        decoded_block = block[::-1]
        decoded_blocks.append(decoded_block)

    # Объединяем расшифрованные блоки и удаляем лишние пробелы справа
    return "".join(decoded_blocks).rstrip()


# Функция шифрования текста
def encode(text: str, a: int = 1, b: int = 1, c: int = 1) -> str:
    decode: str = ""
    for position, symbol in enumerate(text):
        k: int = (a * position**2) + (b * position) + c
        try:
            index: int = (alphabet.index(symbol.upper()) - k) % len(alphabet)
        except Exception:
            print(f'Не найден символ: "{symbol}"')
            return
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
        if method.get() == trisemus:
            encrypted_msg = encode(message)
        else:
            encrypted_msg = encode_cipher(message)
        text_output.delete("1.0", tk.END)
        text_output.insert(tk.END, str(encrypted_msg))
    else:
        messagebox.showwarning("Ошибка", "Поле ввода пусто!")

def encrypt_to_file():
    message = text_input.get("1.0", tk.END).strip()
    if message:
        if method.get() == trisemus:
            encrypted_msg = encode(message)
        else:
            encrypted_msg = encode_cipher(message)
        with open('encoded_text.txt', 'w', encoding='utf-8') as file:
            file.write(encrypted_msg)
        messagebox.showinfo("Успешно", 'Успешная запись в файл "encoded_text.txt"')
    else:
        messagebox.showwarning("Ошибка", "Поле ввода пусто!")


# Функция для дешифрования текста с интерфейса
def decrypt_text():
    encrypted_message = text_output.get("1.0", tk.END).strip()
    if encrypted_message:
        try:
            if method.get() == trisemus:
                decrypted_msg = decode(encrypted_message)
            else:
                decrypted_msg = decode_cipher(encrypted_message)
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
root.title("Шифрование и Дешифрование методом Трисемуса|Одиночной перестановки")
root['bg'] = '#3c85fa'

# Радиокнопки
trisemus = 'Метод Трисемуса'
cipher = 'Метод одиночной перестановки'

method = StringVar(value=trisemus)

trisemus_btn = ttk.Radiobutton(text=trisemus, value=trisemus, variable=method)
trisemus_btn.pack()

cipher_btn = ttk.Radiobutton(text=cipher, value=cipher, variable=method)
cipher_btn.pack()

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
encrypt_to_file_button = tk.Button(root, text='Зашифровать в файл', command=encrypt_to_file)
encrypt_to_file_button.pack(pady=5)

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
