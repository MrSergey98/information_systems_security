from random import choices
import tkinter as tk


P, V, T = 1e-4, 3 * 60 * 24 * 7, 15/7
alphabet = 'qwertyuiopasdfghjklzxcvbnm'


def S_asterix(P, V, T):
    return int(V * T // P)

def solve_A_L(S_asterix):
    L = 1
    A = len(alphabet)
    while A ** L < S_asterix:
        L += 1
    return A, L

def make_safe_password():
    return ''.join(choices(
        alphabet,
        k=solve_A_L(S_asterix(P, V, T))[1],
    ))

def display_safe_password():
    password_field.config(state=tk.NORMAL)
    password_field.delete("1.0", tk.END)
    password_field.insert(tk.END, make_safe_password())
    password_field.config(state=tk.DISABLED)


root = tk.Tk()
root.geometry("400x250")
tk.Label(text=f'P = {P}; V = {V}; T = {T};').pack()
button = tk.Button(text='Создать надежный пароль', command=display_safe_password)
button.pack()
password_field = tk.Text(root, width=20, height=1)
password_field.config(state=tk.DISABLED)
password_field.pack()
root.mainloop()
