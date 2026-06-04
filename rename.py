import os
import tkinter as tk
from tkinter import filedialog, messagebox


def select_folder():
    # フォルダ選択ダイアログを表示
    selected = filedialog.askdirectory()
    if selected:
        folder_path_var.set(selected)


def rename_files():
    folder_path = folder_path_var.get()
    new_name = new_name_var.get().strip()

    # 入力チェック
    if not folder_path:
        messagebox.showerror("エラー", "フォルダを選択してください。")
        return
    if not new_name:
        messagebox.showerror("エラー", "新しいファイル名を入力してください。")
        return

    try:
        # フォルダ内のファイル一覧を取得
        files = os.listdir(folder_path)

        # 画像として一般的な拡張子を対象にする
        valid_extensions = (
            ".jpg",
            ".jpeg",
            ".png",
            ".gif",
            ".bmp",
            ".webp",
            ".PNG",
            ".JPG",
        )

        # 画像ファイルだけを抽出
        image_files = [
            f
            for f in files
            if f.lower().endswith(valid_extensions)
        ]

        # ファイル名順でソート
        image_files.sort()

        if not image_files:
            messagebox.showinfo(
                "情報", "選択されたフォルダに画像ファイルが見つかりませんでした。"
            )
            return

        # 変更処理の確認
        confirm = messagebox.askyesno(
            "確認", f"{len(image_files)}個の画像ファイルをリネームしますか？"
        )
        if not confirm:
            return

        # 1から順に番号を振ってリネームを実行
        for index, filename in enumerate(image_files, start=1):
            # 拡張子を取得
            ext = os.path.splitext(filename)[1]

            # 新しいファイル名を作成
            new_filename = f"{new_name}{index}{ext}"

            # フルパスを作成
            old_file_path = os.path.join(folder_path, filename)
            new_file_path = os.path.join(folder_path, new_filename)

            # 同名ファイルによる上書き衝突を避けるためのチェック
            if os.path.exists(new_file_path):
                continue

            # ファイル名の変更
            os.rename(old_file_path, new_file_path)

        messagebox.showinfo("完了", "ファイル名の一括書き換えが完了しました！")

    except Exception as e:
        messagebox.showerror("エラー", f"エラーが発生しました:\n{str(e)}")


# --- UI画面の設定 ---
root = tk.Tk()
root.title("画像ファイル一括リネームツール")
root.geometry("500x200")
root.resizable(False, False)

folder_path_var = tk.StringVar()
new_name_var = tk.StringVar()

# 1. フォルダ選択部分
lbl_folder = tk.Label(root, text="1. 書き換えるフォルダを選択してください")
lbl_folder.pack(anchor="w", padx=20, pady=(15, 2))

frame_folder = tk.Frame(root)
frame_folder.pack(fill="x", padx=20)

# 【修正箇所】 mr=5 を padx=(0, 5) に直しました
entry_folder = tk.Entry(
    frame_folder, textvariable=folder_path_var, width=45, state="readonly"
)
entry_folder.pack(side="left", fill="x", expand=True, padx=(0, 5))

btn_browse = tk.Button(frame_folder, text=" 参照... ", command=select_folder)
btn_browse.pack(side="right")

# 2. 新しい名前の入力部分
lbl_name = tk.Label(root, text="2. 新しいファイル名（後ろに1からの連番がつきます）")
lbl_name.pack(anchor="w", padx=20, pady=(15, 2))

entry_name = tk.Entry(root, textvariable=new_name_var, width=50)
entry_name.pack(fill="x", padx=20)

# 空白用スペース
tk.Label(root, text="").pack(pady=2)

# 3. 実行ボタン
btn_execute = tk.Button(
    root,
    text="一括リネームを実行する",
    bg="#1f77b4",
    fg="white",
    font=("Arial", 10, "bold"),
    command=rename_files,
)
btn_execute.pack(fill="x", padx=20, ipady=5)

# 画面の起動
root.mainloop()