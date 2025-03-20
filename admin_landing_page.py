import tkinter as tk
from tkinter import messagebox, filedialog
import sqlite3
import smtplib
from email.message import EmailMessage
import os

# Database Setup
def setup_database():
    conn = sqlite3.connect('cms.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY,
                        username TEXT UNIQUE,
                        password TEXT,
                        email TEXT)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS sections (
                        id INTEGER PRIMARY KEY,
                        type TEXT,
                        title TEXT,
                        author TEXT,
                        date TEXT,
                        content TEXT,
                        icon TEXT,
                        link TEXT)''')
    conn.commit()
    conn.close()
setup_database()

# Login Screen
def login():
    def authenticate():
        username = entry_user.get()
        password = entry_pass.get()
        conn = sqlite3.connect('cms.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        user = cursor.fetchone()
        conn.close()
        if user:
            root.deiconify()
            login_window.destroy()
        else:
            messagebox.showerror("Login Failed", "Invalid credentials")
    
    login_window = tk.Toplevel(root)
    login_window.title("Login")
    tk.Label(login_window, text="Username").pack()
    entry_user = tk.Entry(login_window)
    entry_user.pack()
    tk.Label(login_window, text="Password").pack()
    entry_pass = tk.Entry(login_window, show="*")
    entry_pass.pack()
    tk.Button(login_window, text="Login", command=authenticate).pack()
    tk.Button(login_window, text="Forgot Password?", command=reset_password).pack()
    root.withdraw()

def reset_password():
    def send_reset_email():
        email = entry_email.get()
        conn = sqlite3.connect('cms.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE email=?", (email,))
        user = cursor.fetchone()
        conn.close()
        if user:
            msg = EmailMessage()
            msg.set_content("Reset your password using this link.")
            msg['Subject'] = 'Password Reset'
            msg['From'] = 'noreply@cms.com'
            msg['To'] = email
            with smtplib.SMTP('smtp.example.com', 587) as server:
                server.starttls()
                server.login("your_email@example.com", "your_password")
                server.send_message(msg)
            messagebox.showinfo("Success", "Reset email sent")
        else:
            messagebox.showerror("Error", "Email not found")
    
    reset_window = tk.Toplevel(root)
    reset_window.title("Reset Password")
    tk.Label(reset_window, text="Enter your email").pack()
    entry_email = tk.Entry(reset_window)
    entry_email.pack()
    tk.Button(reset_window, text="Send Reset Link", command=send_reset_email).pack()

def add_section():
    def save_section():
        section_type = section_var.get()
        title = entry_title.get()
        author = entry_author.get()
        date = entry_date.get()
        content = text_content.get("1.0", tk.END)
        conn = sqlite3.connect('cms.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO sections (type, title, author, date, content) VALUES (?, ?, ?, ?, ?)",
                       (section_type, title, author, date, content))
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Section added")
        section_window.destroy()
    
    section_window = tk.Toplevel(root)
    section_window.title("Add Section")
    tk.Label(section_window, text="Section Type").pack()
    section_var = tk.StringVar()
    tk.OptionMenu(section_window, section_var, "Article", "Tile", "Modal", "News").pack()
    tk.Label(section_window, text="Title").pack()
    entry_title = tk.Entry(section_window)
    entry_title.pack()
    tk.Label(section_window, text="Author").pack()
    entry_author = tk.Entry(section_window)
    entry_author.pack()
    tk.Label(section_window, text="Date").pack()
    entry_date = tk.Entry(section_window)
    entry_date.pack()
    tk.Label(section_window, text="Content").pack()
    text_content = tk.Text(section_window, height=5, width=40)
    text_content.pack()
    
    tk.Label(section_window, text="Upload Image").pack()
    def upload_image():
        file_path = filedialog.askopenfilename()
        entry_image.insert(0, file_path)
    entry_image = tk.Entry(section_window)
    entry_image.pack()
    tk.Button(section_window, text="Browse", command=upload_image).pack()
    
    tk.Button(section_window, text="Save", command=save_section).pack()

root = tk.Tk()
root.title("CMS Admin Panel")
login()

menu = tk.Menu(root)
root.config(menu=menu)
menu.add_command(label="Add Section", command=add_section)
menu.add_command(label="Logout", command=lambda: root.quit())

root.mainloop()
