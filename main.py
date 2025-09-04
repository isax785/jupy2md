# from jupy2md import jupy2md
from obj.jupy2md import Jupy2Md

import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog, messagebox, Text, ACTIVE, DISABLED
from tkinter.scrolledtext import ScrolledText
# from obj.code_tree import FileCodeTree
import os

CWD = os.path.dirname(__file__)
IMG_LINK = ["Markdown", "HTML", "Wikilinks"]
STYLING = False

class MainWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.initialization()
        self.add_components()
        if STYLING:
            self.set_style()
        self.md_text = None
        # self.set_menu_bar()
    
    def initialization(self):
        self.root.title("Jupy2Md Converter")
        self.root.iconbitmap(os.path.join(CWD, './res/jupy2md01.ico'))
        self.root.minsize(600, 400)
        self.root.grid_rowconfigure(2, weight=1)
        self.root.grid_columnconfigure(1, weight=1)
        self.filepath = None

    def set_style(self):
        theme_filepath = os.path.normpath(os.path.join(CWD, './res/azure/azure.tcl'))
        self.root.tk.call('source', theme_filepath)
        self.root.tk.call("set_theme", "dark")
        self.root.update()

    def add_components(self):
        # Upload file for conversion
        tk.Button(self.root, text="Open File", command=self.browse_upload).grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.upload_entry = tk.Text(self.root, height=2, width=55)
        self.upload_entry.grid(row=0, column=1, columnspan=3, padx=10, pady=5)
        self.upload_entry.grid_configure(sticky="nsew")
        self.upload_entry.grid_rowconfigure(0, weight=1)
        self.upload_entry.config(state=tk.DISABLED)

        # Download section
        tk.Button(self.root, text="Select Folder", command=self.browse_download).grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.download_entry = tk.Text(self.root, height=2, width=55)
        self.download_entry.grid(row=1, column=1, columnspan=3, padx=10, pady=5)
        self.download_entry.grid_configure(sticky="nsew")
        self.download_entry.grid_rowconfigure(0, weight=1)
        self.download_entry.config(state=tk.DISABLED)

        # checkboxes
        self.checkboxes_frame = tk.Frame(self.root)
        self.checkboxes_frame.grid(row=2, column=0, sticky="nw", padx=5)

        self.chkbx_text_var = tk.BooleanVar(value=True)
        self.chkbx_text = tk.Checkbutton(self.checkboxes_frame, text="Text", 
                                         variable=self.chkbx_text_var,
                                         command=self.convert_to_md)
        self.chkbx_text.grid(row=0, column=0, sticky="nw", padx=5)

        self.chkbx_text_img_var = tk.BooleanVar(value=True)
        self.chkbx_text_img = tk.Checkbutton(self.checkboxes_frame, text="Text Images", 
                                         variable=self.chkbx_text_img_var,
                                         command=self.convert_to_md)
        self.chkbx_text_img.grid(row=1, column=0, sticky="nw", padx=5)

        self.chkbx_code_var = tk.BooleanVar(value=True)
        self.chkbx_code = tk.Checkbutton(self.checkboxes_frame, text="Code", 
                                         variable=self.chkbx_code_var,
                                         command=self.convert_to_md)
        self.chkbx_code.grid(row=2, column=0, sticky="nw", padx=5)

        self.chbx_code_output_var = tk.BooleanVar(value=True)
        self.chbx_code_output = tk.Checkbutton(self.checkboxes_frame, 
                                               text="Printout/Output", 
                                               variable=self.chbx_code_output_var,
                                               command=self.convert_to_md)
        self.chbx_code_output.grid(row=3, column=0, sticky="nw", padx=5)

        self.chbx_code_img_var = tk.BooleanVar(value=True)
        self.chbx_code_img = tk.Checkbutton(self.checkboxes_frame, text="Code Images", 
                                       variable=self.chbx_code_img_var, 
                                       command=self.convert_to_md)
        self.chbx_code_img.grid(row=4, column=0, sticky="nw", padx=5)

        # drop-down menu - combobox
        tk.Label(self.checkboxes_frame, text="Image Link Style:").grid(row=5, column=0, sticky="nw", padx=5)
        self.dropdown_var = tk.StringVar()
        self.dropdown_menu = ttk.Combobox(self.checkboxes_frame, textvariable=self.dropdown_var, values=IMG_LINK, state="readonly")
        self.dropdown_menu.bind("<<ComboboxSelected>>", self.convert_to_md)
        self.dropdown_menu.grid(row=6, column=0, padx=5)
        self.dropdown_menu.current(0)

        # display text
        self.display_text = ScrolledText(self.root, width=65, yscrollcommand=True)
        self.display_text.grid(row=2, column=1, columnspan=3, padx=10, pady=5, sticky="nsew")
        self.display_text.grid_configure(sticky="nsew")
        self.display_text.grid_rowconfigure(0, weight=1)
        self.display_text.grid_columnconfigure(0, weight=1)
        self.display_text .config(state=tk.DISABLED)

        # export button
        tk.Button(self.root, text="Export", command=self.export_md).grid(row=3, column=1, columnspan=3, pady=5, padx=10, sticky='nsew')

        # status bar
        self.status_bar_text = tk.StringVar()
        self.status_bar_text.set("-")
        self.status_bar = tk.Label(self.root, textvariable=self.status_bar_text, anchor="w")
        self.status_bar.grid(row=4, column=1, columnspan=3, pady=5, padx=10,sticky='nsew')

    def _write_statusbar(self, mess:str):
        self.status_bar_text.set(mess)

    def browse_upload(self):
        filepath = filedialog.askopenfilename(defaultextension=".ipynb")
        if filepath:
            self.filepath = filepath
            print(f"DBG - Uploaded file: {filepath}")
            extension = filepath.split('.')[-1]
            if extension != 'ipynb':
                self.filename = None
                self._write_statusbar("Please select a .ipynb file.")
            else:
                settings = self.retrieve_settings()
                self.md_text = Jupy2Md(self.filepath, settings=settings)
                self.filename = filepath.split("/")[-1].split('.')[0]
                self._write_into_text(self.upload_entry, filepath)
                self.convert_to_md()
                self._write_statusbar("File Uploaded!")

    def retrieve_settings(self) -> dict:
        settings = {"md_text": self.chkbx_text_var.get(),
                    "md_images": self.chkbx_text_img_var.get(),
                    "code": self.chkbx_code_var.get(),
                    "code_output": self.chbx_code_output_var.get(),
                    "code_text": self.chbx_code_output_var.get(),
                    "code_images": self.chbx_code_img_var.get(),
                    "export": False,
                    "img_link": self.dropdown_menu.get(),
                    "export_folder": False}
        return settings
    
    def convert_to_md(self, export=False, export_folder=None):
        if self.filepath:
            settings = self.retrieve_settings()
            settings.update({"export_folder": export_folder,
                             "export": export})
            self.md_text.convert_to_md(settings)
            self._write_into_text(self.display_text, self.md_text.text)
            self._write_statusbar("Jupyter Notebook converted!")
        else:
            self._write_statusbar("Select a Jupyter Notebook first!")

    def browse_download(self):
        folder = filedialog.askdirectory()
        if folder:
            self.folder_path = folder
            # os.makedirs(self.folder_path, exist_ok=True)
            # filepath = os.path.join(self.folder_path)
            try:
                self.md_text.export = True
                self.md_text.export_folder = self.folder_path
                self._write_into_text(self.download_entry, self.folder_path)
            except Exception as e:
                messagebox.showinfo("Error", e)

    def export_md(self):
        if not self.md_text:
            print("select a file")
            messagebox.showerror("Export", "Select a Jupyter Notebook.")
        else:
            if not self.md_text.export_folder:
                print("select a folder for export")
                messagebox.showerror("Export", "Select a folder for export.")
            else:
                try:
                    self.md_text.export_md(export_folder=self.folder_path)
                    messagebox.showinfo("Export", "File exported successfully.")
                    self._write_statusbar("Export folder: " + os.path.normpath(os.path.join(self.folder_path, self.filename)))
                except Exception as e:
                    messagebox.showinfo("Error", e)
    

    def _write_into_text(self, cell, text):
        cell.config(state="normal")
        cell.delete("1.0", tk.END)
        cell.insert(tk.END, text)
        cell.config(state="disabled")

if __name__ == "__main__":
    window = MainWindow()
    # # theme_filepath = os.path.normpath(os.path.join(CWD, './res/azure/azure.tcl'))
    # theme_filepath = os.path.normpath(os.path.join(CWD, 'azure.tcl'))
    # print(theme_filepath)
    # window.root.tk.call('source', theme_filepath)
    # window.root.tk.call("set_theme", "dark")
    window.root.mainloop()