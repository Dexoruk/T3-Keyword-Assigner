import os
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.filedialog as fd
import sqlite3

window = tk.Tk()
s = ttk.Style()
s.configure("Custom.TButton", background="#0000FF", foreground="#FFFFFF")

def browse_folder():
    folder = fd.askdirectory()
    folder_label.config(text=folder)

def assign_keyword():
    keyword = keyword_entry.get()
    folder = folder_label.cget("text")

    conn = sqlite3.connect("keywords.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS keywords (name text, keyword text)''')
    c.execute("INSERT INTO keywords VALUES (?, ?)", (folder, keyword))
    conn.commit()
    for file in os.listdir(folder):
        c.execute("INSERT INTO keywords VALUES (?, ?)", (file, keyword))
    conn.commit()
    conn.close()

    notification = tk.Toplevel()
    notification.title("Keyword Assigned")
    ttk.Label(notification, text=f"Keyword '{keyword}' assigned to file '{folder}'", font=("TkDefaultFont", 16, "bold")).pack()
    ttk.Button(notification, text="OK", command=notification.destroy, style="Custom.TButton").pack()


def search_keyword():
    keyword = keyword_entry.get()

    conn = sqlite3.connect("keywords.db")
    c = conn.cursor()
    c.execute("SELECT name FROM keywords WHERE keyword=?", (keyword,))
    results = c.fetchall()
    conn.close()
    listbox.delete(0, tk.END)
    for result in results:
        listbox.insert(tk.END, result[0])


window.title("T3 Keyword Assigner")

window.grid_columnconfigure(1, weight=1)

keyword_label = ttk.Label(window, text="Keyword:", font=("TkDefaultFont", 16, "bold"))
keyword_entry = tk.Entry(window)
folder_label = tk.Label(window, text="No folder selected", font=("TkDefaultFont", 16, "bold"))
browse_button = ttk.Button(window, text="Browse", command=browse_folder, style="Custom.TButton")
assign_button = ttk.Button(window, text="Assign Keyword", command=assign_keyword, style="Custom.TButton")
search_button = ttk.Button(window, text="Search", command=search_keyword, style="Custom.TButton")
listbox = tk.Listbox(window, bg="#D3D3D3")

keyword_label.grid(row=0, column=0, sticky="W")
keyword_entry.grid(row=0, column=1, sticky="EW")
folder_label.grid(row=1, column=0, columnspan=2, sticky="EW")
browse_button.grid(row=2, column=0, sticky="W", padx=10, pady=10)
assign_button.grid(row=2, column=1, sticky="E", padx=10, pady=10)
search_button.grid(row=3, column=0, sticky="W", padx=10, pady=10)
listbox.grid(row=4, column=0, columnspan=2, sticky="EW", padx=10, pady=10)


window.mainloop()
