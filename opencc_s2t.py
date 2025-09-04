import tkinter as tk
from tkinter import filedialog, messagebox
from opencc import OpenCC
import os
import sys
# 修復打包後的路徑問題
if getattr(sys, 'frozen', False):
    # 如果是打包後的exe檔案
    filepath = os.path.dirname(sys.executable)
else:
    # 如果是原始Python腳本
    script_path = os.path.abspath(__file__)
    filepath = os.path.dirname(script_path)

def convert_to_traditional():
    """
    開啟檔案選取對話框，讀取簡體中文檔案，
    轉換為繁體中文後，儲存為新檔案。
    """
    # 建立 OpenCC 轉換器，'mc-s2twp.json' 表示簡體到台灣正體 (含詞彙轉換)
    cc = OpenCC('mc-s2twp')
    # 開啟檔案選取對話框
    filepath = filedialog.askopenfilename(
        title="選擇簡體中文檔案",
        filetypes=[("所有檔案", "*.*"), ("文字檔案", "*.txt")]
    )
    # 如果使用者取消選取，則直接返回
    if not filepath:
        return
    try:
        # 讀取原始檔案內容
        with open(filepath, 'r', encoding='utf-8') as f:
            simplified_content = f.read()
        # 進行簡繁轉換
        traditional_content = cc.convert(simplified_content)
        # 產生新的檔名
        directory, filename = os.path.split(filepath)
        name, extension = os.path.splitext(filename)
        new_filename = f"{name}_tw{extension}"
        new_filepath = os.path.join(directory, new_filename)
        # 寫入轉換後的內容至新檔案
        with open(new_filepath, 'w', encoding='utf-8') as f:
            f.write(traditional_content)
        messagebox.showinfo("成功", f"檔案已成功轉換並儲存於：\n{new_filepath}")
    except Exception as e:
        messagebox.showerror("錯誤", f"轉換過程中發生錯誤：\n{e}")

# --- GUI 介面設定 ---
# 建立主視窗
root = tk.Tk()
root.title("簡轉繁檔案轉換工具")
# 設定視窗大小並置中
window_width = 400
window_height = 200
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
center_x = int(screen_width/2 - window_width/2)
center_y = int(screen_height/2 - window_height/2)
root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
root.resizable(False, False)  # 禁止調整視窗大小
# 建立並放置框架
frame = tk.Frame(root)
frame.pack(pady=50)
# 建立並放置按鈕
convert_button = tk.Button(frame, text="選擇檔案並轉換", command=convert_to_traditional, font=(
    "Arial", 14), padx=20, pady=10)
convert_button.pack()
# 啟動 GUI 事件迴圈
root.mainloop()
