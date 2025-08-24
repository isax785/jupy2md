# from jupy2md import jupy2md
from obj.jupy2md import Jupy2Md

import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog, messagebox, Text, ACTIVE, DISABLED
from tkinter.scrolledtext import ScrolledText
# from obj.code_tree import FileCodeTree
import os

CWD = os.path.dirname(__file__)


class MainWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.initialization()
        self.set_style()
        self.add_components()
        self.md_text = None
        # self.set_menu_bar()
    
    def initialization(self):
        self.root.title("Jupy2Md Converter")
        self.root.iconbitmap(os.path.join(CWD, './res/jupy2md01.ico'))
        self.root.geometry("600x400")
        self.filepath = None
    
    def set_style(self):
        self.style = ttk.Style(self.root)
        self.style.theme_use("default")

    def add_components(self):
        tk.Button(self.root, text="Open File", command=self.browse_upload).grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.upload_entry = tk.Text(self.root, height=2, width=55)
        self.upload_entry.grid(row=0, column=1, columnspan=3, padx=10, pady=5)

        # Download section
        tk.Button(self.root, text="Select Folder", command=self.browse_download).grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.download_entry = tk.Label(self.root, text="Select a destination folder", anchor="w")
        self.download_entry = tk.Text(self.root, height=2, width=55)
        self.download_entry.grid(row=1, column=1, columnspan=3, padx=5, pady=5)

        # checkboxes
        self.chkbx_code_var = tk.BooleanVar(value=True)
        self.chkbx_code = tk.Checkbutton(self.root, text="Code", variable=self.chkbx_code_var, command=self.convert_to_md)
        self.chkbx_code.grid(row=2, column=1, sticky="w", padx=20, pady=5)

        self.chbx_code_output_var = tk.BooleanVar(value=True)
        self.chbx_code_output = tk.Checkbutton(self.root, text="Code Output", variable=self.chbx_code_output_var, command=self.convert_to_md)
        self.chbx_code_output.grid(row=2, column=2, sticky="w", pady=5)

        self.chbx_img_var = tk.BooleanVar(value=True)
        self.chbx_img = tk.Checkbutton(self.root, text="Images", variable=self.chbx_img_var, command=self.convert_to_md)
        self.chbx_img.grid(row=2, column=3, sticky="w", pady=5)

        # display text
        self.display_text = ScrolledText(self.root, width=65, height=15, yscrollcommand=True)
        self.display_text.grid(row=3, column=0, columnspan=4, padx=20, pady=5, sticky="w")

    def browse_upload(self):
        filepath = filedialog.askopenfilename(defaultextension=".ipynb")
        if filepath:
            self.filepath = filepath
            print(f"DBG - Uploaded file: {filepath}")
            extension = filepath.split('.')[-1]
            if extension != 'ipynb':
                self.filename = None
                self._write_into_text(self.display_text, "Please select a .ipynb file.")
            else:
                self.filename = filepath.split("/")[-1].split('.')[0]
                self._write_into_text(self.upload_entry, filepath)
                self.convert_to_md()
    
    def convert_to_md(self, export=False, export_folder=None):
        print("DBG - conversion called!") # DEBUG
        if self.filepath:
            settings = {"code": self.chkbx_code_var.get(),
                        "code_output": self.chbx_code_output_var.get(),
                        "code_text": self.chbx_code_output_var.get(),
                        "code_images": self.chbx_img_var.get(),
                        "images": self.chbx_img_var.get(),
                        "code_images": self.chbx_img_var.get(),
                        "export_folder": export_folder,
                        "export": export}
            self.md_text = Jupy2Md(self.filepath, settings=settings)
            self._write_into_text(self.display_text, self.md_text.text)

    def browse_download(self):
        folder = filedialog.askdirectory()
        if folder:
            folder_path = os.path.join(folder, self.filename)
            os.makedirs(folder_path, exist_ok=True)
            filepath = os.path.join(folder_path)
            try:
                self.convert_to_md(export=True, export_folder=folder_path)
                self._write_into_text(self.download_entry, filepath + " --> SAVED!")
                messagebox.showinfo("Export", "File exported successfully.")
            except Exception as e:
                messagebox.showinfo("Error", e)

    def _write_into_text(self, cell, text):
        cell.config(state="normal")
        cell.delete("1.0", tk.END)
        cell.insert(tk.END, text)
        cell.config(state="disabled")

    # def upload_action(self):
    #     self.file_path = filedialog.askopenfilename()
    #     if self.file_path:
    #         self.file_label.config(text=os.path.basename(self.file_path))
    #         self.markdown_text = jupy2md(self.file_path, export=False)

    # def export_file(self):
    #     self.export_path = filedialog.asksaveasfilename(defaultextension=".txt",
    #                                            filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
    #     if self.export_path:
    #         self.export_filename.config(text=os.path.basename(self.export_path))
    #         content = self.text.get(1.0, tk.END)
    #         with open(self.export_path, 'w', encoding="utf-8") as file:
    #             file.write(content)
    #         messagebox.showinfo("Export", "File exported successfully.")

if __name__ == "__main__":
    window = MainWindow()
    window.root.mainloop()