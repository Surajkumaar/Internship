import tkinter as tk
from tkinter import *
from tkinter import filedialog, messagebox
from PIL import ImageTk, Image
import cv2
import numpy as np

# Initialize tkinter
window = Tk()
window.geometry("900x700")
window.title("Image Encryption Decryption")
window.configure(bg="light blue")

# Global variables
global x, panelA, panelB, filename, image_encrypted, key
x = None
filename = None
image_encrypted = None
key = None
panelA = None
panelB = None

# Function to get path
def getpath(path):
    a = path.split('/')
    fname = a[-1]
    l = len(fname)
    location = path[:-l]
    return location

def getfoldername(path):
    a = path.split('/')
    name = a[-1]
    return name

def getfilename(path):
    a = path.split('/')
    fname = a[-1]
    a = fname.split('.')
    a = a[0]
    return a

# Function to open a file
def openfilename():
    global filename
    filename = filedialog.askopenfilename(title="Open", filetypes=[("Image files", ".png;.jpg;*.jpeg")])
    return filename

# Function to open and display image
def open_img():
    global x, panelA, panelB, filename
    x = openfilename()
    if x:
        img = Image.open(x)
        img.thumbnail((350, 350))
        img = ImageTk.PhotoImage(img)

        if panelA is None:
            panelA_frame = Frame(window, bg="white", width=400, height=400)
            panelA_frame.place(x=150, y=200)  
            panelA = Label(panelA_frame, image=img)
            panelA.image = img
            panelA.pack(padx=10, pady=10)
        else:
            panelA.configure(image=img)
            panelA.image = img

        if panelB is None:
            panelB_frame = Frame(window, bg="white", width=400, height=400)
            panelB_frame.place(x=550, y=200) 
            panelB = Label(panelB_frame, image=img)
            panelB.image = img
            panelB.pack(padx=10, pady=10)
        else:
            panelB.configure(image=img)
            panelB.image = img
    else:
        messagebox.showwarning("Warning", "No image selected.")

# Function for encryption
def en_fun(x):
    global image_encrypted, key
    image_input = cv2.imread(x, 1) 
    if image_input is not None:
        (x1, y, z) = image_input.shape  
        image_input = image_input.astype(float) / 255.0
        mu, sigma = 0, 0.1
        key = np.random.normal(mu, sigma, (x1, y, z)) + np.finfo(float).eps
        image_encrypted = image_input / key
        cv2.imwrite('image_encrypted.jpg', image_encrypted * 255)
        imge = Image.open('image_encrypted.jpg')
        imge.thumbnail((350, 350))
        imge = ImageTk.PhotoImage(imge)

        if panelB is not None:
            panelB.configure(image=imge)
            panelB.image = imge

        messagebox.showinfo("Encrypt Status", "Image Encrypted successfully.")
        filename = filedialog.asksaveasfile(mode='w', defaultextension=".jpg", filetypes=[("JPEG files", "*.jpg")])
        if filename:
            with open(filename.name, 'wb') as f:
                f.write(open('image_encrypted.jpg', 'rb').read())
            messagebox.showinfo("Success", "Encrypted image saved successfully!")
    else:
        messagebox.showwarning("Warning", "Failed to read image.")

# Function for decryption
def de_fun():
    global image_encrypted, key
    if image_encrypted is not None and key is not None:
        image_output = image_encrypted * key
        image_output = np.clip(image_output, 0, 1) * 255.0  
        image_output = image_output.astype(np.uint8)  
        cv2.imwrite('image_output.jpg', image_output)
        imgd = Image.open('image_output.jpg')
        imgd.thumbnail((350, 350))
        imgd = ImageTk.PhotoImage(imgd)

        if panelB is not None:
            panelB.configure(image=imgd)
            panelB.image = imgd

        messagebox.showinfo("Decrypt Status", "Image decrypted successfully.")
        filename = filedialog.asksaveasfile(mode='w', defaultextension=".jpg", filetypes=[("JPEG files", "*.jpg")])
        if filename:
            with open(filename.name, 'wb') as f:
                f.write(open('image_output.jpg', 'rb').read())
            messagebox.showinfo("Success", "Decrypted image saved successfully!")
    else:
        messagebox.showwarning("Warning", "Image not encrypted yet.")

# Function to reset
def reset():
    global x, panelA, panelB
    if x is not None:
        img = Image.open(x)
        img.thumbnail((350, 350))
        img = ImageTk.PhotoImage(img)

        if panelB is not None:
            panelB.configure(image=img)
            panelB.image = img

        messagebox.showinfo("Success", "Image reset to original format!")
    else:
        messagebox.showwarning("Warning", "No image selected.")

# Function for saving the encrypted image
def save_img():
    global filename
    if filename is not None:
        img = Image.open(filename)
        img.save('encrypted_image.jpg')
        messagebox.showinfo("Success", "Encrypted Image Saved Successfully!")
    else:
        messagebox.showwarning("Warning", "No image to save.")

# Function for exit application
def exit_win():
    if messagebox.askokcancel("Exit", "Do you want to exit?"):
        window.destroy()

# Gui
title_label = Label(window, text="Image Encryption Decryption", font=("Arial", 30), bg="light blue", fg="black")
title_label.place(x=200, y=20) 

original_label = Label(window, text="Original Image", font=("Arial", 20), bg="light blue", fg="black")
original_label.place(x=180, y=150)  

encrypted_label = Label(window, text="Processed Image", font=("Arial", 20), bg="light blue", fg="black")
encrypted_label.place(x=580, y=150)  

choose_button = Button(window, text="Choose", command=open_img, font=("Arial", 15), bg="black", fg="white", borderwidth=3, relief="raised")
choose_button.place(x=50, y=50)

encrypt_button = Button(window, text="Encrypt", command=lambda: en_fun(x), font=("Arial", 15), bg="black", fg="white", borderwidth=3, relief="raised")
encrypt_button.place(x=50, y=550)

decrypt_button = Button(window, text="Decrypt", command=de_fun, font=("Arial", 15), bg="black", fg="white", borderwidth=3, relief="raised")
decrypt_button.place(x=200, y=550)

reset_button = Button(window, text="Reset", command=reset, font=("Arial", 15), bg="white", fg="black", borderwidth=3, relief="raised")
reset_button.place(x=350, y=550)

save_button = Button(window, text="Save", command=save_img, font=("Arial", 15), bg="blue", fg="white", borderwidth=3, relief="raised")
save_button.place(x=500, y=550)

exit_button = Button(window, text="EXIT", command=exit_win, font=("Arial", 15), bg="red", fg="blue", borderwidth=3, relief="raised")
exit_button.place(x=800, y=550)

window.protocol("WM_DELETE_WINDOW", exit_win)
window.mainloop()