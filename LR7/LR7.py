import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import base64


class MainWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Шифрование")
        self.root.geometry("300x200")

        frame = tk.Frame(self.root)
        frame.pack(expand=True)

        tk.Button(frame, text="Отправитель", command=self.open_sender,
                  width=20, height=2).pack(pady=10)
        tk.Button(frame, text="Получатель", command=self.open_receiver,
                  width=20, height=2).pack(pady=10)

    def open_sender(self):
        SenderWindow()

    def open_receiver(self):
        ReceiverWindow()

    def run(self):
        self.root.mainloop()


class CustomText(tk.Text):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.bind('<Control-v>', self.paste)
        self.bind('<Control-V>', self.paste)
        self.bind('<Control-c>', self.copy)
        self.bind('<Control-C>', self.copy)
        self.bind('<Control-x>', self.cut)
        self.bind('<Control-X>', self.cut)
        self.bind('<Button-3>', self.show_context_menu)

    def paste(self, event=None):
        try:
            text = self.clipboard_get()
            self.insert('insert', text)
        except:
            pass
        return 'break'

    def copy(self, event=None):
        try:
            text = self.get('sel.first', 'sel.last')
            self.clipboard_clear()
            self.clipboard_append(text)
        except:
            pass
        return 'break'

    def cut(self, event=None):
        self.copy()
        try:
            self.delete('sel.first', 'sel.last')
        except:
            pass
        return 'break'

    def show_context_menu(self, event):
        menu = tk.Menu(self, tearoff=0)
        menu.add_command(label="Вырезать", command=self.cut)
        menu.add_command(label="Копировать", command=self.copy)
        menu.add_command(label="Вставить", command=self.paste)
        menu.post(event.x_root, event.y_root)


def encrypt(text, key):
    # Преобразуем текст в байты
    text_bytes = text.encode('utf-8')
    # Применяем XOR к каждому байту
    encrypted_bytes = bytes([b ^ (key % 256) for b in text_bytes])
    # Кодируем в base64
    return base64.b64encode(encrypted_bytes).decode('utf-8')


def decrypt(encoded_text, key):
    try:
        # Декодируем из base64
        encrypted_bytes = base64.b64decode(encoded_text)
        # Применяем XOR с тем же ключом
        decrypted_bytes = bytes([b ^ (key % 256) for b in encrypted_bytes])
        # Преобразуем обратно в текст
        return decrypted_bytes.decode('utf-8')
    except Exception as e:
        raise ValueError("Ошибка при расшифровке") from e


class SenderWindow:
    def __init__(self):
        self.window = tk.Toplevel()
        self.window.title("Отправитель")
        self.window.geometry("400x550")

        self.key = tk.StringVar()

        tk.Button(self.window, text="Сформировать ключи",
                  command=self.generate_key).pack(pady=10)

        key_frame = tk.Frame(self.window)
        key_frame.pack(fill='x', padx=20)

        tk.Label(key_frame, text="Сгенерированный ключ:").pack(side='left')
        tk.Label(key_frame, textvariable=self.key).pack(side='left', padx=5)
        tk.Button(key_frame, text="Копировать ключ",
                  command=lambda: self.copy_to_clipboard(self.key.get())).pack(side='right')

        tk.Label(self.window, text="Введите текст для шифрования:").pack(pady=10)
        self.text_input = CustomText(self.window, height=10)
        self.text_input.pack(padx=20)

        tk.Button(self.window, text="Закодировать и подписаться",
                  command=self.encrypt_text).pack(pady=10)

        tk.Label(self.window, text="Зашифрованный текст:").pack(pady=10)
        self.encrypted_output = CustomText(self.window, height=10)
        self.encrypted_output.pack(padx=20)

        tk.Button(self.window, text="Копировать зашифрованный текст",
                  command=lambda: self.copy_to_clipboard(
                      self.encrypted_output.get("1.0", tk.END).strip()
                  )).pack(pady=5)

    def copy_to_clipboard(self, text):
        self.window.clipboard_clear()
        self.window.clipboard_append(text)
        messagebox.showinfo("Успешно", "Текст скопирован в буфер обмена!")

    def generate_key(self):
        D = 17
        W = datetime.now().day
        X = int('17102003')

        key = (X % 100) * D + W
        self.key.set(str(key))

    def encrypt_text(self):
        if not self.key.get():
            messagebox.showerror("Ошибка", "Сначала сгенерируйте ключ!")
            return

        text = self.text_input.get("1.0", tk.END).strip()
        if not text:
            messagebox.showerror("Ошибка", "Введите текст для шифрования!")
            return

        key = int(self.key.get())

        try:
            encrypted = encrypt(text, key)
            self.encrypted_output.delete("1.0", tk.END)
            self.encrypted_output.insert("1.0", encrypted)
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка при шифровании: {str(e)}")


class ReceiverWindow:
    def __init__(self):
        self.window = tk.Toplevel()
        self.window.title("Получатель")
        self.window.geometry("400x550")

        tk.Label(self.window, text="Введите ключ:").pack(pady=10)
        self.key_input = tk.Entry(self.window)
        self.key_input.pack()

        self.key_input.bind('<Control-v>', lambda e: self.paste_to_entry())
        self.key_input.bind('<Button-3>', self.show_entry_context_menu)

        tk.Label(self.window, text="Введите зашифрованное сообщение:").pack(pady=10)
        self.encrypted_input = CustomText(self.window, height=10)
        self.encrypted_input.pack(padx=20)

        tk.Button(self.window, text="Расшифровать",
                  command=self.decrypt_text).pack(pady=10)

        tk.Label(self.window, text="Расшифрованное сообщение:").pack(pady=10)
        self.decrypted_output = CustomText(self.window, height=10)
        self.decrypted_output.pack(padx=20)

        tk.Button(self.window, text="Копировать расшифрованный текст",
                  command=lambda: self.copy_to_clipboard(
                      self.decrypted_output.get("1.0", tk.END).strip()
                  )).pack(pady=5)

    def paste_to_entry(self):
        try:
            text = self.window.clipboard_get()
            self.key_input.delete(0, tk.END)
            self.key_input.insert(0, text)
        except:
            pass
        return 'break'

    def show_entry_context_menu(self, event):
        menu = tk.Menu(self.window, tearoff=0)
        menu.add_command(label="Вставить", command=self.paste_to_entry)
        menu.post(event.x_root, event.y_root)

    def copy_to_clipboard(self, text):
        self.window.clipboard_clear()
        self.window.clipboard_append(text)
        messagebox.showinfo("Успешно", "Текст скопирован в буфер обмена!")

    def decrypt_text(self):
        try:
            key = int(self.key_input.get())
        except ValueError:
            messagebox.showerror("Ошибка", "Введите корректный ключ!")
            return

        encrypted = self.encrypted_input.get("1.0", tk.END).strip()
        if not encrypted:
            messagebox.showerror("Ошибка", "Введите зашифрованное сообщение!")
            return

        try:
            decrypted = decrypt(encrypted, key)
            self.decrypted_output.delete("1.0", tk.END)
            self.decrypted_output.insert("1.0", decrypted)
        except ValueError as e:
            messagebox.showerror("Ошибка", "Ошибка при расшифровке. Проверьте введенный текст и ключ.")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Неизвестная ошибка: {str(e)}")


if __name__ == "__main__":
    app = MainWindow()
    app.run()