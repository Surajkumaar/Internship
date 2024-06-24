import tkinter as tk
import sys

class CaesarCipher(tk.Frame):
    def __init__(self, root):
        self.colour1 = '#072b63'  
        self.colour2 = '#ADD8E6'  
        self.colour3 = '#89b9e1'  

        self.letters = 'abcdefghijklmnopqrstuvwxyz'  
        self.num_letters = len(self.letters)

        super().__init__(root, bg=self.colour1) 

        self.main_frame = self

        self.main_frame.pack(fill=tk.BOTH, expand=True)
        self.main_frame.columnconfigure(0, weight=1)
        self.render_widgets()  

    def render_widgets(self):
        self.title = tk.Label(
            self.main_frame,
            bg=self.colour1,
            fg=self.colour2,
            font=('Arial', 22, 'bold'),
            text='Caesar Cipher'
        )
        self.title.grid(column=0, row=0, sticky=tk.EW, pady=35)

        self.text_widget = tk.Text(
            self.main_frame,
            bg=self.colour2,
            fg=self.colour1,
            selectbackground=self.colour1,
            selectforeground=self.colour2,
            font=('Arial', 17),
            height=5,
            padx=10,
            pady=10,
            highlightthickness=0,
            border=0
        )
        self.text_widget.grid(column=0, row=1, padx=100)

        self.key_label = tk.Label(
            self.main_frame,
            bg=self.colour1,
            fg=self.colour2,
            font=('Arial', 13),
            text=f'Key (1-{self.num_letters - 1})',
            justify=tk.CENTER
        )
        self.key_label.grid(column=0, row=2, pady=(38, 10))

        self.buttons_container = tk.Frame(self.main_frame, bg=self.colour1)
        self.buttons_container.columnconfigure(0, weight=1)
        self.buttons_container.columnconfigure(1, weight=1)
        self.buttons_container.columnconfigure(2, weight=1)
        self.buttons_container.grid(column=0, row=3, sticky=tk.NSEW, padx=100)

        self.button_encrypt = tk.Button(
            self.buttons_container,
            bg=self.colour2,
            fg=self.colour1,
            activebackground=self.colour3,
            activeforeground=self.colour1,
            font=("Arial", 15),
            text='Encrypt',
            width=6,
            height=1,
            cursor='hand1',
            highlightthickness=0,
            border=0,
            state=tk.DISABLED,
            command=self.encrypt_command
        )
        self.button_encrypt.grid(column=0, row=0, ipadx=5, ipady=5)

        self.button_decrypt = tk.Button(
            self.buttons_container,
            bg=self.colour2,
            fg=self.colour1,
            activebackground=self.colour3,
            activeforeground=self.colour1,
            font=("Arial", 15),
            text='Decrypt',
            width=6,
            height=1,
            cursor='hand1',
            highlightthickness=0,
            border=0,
            state=tk.DISABLED,
            command=self.decrypt_command
        )
        self.button_decrypt.grid(column=2, row=0, ipadx=5, ipady=5)

        self.key_entry_validation_command = self.buttons_container.register(self.key_entry_validation)
        self.key_entry = tk.Entry(
            self.buttons_container,
            bg=self.colour2,
            fg=self.colour1,
            selectbackground=self.colour1,
            selectforeground=self.colour2,
            font=('Arial', 15),
            width=6,
            highlightthickness=0,
            border=0,
            justify=tk.CENTER,
            validate='key',
            validatecommand=(self.key_entry_validation_command, '%P')
        )
        self.key_entry.grid(column=1, row=0, ipady=9)

    def key_entry_validation(self, value):
        if value == '':
            self.button_decrypt['state'] = tk.DISABLED
            self.button_encrypt['state'] = tk.DISABLED
            return True

        try:
            value = int(value)
        except ValueError:
            return False

        if value <= 0 or value >= self.num_letters:
            return False

        self.button_decrypt['state'] = tk.NORMAL
        self.button_encrypt['state'] = tk.NORMAL

        return True

    def encrypt_decrypt(self, text, mode, key):
        letters = 'abcdefghijklmnopqrstuvwxyz'
        num_letters = len(letters)
        result = ''

        if mode == 'd':
            key = -key

        for letter in text:
            letter = letter.lower()
            if letter != ' ':
                index = letters.find(letter)
                if index == -1:
                    result += letter
                else:
                    new_index = index + key
                    if new_index >= num_letters:
                        new_index -= num_letters
                    elif new_index < 0:
                        new_index += num_letters
                    result += letters[new_index]
            else:
                result += ' '  
        return result

    def encrypt_command(self):
        key = self.key_entry.get()
        text = self.text_widget.get('1.0', tk.END)
        self.text_widget.delete('1.0', tk.END)
        self.text_widget.insert('1.0', self.encrypt_decrypt(text, 'e', int(key)))

    def decrypt_command(self):
        key = self.key_entry.get()
        text = self.text_widget.get('1.0', tk.END)
        self.text_widget.delete('1.0', tk.END)
        self.text_widget.insert('1.0', self.encrypt_decrypt(text, 'd', int(key)))

operating_system = sys.platform
root = tk.Tk()
caesar_cipher_app = CaesarCipher(root)
root.title('Caesar Cipher')

if 'win' in operating_system:
    root.geometry('800x450')
elif 'linux' in operating_system:
    root.geometry('800x470')
elif 'darwin' in operating_system:
    root.geometry('800x470')

root.resizable(width=False, height=False)
root.mainloop()
