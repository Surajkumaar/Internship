import customtkinter
from tkinter import *
from tkinter import messagebox
import re

app = customtkinter.CTk()
app.title('Password Checker')
app.geometry('400x300+480+200')
app.config(bg='blue')
app.resizable(False, False)


title_font = ('Arial', 20, 'bold')
subtitle_font = ('Arial', 17, 'bold')
button_font = ('Arial', 18, 'bold')

#Function1
def is_pass_strong(password):
    if len(password) < 6:
        return False
    if not re.search(r'[A-Z]',password):
        return False
    
    if not re.search(r'[a-z]',password):
        return False
    
    if not re.search(r'[0-9]',password):
        return False
    
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]',password):
        return False
    
    return True

#Function2
def display_pass():
    password = pass_text_box.get()
    if password:
        result_text.configure(state ='normal')
        result_text.delete (0,END)

        if is_pass_strong(password):
            result_text.insert(0,"Strong")
            result_text.configure(fg_color ="green")

        else:
            result_text.insert(0,"Not Recommended")
            result_text.configure(fg_color = 'red')

        result_text.configure(state='disabled')
    else:
        messagebox.showerror(title='error',message='Enter a Password to Check')

#GUI
title_label = customtkinter.CTkLabel(app,text="Password Complexity Checker",font=title_font,text_color='white',bg_color='blue')
title_label.place(x=50,y=20)

pass_text_box = customtkinter.CTkEntry(app,font=subtitle_font,text_color='black',fg_color="white",bg_color='blue',border_color='red',width=300,height=50)
pass_text_box.place(x=50,y=60)

Check_button = customtkinter.CTkButton(app,command=display_pass,text='Check Password',font=button_font,text_color='#FFF',fg_color='black',bg_color='blue',hover_color='#BD3602',cursor='hand2',corner_radius=20,width=150,height=40)
Check_button.place(x=100,y=130)

pass_strength_label = customtkinter.CTkLabel(app,text="Your Password Strength",font=title_font,text_color='white',bg_color='blue')
pass_strength_label.place(x=80,y=200)

result_text = customtkinter.CTkEntry(app,state='disabled',font=subtitle_font,text_color='white',fg_color='white',border_color='blue',justify = 'center',width=200,height=30)
result_text.place(x=100,y=240)


app.mainloop()
