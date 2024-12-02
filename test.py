import tkinter as tk
from tkinter import ttk

# Tạo cửa sổ Tkinter
root = tk.Tk()

# Tạo Treeview widget
tree = ttk.Treeview(root, columns=("MST", "Tên công ty", "Ghi chú"), show="headings")
tree.pack()

# Đặt tên cho các cột
tree.heading("MST", text="MST")
tree.heading("Tên công ty", text="Tên công ty")
tree.heading("Ghi chú", text="Ghi chú")

# Mảng dữ liệu
data = [
    ["03", "ABC Company", "Note 1"],
    ['04', "XYZ Company", "Note 2"],
    ['03', "LMN Company", "Note 3"]
]

# Chuyển dữ liệu vào Treeview, đảm bảo giá trị là chuỗi
for row in data:
    tree.insert("", "end", text = row[0],values=[str(value) for value in row])

# Hàm để xử lý khi chọn một hàng
def on_tree_select(event):
    selected_item = tree.selection()
    if selected_item:
        item = tree.item(selected_item[0])
        print(item)
        values = item["values"]
        
        # In ra giá trị của hàng được chọn
        print("Selected values:", values)
        
        # Ví dụ điền vào các ô nhập liệu:
        print(f"MST: {str(values[0])}")  # Đảm bảo MST luôn được hiển thị là chuỗi
        print(f"Tên công ty: {values[1]}")
        print(f"Ghi chú: {values[2]}")

# Gắn sự kiện cho Treeview
tree.bind("<<TreeviewSelect>>", on_tree_select)

# Chạy ứng dụng Tkinter
root.mainloop()
