import tkinter as tk
from tkinter import filedialog, messagebox

import hashlib
import os
import tkinter.ttk as ttk
import pyperclip

class HashCalculatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Hash Calculator")
        self.root.geometry("400x400")  # 调整界面大小

        self.file_label = tk.Label(root, text="选择文件：")
        self.file_label.pack()

        self.file_button = tk.Button(root, text="浏览", command=self.browse_file)
        self.file_button.pack()

        self.hash_algorithm_label = tk.Label(root, text="选择哈希算法：")
        self.hash_algorithm_label.pack()

        self.hash_algorithm_var = tk.StringVar()
        self.hash_algorithm_var.set("sha256")  # 默认选择SHA-256

        self.hash_algorithm_menu = tk.OptionMenu(root, self.hash_algorithm_var, "md5", "sha1", "sha256", "sha512")
        self.hash_algorithm_menu.pack()

        self.calculate_button = tk.Button(root, text="计算哈希值", command=self.calculate_hash)
        self.calculate_button.pack()

        self.progress_bar = ttk.Progressbar(root, orient="horizontal", mode="determinate")
        self.progress_bar.pack(fill="x", padx=10, pady=10)

        self.percent_label = tk.Label(root, text="")
        self.percent_label.pack()

        self.result_label = tk.Label(root, text="")
        self.result_label.pack()

        self.copy_button = tk.Button(root, text="复制哈希值", command=self.copy_hash)
        self.copy_button.pack()

        self.hash_input_label = tk.Label(root, text="输入要比对的哈希值：")
        self.hash_input_label.pack()

        self.hash_input = tk.Text(root, height=3)
        self.hash_input.pack()

        self.compare_button = tk.Button(root, text="比对哈希值", command=self.compare_hash)
        self.compare_button.pack()

    def browse_file(self):
        selected_file = filedialog.askopenfilename()
        self.selected_file = selected_file

    def calculate_hash(self):
        if hasattr(self, 'selected_file'):
            selected_algorithm = self.hash_algorithm_var.get()
            hash_obj = hashlib.new(selected_algorithm)
            
            file_size = os.path.getsize(self.selected_file)
            self.progress_bar["maximum"] = file_size
            self.progress_bar["value"] = 0

            with open(self.selected_file, 'rb') as f:
                while chunk := f.read(8192):
                    hash_obj.update(chunk)
                    self.progress_bar["value"] += len(chunk)
                    self.root.update_idletasks()  # 更新界面
                    percent_complete = (self.progress_bar["value"] / self.progress_bar["maximum"]) * 100
                    self.percent_label.config(text=f"已完成：{percent_complete:.2f}%")

            hash_value = hash_obj.hexdigest()
            self.result_label.config(text=f"计算结果：{selected_algorithm.upper()} 哈希值：{hash_value}")
            self.calculated_hash = hash_value
        else:
            self.result_label.config(text="请先选择文件！")

    def copy_hash(self):
        if hasattr(self, 'calculated_hash'):
            pyperclip.copy(self.calculated_hash)
            self.copy_button.config(text="已复制")
        else:
            self.copy_button.config(text="无可复制的哈希值")

    def compare_hash(self):
        if hasattr(self, 'calculated_hash'):
            input_hash = self.hash_input.get("1.0", "end-1c").strip()
            if input_hash:
                if self.calculated_hash == input_hash:
                    messagebox.showinfo("比对结果", "哈希值匹配！")
                else:
                    messagebox.showwarning("比对结果", "哈希值不匹配！")
            else:
                messagebox.showerror("错误", "请输入要比对的哈希值！")
        else:
            messagebox.showerror("错误", "请先计算哈希值！")

if __name__ == "__main__":
    root = tk.Tk()
    app = HashCalculatorApp(root)
    root.mainloop()
